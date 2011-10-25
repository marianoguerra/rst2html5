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

def docinfo_address(node, translator):
    return docinfo_item(node, translator, lambda: Pre(class_="address"))

def docinfo_authors(node, translator):
    return docinfo_item(node, translator, lambda: Ul(class_="authors"))

def docinfo_item(node, translator, inner=None):
    name = node.tagname
    label = translator.language.labels.get(name, name)

    td = Td()
    current = td

    if inner is not None:
        current = inner()
        td.append(current)

    translator.current.append(Tr(Th(label), td))

    return current

def classifier(node, translator):
    term = translator.current[-1]

    new_current = Span(class_="classifier")

    term.append(Span(" :", class_="classifier-delimiter"))
    term.append(new_current)

    return new_current

def admonition(node, translator):
    classes = " ".join(node.get('classes', []))

    tagname = node.tagname.lower()

    if classes:
        classes = " " + classes

    if tagname in ('note', 'tip', 'hint'):
        cls = 'alert-message block-message info'
    elif tagname in ('attention', 'caution', 'important', 'warning'):
        cls = 'alert-message block-message warning'
    elif tagname in ('error', 'danger'):
        cls = 'alert-message block-message error'
    else:
        cls = 'alert-message block-message ' + tagname

    cls += classes

    title = ""

    if tagname != "admonition":
        title = tagname.title()

    div = Div(P(title, class_="admonition-title"), class_=cls)
    translator.current.append(div)

    return div

def skip(node, translator):
    return translator.current

NODES = {
    "Text": None,
    "abbreviation": Abbr,
    "acronym": Abbr,

    # docinfo
    "address": docinfo_address,
    "organization": docinfo_item,
    "revision": docinfo_item,
    "status": docinfo_item,
    "version": docinfo_item,
    "author": docinfo_item,
    "authors": docinfo_authors,
    "contact": docinfo_item,
    "copyright": docinfo_item,
    "date": docinfo_item,

    "docinfo": Table,
    "docinfo_item": None,

    "admonition": admonition,
    "note": admonition,
    "tip": admonition,
    "note": admonition,
    "hint": admonition,
    "attention": admonition,
    "caution": admonition,
    "important": admonition,
    "warning": admonition,
    "error": admonition,
    "danger": admonition,

    "attribution": (P, "attribution"),
    "block_quote": Blockquote,
    "bullet_list": Ul,
    "caption": Caption,
    "citation": Cite,
    "citation_reference": None,
    "classifier": classifier,
    "colspec": None,
    "comment": Comment,
    "compound": None,
    "container": None,
    "decoration": None,
    "definition": Dd,
    "definition_list": Dl,
    "definition_list_item": skip,
    "description": Td,
    "doctest_block": Pre,
    "document": None,
    "emphasis": Em,
    "entry": Td,
    "enumerated_list": Ol,
    "field": Tr,
    "field_body": Td,
    "field_list": Table,
    "field_name": Th,
    "figure": None,
    "footer": Footer,
    "footnote": None,
    "footnote_reference": None,
    "generated": skip,
    "header": Header,
    "image": Img,
    "inline": Span,
    "label": None,
    "legend": None,
    "line": None,
    "line_block": None,
    "list_item": Li,
    "literal": (Span, "pre"),
    "literal_block": (Pre, "literal-block"),
    "math": None,
    "math_block": None,
    "meta": Meta,
    "option": (P, "option"),
    "option_argument": Var,
    "option_group": Td,
    "option_list": (Table, "option-list"),
    "option_list_item": Tr,
    "option_string": skip,
    "paragraph": P,
    "problematic": None,
    "raw": None,
    "reference": None,
    "row": Tr,
    "rubric": None,
    "section": None,
    "sidebar": Aside,
    "strong": Strong,
    "subscript": Sub,
    "substitution_definition": None,
    "substitution_reference": None,
    "subtitle": H2,
    "superscript": Sup,
    "system_message": None,
    "table": Table,
    "target": None,
    "tbody": Tbody,
    "term": Dt,
    "tgroup": Colgroup,
    "thead": Thead,
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
        tree = Html(
            Head(
                Title("document"),
                self.css("html5css3/bootstrap.css"),
                self.css("html5css3/rst2html5.css")
            ),
            self.root
        )

        return tree.format(0, self.indent)

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

    def visit_footnote_reference(self, node):
        href = '#' + node['refid']
        tag = A(class_="footnote-reference", href=href)

        self.parents.append(self.current)
        self.current.append(Sup(tag))
        self.current = tag

    def visit_author(self, node):
        if isinstance(self.current, Ul):
            tag = Li(class_="author")
            self.current.append(tag)
        else:
            tag = docinfo_item(node, self)

        self.parents.append(self.current)
        self.current = tag

    def visit_image(self, node):
        atts = {}
        uri = node['uri']
        # place SVG and SWF images in an <object> element
        types = {
            '.svg': 'image/svg+xml',
            '.swf': 'application/x-shockwave-flash'
        }

        ext = os.path.splitext(uri)[1].lower()

        if ext in ('.svg', '.swf'):
            atts['data'] = uri
            atts['type'] = types[ext]
        else:
            atts['src'] = uri
            atts['alt'] = node.get('alt', uri)
        # image size
        if 'width' in node:
            atts['width'] = node['width']
        if 'height' in node:
            atts['height'] = node['height']
        if 'scale' in node:
            if Image and not ('width' in node and 'height' in node):
                try:
                    im = Image.open(str(uri))
                except (IOError, # Source image can't be found or opened
                        UnicodeError):  # PIL doesn't like Unicode paths.
                    pass
                else:
                    if 'width' not in atts:
                        atts['width'] = str(im.size[0])
                    if 'height' not in atts:
                        atts['height'] = str(im.size[1])
                    del im
            for att_name in 'width', 'height':
                if att_name in atts:
                    match = re.match(r'([0-9.]+)(\S*)$', atts[att_name])
                    assert match
                    atts[att_name] = '%s%s' % (
                        float(match.group(1)) * (float(node['scale']) / 100),
                        match.group(2))
        style = []
        for att_name in 'width', 'height':
            if att_name in atts:
                if re.match(r'^[0-9.]+$', atts[att_name]):
                    # Interpret unitless values as pixels.
                    atts[att_name] += 'px'
                style.append('%s: %s;' % (att_name, atts[att_name]))
                del atts[att_name]
        if style:
            atts['style'] = ' '.join(style)
        if (isinstance(node.parent, nodes.TextElement) or
            (isinstance(node.parent, nodes.reference) and
             not isinstance(node.parent.parent, nodes.TextElement))):
            # Inline context or surrounded by <a>...</a>.
            suffix = ''
        else:
            suffix = '\n'
        if 'align' in node:
            atts['class'] = 'align-%s' % node['align']

        if ext in ('.svg', '.swf'): # place in an object element,
            tag = Object(node.get('alt', uri))
        else:
            tag = Img()

        tag.attrib.update(atts)

        self.parents.append(self.current)
        self.current.append(Sup(tag))
        self.current = tag

    def unknown_visit(self, node):
        nodename = node.__class__.__name__

        handler = NODES.get(nodename, None)
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
            new_current = Div(class_=nodename)

        self.parents.append(self.current)

        if not handled_elsewhere:
            self.current.append(new_current)

        self.current = new_current

    unknown_departure = pop_parent
    depart_reference = pop_parent

