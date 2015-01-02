Mathjax example
===============

build me with --mathjax

to see some nice math like this \[ax^2 + bx + c = 0\]
$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$

$x+\sqrt{1-x^2}$

pass me --mathjax-opts config=path to embed the config from a file::

    ./bin/rst2html5 --mathjax --mathjax-opts config=html5css3/thirdparty/MathJax/config/default.js --embed-content examples/mathjax.rst mathjax.html

content like the following::

      MathJax.Hub.Config({
        extensions: ["tex2jax.js"],
        jax: ["input/TeX", "output/HTML-CSS"],
        tex2jax: {
          inlineMath: [ ['$','$'], ["\\(","\\)"] ],
          displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
          processEscapes: true
        },
        "HTML-CSS": { availableFonts: ["TeX"] }
      });

you can also customize the mathjax cdn path by passing the url parameter to
matjax opts like::

    --mathjax-opts url=http://cdn.mathjax.org/mathjax/latest/MathJax.js

this page was compiled with this command::

    ./bin/rst2html5 --mathjax --mathjax-opts url=http://cdn.mathjax.org/mathjax/latest/MathJax.js\?config=TeX-AMS-MML_HTMLorMML examples/mathjax.rst mathjax.html
