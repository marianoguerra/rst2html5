# $Id: __init__.py 7061 2011-06-29 16:24:09Z milde $
# Author: Mariano Guerra <luismarianoguerra@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Simple HyperText Markup Language document tree Writer.

The output conforms to the HTML version 5

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

from docutils import frontend, nodes, utils, writers, languages

from html import *
# import default post processors so they register
import postprocessors

class Writer(writers.Writer):

    default_stylesheet = 'rst2html5.css'

    default_stylesheet_path = utils.relative_path(
        os.path.join(os.getcwd(), 'dummy'),
        os.path.join(os.path.dirname(__file__), default_stylesheet))

    settings_spec = (
        'HTML-Specific Options',
        None,
        [('Specify comma separated list of stylesheet URLs. '
          'Overrides previous --stylesheet and --stylesheet-path settings.',
          ['--stylesheet'],
          {'metavar': '<URL>', 'overrides': 'stylesheet_path'}),
         ('Specify comma separated list of stylesheet paths. '
          'With --link-stylesheet, '
          'the path is rewritten relative to the output HTML file. '
          'Default: "%s"' % default_stylesheet_path,
          ['--stylesheet-path'],
          {'metavar': '<file>', 'overrides': 'stylesheet',
           'default': default_stylesheet_path}),
         ('Embed the content (css, js, etc) in the output HTML file.  The content '
          'files must be accessible during processing. This is the default.',
          ['--embed-content'],
          {'default': 1, 'action': 'store_true',
           'validator': frontend.validate_boolean}),
         ('Link to the content in the output HTML file. '
          'Default: embed content.',
          ['--link-content'],
          {'dest': 'embed_content', 'action': 'store_false'}),
         ('Specify the initial header level.  Default is 1 for "<h1>".  '
          'Does not affect document title & subtitle (see --no-doc-title).',
          ['--initial-header-level'],
          {'choices': '1 2 3 4 5 6'.split(), 'default': '1',
           'metavar': '<level>'}),
         ('Format for footnote references: one of "superscript" or '
          '"brackets".  Default is "brackets".',
          ['--footnote-references'],
          {'choices': ['superscript', 'brackets'], 'default': 'brackets',
           'metavar': '<format>',
           'overrides': 'trim_footnote_reference_space'})
         ])

    settings_defaults = {
        'output_encoding_error_handler': 'xmlcharrefreplace'
    }

    post_processors = {}

    def __init__(self):
        writers.Writer.__init__(self)
        self.translator_class = HTMLTranslator

    @classmethod
    def add_postprocessor(cls, name, opt_name, processor):
        opt_switch = '--' + opt_name.replace("_", "-")

        cls.settings_spec[2].append((name, [opt_switch], {
                'dest': opt_name,
                'action': 'store_true',
                'validator': frontend.validate_boolean
            }
        ))

        cls.post_processors[opt_name] = processor

    def translate(self):
        visitor = self.translator_class(self.document)
        self.document.walkabout(visitor)
        tree = visitor.get_tree()

        settings = self.document.settings
        embed = settings.embed_content

        for (key, processor) in Writer.post_processors.iteritems():
            if getattr(settings, key):
                processor(tree, embed)

        self.output = DOCTYPE
        self.output += str(tree)

for (key, data) in postprocessors.PROCESSORS.iteritems():
    Writer.add_postprocessor(data["name"], key, data["processor"])


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

    translator._append(Tr(Td(label, class_="field-label"), td), node)

    return current

def problematic(node, translator):
    name = node.tagname
    label = translator.language.labels.get(name, name)

    current = Span(class_="problematic")
    wrapper = A(current, href="#" + node['refid'])

    translator._append(wrapper, node)

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

    cls = 'alert-message block-message '

    if tagname in ('note', 'tip', 'hint'):
        cls += 'info'
    elif tagname in ('attention', 'caution', 'important', 'warning'):
        cls += 'warning'
    elif tagname in ('error', 'danger'):
        cls += 'error'
    else:
        cls += tagname

    cls += classes

    title = ""

    if tagname != "admonition":
        title = tagname.title()

    div = Div(P(title, class_="admonition-title"), class_=cls)
    translator._append(div, node)

    return div

def skip(node, translator):
    return translator.current

def swallow_childs(node, translator):
    return Span(class_="remove-me")

NODES = {
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
    "caption": Figcaption,
    "citation": (Div, "cite"),
    "citation_reference": None,
    "classifier": classifier,
    "colspec": skip,
    "comment": lambda node, _: Comment(node),
    "compound": None,
    "container": None,
    "decoration": skip,
    "definition": Dd,
    "definition_list": Dl,
    "definition_list_item": skip,
    "description": Td,
    "doctest_block": (Pre, "prettyprint lang-python"),
    "document": None,
    "emphasis": Em,
    "field": Tr,
    "field_body": Td,
    "field_list": Table,
    "field_name": (Td, "field-label"),
    "figure": Figure,
    "footer": skip, # TODO temporary skip
    "footnote": None,
    "footnote_reference": None,
    "generated": skip,
    "header": skip, # TODO temporary skip
    "image": Img,
    "inline": Span,
    "label": (Div, "du-label"),
    "legend": skip,
    "line": None,
    "line_block": None,
    "list_item": Li,
    "literal": Code, # inline literal markup use the <code> tag in HTML5. inline code uses <code class="code">
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
    "problematic": problematic,
    "raw": None,
    "reference": None,
    "row": Tr,
    "rubric": None,
    "sidebar": Aside,
    "strong": Strong,
    "subscript": Sub,
    "substitution_definition": swallow_childs,
    "substitution_reference": None,
    "superscript": Sup,
    "table": Table,
    "tbody": Tbody,
    "term": Dt,
    "tgroup": skip,
    "thead": Thead,
    "title_reference": Cite,
    "transition": Hr,

    # handled in visit_*
    "entry": None,
    "enumerated_list": None,
    "literal_block": None,
    "target": None,
    "text": None,
    "title": None,
    "topic": None,
    "section": None,
    "subtitle": None,
    "system_message": None,
}

class HTMLTranslator(nodes.NodeVisitor):
    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self.root = Body()
        self.indent = 1
        self.parents = []
        self.current = self.root
        self.settings = document.settings

        self.title = self.settings.title or ""
        self.title_level = int(self.settings.initial_header_level)
        lcode = document.settings.language_code

        try:
            self.language = languages.get_language(lcode)
        except TypeError:
            self.language = languages.get_language(lcode, document.reporter)

        # make settings for this
        self.content_type = self.settings.output_encoding

        self.head = Head(
            Meta(charset=self.content_type),
            Title(self.title))

        styles = utils.get_stylesheet_list(self.settings)

        for style in styles:
            self.head.append(self.css(style))

    def css(self, path):
        if self.settings.embed_content:
            content = open(path).read()
            return Style(content, type="text/css")
        else:
            return Link(href=path, rel="stylesheet", type_="text/css")

    def js(self, path):
        content = open(path).read().decode('utf-8')
        return Script(content)

    def get_tree(self):
        return Html(self.head, self.root)

    def astext(self):
        return self.get_tree().format(0, self.indent)

    def _stack(self, tag, node, append_tag=True):
        self.parents.append(self.current)

        if append_tag:
            self._append(tag, node)

        self.current = tag

    def _append(self, tag, node):
        self.current.append(tag)

        if isinstance(tag, basestring):
            return

        atts = {}
        ids = []

        classes = node.get('classes', [])

        cls = node.get("class", None)
        if cls is not None:
            classes.append(cls)

        # move language specification to 'lang' attribute
        languages = [cls for cls in classes
                     if cls.startswith('language-')]

        if languages:
            # attribute name is 'lang' in XHTML 1.0 but 'xml:lang' in 1.1
            atts['lang'] = languages[0][9:]
            classes.pop(classes.index(languages[0]))

        classes = ' '.join(classes).strip()

        if classes:
            atts['class'] = classes

        assert 'id' not in atts

        ids.extend(node.get('ids', []))

        if 'ids' in atts:
            ids.extend(atts['ids'])
            del atts['ids']

        if ids:
            atts['id'] = ids[0]

            for id in ids[1:]:
                self.current.append(Span(id=id))

        tag.attrib.update(atts)


    def pop_parent(self, node):
        self.current = self.parents.pop()

    def visit_Text(self, node):
        self._append(unicode(node.astext()), node)

    def visit_entry(self, node):
        atts = {}
        if isinstance(node.parent.parent, nodes.thead):
            tag = Th()
        else:
            tag = Td()

        if 'morerows' in node:
            atts['rowspan'] = node['morerows'] + 1

        if 'morecols' in node:
            atts['colspan'] = node['morecols'] + 1

        tag.attrib.update(atts)

        if len(node) == 0:              # empty cell
            tag.append(".")

        self._stack(tag, node)

    def depart_Text(self, node):
        pass

    def visit_literal_block(self, node):
        pre = Pre()
        self._stack(pre, node, True)
        if 'code' in node.get('classes', []):
            code = Code()
            self._stack(code, node)
            del pre.attrib['class']

    def depart_literal_block(self, node):
        if isinstance(self.current, Code):
            self.current = self.parents.pop()

        self.current = self.parents.pop()

    def visit_title(self, node, sub=0):
        if isinstance(self.current, Table):
            self._stack(Caption(), node)
        else:
            heading = HEADINGS.get(self.title_level + sub, H6)()
            current = heading
            insert_current = True

            # only wrap in header tags if the <title> is a child of section
            # this excludes the main page title, subtitles and topics
            if self.current.tag == "section":
                self._stack(Header(), node, True)

            if node.hasattr('refid'):
                current = A(href= '#' + node['refid'])
                heading.append(current)
                insert_current = False
                self._append(heading, node)

            self._stack(current, node, insert_current)

    def depart_title(self, node):
        self.current = self.parents.pop()

        if self.current.tag == "header":
            self.current = self.parents.pop()

    def visit_subtitle(self, node):
        self.visit_title(node, 1)

    def visit_topic(self, node):
        self.title_level += 1
        self._stack(Div(class_="topic"), node)

    def depart_topic(self, node):
        self.title_level -= 1
        self.pop_parent(node)

    def visit_section(self, node):
        self.title_level += 1
        self._stack(Section(), node)

    depart_section = depart_topic

    def visit_document(self, node):
        #self.head[1].text = node.get('title', 'document')
        pass

    def depart_document(self, node):
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
        self._stack(tag, node)

    def visit_citation_reference(self, node):
        tag = A(href='#' + node['refid'], class_="citation-reference")
        self._stack(tag, node)

    def visit_footnote_reference(self, node):
        href = '#' + node['refid']
        tag = A(class_="footnote-reference", href=href)

        self._stack(tag, node)

    def visit_target(self, node):
        self._stack(Span(class_="target"), node)

    def visit_author(self, node):
        if isinstance(self.current, Ul):
            tag = Li(class_="author")
            self._append(tag, node)
        else:
            tag = docinfo_item(node, self)

        self.parents.append(self.current)
        self.current = tag

    def visit_enumerated_list(self, node):
        atts = {}

        if 'start' in node:
            atts['start'] = node['start']

        if 'enumtype' in node:
            atts['class'] = node['enumtype']

        self._stack(Ol(**atts), node)

    def visit_system_message(self, node):
        msg_type = node['type']
        cont = Div(class_='alert-message block-message system-message ' +
                msg_type.lower())
        text = P("System Message: %s/%s" % (msg_type, node['level']),
            class_='system-message-title admonition-title')

        cont.append(text)

        backlinks = ''

        if len(node['backrefs']):
            backrefs = node['backrefs']

            if len(backrefs) == 1:
                backlinks = Em(A("backlink", href="#" +  backrefs[0]))
            else:
                backlinks = Div(P("backlinks"), class_="backrefs")

                for (i, backref) in enumerate(backrefs):
                    backlinks.append(A(str(i), href="#" +  backref))
                    backlinks.append(" ")

        if node.hasattr('line'):
            line = 'line %s ' % node['line']
        else:
            line = ' '

        cont.append(Span(quote(node['source']), class_="literal"))
        cont.append(line)
        cont.append(backlinks)

        self._stack(cont, node)

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

        if 'align' in node:
            atts['class'] = 'align-%s' % node['align']

        if ext in ('.svg', '.swf'): # place in an object element,
            tag = Object(node.get('alt', uri))
        else:
            tag = Img()

        tag.attrib.update(atts)

        self._stack(tag, node)

    def unknown_visit(self, node):
        nodename = node.__class__.__name__

        handler = NODES.get(nodename, None)
        already_inserted = False

        if isinstance(handler, tuple):
            tag_class, cls = handler
            new_current = tag_class(class_=cls)
        elif type(handler) == type and issubclass(handler, TagBase):
            new_current = handler()
        elif callable(handler):
            new_current = handler(node, self)
            already_inserted = True
        else:
            known_attributes = self.get_known_attributes(node)
            new_current = Div(**known_attributes)

        self._stack(new_current, node, not already_inserted)

    def get_known_attributes(self, node):
        attrs = {}

        for attr, value in node.attributes.iteritems():
            if attr.startswith("data-") or attr in {'title', 'class', 'id'}:
                attrs[attr] = value

        return attrs

    unknown_departure = pop_parent
    depart_reference = pop_parent
