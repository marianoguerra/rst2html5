rst2html5 tools - RestructuredText to HTML5 + bootstrap css
===========================================================

We all love rst and the ability to generate any format, but the rst2html tool generates really basic html and css.

This tool will generate newer, nicer, more readable markup and provide ways to modify the output with extensions like nice css
thanks to twitter's bootstrap css or online presentations with deck.js

get it
------

via pip::

        pip install rst2html5-tools

locally::

        git clone https://github.com/marianoguerra/rst2html5.git
        cd rst2html5
        git submodule init
        git submodule update

        sudo python setup.py install

use it
------

to generate a basic html document::

        rst2html5 examples/slides.rst > clean.html

to generate a set of slides using deck.js::

        rst2html5 --deck-js --pretty-print-code --embed-content examples/slides.rst > deck.html

to generate a set of slides using reveal.js::

        rst2html5 --jquery --reveal-js --pretty-print-code examples/slides.rst > reveal.html

to generate a set of slides using impress.js::

    rst2html5 --stylesheet-path=html5css3/thirdparty/impressjs/css/impress-demo.css --impress-js examples/impress.rst > output/impress.html

to generate a page using bootstrap::

        rst2html5 --bootstrap-css --pretty-print-code --jquery --embed-content examples/slides.rst > bootstrap.html

to higlight code with pygments::

    rst2html5 --pygments examples/codeblock.rst > code.html

note that you will have to add the stylesheet for the code to actually highlight, this just does the code parsing and html transformation.

to embed images inside the html file to have a single .html file to distribute
add the --embed-images option.

to add `mathjax <http://mathjax.org>`_ support::

    rst2html5 --mathjax examples/mathjax.rst mathjax.html

post processors support optional parameters, they are passed with a command
line option with the same name as the post processor appending "-opts" at the
end, for example to change the revealjs theme you can do::

        rst2html5 --jquery --reveal-js --reveal-js-opts theme=serif examples/slides.rst > reveal.html

you can also pass the base path to the theme css file::

        rst2html5 --jquery --reveal-js --reveal-js-opts theme=serif,themepath=~/mytheme examples/slides.rst > reveal.html

it will look at the theme at ~/mytheme/serif.css

options are passed as a comma separated list of key value pairs separated with
an equal sign, values are parsed as json, if parsing fails they are passed as
strings, for example here is an example of options::

    --some-processor-opts theme=serif,count=4,verbose=true,foo=null

if a key is passed more than once that parameter is passed to the processor as a list of values, note that if only one value is passed it's passed as it is, the convenience function as_list is provided to handle this case if you want to always receive a list.

to add custom js files to the resulting file you can use the --add-js post processor like this::

    rst2html5 slides.rst --add-js --add-js-opts path=foo.js,path=bar.js

that command will add foo.js and bar.js as scripts in the resulting html file.

Pretty Print Code Notes
.......................

enable it::

    --pretty-print-code

add language specific lexers::

    --pretty-print-code-opts langs=clj:erlang

Note: you have to pass both options when passing opts to prettify like this::

    --pretty-print-code --pretty-print-code-opts langs=clj:erlang

that is, the name of the languages separated by colons, available lexers at the
moment of this writing are:

* apollo
* basic
* clj
* css
* dart
* erlang
* go
* hs
* lisp
* llvm
* lua
* matlab
* ml
* mumps
* n
* pascal
* proto
* rd
* r
* scala
* sql
* tcl
* tex
* vb
* vhdl
* wiki
* xq
* yaml

you can see the available lexers under html5css3/thirdparty/prettify/lang-\*.js

RevealJs Notes
..............

to print pass --reveal-js-opts printpdf=true, for example::

    rst2html5 --jquery --reveal-js --reveal-js-opts printpdf=true examples/slides.rst > reveal-print.html

this can be used to open with chrome or chromium and print as pdf as described here: https://github.com/hakimel/reveal.js#pdf-export

see it
------

you can see the examples from the above commands here:

* http://marianoguerra.github.com/rst2html5/output/clean.html
* http://marianoguerra.github.com/rst2html5/output/reveal.html
* http://marianoguerra.github.com/rst2html5/output/deck.html
* http://marianoguerra.github.com/rst2html5/output/impress.html
* http://marianoguerra.github.com/rst2html5/output/bootstrap.html

example of video directive

* http://marianoguerra.github.com/rst2html5/output/videos.html


want to contribute ?
--------------------

clone and send us a pull request! ::

    git clone https://github.com/marianoguerra/rst2html5.git
    cd rst2html5
    git submodule update --init
    python setup.py develop

note to self to release
-----------------------

* update version on setup.py

::

    python setup.py sdist upload
