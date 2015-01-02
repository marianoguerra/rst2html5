#!/usr/bin/env python

# $Id: rst2html.py 4564 2006-05-21 20:44:42Z wiemann $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.


"""
A minimal front end to the Docutils Publisher, producing HTML.
"""


def main():
    try:
        import locale
        locale.setlocale(locale.LC_ALL, '')
    except:
        pass

    import os
    import sys
    command = sys.argv[0]
    command_dir = os.path.dirname(command)[:-3]
    sys.path.append(command_dir)

    from docutils.core import publish_cmdline, default_description

    import html5css3
    description = ('Generates html5 documents from standalone reStructuredText '
                   'sources.  ' + default_description)

    publish_cmdline(writer_name='html5', writer=html5css3.Writer(),
            description=description)
