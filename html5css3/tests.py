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


def rst2html(rst, only_body=True):
    """
    Convert RST to HTML.

    If ``only_body`` is true then only the HTML code between the opening
    and closing ``body`` tag is returned.
    """
    result = publish_string(
        source=rst,
        writer=Writer(),
        writer_name='html5css3',
        settings_overrides={'input_encoding': 'utf8'},
    ).decode('utf8')
    if only_body:
        start = result.index('<body>') + 6
        stop = result.rindex('</body>')
        result = result[start:stop]
    return result


def assert_rst(rst, html, only_body=True, dedent=True):
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
    """
    __tracebackhide__ = True  # Hide this function in py.test tracebacks
    if dedent:
        rst = textwrap.dedent(remove_whitespace_lines(rst))
        html = textwrap.dedent(remove_whitespace_lines(html))
    result = rst2html(rst, only_body)
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

