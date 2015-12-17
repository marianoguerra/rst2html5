#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

# Author: Florian Brucker <mail@florianbrucker.de>
# Copyright: This module has been placed in the public domain.

"""
Math handling for ``html5css3``.
"""

from __future__ import unicode_literals

import codecs
import os.path

from docutils.utils.math.unichar2tex import uni2tex_table
from docutils.utils.math import math2html, pick_math_environment
from docutils.utils.math.latex2mathml import parse_latex_math

from .html import *


__all__ = ['HTMLMathHandler', 'LateXMathHandler', 'MathHandler',
           'MathJaxMathHandler', 'MathMLMathHandler', 'SimpleMathHandler']


class MathHandler(object):
    """
    Abstract math handler.
    """
    CLASS = None
    BLOCK_WRAPPER = '%(code)s'
    INLINE_WRAPPER = '%(code)s'

    def __init__(self):
        self._setup_done = False

    def convert(self, translator, node, block):
        if not self._setup_done:
            self._setup(translator)
            self._setup_done = True
        code = node.astext()
        if block:
            env = pick_math_environment(code)
            wrapper = self.BLOCK_WRAPPER
        else:
            env = ''
            wrapper = self.INLINE_WRAPPER
        code = code.translate(uni2tex_table)
        code = wrapper % {'code': code, 'env': env}
        tag = self._create_tag(code, block)
        if self.CLASS:
            tag.attrib['class'] = self.CLASS
        return tag

    def _create_tag(self, code, block):
        raise NotImplementedError('Must be implemented in subclass.')

    def _setup(self, translator):
        pass


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
    BLOCK_TAG = Pre
    INLINE_TAG = Tt
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

    DEFAULT_URL = 'http://cdn.mathjax.org/mathjax/latest/MathJax.js'
    DEFAULT_CONFIG = """
        MathJax.Hub.Config({
            extensions: ["tex2jax.js"],
            jax: ["input/TeX", "output/HTML-CSS"],
            tex2jax: {
                inlineMath: [["\\\\(","\\\\)"]],
                displayMath: [['$$','$$'], ["\\\\[","\\\\]"]],
                processEscapes: true
            },
            "HTML-CSS": { availableFonts: ["TeX"] }
        });"""

    def __init__(self, js_url=None, config_filename=None):
        super(MathJaxMathHandler, self).__init__()
        self.js_url = js_url or self.DEFAULT_URL
        if config_filename:
            with codecs.open(config_filename, 'r', encoding='utf8') as f:
                self.config = f.read()
        else:
            self.config = self.DEFAULT_CONFIG

    def _setup(self, translator):
        translator.head.append(Script(self.config,
                               type="text/x-mathjax-config"))
        translator.head.append(Script(src=self.js_url))


class MathMLMathHandler(MathHandler):
    """
    Math handler for MathML output.
    """
    BLOCK_WRAPPER = '%(code)s'
    INLINE_WRAPPER = '%(code)s'

    def _create_tag(self, code, block):
        tree = parse_latex_math(code, inline=(not block))
        html = ''.join(tree.xml())
        tag = html_to_tags(html)[0]

        def strip_ns(tag):
            del tag.attrib['xmlns']
            for child in tag:
                strip_ns(child)

        for child in tag:
            strip_ns(child)
        return tag


class HTMLMathHandler(MathHandler):
    """
    Math handler for HTML output.
    """
    CLASS = 'formula'
    BLOCK_WRAPPER = '\\begin{%(env)s}\n%(code)s\n\\end{%(env)s}'
    INLINE_WRAPPER = '$%(code)s$'
    DEFAULT_CSS = os.path.join(os.path.dirname(__file__), 'math.css')

    def __init__(self, css_filename=None):
        super(HTMLMathHandler, self).__init__()
        self.css_filename = css_filename or self.DEFAULT_CSS

    def _create_tag(self, code, block):
        math2html.DocumentParameters.displaymode = block
        html = math2html.math2html(code)
        tags = html_to_tags(html)
        if block:
            return Div(*tags)
        else:
            return Span(*tags)

    def _setup(self, translator):
        translator.css(os.path.relpath(self.css_filename))


