.. image:: https://img.shields.io/badge/Donate-PayPal-green.svg
    :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=X9KC9TLLXPQWA

=========
DashTable
=========

.. contents::

Video Tutorial
==============

.. image:: http://i.imgur.com/v1rGCHn.png
    :target: https://www.youtube.com/watch?v=bdcswQq4lIM&feature=youtu.be

Introduction
============

Use DashTable to create ASCII tables like this reStructured_ Table:

.. _reStructured: http://docutils.sourceforge.net/docs/user/rst/quickref.html#tables

::

    +------------+------------+------------+
    | Header 1   | Header 2   | Header 3   |
    +============+============+============+
    | body row 1 | column 2   | column 3   |
    +------------+------------+------------+
    | body row 2 | Cells may span columns. |
    +------------+------------+------------+
    | body row 3 | Cells may  | - Cells    |
    +------------+ span rows. | - contain  |
    | body row 4 |            | - blocks.  |
    +------------+------------+------------+

Installation
============

::

    pip install dashtable

Example Usage
=============

HTML to reStructured Table
--------------------------

html2rst requires a filepath or a string to work.

.. code-block:: python

    from dashtable import html2rst

    filepath = "path/to/html/file.html"
    print(html2rst(filepath, force_headers=False, center_cells=False))


Command Line Method:

::

    python html2rst.py input.html output.rst --force_headers --center_cells --center_headers

HTML to MarkDown Table
----------------------

html2md requires a filepath or a string to work.

.. code-block:: python

    from dashtable import html2md

    filepath = "path/to/html/file.html"
    print(html2md(filepath))

Command line method:

::

    python html2md.py input.html output.md

List of Lists to reStructered Table
-----------------------------------

.. code-block:: python

    from dashtable import data2rst

    table = [
        ['Row\nSpan', 'Header'],
        ['Cell', ''],
        ['Column Span', '']
        ]

    column_span = ([0, 0], [1, 0])
    row_span = ([2, 0], [2, 1])

    my_spans = [column_span, row_span]

    print(data2rst(table, spans=my_spans, use_headers=True, center_cells=False, center_headers=True))

List of Lists to Markdown Table
-------------------------------

.. code-block:: python

    from dashtable import data2md

    table = [
        ['Header 1', 'Header 2', 'Header 3'],
        ['Column 1', 'Column 2', 'Column 3']
    ]

    print(data2md(table))
    

