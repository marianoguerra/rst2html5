import os

import html5css3
import html

BASE_PATH = os.path.dirname(__file__)

def abspath(path):
    return os.path.join(BASE_PATH, "..", path)

def js(path, embed=True):
    content = open(abspath(path)).read().decode('utf-8')

    if embed:
        return html.Script(content)
    else:
        return html.Script(src=path)

def css(path, embed=True):
    content = open(abspath(path)).read().decode('utf-8')

    if embed:
        return html.Style(content, type="text/css")
    else:
        return html.Link(href=path, rel="stylesheet", type="text/css")

def pretty_print_code(tree, embed=True):
    head = tree[0]
    body = tree[1]

    body.append(js("prettify.js", embed))
    body.append(html.Script("$(function () { prettyPrint() })"))

    head.append(css("prettify.css"))

def jquery(tree, embed=True):
    body = tree[1]
    body.append(js("jquery-1.7.1.min.js", embed))

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

    body.append(html.Script("$(function () { $.deck('.slide'); });"))

def revealjs(tree, embed=True):
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
        return os.path.join("thirdparty", "revealjs", *args)

    # remove the default style
    head.remove(head.find("./style"))
    add_class(body, "reveal")
    slides = html.Div(class_="slides")

    for item in list(body):
        body.remove(item)
        slides.append(item)

    body.append(slides)

    # <link rel="stylesheet" href="css/reveal.css">
    # <link rel="stylesheet" href="css/theme/default.css" id="theme">
    head.append(css(path("css", "reveal.css"), embed))
    head.append(css(path("css", "theme", "default.css"), embed))

    # <!-- For syntax highlighting -->
    # <link rel="stylesheet" href="lib/css/zenburn.css">
    # head.append(css(path("lib", "css", "zenburn.css"), embed))

    # <script src="lib/js/head.min.js"></script>
    # <script src="js/reveal.min.js"></script>
    body.append(js(path("lib", "js", "head.min.js"), embed))
    body.append(js(path("js", "reveal.min.js"), embed))

    body.append(html.Script("$(function () { Reveal.initialize({history:true}); });"))

def bootstrap_css(tree, embed=True):
    head = tree[0]

    head.append(css("bootstrap.css", embed))
    head.append(css("rst2html5.css", embed))

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
    "reveal_js": {
        "name": "reveal.js",
        "processor": revealjs
    },
    "bootstrap_css": {
        "name": "bootstrap css",
        "processor": bootstrap_css
    }
}
