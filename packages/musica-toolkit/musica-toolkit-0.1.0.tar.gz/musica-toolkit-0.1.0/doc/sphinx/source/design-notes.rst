.. _design-note-page:

==============
 Design Notes
==============

General Design
==============

Coding Philosophy
-----------------

Musica tries to provide a clean oriented object API rather than a set of macros.

.. And the implementation tries to respect usual coding standard.

In particular, for efficiency and readability reasons, we distinguish API docstrings and user guide,
and unit tests leave in separated files.

As Donald Knuth written, "Premature optimisation is the root of all evil (or at least most of it) in
programming".  Thus further optimisations must be motivated by code profiling.

Module loading should be fast in comparison to the human perception.  Lazy loading can help to meet
this requirement.

We use the last features of the Python language, thus we require an up to date Python 3 interpreter.

Internationalisation
--------------------

Musica supports Latin and English conventions, internationalisation of music therms is provided by
gettext.

Music also try to be independent of the Western music system.

Music Theory Implementation
---------------------------

Musica implements the western music system from its mathematical foundation. It means the music
system is mostly generated automatically rather than hardcoded in the source.  For example, the
Twelve-tone equal temperament is just defined by 12 tones, 7 natural notes (C, D, E, F, G, A, B) and
A440 as reference pitch.  The distribution of the notes is then determined from Pythagorean and
equal temperament theory.  See the module :mod:`Musica.Math.MusicTheory` for further details.

Figure Generation
-----------------

The best actual open formats for figures are PDF (Portable Document Format) and SVG (Scalable Vector
Graphics).  PDF and SVG are quite similar regarding the way to describe graphics, but they serve two
different purposes.  PDF is a binary format optimised for printed document rather than SVG is based
on XML and thus well suited for application inter-exchanges and web technologies.  XML is an
advantage of SVG over PDF, since it is easier to write XML than to deal with a binary format.  For
the same reason, it is easier to modify an SVG document than a PDF document.

In practice, we need both formats, depending if we want to make a printable document or create a web
content.  But this is not an issue, since we can convert a document from PDF to SVG, and vice versa.
We can thus imagine to generate a high quality document in PDF and then convert it to SVG.

If we want to generate scores or parts of scores, then the best solution is to use the `LilyPond
<http://lilypond.org/index.fr.html>`_ engraving program.  However Lilypond is not well suited when
we want a full control of the layout, in this case a basic engraving system is more adapted.

To generate high quality figures, we need these components:

* a basic geometry engine to compute coordinates,
* a text engine to format advanced text,
* a graphic engine to abstract a low level API (SVG or PDF),
* a library to write PDF or SVG.

There are several solutions to achieve this. We could simply generate XML from Python, but a text
engine like LaTeX is unrivalled, especially as we cannot use the power of HTML and `Mathjax
<https://www.mathjax.org>`_.  We could also use a graphic library, like the vector graphics language
and processor `Asymptote <http://asymptote.sourceforge.net>`_ , or the `ReportLab open-source PDF
Toolkit <http://www.reportlab.com/opensource>`_.  Note that Asymptote uses internally LaTeX to
generate labels.

Another solution is to use the power of `LaTeX <https://en.wikipedia.org/wiki/LaTeX>`_ in
combination with the package `TikZ/PGF <http://pgf.sourceforge.net>`_, a graphic systems for TeX and
the `Emmentaler font
<http://lilypond.org/doc/v2.19/Documentation/notation/the-emmentaler-font.html>`_ from the Lilypond
project. This solution provides a text engine and a graphic engine which abstract the PDF format.

Up to now, any TeX engine is able to generate directly SVG, but we have several possibilities to get
it.  We can convert PDF to SVG using `pdf2svg <http://www.cityinthesky.co.uk/opensource/pdf2svg>`_,
`MuPDF <https://mupdf.com>`_ or `Inkscape <https://inkscape.org>`_.  But we have a more direct path
using the `dvisvgm <http://dvisvgm.bplaced.net>`_ tool which convert DVI to SVG, since PGF has a
driver for `dvisvgm`.

Despite TeX was developed in 1978, many developers continue to improve and update it.  Recently the
`LuaTeX <http://www.luatex.org>`_ engine provides an interesting alternative to pdfTeX and new
features that benefit to PGF.

Another advantage of the TeX approach, is to provide an output in TeX/PGF which provides a
description of the figure in a graphic language that can be modified in an editor and then an SVG
output which can modified in an GUI SVG editor like Inkscape.  Despite the inherent complexity of
TeX/PGF, a tools like Inkscape is poorly adapted to make technical figures.

In conclusion, the approach to make figure in Musica provides three levels: the Python level, the
TeX/PGF level and finally the SVG level.

Coding
======

Copy constructor
----------------

.. code:: py3

    foo = Foo(...)

    bar = Foo(foo)       # C++ style
    bar = foo.clone()    # generic interface, don't ensure a particular type
    bar = Foo.clone(foo) # ensure type
