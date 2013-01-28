rst2html5 - RestructuredText to HTML5 + bootstrap css
=====================================================

we all love rst and the hability to generate any format, but the rst2html tool
generates really basic html and css.

this tool will generate newer, nicer, more readable markup and provide
ways to modify the output with extensions like nice css
thanks too twitter's bootstrap css or online presentations with deck.js

get it
------

::

        git clone https://github.com/marianoguerra/rst2html5.git
        cd rst2html5
        git submodule update --init

use it
------

to generate a set of slides using deck.js::

        cd rst2html5
        ./bin/rst2html5 --deck-js --pretty-print-code --embed-content examples/slides.rst > deck.html

to generate a set of slides using reveal.js::

        bin/rst2html5 --jquery --reveal-js --pretty-print-code examples/slides.rst > reveal.html

to generate a set of slides using impress.js::

    ./bin/rst2html5 --stylesheet-path=html5css3/thirdparty/impressjs/css/impress-demo.css --impress-js examples/impress.rst > output/impress.html

to generate a page using bootstrap::

        ./bin/rst2html5 --bootstrap-css --pretty-print-code --jquery --embed-content examples/slides.rst > bootstrap.html

to embed images inside the html file to have a single .html file to distribute
add the --embed-images option.

see it
------

you can see the examples from the above commands here:

* http://marianoguerra.github.com/rst2html5/output/reveal.html
* http://marianoguerra.github.com/rst2html5/output/deck.html
* http://marianoguerra.github.com/rst2html5/output/impress.html
* http://marianoguerra.github.com/rst2html5/output/bootstrap.html
