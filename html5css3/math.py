#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

# Author: Florian Brucker <mail@florianbrucker.de>
# Copyright: This module has been placed in the public domain.

"""
Math handling for ``html5css3``.
"""

from __future__ import unicode_literals

from docutils.utils.math.unichar2tex import uni2tex_table
from docutils.utils.math import math2html, pick_math_environment
from docutils.utils.math.latex2mathml import parse_latex_math

from .html import *


class MathHandler(object):
    """
    Abstract math handler.
    """
    CLASS = None
    BLOCK_WRAPPER = '%(code)s'
    INLINE_WRAPPER = '%(code)s'

    def __init__(self, options):
        self.options = options

    def convert(self, translator, node, block):
        code = node.astext()
        if block:
            env = pick_math_environment(code)
            wrapper = self.BLOCK_WRAPPER
        else:
            env = ''
            wrapper = self.INLINE_WRAPPER
        code = quote(code).translate(uni2tex_table)
        code = wrapper % {'code': code, 'env': env}
        tag = self._create_tag(code, block)
        if self.CLASS:
            tag.attrib['class'] = self.CLASS
        return tag

    def _create_tag(self, code, block):
        raise NotImplementedError('Must be implemented in subclass.')


class SimpleMathHandler(MathHandler):
    """
    Base class for simple math handlers.
    """
    BLOCK_TAG = None
    INLINE_TAG = None

    def _create_tag(self, code, block):
        if block:
            return self.BLOCK_TAG(code)
        else:
            return self.INLINE_TAG(code)


class LaTeXMathHandler(SimpleMathHandler):
    """
    Math handler for raw LaTeX output.
    """
    BLOCK_TAG = Div
    INLINE_TAG = Span
    CLASS = 'math'
    BLOCK_WRAPPER = '%(code)s'
    INLINE_WRAPPER = '%(code)s'


class MathJaxMathHandler(SimpleMathHandler):
    """
    Math handler for MathJax output.
    """
    BLOCK_TAG = Div
    INLINE_TAG = Span
    CLASS = 'math'
    BLOCK_WRAPPER = '\\begin{%(env)s}\n%(code)s\n\\end{%(env)s}'
    INLINE_WRAPPER = '\(%(code)s\)'

    # FIXME: Include MathJax JS + CSS


class MathMLMathHandler(MathHandler):
    """
    Math handler for MathML output.
    """
    CLASS = None
    BLOCK_WRAPPER = '%(code)s'
    INLINE_WRAPPER = '%(code)s'

    def _create_tag(self, code, block):
        # FIXME: Set doctype and content_type
        tree = parse_latex_math(code, inline=(not block))
        html = ''.join(tree.xml())
        return html_to_tags(html)[0]


class HTMLMathHandler(MathHandler):
    """
    Math handler for HTML output.
    """
    CLASS = 'formula'
    BLOCK_WRAPPER = '\\begin{%(env)s}\n%(code)s\n\\end{%(env)s}'
    INLINE_WRAPPER = '$%(code)s$'

    def _create_tag(self, code, block):
        math2html.DocumentParameters.displaymode = block
        html = math2html.math2html(code)
        tags = html_to_tags(html)
        if block:
            return Div(*tags)
        else:
            return Span(*tags)


MATH_HANDLERS = {
    'latex': LaTeXMathHandler,
    'mathjax': MathJaxMathHandler,
    'mathml': MathMLMathHandler,
    'html': HTMLMathHandler,
}


def get_math_handler(math_output):
    """
    Get math handler by name.

    ``math_output`` is the docutils configuration variable of the same
    name. It specifies the name the math handler to use. The name may be
    followed by additional options, separated from the name by a space.

    The return value is an instance of ``MathHandler``.
    """
    fields = math_output.split(None, 1)
    if len(fields) == 1:
        name = math_output
        options = ''
    else:
        name, options = fields
    try:
        cls = MATH_HANDLERS[name.lower()]
    except KeyError:
        raise ValueError('Math handler "%s" does not exist.' % name)
    return cls(options)

