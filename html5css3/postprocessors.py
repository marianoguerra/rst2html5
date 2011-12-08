import os

import html5css3

from html import *

def js(path, embed=True):
    content = open(path).read().decode('utf-8')
    # TODO: handle non embeding
    return Script(content)

def css(path, embed=True):
    content = open(path).read().decode('utf-8')
    # TODO: handle non embeding
    return Style(content, type="text/css")

def pretty_print_code(tree, embed=True):
    # TODO: make a query
    head = tree[0]
    body = tree[1]

    body.append(js("html5css3/prettify.js", embed))
    body.append(Script("$(function () { prettyPrint() })"))

    head.append(css("html5css3/prettify.css"))

def jquery(tree, embed=True):
    body = tree[1]
    body.append(js("html5css3/jquery-1.7.1.min.js", embed))

def deckjs(tree, embed=True):
    head = tree[0]
    body = tree[1]

    def add_class(element, cls_name):
        cls = element.get("class", "")

        if cls:
            cls += " " + cls_name
        else:
            cls += cls_name

        element.set("class", cls)

    def path(*args):
        return os.path.join("thirdparty", "deckjs", *args)

    add_class(body, "deck-container")

    for section in tree.findall(".//section"):
        add_class(section, "slide")

    # Core and extension CSS files
    head.append(css(path("core", "deck.core.css"), embed))
    head.append(css(path("extensions", "goto", "deck.goto.css"), embed))
    head.append(css(path("extensions", "menu", "deck.menu.css"), embed))
    head.append(css(path("extensions", "navigation", "deck.navigation.css"), embed))
    head.append(css(path("extensions", "status", "deck.status.css"), embed))
    head.append(css(path("extensions", "hash", "deck.hash.css"), embed))

    # Theme CSS files (menu swaps these out)
    head.append(css(path("themes", "style", "web-2.0.css"), embed))
    head.append(css(path("themes", "transition", "horizontal-slide.css"), embed))

    body.append(js(path("modernizr.custom.js"), embed))
    jquery(tree, embed)

    # Deck Core and extensions
    body.append(js(path("core", "deck.core.js"), embed))
    body.append(js(path("extensions", "hash", "deck.hash.js"), embed))
    body.append(js(path("extensions", "menu", "deck.menu.js"), embed))
    body.append(js(path("extensions", "goto", "deck.goto.js"), embed))
    body.append(js(path("extensions", "status", "deck.status.js"), embed))
    body.append(js(path("extensions", "navigation", "deck.navigation.js"), embed))

    body.append(Script("$(function () { $.deck('.slide'); });"))


def bootstrap_css(tree, embed=True):
    head = tree[0]

    head.append(css("html5css3/bootstrap.css"))
    head.append(css("html5css3/rst2html5.css"))

PROCESSORS = {
    "jquery": {
        "name": "add jquery",
        "processor": jquery
    },
    "pretty_print_code": {
        "name": "pretty print code",
        "processor": pretty_print_code
    },
    "deck_js": {
        "name": "deck.js",
        "processor": deckjs
    },
    "bootstrap_css": {
        "name": "bootstrap css",
        "processor": bootstrap_css
    }
}
