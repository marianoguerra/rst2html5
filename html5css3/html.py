'''classes to ease the creation of html documents'''

import xml.etree.ElementTree as ET
import sys

IS_PY3 = sys.version[0] == '3'

if IS_PY3:
    unicode = str


if callable(ET.Element) and hasattr(ET, "_ElementInterface"):
    class Element(ET._ElementInterface, object):
        pass
else:
    class Element(ET.Element):
        pass

def quote(text):
    """encode html entities"""
    text = unicode(text)
    return text.translate({
        ord('&'): u'&amp;',
        ord('<'): u'&lt;',
        ord('"'): u'&quot;',
        ord('>'): u'&gt;',
        ord('@'): u'&#64;',
        0xa0: u'&nbsp;'})

def nop(text):
    return text

def to_str(value):
    if isinstance(value, unicode):
        return value
    return unicode(value)

def escape_attrs(node):
    node.attrib = dict([(key.rstrip("_"), unicode(val))
        for (key, val) in node.attrib.items()])

    for child in node:
        escape_attrs(child)

class TagBase(Element):
    "base class for all tags"

    SELF_CLOSING = False
    COMPACT = False
    QUOTE = True

    def __init__(self, childs, attrs):
        "add childs and call parent constructor"
        tag = self.__class__.__name__.lower()
        Element.__init__(self, tag, attrs)

        for child in childs:
            self.append(child)

        escape_attrs(self)

    def append(self, child):
        children = list(self)
        if not isinstance(child, Element):
            if children:
                last_children = children[-1]

                if last_children.tail is None:
                    last_children.tail = to_str(child)
                else:
                    last_children.tail += to_str(child)

            elif self.text is None:
                self.text = to_str(child)
            else:
                self.text += to_str(child)
        else:
            Element.append(self, child)

    def __repr__(self):
        return ET.tostring(self, "utf-8", "html")

    def __str__(self):
        "return a string representation"
        text = ET.tostring(self, "utf-8", "html")
        if IS_PY3:
            return text.decode('utf8')
        return text

Comment = ET.Comment


# List of HTML tags for dynamically creating tag classes.
#
# Keys are tag names, values are lists containing the values for
# ``TagBase.QUOTE``, ``TagBase.COMPACT``, ``TagBase.SELF_CLOSING``, and
# ``TagBase.__doc__``.
#
# See also ``create_tags``.
_TAGS = {
    "a": (True, True, False, "Defines a hyperlink"),
    "abbr": (True, False, False, "Defines an abbreviation"),
    "address": (True, False, False, "Defines an address element"),
    "area": (True, False, False, "Defines an area inside an image map"),
    "article": (True, False, False, "Defines an article"),
    "aside": (True, False, False, "Defines content aside from the page content"),
    "audio": (True, False, False, "Defines sound content"),
    "b": (True, False, False, "Defines bold text"),
    "base": (True, False, False, "Defines a base URL for all the links in a page"),
    "bdi": (True, False, False, "Defines text that is isolated from its surrounding"
        "text direction settings"),
    "bdo": (True, False, False, "Defines the direction of text display"),
    "blockquote": (True, False, False, "Defines a long quotation"),
    "body": (True, False, False, "Defines the body element"),
    "br": (True, False, True, "Inserts a single line break"),
    "button": (True, False, False, "Defines a push button"),
    "canvas": (True, False, False, "Defines graphics"),
    "caption": (True, False, False, "Defines a table caption"),
    "cite": (True, True, False, "Defines a citation"),
    "code": (True, False, False, "Defines computer code text"),
    "col": (True, False, False, "Defines attributes for table columns "),
    "colgroup": (True, False, False, "Defines groups of table columns"),
    "command": (True, False, False, "Defines a command button"),
    "datalist": (True, False, False, "Defines a list of options for an input field"),
    "dd": (True, False, False, "Defines a definition description"),
    "del": (True, False, False, "Defines deleted text"),
    "details": (True, False, False, "Defines details of an element"),
    "dfn": (True, False, False, "Defines a definition term"),
    "div": (True, False, False, "Defines a section in a document"),
    "dl": (True, False, False, "Defines a definition list"),
    "dt": (True, False, False, "Defines a definition term"),
    "em": (True, True, False, "Defines emphasized text "),
    "embed": (True, False, False, "Defines external interactive content or plugin"),
    "fieldset": (True, False, False, "Defines a fieldset"),
    "figcaption": (True, False, False, "Defines the caption of a figure element"),
    "figure": (True, False, False, "Defines a group of media content, and their caption"),
    "footer": (True, False, False, "Defines a footer for a section or page"),
    "form": (True, False, False, "Defines a form "),
    "h1": (True, True, False, "Defines header level 1"),
    "h2": (True, True, False, "Defines header level 2"),
    "h3": (True, True, False, "Defines header level 3"),
    "h4": (True, True, False, "Defines header level 4"),
    "h5": (True, True, False, "Defines header level 5"),
    "h6": (True, True, False, "Defines header level 6"),
    "head": (True, False, False, "Defines information about the document"),
    "header": (True, False, False, "Defines a header for a section or page"),
    "hgroup": (True, False, False, "Defines information about a section in a document"),
    "hr": (True, False, True, "Defines a horizontal rule"),
    "html": (True, False, False, "Defines an html document"),
    "i": (True, True, False, "Defines italic text"),
    "iframe": (True, False, False, "Defines an inline sub window (frame)"),
    "img": (True, False, True, "Defines an image"),
    "input": (True, False, True, "Defines an input field"),
    "ins": (True, False, False, "Defines inserted text"),
    "keygen": (True, False, False, "Defines a key pair generator field (for forms)"),
    "kbd": (True, False, False, "Defines keyboard text"),
    "label": (True, True, False, "Defines a label for a form control"),
    "legend": (True, False, False, "Defines a title in a fieldset"),
    "li": (True, False, False, "Defines a list item"),
    "link": (True, False, True, "Defines a resource reference"),
    "map": (True, False, False, "Defines an image map "),
    "mark": (True, False, False, "Defines marked text"),
    "menu": (True, False, False, "Defines a menu list"),
    "meta": (True, False, True, "Defines meta information"),
    "meter": (True, False, False, "Defines a scalar measurement within a known range"),
    "nav": (True, False, False, "Defines navigation links"),
    "noscript": (True, False, False, "Defines a noscript section"),
    "object": (True, False, False, "Defines an embedded object"),
    "ol": (True, False, False, "Defines an ordered list"),
    "optgroup": (True, False, False, "Defines an option group"),
    "option": (True, False, False, "Defines an option in a drop-down list"),
    "output": (True, False, False, "Defines the result of a calculation"),
    "p": (True, True, False, "Defines a paragraph"),
    "param": (True, False, False, "Defines a parameter for an object"),
    "pre": (True, True, False, "Defines preformatted text"),
    "progress": (True, False, False, "Represents the progress of a task"),
    "q": (True, False, False, "Defines a short quotation"),
    "rp": (True, False, False, "Used in ruby annotations to define what to show if a "
            "browser does not support the ruby element"),
    "rt": (True, False, False, "Defines explanation to ruby annotations"),
    "ruby": (True, False, False, "Defines ruby annotations"),
    "s": (True, True, False, "Defines text that is no longer correct"),
    "samp": (True, False, False, "Defines sample computer code"),
    "script": (False, True, False, "Defines a script"),
    "section": (True, False, False, "Defines a section"),
    "select": (True, False, False, "Defines a selectable list"),
    "small": (True, True, False, "Defines smaller text"),
    "source": (True, False, False, "Defines multiple media resources for media elements, "
            "such as audio and video"),
    "span": (True, True, False, "Defines a section in a document"),
    "strong": (True, True, False, "Defines strong text"),
    "style": (False, False, False, "Defines a style definition"),
    "sub": (True, True, False, "Defines subscripted text"),
    "summary": (True, False, False, "Defines the header of a 'detail' element"),
    "sup": (True, True, False, "Defines superscripted text"),
    "table": (True, False, False, "Defines a table"),
    "tbody": (True, False, False, "Defines a table body"),
    "td": (True, False, False, "Defines a table cell"),
    "textarea": (True, False, False, "Defines a text area"),
    "tfoot": (True, False, False, "Defines a table footer"),
    "th": (True, False, False, "Defines a table header"),
    "thead": (True, False, False, "Defines a table header"),
    "time": (True, False, False, "Defines a date/time"),
    "title": (True, False, False, "Defines the document title"),
    "tr": (True, False, False, "Defines a table row"),
    "track": (True, False, False, "Defines text tracks used in mediaplayers"),
    "tt": (True, True, False, "Defines teletype text"),
    "ul": (True, False, False, "Defines an unordered list"),
    "var": (True, True, False, "Defines a variable"),
    "video": (True, False, False, "Defines a video or movie"),
    "wbr": (True, False, False, "Defines a possible line-break"),

    # MathML tags
    "math": (True, False, False, "MathML top-level container"),
    "maction": (True, False, False, "MathML Binded actions to sub-expressions"),
    "maligngroup": (True, False, False, "MathML Alignment group"),
    "malignmark": (True, False, False, "MathML Alignment points"),
    "menclose": (True, False, False, "MathML Enclosed contents"),
    "merror": (True, False, False, "MathML Enclosed syntax error messages"),
    "mfenced": (True, False, False, "MathML Parentheses"),
    "mfrac": (True, False, False, "MathML Fraction"),
    "mglyph": (True, False, False, "MathML Displaying non-standard symbols"),
    "mi": (True, False, False, "MathML Identifier"),
    "mlabeledtr": (True, False, False, "MathML Labeled row in a table or a matrix"),
    "mlongdiv": (True, False, False, "MathML Long division notation"),
    "mmultiscripts": (True, False, False, "MathML Prescripts and tensor indices"),
    "mn": (True, False, False, "MathML Number"),
    "mo": (True, False, False, "MathML Operator"),
    "mover": (True, False, False, "MathML Overscript"),
    "mpadded": (True, False, False, "MathML Space around content"),
    "mphantom": (True, False, False, "MathML Invisible content with reserved space"),
    "mroot": (True, False, False, "MathML Radical with specified index"),
    "mrow": (True, False, False, "MathML Grouped sub-expressions"),
    "ms": (True, False, False, "MathML String literal"),
    "mscarries": (True, False, False, "MathML Annotations such as carries"),
    "mscarry": (True, False, False, "MathML Single carry"),
    "msgroup": (True, False, False, "MathML Grouped rows"),
    "msline": (True, False, False, "MathML Horizontal line"),
    "mspace": (True, False, False, "MathML Space"),
    "msqrt": (True, False, False, "MathML Square root without an index"),
    "msrow": (True, False, False, "MathML Rows"),
    "mstack": (True, False, False, "MathML Stacked alignment"),
    "mstyle": (True, False, False, "MathML Style change"),
    "msub": (True, False, False, "MathML Subscript"),
    "msup": (True, False, False, "MathML Superscript"),
    "msubsup": (True, False, False, "MathML Subscript-superscript pair"),
    "mtable": (True, False, False, "MathML Table or matrix"),
    "mtd": (True, False, False, "MathML Cell in a table or a matrix"),
    "mtext": (True, False, False, "MathML Text"),
    "mtr": (True, False, False, "MathML Row in a table or a matrix"),
    "munder": (True, False, False, "MathML Underscript"),
    "munderover": (True, False, False, "MathML Underscript-overscript pair"),
}


def _create_tags(ctx):
    "create all classes and put them in ctx"

    for (tag, info) in _TAGS.items():
        class_name = tag.title()
        quote_, compact, self_closing, docs = info

        def __init__(self, *childs, **attrs):
            TagBase.__init__(self, childs, attrs)

        cls = type(class_name, (TagBase,), {
            "__doc__": docs,
            "__init__": __init__
        })

        cls.QUOTE = quote_
        cls.COMPACT = compact
        cls.SELF_CLOSING = self_closing

        ctx[class_name] = cls

_create_tags(globals())


def tag_from_element(el):
    """
    Convert an Element into a Tag.

    ``el`` is an instance of ``Element``. Returns an instance of the
    corresponding subclass of ``TagBase``.
    """
    tag = el.tag
    namespace = None
    if tag.startswith('{'):
        # Strip namespace of the form "{namespace}tag"
        namespace,tag = tag[1:].split('}')
    try:
        cls = globals()[tag.title()]
        if not issubclass(cls, TagBase):
            raise KeyError()
    except KeyError:
        raise ValueError("TagBase doesn't have a subclass for '%s'." % tag)
    children = [tag_from_element(c) for c in el]
    tag = cls(*children, **el.attrib)
    tag.text = el.text
    tag.tail = el.tail
    if namespace:
        tag.attrib['xmlns'] = namespace
    return tag


def html_to_tags(code):
    """
    Convert HTML code to tags.

    ``code`` is a string containing HTML code. The return value is a
    list of corresponding instances of ``TagBase``.
    """
    code = ('<div>' + code + '</div>').encode('utf8')
    el = ET.fromstring(code)
    return [tag_from_element(c) for c in el]


DOCTYPE = "<!DOCTYPE html>"

HEADINGS = {
    1: H1,
    2: H2,
    3: H3,
    4: H4,
    5: H5,
    6: H6
}
