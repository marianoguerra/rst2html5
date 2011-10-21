# $Id: __init__.py 7061 2011-06-29 16:24:09Z milde $
# Author: Mariano Guerra <luismarianoguerra@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Simple HyperText Markup Language document tree Writer.

The output conforms to the HTML version 5

The css "html5css3.css" is required

The css is based on twitter bootstrap:
http://twitter.github.com/bootstrap/

this code is based on html4css1
"""

__docformat__ = 'reStructuredText'


import os
import re
import sys
import time

import os.path

try:
    import Image                        # check for the Python Imaging Library
except ImportError:
    Image = None

import docutils

from docutils import frontend, nodes, utils, writers, languages, io

from docutils.math import unimathsymbols2tex

from html import *

try:
    from docutils.math import pick_math_environment
except ImportError:
    def pick_math_environment(code, numbered=False):
        """Return the right math environment to display `code`.

        The test simply looks for line-breaks (``\\``) outside environments.
        Multi-line formulae are set with ``align``, one-liners with
        ``equation``.

        If `numbered` evaluates to ``False``, the "starred" versions are used
        to suppress numbering.
        """
        # cut out environment content:
        chunks = code.split(r'\begin{')
        toplevel_code = ''.join([chunk.split(r'\end{')[-1]
                                 for chunk in chunks])
        if toplevel_code.find(r'\\') >= 0:
            env = 'align'
        else:
            env = 'equation'
        if not numbered:
            env += '*'
        return env

from docutils.math.latex2mathml import parse_latex_math
from docutils.math.math2html import math2html

from docutils.transforms import writer_aux


class Writer(writers.Writer):

    settings_defaults = {
        'output_encoding_error_handler': 'xmlcharrefreplace'
    }

    def __init__(self):
        writers.Writer.__init__(self)
        self.translator_class = HTMLTranslator

    def translate(self):
        self.visitor = visitor = self.translator_class(self.document)
        self.document.walkabout(visitor)
        self.output = visitor.astext()

def docinfo_item(node, translator):
    name = node.tagname
    label = translator.language.labels.get(name, name)

    td = Td()
    translator.current.append(Tr(Td(label), td))

    return td

NODES = {
    "Text": None,
    "abbreviation": Abbr,
    "acronym": Abbr,

    # docinfo
    "address": docinfo_item,
    "organization": docinfo_item,
    "revision": docinfo_item,
    "status": docinfo_item,
    "version": docinfo_item,
    "author": docinfo_item,
    "authors": None,
    "contact": docinfo_item,
    "copyright": docinfo_item,
    "date": docinfo_item,

    "docinfo": Table,
    "docinfo_item": None,

    "admonition": None,
    "attribution": (P, "attribution"),
    "block_quote": Blockquote,
    "bullet_list": Ul,
    "caption": Caption,
    "citation": Cite,
    "citation_reference": None,
    "classifier": Span,
    "colspec": None,
    "comment": Comment,
    "compound": None,
    "container": None,
    "decoration": None,
    "definition": Dd,
    "definition_list": Dl,
    "definition_list_item": None,
    "description": None,
    "doctest_block": None,
    "document": None,
    "emphasis": Em,
    "entry": None,
    "enumerated_list": Ol,
    "field": None,
    "field_body": None,
    "field_list": None,
    "field_name": None,
    "figure": None,
    "footer": Footer,
    "footnote": (Div, "footnote"),
    "footnote_reference": None,
    "generated": None,
    "header": Header,
    "image": None,
    "inline": Span,
    "label": None,
    "legend": None,
    "line": None,
    "line_block": None,
    "list_item": Li,
    "literal": (Span, "pre"),
    "literal_block": Pre,
    "math": None,
    "math_block": None,
    "meta": Meta,
    "option": (Span, "option"),
    "option_argument": Var,
    "option_group": None,
    "option_list": None,
    "option_list_item": None,
    "option_string": None,
    "paragraph": P,
    "problematic": None,
    "raw": None,
    "reference": None,
    "row": None,
    "rubric": None,
    "section": None,
    "sidebar": Aside,
    "strong": Strong,
    "subscript": Sub,
    "substitution_definition": None,
    "substitution_reference": None,
    "subtitle": Sub,
    "superscript": Sup,
    "system_message": None,
    "table": None,
    "target": None,
    "tbody": None,
    "term": None,
    "tgroup": None,
    "thead": None,
    "title": H1,
    "title_reference": None,
    "topic": None,
    "transition": None
}

class HTMLTranslator(nodes.NodeVisitor):
    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self.root = Body()
        self.indent = 1
        self.parents = []
        self.current = self.root

        lcode = document.settings.language_code
        self.language = languages.get_language(lcode, document.reporter)

    def css(self, path):
        content = open(path).read()
        return Style(content, type="text/css")

    def astext(self):
        return Html(
            Head(
                Title("document"),
                self.css("html5css3/html5css3.css")
            ),
            self.root
        ).format(0, self.indent)

    def pop_parent(self, node):
        self.current = self.parents.pop()

    def visit_Text(self, node):
        self.current.append(node.astext())

    def depart_Text(self, node):
        pass

    def visit_reference(self, node):
        tag = A()
        atts = {"class": "reference"}

        if 'refuri' in node:
            atts['href'] = node['refuri']
            atts['class'] += ' external'
        else:
            assert 'refid' in node, \
                   'References must have "refuri" or "refid" attribute.'
            atts['href'] = '#' + node['refid']
            atts['class'] += ' internal'
        if not isinstance(node.parent, nodes.TextElement):
            assert len(node) == 1 and isinstance(node[0], nodes.image)
            atts['class'] += ' image-reference'

        tag.attrib.update(atts)

        self.parents.append(self.current)
        self.current.append(tag)
        self.current = tag

    def unknown_visit(self, node):
        handler = NODES.get(node.tagname, None)
        handled_elsewhere = False

        if isinstance(handler, tuple):
            tag_class, cls = handler
            new_current = tag_class(class_=cls)
        elif type(handler) == type and issubclass(handler, TagBase):
            new_current = handler()
        elif callable(handler):
            new_current = handler(node, self)
            handled_elsewhere = True
        else:
            new_current = Div(class_=node.tagname)

        self.parents.append(self.current)

        if not handled_elsewhere:
            self.current.append(new_current)

        self.current = new_current

    unknown_departure = pop_parent
    depart_reference = pop_parent

class SimpleListChecker(nodes.GenericNodeVisitor):

    """
    Raise `nodes.NodeFound` if non-simple list item is encountered.

    Here "simple" means a list item containing nothing other than a single
    paragraph, a simple list, or a paragraph followed by a simple list.
    """

    def default_visit(self, node):
        raise nodes.NodeFound

    def visit_bullet_list(self, node):
        pass

    def visit_enumerated_list(self, node):
        pass

    def visit_list_item(self, node):
        children = []
        for child in node.children:
            if not isinstance(child, nodes.Invisible):
                children.append(child)
        if (children and isinstance(children[0], nodes.paragraph)
            and (isinstance(children[-1], nodes.bullet_list)
                 or isinstance(children[-1], nodes.enumerated_list))):
            children.pop()
        if len(children) <= 1:
            return
        else:
            raise nodes.NodeFound

    def visit_paragraph(self, node):
        raise nodes.SkipNode

    def invisible_visit(self, node):
        """Invisible nodes should be ignored."""
        raise nodes.SkipNode

    visit_comment = invisible_visit
    visit_substitution_definition = invisible_visit
    visit_target = invisible_visit
    visit_pending = invisible_visit
