'''classes to ease the creation of html documents'''

import xml.etree.ElementTree as ET

class TagBase(ET.Element):
    def __init__(self, childs, attrs):
        ET.Element.__init__(self, self.__class__.__name__.lower(), attrs)

        for child in childs:
            self.append(child)

    def format(self, level=0):
        indent = " " * level

        if self.__class__.SELF_CLOSING:
            return "%s<%s%s />" % (indent, self.tag, attrs)
        else:
            attrs = " ".join(['%s="%s"' % (name, val) for (name, val) in self.attrib.iteritems()])

            nl = "\n" + indent

            if attrs:
                attrs = " " + attrs

            def format_child(child):
                if isinstance(child, TagBase):
                    return child.format(level + 1)
                else:
                    return indent + " " + str(child)

            childs = nl.join([format_child(child) for child in list(self)])

            if childs:
                childs = nl + childs + nl

            return "%s<%s%s>%s</%s>" % (indent, self.tag, attrs, childs, self.tag)

    def __str__(self):
        return self.format(0)

    __repr__ = __str__

TAGS = {
    "a": (False, "Defines a hyperlink"),
    "abbr": (False, "Defines an abbreviation"),
    "address": (False, "Defines an address element"),
    "area": (False, "Defines an area inside an image map"),
    "article": (False, "Defines an article"),
    "aside": (False, "Defines content aside from the page content"),
    "audio": (False, "Defines sound content"),
    "b": (False, "Defines bold text"),
    "base": (False, "Defines a base URL for all the links in a page"),
    "bdi": (False, "Defines text that is isolated from its surrounding text direction settings"),
    "bdo": (False, "Defines the direction of text display"),
    "blockquote": (False, "Defines a long quotation"),
    "body": (False, "Defines the body element"),
    "br": (True, "Inserts a single line break"),
    "button": (False, "Defines a push button"),
    "canvas": (False, "Defines graphics"),
    "caption": (False, "Defines a table caption"),
    "cite": (False, "Defines a citation"),
    "code": (False, "Defines computer code text"),
    "col": (False, "Defines attributes for table columns "),
    "colgroup": (False, "Defines groups of table columns"),
    "command": (False, "Defines a command button"),
    "datalist": (False, "Defines a list of options for an input field"),
    "dd": (False, "Defines a definition description"),
    "del": (False, "Defines deleted text"),
    "details": (False, "Defines details of an element"),
    "dfn": (False, "Defines a definition term"),
    "div": (False, "Defines a section in a document"),
    "dl": (False, "Defines a definition list"),
    "dt": (False, "Defines a definition term"),
    "em": (False, "Defines emphasized text "),
    "embed": (False, "Defines external interactive content or plugin"),
    "fieldset": (False, "Defines a fieldset"),
    "figcaption": (False, "Defines the caption of a figure element"),
    "figure": (False, "Defines a group of media content, and their caption"),
    "footer": (False, "Defines a footer for a section or page"),
    "form": (False, "Defines a form "),
    "h1": (False, "Defines header level 1"),
    "h2": (False, "Defines header level 2"),
    "h3": (False, "Defines header level 3"),
    "h4": (False, "Defines header level 4"),
    "h5": (False, "Defines header level 5"),
    "h6": (False, "Defines header level 6"),
    "head": (False, "Defines information about the document"),
    "header": (False, "Defines a header for a section or page"),
    "hgroup": (False, "Defines information about a section in a document"),
    "hr": (True, "Defines a horizontal rule"),
    "html": (False, "Defines an html document"),
    "i": (False, "Defines italic text"),
    "iframe": (False, "Defines an inline sub window (frame)"),
    "img": (True, "Defines an image"),
    "input": (True, "Defines an input field"),
    "ins": (False, "Defines inserted text"),
    "keygen": (False, "Defines a key pair generator field (for forms)"),
    "kbd": (False, "Defines keyboard text"),
    "label": (False, "Defines a label for a form control"),
    "legend": (False, "Defines a title in a fieldset"),
    "li": (False, "Defines a list item"),
    "link": (False, "Defines a resource reference"),
    "map": (False, "Defines an image map "),
    "mark": (False, "Defines marked text"),
    "menu": (False, "Defines a menu list"),
    "meta": (True, "Defines meta information"),
    "meter": (False, "Defines a scalar measurement within a known range"),
    "nav": (False, "Defines navigation links"),
    "noscript": (False, "Defines a noscript section"),
    "object": (False, "Defines an embedded object"),
    "ol": (False, "Defines an ordered list"),
    "optgroup": (False, "Defines an option group"),
    "option": (False, "Defines an option in a drop-down list"),
    "output": (False, "Defines the result of a calculation"),
    "p": (False, "Defines a paragraph"),
    "param": (False, "Defines a parameter for an object"),
    "pre": (False, "Defines preformatted text"),
    "progress": (False, "Represents the progress of a task"),
    "q": (False, "Defines a short quotation"),
    "rp": (False, "Used in ruby annotations to define what to show if a browser does not support the ruby element"),
    "rt": (False, "Defines explanation to ruby annotations"),
    "ruby": (False, "Defines ruby annotations"),
    "s": (False, "Defines text that is no longer correct"),
    "samp": (False, "Defines sample computer code"),
    "script": (False, "Defines a script"),
    "section": (False, "Defines a section"),
    "select": (False, "Defines a selectable list"),
    "small": (False, "Defines smaller text"),
    "source": (False, "Defines multiple media resources for media elements, such as audio and video"),
    "span": (False, "Defines a section in a document"),
    "strong": (False, "Defines strong text"),
    "style": (False, "Defines a style definition"),
    "sub": (False, "Defines subscripted text"),
    "summary": (False, "Defines the header of a 'detail' element"),
    "sup": (False, "Defines superscripted text"),
    "table": (False, "Defines a table"),
    "tbody": (False, "Defines a table body"),
    "td": (False, "Defines a table cell"),
    "textarea": (False, "Defines a text area"),
    "tfoot": (False, "Defines a table footer"),
    "th": (False, "Defines a table header"),
    "thead": (False, "Defines a table header"),
    "time": (False, "Defines a date/time"),
    "title": (False, "Defines the document title"),
    "tr": (False, "Defines a table row"),
    "track": (False, "Defines text tracks used in mediaplayers"),
    "ul": (False, "Defines an unordered list"),
    "var": (False, "Defines a variable"),
    "video": (False, "Defines a video or movie"),
    "wbr": (False, "Defines a possible line-break")
}

def create_tags(ctx):
    for (tag, info) in TAGS.iteritems():
        class_name = tag.title()
        self_closing, docs = info

        def __init__(self, *childs, **attrs):
            TagBase.__init__(self, childs, attrs)


        cls = type(class_name, (TagBase,), {
            "__doc__": docs,
            "__init__": __init__
        })

        cls.SELF_CLOSING = self_closing

        ctx[class_name] = cls

create_tags(globals())
