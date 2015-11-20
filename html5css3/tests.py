#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

# Author: Florian Brucker <mail@florianbrucker.de>
# Copyright: This module has been placed in the public domain.

"""
Tests for ``html5css3``.

These tests are intended to be run via pytest_. To
execute all ``html5css3`` tests on all supported Python versions simply
run ``tox`` in the project's root directory (this requires tox_).

.. _pytest: http://pytest.org
.. _tox: https://tox.readthedocs.org
"""

from __future__ import unicode_literals

import textwrap
import re

from docutils.core import publish_string

from . import Writer


#
# Utility Functions
#

def remove_whitespace_lines(s):
    """
    Remove whitespace-only lines at the beginning and end of a string.
    """
    return re.sub(r'^([^\S\n]*\n)*', '', re.sub(r'(\n[^\S\n]*)*$', '', s))


def get_body(html):
    """
    Extract HTML code inside ``body`` tag.
    """
    start = html.index('<body>') + 6
    stop = html.rindex('</body>')
    return html[start:stop]


def rst2html(rst, **kwargs):
    """
    Convert RST to HTML.

    Keyword arguments are passed on to the writer.
    """
    settings = {'input_encoding': 'utf8'}
    settings.update(kwargs)
    result = publish_string(
        source=rst,
        writer=Writer(),
        writer_name='html5css3',
        settings_overrides=settings,
    ).decode('utf8')
    return result


def assert_rst(rst, html, only_body=True, dedent=True, **kwargs):
    """
    Assert that RST is correctly converted to HTML.

    The RST code in ``rst`` is converted to HTML and compared with the
    HTML code in ``html``. If they do not match an ``AssertionError``
    is raised.

    If ``only_body`` is true then only the generated HTML code between
    the opening and closing ``body`` tag is compared to the expected
    result.

    If ``dedent`` is true then ``rst`` and ``html`` are preprocessed as
    follows: First, empty and white-space lines at the beginning and end
    are removed. The remaining lines are then dedented, i.e. common
    leading whitespace is stripped. This allows for more flexibility
    when formatting test source code.

    Any remaining keyword arguments are passed on to the HTML writer.
    """
    __tracebackhide__ = True  # Hide this function in py.test tracebacks
    if dedent:
        rst = textwrap.dedent(remove_whitespace_lines(rst))
        html = textwrap.dedent(remove_whitespace_lines(html))
    result = rst2html(rst, **kwargs)
    if only_body:
        result = get_body(result)
    assert result == html


#
# Tests
#


def test_multiple_and_nested_tags_in_raw():
    """
    Multiple and nested tags in raw-directives.
    """
    # See https://github.com/marianoguerra/rst2html5/issues/72
    assert_rst("""
        .. raw:: html

            <p id="d1">x<a href="foo">y</a>z</p>
            <p>a<em class="bar">b</em>c</p>
            foo <b>bar</b>
        """, """
            <p id="d1">x<a href="foo">y</a>z</p>
            <p>a<em class="bar">b</em>c</p>
            foo <b>bar</b>
        """)


def test_non_ascii_chars_in_attributes():
    """
    Non-ASCII characters in HTML attributes.
    """
    # See https://github.com/marianoguerra/rst2html5/issues/73
    assert_rst("""
        .. figure:: image.png
            :alt: ö
        """, """
            <figure><img alt="ö" src="image.png"></figure>
        """)


INLINE_MATH_RST = r':math:`\lambda^2 + \sum_{i=1}^n \frac{x}{y}`'

BLOCK_MATH_RST = r"""
.. math::

    \lambda^2 + \sum_{i=1}^n \frac{x}{y}
"""


def test_math_html_inline():
    """
    Inline math to HTML conversion.
    """
    assert_rst(
        INLINE_MATH_RST,
        '<p><span class="formula"><i>λ</i><sup>2</sup> + <span class="limits"><span class="limit"><span class="symbol">∑</span></span></span><span class="scripts"><sup class="script"><i>n</i></sup><sub class="script"><i>i</i> = 1</sub></span><span class="fraction"><span class="ignored">(</span><span class="numerator"><i>x</i></span><span class="ignored">)/(</span><span class="denominator"><i>y</i></span><span class="ignored">)</span></span></span></p>',
        math_output='html')


def test_math_html_block():
    """
    Block math to HTML conversion.
    """
    assert_rst(
        BLOCK_MATH_RST,
        '<div class="formula"><i>λ</i><sup>2</sup> + <span class="limits"><sup class="limit"><i>n</i></sup><span class="limit"><span class="symbol">∑</span></span><sub class="limit"><i>i</i> = 1</sub></span><span class="fraction"><span class="ignored">(</span><span class="numerator"><i>x</i></span><span class="ignored">)/(</span><span class="denominator"><i>y</i></span><span class="ignored">)</span></span></div>',
        math_output='html')


def test_math_mathml_inline():
    """
    Inline math to MathML conversion.
    """
    assert_rst(
        INLINE_MATH_RST, """
        <p><math xmlns="http://www.w3.org/1998/Math/MathML">
        <mrow><msup><mi>λ</mi><mn>2</mn></msup><mo>+</mo><munderover><mo>∑</mo>
        <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>n</mi></munderover><mfrac>
        <mrow><mi>x</mi></mrow>
        <mrow><mi>y</mi></mrow></mfrac></mrow></math></p>
        """,
        math_output='mathml')


def test_math_mathml_block():
    """
    Block math to MathML conversion.
    """
    assert_rst(
        BLOCK_MATH_RST,
        """
        <math mode="display" xmlns="http://www.w3.org/1998/Math/MathML">
        <mtable>
        <mtr>
        <mtd><msup><mi>λ</mi><mn>2</mn></msup><mo>+</mo><munderover><mo>∑</mo>
        <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>n</mi></munderover><mfrac>
        <mrow><mi>x</mi></mrow>
        <mrow><mi>y</mi></mrow></mfrac></mtd></mtr></mtable></math>
        """,
        math_output='mathml')


def test_math_latex_inline():
    """
    Inline math to LaTeX conversion.
    """
    assert_rst(
        INLINE_MATH_RST,
        r'<p><tt class="math">\lambda^2 + \sum_{i=1}^n \frac{x}{y}</tt></p>',
        math_output='latex')


def test_math_latex_block():
    """
    Block math to LaTeX conversion.
    """
    assert_rst(
        BLOCK_MATH_RST,
        r'<pre class="math">\lambda^2 + \sum_{i=1}^n \frac{x}{y}</pre>',
        math_output='latex')


def test_math_mathjax_inline():
    """
    Inline math to MathJax conversion.
    """
    assert_rst(
        INLINE_MATH_RST,
        r'<p><span class="math">\(\lambda^2 + \sum_{i=1}^n \frac{x}{y}\)</span></p>',
        math_output='mathjax')


def test_math_mathjax_block():
    """
    Block math to MathJax conversion.
    """
    assert_rst(
        BLOCK_MATH_RST,
        r"""
        <div class="math">\begin{equation*}
        \lambda^2 + \sum_{i=1}^n \frac{x}{y}
        \end{equation*}</div>
        """,
        math_output='mathjax')

