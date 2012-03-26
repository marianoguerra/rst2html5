efene
=====

.. class:: big

Erlang Factory Lite Brussels 2012

.. class:: by

Mariano Guerra

me
==

* Mariano Guerra
* http://github.com/marianoguerra
* C ASM C++ JAVA Python PHP JS C# Erlang Scala
* I may be a language geek
* I ♥ Python/JS/Erlang
* I like to create stuff

efene
=====

* http://efenelang.org
* programming language for the erlang VM

fnt
===

* http://marianoguerra.com.ar/fnt/
* jquery templates to erlang bytecode compiler

  * https://github.com/jquery/jquery-tmpl

write a template like this
--------------------------

.. class:: prettyprint

::

        hello ${name}!


compile it
----------

.. class:: prettyprint lang-erlang

::

        fnt:build(tpls, [{hello, "hello.fnt"}, {hello_name, "helloname.fnt"}]).

fnt (usage)
===========

.. class:: prettyprint lang-erlang

::

        6> tpls:hello_name([{name, "mariano"}]).
        ["hello ","mariano","!\n"]

        7> OutName = tpls:hello_name([{name, "mariano"}]).
        ["hello ","mariano","!\n"]

        8> io:format(OutName).
        hello mariano!
        ok

        9> OutName1 = tpls:hello_name([]).
        ["hello ","undefined","!\n"]

        10> io:format(OutName1).
        hello undefined!
        ok

fnt (low level)
===============

.. class:: prettyprint lang-erlang

::

        10> io:format(fnt:to_erlang(tpls, [{hello, "hello.fnt"}, {hello_name, "helloname.fnt"}, {greet, "greet.fnt"}, {list, "list.fnt"}, {insecure, "insecure.fnt"}])).
        -module(tpls).

        -export([hello/1, hello_name/1, greet/1, list/1,
                 insecure/1]).

        hello(Context) -> ["hello world!\n"].

        hello_name(Context) ->
            ["hello ", fnt:escape(fnt:get(Context, [name])), "!\n"].

        greet(Context) ->
            [case fnt:get(Context, [name]) == "admin" of
               true -> " well hello sir ";
               _ ->
                   case fnt:get(Context, [name]) == "root" of
                     true -> " you shouldn't be using the root user ";
                     _ ->
                         [" welcome ", fnt:escape(fnt:get(Context, [name])),
                          "! "]
                   end
             end,
             "\n\n",
             case fnt:get(Context, [name]) == "mariano" of
               true -> "hello mariano, you have superpowers!";
               _ -> ""
             end,
             "\n"].

        list(Context) ->
            [fnt:each(fnt:get(Context, [item]),
                      fun (Index, Value) ->
                              [" ", fnt:escape(Index), ": ", fnt:escape(Value), "\n"]
                      end),
             "\n"].

        insecure(Context) ->
            ["this is some content without escaping: ",
             fnt:get(Context, [value]),
             "\nthe same content escaped: ",
             fnt:escape(fnt:get(Context, [value])), "\n"].

qrly
====

* jquery selectors in erlang for xml/html
* https://github.com/marianoguerra/qrly

qrly (usage)
============

.. class:: prettyprint lang-erlang

::

        1> {ok, Qrly} = qrly_html:parse("../extra/test/test.html").
        ...

        2> Q1 = qrly_html:filter(Qrly, "h1").
        [{<<"h1">>,
          [{<<"class">>,<<"first-title asdwordclass">>}],
          [<<"personal">>]},
         {<<"h1">>,
          [{<<"class">>,<<"second-title wordclass">>}],
          [<<"projects">>]},
         {<<"h1">>,
          [{<<"title">>,<<"others">>},
           {<<"class">>,<<"third-title wordclass">>}],
          [<<"others">>]}]

        3> Q2 = qrly_html:filter(Qrly, "h1.first-title").
        [{<<"h1">>,
          [{<<"class">>,<<"first-title asdwordclass">>}],
          [<<"personal">>]}]

        4> io:format("~s~n", [qrly_html:to_string(Q1)]).
        <div><h1 class="first-title asdwordclass">personal</h1><h1 class="second-title wordclass">projects</h1><h1 title="others" class="third-title wordclass">others</h1></div>
        ok

        5> io:format("~s~n", [qrly_html:to_string(Q2)]).
        <div><h1 class="first-title asdwordclass">personal</h1></div>
        ok

erlang Argentina
================

* first Spanish speaking erlang user's group
* http://erlang.org.ar

pynerl
======

* run an embedded python interpreter in erlang
* https://github.com/marianoguerra/pynerl

.. class:: prettyprint lang-erlang

pynerl (usage)
==============

.. class:: prettyprint lang-erlang

::

        1> pynerl:eval("t = 1", "t").
        1

        2> pynerl:eval("t = 1 * 2", "t").
        2

        3> pynerl:eval("import time;t = time.time()", "t").
        1274236802.877999

        4> pynerl:eval("import random;t = random.random()", "t").
        0.45102117275294684

        5> pynerl:eval("t = print('hello erlang or python')", "t").
        hello erlang or python
                              none

        6> pynerl:call("time", "time", []).
        1274236859.510859

        7> pynerl:call("random", "random", []).
        0.9623136682858975

        8> pynerl:eval("t = True", "t").
        true

        9> pynerl:eval("t = 2.3", "t").
        2.3

and more stuff
==============

emesene
-------

* multi protocol/multi platform desktop IM client
* http://emesene.org
* python & gtk
* MSN, Jabber, Facebook chat, Gtalk

rst2html5
---------

* the thing that made this presentation
* https://github.com/marianoguerra/rst2html5/

why are you showing me all this?
================================

* to show what I like, what I do
* to see if you want to help me in some project ;)
* so you know where my opinions come from

you
===

* do you know erlang?

  * by name
  * coded hello world
  * coded simple app
  * erlang coder
  * I'm Joe Armstrong

* do you know efene?
* functional programmer
* OO programmer

so ... what's efene?
====================

* programming language for the erlang VM

  * compiles to bytecode
  * or translates to erlang

* python/js like syntax
* 100% compatible with erlang
  
  * all erlang syntax supported
  * 100% interoperability

* some syntactic sugar
* some extra features

history
=======

* started as a calculator to play with erlang (Oct 2009)
* the calculator got variables
* then functions
* then got from interpreted to compiled
* and it started to look like a language
* blogged about it
* got invited to Erlang Factory London 2010 (!)

status
======

* the core language is [almost] finished
* needs more documentation, examples, tutorials, promotion
* maybe more libs
* definitely more users :)

reason of existence
===================

* ideas behind erlang are really interesting
* I would like to help promoting erlang
* some people complain about the syntax
* some people complain about missing features or minor annoyances
* I like to make stuff :)
 
reason of existence (cont.)
============================

      In any language design, the total time spent discussing
      a feature in this list is proportional to two raised to
      the power of its position.

      0. Semantics
      1. Syntax
      2. Lexical syntax
      3. Lexical syntax of comments

.. class:: by

Wadler's Law

reason of existence (cont..)
============================

        Syntax is the user interface of programming languages

.. class:: by

Simon Peyton-Jones

reason of existence (cont...)
=============================

many languages taking erlang concepts                                          

* go                                                                          
* rust                                                                        
* dart                                                                        
* clojure
* scala                                                                       

  * akka                                                                      
                                                                               
they are willing to reinvent erlang, but not use it :(
                                                                               
reason of existence (cont....)
==============================

        Any sufficiently complicated concurrent/fault tolerant program contains
        an ad hoc, informally-specified, bug-ridden, slow implementation of half of
        Erlang.

.. class:: by

Mariano Guerra's Tenth Rule                                                    
        
show me some code
=================

Hello World (efene)
===================

.. class:: prettyprint lang-python

::

        @public
        hello = fn ("Winston Churchill") {
            io.format("Well, hello sir~n")
        }

        fn (Name) {
            io.format("Hello ~s!~n", [Name])
        }

        @public
        run = fn () {
            hello("Winston Churchill")
            hello("Erlang Factory Lite Brussels")
        }

output
------

::

        ➜  fnc hello.fn
        Compiling hello.fn

        ➜  fnc -r hello run
        Well, hello sir
        Hello Erlang Factory Lite Brussels!


Hello World (erlang)
====================

.. class:: prettyprint lang-erlang

::

        -module(hello).

        -export([hello/1, run/0]).

        hello("Winston Churchill") ->
            io:format("Well, hello sir~n");
        hello(Name) ->
            io:format("Hello ~s!~n", [Name]).

        run() ->
            hello("Winston Churchill"),
            hello("Erlang Factory Lite Brussels").

Hello World (ifene)
===================

.. class:: prettyprint lang-python

::

        @public
        hello = fn ("Winston Churchill")
            io.format("Well, hello sir~n")

        fn (Name)
            io.format("Hello ~s!~n", [Name])

        @public
        run = fn ()
            hello("Winston Churchill")
            hello("Erlang Factory Lite Brussels")

what we saw in the examples
===========================

* no punctuation
* no repetition of function names
* no need to declare the module

  * unless you want to

* local attributes
* curly braces or indentation

temporary variables (erlang)
============================

.. class:: prettyprint lang-erlang

::

        -module(tempvars).

        -export([run/0]).

        add(L, N) ->
            add(L, N, []).

        add([], _N, Accum) ->
            lists:reverse(Accum);

        add([H | T], N, Accum) ->
            add(T, N, [H + N | Accum]).

        run() ->
            L = lists:seq(1, 10),

            L1 = add(L, 2),
            L2 = lists:reverse(L1),

            io:format("~p~n", [L2]).

temporary variables (ifene)
===========================

.. class:: prettyprint lang-python

::

        add = fn (L, N)
            add(L, N, [])

        add = fn ([], _N, Accum)
            lists.reverse(Accum)

        fn ([H:T], N, Accum)
            add(T, N, [H + N:Accum])

        @public
        run = fn ()
            L = 1 .. 10 -> add(2) -> lists.reverse()

            io.format("~p~n", [L])

data types
==========

.. class:: prettyprint lang-python

::

        >>> 1
        1

        >>> 1.2
        1.2

        >>> atom
        atom

        >>> Var = "string"
        "string"

        >>> Bstr = <["binary string"]>
        <["binary string"]>

        >>> [1, 2, 3]
        [1, 2, 3]

        >>> (1, 2, 3)
        (1, 2, 3)

        >>> [X + 1 for X in 1 .. 10]
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        >>> for X in 1 .. 10 { X + 1 }
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

objects
=======

.. class:: prettyprint lang-python

::

        >>> P = {name: "Mariano", lastname: "Guerra"}
        {name: "Mariano", lastname: "Guerra"}

        >>> P.name
        "Mariano"

        >>> P.lastname
        "Guerra"

        >>> P1 = struct.set_prototype(P)
        {name: "Mariano", lastname: "Guerra"}

        >>> P1.has(name)
        true

        >>> P1.has(lastname)
        true

        >>> P1.has(money)
        false

        >>> P1.fields()
        [name, lastname]

        >>> P1.to_plist()
        [(name, "Mariano"), (lastname, "Guerra")]


objects (cont)
==============

.. class:: prettyprint lang-python

::

        >>> P2 = P1.name := "Luis Mariano"
        {name: "Luis Mariano", lastname: "Guerra"}

        >>> P1
        {name: "Mariano", lastname: "Guerra"}

        >>> P1.format()
        [123, "name: \"Mariano\", lastname: \"Guerra\"", 125]

        >>> P1.print()
        {name: "Mariano", lastname: "Guerra"}
        ok

        >>> P3 = struct.from_plist([name => "bob", lastname => "sponge"])
        {name: "bob", lastname: "sponge"}

        >>> ok => 42
        (ok, 42)

blocks
======

.. class:: prettyprint lang-python

::

        @public
        run = fn
            L = lst.map(1 .. 10) do (X)
                X * 2

            io.format("~p~n", [L])

output
------

::

        ➜  fnc block.ifn
        Compiling block.ifn

        ➜  fnc -r block run
        [2,4,6,8,10,12,14,16,18,20]

meta (erlang)
=============

.. class:: prettyprint lang-erlang

::

        -module(meta).

        -export([erlfun/1]).

        -define(ERLNUM, 4).
        -define(ERLMACRO(A), A + 1).

        erlfun(A) ->
            fun (B) ->
                B * A
            end.

meta (ifene)
============

.. class:: prettyprint lang-python

::

        @import("meta.erl")

        $FnNum = 42
        $FnMacro = fn (A)
            A + 1

        fnfun = fn (A)
            fn (B)
                B * A

        @public
        run = fn ()
            io.format("erlang constant ~p, macro ~p, fun ~p~n", [
                $ERLNUM,
                $ERLMACRO(1),
                erlfun(2)(3)])

            io.format("efene constant ~p, macro ~p, fun ~p~n", [
                $FnNum,
                $FnMacro(1),
                fnfun(2)(3)])

more meta
=========

.. class:: prettyprint lang-python

::

        @public
        run = fn ()
            L = $[lists.seq(1000, 1010)]
            io.format("~p~n", [L])

.. class:: prettyprint lang-erlang

::

        -module(moremeta).

        -export([run/0]).

        run() ->
            L = [1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007,
                 1008, 1009, 1010],
            io:format("~p~n", [L]).

even more meta
==============

.. class:: prettyprint lang-python

::

        >>> [|A + 1|]
        (op, 1, '+', (var, 1, 'A'), (integer, 1, 1))

        >>> ast.line(15, [|A + 1|])
        (op, 15, '+', (var, 15, 'A'), (integer, 15, 1))

        >>> A = [|1|]
        (integer, 1, 1)

        >>> B = [|2|]
        (integer, 1, 2)

        >>> Add = [|$(A) + $(B)|]
        (op, 1, '+', (integer, 1, 1), (integer, 1, 2))

other features
==============

* support for records, @spec and @type annotations

  * all implemented as libraries (except record access and manipulation)
  * import is a library too and can be extended to import other file types

* function calls in if expressions
* operator like python/js

  * and or xor not

    * for non short circuit versions: andd orr

  * \+ \- \* / % 
  * == === <= >= < > != !== 


what I would like efene to become
=================================

* efene should be to erlang what coffeescript is to javascript

  * an alternative
  * different syntax, same semantics
  * integrate well with existing tools
  * generate readable erlang code (if requested)
  * zero friction to mix erlang/efene
  * a place to try new ideas faster

* a language that plays nice with the web
* a welcoming place for newbies
* a place where experimenting is OK

future
======

* documentation
* finish porting tests to etap
* promotion
* more user friendliness
  
  * better error messages
  * better tools
  * documentation

help!
=====

* try efene
* join the mailing list
* report issues
* submit improvements
* spread the word

  * read/correct/improve the docs
  * write blog posts/tutorials

* write or improve tools

  * syntax highlighters
  * rebar integration
  * text editor integration
  * others

technical stuff
===============

* lexx
  
  * fnc -t lex

* yecc

  * fnc -t tree
  * fnc -t ast
  * fnc -t mod

* compile (compile:forms)

  * fnc -t beam
  * fnc  

how do I build it?
==================

::

        git clone https://github.com/marianoguerra/efene.git
        cd efene
        ./build.sh

build.sh will
-------------

* compile the fnc binary

  * cd tools
  * make

* rebar get-deps
* rebar compile

first time usage (REPL)
=======================

run
---

::

        $ bin/fnc -s

write
-----

.. class:: prettyprint lang-python

::

        >>> io.format("Hello world!~n")
        Hello world!
        ok

        >>> 

first time usage (compiling)
============================

write (hello.fn)
----------------

.. class:: prettyprint lang-python

::

        @public
        run = fn () {
            io.format("Hello World!~n")
        }

compile
-------

::

        $ fnc hello.fn 
        Compiling hello.fn

run
---

::

        $ fnc -r hello run
        Hello World!

first time usage (translating)
==============================

run
---

::

        $ fnc -t erl hello.fn 

you get
-------

.. class:: prettyprint lang-erlang

::

        -module(hello).

        -export([run/0]).

        run() -> io:format("Hello World!~n").



efene in your app
=================

Create a dir for the project, and download rebar
------------------------------------------------

::

        $ mkdir myapp
        $ cd myapp
        $ wget http://bitbucket.org/basho/rebar/downloads/rebar; chmod u+x rebar

Create a file named rebar.config
--------------------------------

.. class:: prettyprint lang-erlang

::

        {deps, [
          {efene, ".*",
            {git, "git://github.com/marianoguerra/efene.git", "master"}
          },
          {rebar_efene_plugin, ".*",
            {git, "git://github.com/DavidMikeSimon/rebar_efene_plugin.git", "stable"}
          }
        ]}.

        {plugins, [ rebar_efene_plugin ]}.
        {plugin_dir, "deps/rebar_efene_plugin/src"}.

efene in your app (cont.)
=========================

Create a directory named src, and within it create a myapp.app.src file
-----------------------------------------------------------------------

.. class:: prettyprint lang-erlang

::

        {application, myapp, [
          {description, "My first app ever"},
          {vsn, "0.0.1"}
        ]}.

write an efene file
-------------------

tell rebar to get the dependencies and compile
----------------------------------------------

::

        $ rebar get-deps
        $ rebar compile

thanks!
=======

