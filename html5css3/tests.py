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
from .math import MathJaxMathHandler


#
# Utility Functions
#

def dedent_string(s):
    """
    Strip empty lines at the start and end of a string and dedent it.

    Empty and whitespace-only lines at the beginning and end of ``s``
    are removed. The remaining lines are dedented, i.e. common leading
    whitespace is stripped.
    """
    s = re.sub(r'^([^\S\n]*\n)*', '', re.sub(r'(\n[^\S\n]*)*$', '', s))
    return textwrap.dedent(s)


class RST(object):
    """
    ReStructuredText to HTML test tool.
    """
    def __init__(self, rst, dedent=True, **kwargs):
        """
        Convert reStructuredText to HTML.

        If ``dedent`` is true then ``rst`` is passed through
        ``dedent_string``.

        Any other keyword arguments are passed on to the writer.
        """
        self.dedent = dedent
        if dedent:
            rst = dedent_string(rst)
        self.rst = rst
        self.html = rst2html(rst, **kwargs)

    def assert_body(self, expected, dedent=None):
        """
        Assert that the generated body matches the expectations.

        Compares the generated HTML body against ``expected`` and raises
        an ``AssertionError`` if they don't match.

        If ``dedent`` is not given then its value at construction time
        is used. If ``dedent`` is true then ``expected`` is passed
        through ``dedent_string``.
        """
        __tracebackhide__ = True  # Hide this function in py.test tracebacks
        if dedent is None:
            dedent = self.dedent
        if dedent:
            expected = dedent_string(expected)
        body = get_body(self.html)
        assert body == expected
        return self

    def assert_contains(self, text, num=None):
        """
        Assert that the generated HTML contains some text.

        If ``num`` is given then the number of occurrences of ``text``
        in the generated HTML must match ``num``.
        """
        __tracebackhide__ = True  # Hide this function in py.test tracebacks
        count = self.html.count(text)
        if num is None:
            assert count > 0
        else:
            assert count == num
        return self


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


def get_body(html):
    """
    Extract HTML code inside ``body`` tag.
    """
    start = html.index('<body>') + 6
    stop = html.rindex('</body>')
    return html[start:stop]


#
# Tests
#


def test_multiple_and_nested_tags_in_raw():
    """
    Multiple and nested tags in raw-directives.
    """
    # See https://github.com/marianoguerra/rst2html5/issues/72
    RST("""
        .. raw:: html

            <p id="d1">x<a href="foo">y</a>z</p>
            <p>a<em class="bar">b</em>c</p>
            foo <b>bar</b>
    """).assert_body("""
            <p id="d1">x<a href="foo">y</a>z</p>
            <p>a<em class="bar">b</em>c</p>
            foo <b>bar</b>
    """)


def test_non_ascii_chars_in_attributes():
    """
    Non-ASCII characters in HTML attributes.
    """
    # See https://github.com/marianoguerra/rst2html5/issues/73
    RST("""
        .. figure:: image.png
            :alt: ö
    """).assert_body("""
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
    (RST(INLINE_MATH_RST,
         math_output='html')
    .assert_body(
        '<p><span class="formula"><i>λ</i><sup>2</sup> + <span class="limits"><span class="limit"><span class="symbol">∑</span></span></span><span class="scripts"><sup class="script"><i>n</i></sup><sub class="script"><i>i</i> = 1</sub></span><span class="fraction"><span class="ignored">(</span><span class="numerator"><i>x</i></span><span class="ignored">)/(</span><span class="denominator"><i>y</i></span><span class="ignored">)</span></span></span></p>'
    ))



def test_math_html_block():
    """
    Block math to HTML conversion.
    """
    (RST(BLOCK_MATH_RST,
         math_output='html')
    .assert_body(
        '<div class="formula"><i>λ</i><sup>2</sup> + <span class="limits"><sup class="limit"><i>n</i></sup><span class="limit"><span class="symbol">∑</span></span><sub class="limit"><i>i</i> = 1</sub></span><span class="fraction"><span class="ignored">(</span><span class="numerator"><i>x</i></span><span class="ignored">)/(</span><span class="denominator"><i>y</i></span><span class="ignored">)</span></span></div>',
    ))


def test_math_mathml_inline():
    """
    Inline math to MathML conversion.
    """
    (RST(INLINE_MATH_RST,
         math_output='mathml')
    .assert_body("""
        <p><math xmlns="http://www.w3.org/1998/Math/MathML">
        <mrow><msup><mi>λ</mi><mn>2</mn></msup><mo>+</mo><munderover><mo>∑</mo>
        <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>n</mi></munderover><mfrac>
        <mrow><mi>x</mi></mrow>
        <mrow><mi>y</mi></mrow></mfrac></mrow></math></p>
    """))


def test_math_mathml_block():
    """
    Block math to MathML conversion.
    """
    (RST(BLOCK_MATH_RST,
         math_output='mathml')
    .assert_body("""
        <math mode="display" xmlns="http://www.w3.org/1998/Math/MathML">
        <mtable>
        <mtr>
        <mtd><msup><mi>λ</mi><mn>2</mn></msup><mo>+</mo><munderover><mo>∑</mo>
        <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>n</mi></munderover><mfrac>
        <mrow><mi>x</mi></mrow>
        <mrow><mi>y</mi></mrow></mfrac></mtd></mtr></mtable></math>
    """))


def test_math_latex_inline():
    """
    Inline math to LaTeX conversion.
    """
    (RST(INLINE_MATH_RST,
         math_output='latex')
    .assert_body(
        r'<p><tt class="math">\lambda^2 + \sum_{i=1}^n \frac{x}{y}</tt></p>',
    ))


def test_math_latex_block():
    """
    Block math to LaTeX conversion.
    """
    (RST(BLOCK_MATH_RST,
        math_output='latex')
    .assert_body(
        r'<pre class="math">\lambda^2 + \sum_{i=1}^n \frac{x}{y}</pre>',
    ))


MATHJAX_JS_REF = '<script src="%s"></script>' % MathJaxMathHandler.DEFAULT_URL
MATHJAX_CONFIG = MathJaxMathHandler.DEFAULT_CONFIG


def test_math_mathjax_inline():
    """
    Inline math to MathJax conversion.
    """
    (RST(INLINE_MATH_RST,
         math_output='mathjax')
    .assert_body(
        r'<p><span class="math">\(\lambda^2 + \sum_{i=1}^n \frac{x}{y}\)</span></p>',
    )
    .assert_contains(MATHJAX_JS_REF, 1)
    .assert_contains(MATHJAX_CONFIG, 1))


def test_math_mathjax_block():
    """
    Block math to MathJax conversion.
    """
    (RST(BLOCK_MATH_RST,
         math_output='mathjax')
    .assert_body(r"""
        <div class="math">\begin{equation*}
        \lambda^2 + \sum_{i=1}^n \frac{x}{y}
        \end{equation*}</div>
    """)
    .assert_contains(MATHJAX_JS_REF, 1)
    .assert_contains(MATHJAX_CONFIG, 1))

