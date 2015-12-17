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

import contextlib
import os.path
import re
import tempfile
import textwrap

from docutils.core import publish_string

from . import Writer
from .math import HTMLMathHandler, MathJaxMathHandler


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

    def print_html(self):
        """
        Print HTML to STDOUT for debugging.
        """
        print(self.html)
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


@contextlib.contextmanager
def temp_file(content):
    """
    Context manager that supplies a temporary file with given content.
    """
    with tempfile.NamedTemporaryFile() as f:
        f.write(content.encode('utf8'))
        f.seek(0)
        yield f.name


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


INLINE_MATH_RST = r':math:`\lambda^2 < \sum_{i=1}^n \frac{x}{y}`'

BLOCK_MATH_RST = r"""
.. math::

    \lambda^2 < \sum_{i=1}^n \frac{x}{y}
"""


MATH_CSS_FILE = os.path.relpath(HTMLMathHandler.DEFAULT_CSS)

def _math_css_link(path=None):
    path = path or MATH_CSS_FILE
    return '<link href="%s" rel="stylesheet" type="text/css">' % path


def test_math_html_inline():
    """
    Inline math to HTML conversion.
    """
    (RST(INLINE_MATH_RST + ' ' + INLINE_MATH_RST,
         math_output='html',
         embed_content=False)
    .assert_body(
        '<p><span class="formula"><i>λ</i><sup>2</sup> &lt; <span class="limits"><span class="limit"><span class="symbol">∑</span></span></span><span class="scripts"><sup class="script"><i>n</i></sup><sub class="script"><i>i</i> = 1</sub></span><span class="fraction"><span class="ignored">(</span><span class="numerator"><i>x</i></span><span class="ignored">)/(</span><span class="denominator"><i>y</i></span><span class="ignored">)</span></span></span> <span class="formula"><i>λ</i><sup>2</sup> &lt; <span class="limits"><span class="limit"><span class="symbol">∑</span></span></span><span class="scripts"><sup class="script"><i>n</i></sup><sub class="script"><i>i</i> = 1</sub></span><span class="fraction"><span class="ignored">(</span><span class="numerator"><i>x</i></span><span class="ignored">)/(</span><span class="denominator"><i>y</i></span><span class="ignored">)</span></span></span></p>'
    )
    .assert_contains(_math_css_link(), 1))


def test_math_html_block():
    """
    Block math to HTML conversion.
    """
    (RST(BLOCK_MATH_RST + '\n\n' + BLOCK_MATH_RST,
         math_output='html',
         embed_content=False)
    .assert_body(
        '<div class="formula"><i>λ</i><sup>2</sup> &lt; <span class="limits"><sup class="limit"><i>n</i></sup><span class="limit"><span class="symbol">∑</span></span><sub class="limit"><i>i</i> = 1</sub></span><span class="fraction"><span class="ignored">(</span><span class="numerator"><i>x</i></span><span class="ignored">)/(</span><span class="denominator"><i>y</i></span><span class="ignored">)</span></span></div><div class="formula"><i>λ</i><sup>2</sup> &lt; <span class="limits"><sup class="limit"><i>n</i></sup><span class="limit"><span class="symbol">∑</span></span><sub class="limit"><i>i</i> = 1</sub></span><span class="fraction"><span class="ignored">(</span><span class="numerator"><i>x</i></span><span class="ignored">)/(</span><span class="denominator"><i>y</i></span><span class="ignored">)</span></span></div>',
    )
    .assert_contains(_math_css_link(), 1))


def test_math_html_config_math_opts():
    """
    HTML math configuration via "--math-opts".
    """
    (RST(INLINE_MATH_RST,
         math_output='html ../my/math.css',
         embed_content=False)
     .print_html()
     .assert_contains(_math_css_link('../my/math.css'), 1))


def test_math_html_config_math_css():
    """
    HTML math configuration via "--math-css".
    """
    (RST(INLINE_MATH_RST,
         math_output='html',
         math_css='../my/math.css',
         embed_content=False)
     .print_html()
     .assert_contains(_math_css_link('../my/math.css'), 1))


def test_math_mathml_inline():
    """
    Inline math to MathML conversion.
    """
    (RST(INLINE_MATH_RST,
         math_output='mathml')
    .assert_body("""
        <p><math xmlns="http://www.w3.org/1998/Math/MathML">
        <mrow><msup><mi>λ</mi><mn>2</mn></msup><mo>&lt;</mo><munderover><mo>∑</mo>
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
        <mtd><msup><mi>λ</mi><mn>2</mn></msup><mo>&lt;</mo><munderover><mo>∑</mo>
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
        r'<p><tt class="math">\lambda^2 &lt; \sum_{i=1}^n \frac{x}{y}</tt></p>',
    ))


def test_math_latex_block():
    """
    Block math to LaTeX conversion.
    """
    (RST(BLOCK_MATH_RST,
        math_output='latex')
    .assert_body(
        r'<pre class="math">\lambda^2 &lt; \sum_{i=1}^n \frac{x}{y}</pre>',
    ))


def _mathjax_js_ref(url=None):
    url = url or MathJaxMathHandler.DEFAULT_URL
    return '<script src="%s"></script>' % url

MATHJAX_CONFIG = MathJaxMathHandler.DEFAULT_CONFIG


def test_math_mathjax_inline():
    """
    Inline math to MathJax conversion.
    """
    (RST(INLINE_MATH_RST + ' ' + INLINE_MATH_RST,
         math_output='mathjax')
    .assert_body(
        r'<p><span class="math">\(\lambda^2 &lt; \sum_{i=1}^n \frac{x}{y}\)</span> <span class="math">\(\lambda^2 &lt; \sum_{i=1}^n \frac{x}{y}\)</span></p>',
    )
    .assert_contains(_mathjax_js_ref(), 1)
    .assert_contains(MATHJAX_CONFIG, 1))


def test_math_mathjax_block():
    """
    Block math to MathJax conversion.
    """
    (RST(BLOCK_MATH_RST + '\n\n' + BLOCK_MATH_RST,
         math_output='mathjax')
    .assert_body(r"""
        <div class="math">\begin{equation*}
        \lambda^2 &lt; \sum_{i=1}^n \frac{x}{y}
        \end{equation*}</div><div class="math">\begin{equation*}
        \lambda^2 &lt; \sum_{i=1}^n \frac{x}{y}
        \end{equation*}</div>
    """)
    .assert_contains(_mathjax_js_ref(), 1)
    .assert_contains(MATHJAX_CONFIG, 1))


def test_math_mathjax_config_math_opts():
    """
    MathJax configuration via additional option to "--math-opts".
    """
    (RST(INLINE_MATH_RST,
         math_output='mathjax http://my/mathjax.js')
     .assert_contains(_mathjax_js_ref('http://my/mathjax.js')))


def test_math_mathjax_config_mathjax_opts():
    """
    MathJax configuration via "--mathjax-opts".
    """
    (RST(INLINE_MATH_RST,
         math_output='mathjax',
         mathjax_opts='url=http://my/mathjax.js')
     .assert_contains(_mathjax_js_ref('http://my/mathjax.js')))
    with temp_file('my_config') as filename:
        (RST(INLINE_MATH_RST,
             math_output='mathjax',
             mathjax_opts='config=' + filename)
         .assert_contains('my_config'))
        (RST(INLINE_MATH_RST,
             math_output='mathjax',
             mathjax_opts='url=http://my/mathjax.js,config=' + filename)
         .assert_contains(_mathjax_js_ref('http://my/mathjax.js'))
         .assert_contains('my_config'))


def test_math_mathjax_config_mathjax_url():
    """
    MathJax configuration via "--mathjax-url".
    """
    (RST(INLINE_MATH_RST,
         math_output='mathjax',
         mathjax_url='http://my/mathjax.js')
     .assert_contains(_mathjax_js_ref('http://my/mathjax.js')))


def test_math_mathjax_config_mathjax_config():
    """
    MathJax configuration via "--mathjax-config".
    """
    with temp_file('my_config') as filename:
        (RST(INLINE_MATH_RST,
             math_output='mathjax',
             mathjax_config=filename)
         .assert_contains('my_config'))

