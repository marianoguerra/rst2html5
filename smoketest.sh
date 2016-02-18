#!/usr/bin/env sh

mkdir -p smoketestoutput
rst2html5 examples/slides.rst > smoketestoutput/clean.html
rst2html5 --deck-js --pretty-print-code --embed-content examples/slides.rst > smoketestoutput/deck.html
rst2html5 --jquery --reveal-js --pretty-print-code examples/slides.rst > smoketestoutput/reveal.html
rst2html5 --stylesheet-path=html5css3/thirdparty/impressjs/css/impress-demo.css --impress-js examples/impress.rst > smoketestoutput/impress.html
rst2html5 --bootstrap-css --pretty-print-code --jquery --embed-content examples/slides.rst > smoketestoutput/bootstrap.html
rst2html5 --pygments examples/codeblock.rst > smoketestoutput/code.html
rst2html5 --jquery --reveal-js --reveal-js-opts theme=serif examples/slides.rst > smoketestoutput/reveal.html
rst2html5 --jquery --reveal-js --reveal-js-opts printpdf=true examples/slides.rst > smoketestoutput/reveal-print.html
