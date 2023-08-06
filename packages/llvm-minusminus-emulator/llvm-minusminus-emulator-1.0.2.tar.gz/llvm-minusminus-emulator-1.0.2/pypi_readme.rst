Overview
========

This application is an emulator/debugger for LLVM-- as defined in the
Compiler course (dOvs) at Aarhus University.

While I hope that you will find it useful, the tool is being provided AS
IS, this means

#. There is no guarantee that emulator emulates LLVM-- correctly.
   Various liberties has been taken to simplify the emulations, e.g.
   values of type ``i64`` can be arbitrarily large. And there can, of
   course, be bugs in the application.
#. Not all parts of LLVM-- has been implemented. While the main set of
   instructions and types has been implemented at this point, you might
   hit a "TODO: Not implemented yet" message.
#. Many type annotations are being ignored. This means that ill-typed
   LLVM-- programs might be emulated without a problem. This can give a
   false sense of security, so always use a tool like ``clang``, if you
   want to check types of your generated code
#. We, as TAs, do not give support for this emulator.
#. **If your generated code works in this emulator, but not in clang,
   your generated code is incorrect!** We, as TAs, will **not** accept
   it.

Requirements
============

This application is written in Python. It was developed in Python 3.6,
but I expected to work for Python 3.5 and above. Note that Python 2 is
not supported.

Several Linux distributions have Python 2 as the default. You can
usually use the commands ``python3``, ``pip3``, etc. to use Python 3 on
such systems (assuming you have installed Python 3).

The application uses some third party libraries as indicated in
``requirements.txt``.

This project is designed for Linux, though I do not expect there to be
any issues on other platforms. As a consequence the commands given below
are designed for a Linux shell. Lines beginning with a dollar sign ($)
indicate commands you enter into your terminal, other lines are output
from running those commands

Getting Python 3
----------------

To see if you already have Python 3 installed, try running (the lines
beginning with $):

.. code:: bash

    $ python --version
    Python 2.7.14
    $ python3 --version
    Python 3.6.3

If one of these commands gives a version number >= 3, you have Python 3
through that command (without ``--version``, of course). In the example
above, I need to use the command ``python3`` in order to use the correct
version of Python for this emulator.

Otherwise, you could try to install Python 3 via your package manager.
Depending on which Linux distribution you use, you could try something
like

.. code:: bash

    $ apt install python3

or

.. code:: bash

    $ sudo apt install python3

Getting pip for Python 3
------------------------

You need pip to (easily) install Python packages. If your Linux
distribution came with Python 2 and pip, the pip you have might not work
for Python 3. Let us first check that:

.. code:: bash

    $ pip --version
    pip 9.0.1 from /usr/lib/python2.7/site-packages (python 2.7)
    $ pip3 --version
    pip 9.0.1 from /usr/lib/python3.6/site-packages (python 3.6)

As with the Python version commands in the last section, I have to use
``pip3``. If I just used ``pip`` packages would be installed for Python
2, which I do not want.

Pip should come with newer versions of Python. If you have a new version
of Python, but no pip, you might need to install it seperately. You
could try (depending on your Linux distribution)

.. code:: bash

    $ apt install python3-pip

or

.. code:: bash

    $ sudo apt install python3-pip

Installation
============

Installation includes

-  Downloading and installing dependencies
-  Downloading the emulator
-  Storing the emulator libraries where your other Python libraries are
-  Adding a small script to easily start the emulator

Pip way
-------

The recommended way to quickly install and use the emulator, is to
install it via pip. The name on PyPI (where pip gets the software from)
is ``llvm-minusminus-emulator`` [1]_.

Make sure that you have Python 3 and pip installed (see above). Then
install the emulator by running

.. code:: bash

    $ pip3 install llvm-minusminus-emulator

If all goes well, you are now ready to use the emulator.

Git way
-------

To get the very latest version, you can do the following

If you have not already, download the code.

.. code:: bash

    $ cd path/to/folder/where/you/want/to/store/the/emulator
    $ git clone git@gitlab.com:cfreksen/llvm--emulator.git

To install the software, you can use ``pip`` on the folder containing
``setup.py``:

.. code:: bash

    $ cd path/to/folder/where/you//stored/the/emulator/llvm--emulator
    $ pip3 install .

You should now be ready to use the software.

Uninstalling
------------

To remove the emulator, just uninstall via pip:

.. code:: bash

    $ pip3 uninstall llvm-minusminus-emulator

Usage
=====

If installing the emulator went well, a script (``llvm--emulator``)
should have been added to your ``bin`` folder. This means that you can
start the emulator (wherever you are), by running that script:

.. code:: bash

    $ llvm--emulator --help
    usage: llvm--emulator [-h] [-a AUTO_PATH]

    A hacky LLVM-- emulator/debugger

    optional arguments:
      -h, --help            show this help message and exit
      -a AUTO_PATH, --auto AUTO_PATH
                            Automatically step through llvm in the given file

To automatically step through a LLVM file (and be quite verbose about
it), you can use the ``-a`` (``--auto``) flag:

.. code:: bash

    $ llvm--emulator -a path/to/your/file.ll

When running the emulator you might get messages like the following:

.. code:: bash

    WARNING: Couldn't open 'parser.out'. [Errno 13] Permission denied: '/usr/lib/python3.6/site-packages/llvm_emulator/parser.out'
    WARNING: Couldn't create 'parsetab'. [Errno 13] Permission denied: '/usr/lib/python3.6/site-packages/llvm_emulator/parsetab.py'

This is because the script does not have permission to write files among
your Python libraries. This is because the parser inside the emulator
tries to cache its parsing table (think of ``tiger.grm.sml``) where the
parsing code is located. If does not have permission to do that, it
still parses your LLVM code; it just needs to rebuild the parsing table
next time you run the emulator. These warnings should be safe to ignore.

I have tried to fix this issue without success, so hopefully you can
live with a few warning messages.

Example
-------

Let us say, that we have the following LLVM-- code in ``some_file.ll``

.. code:: llvm

    %Ttigermain = type { i64, i64, i64 }

    define i64 @tigermain (i64 %U_mainSL_8, i64 %U_mainDummy_9) {
        %t = alloca %Ttigermain
        %a = getelementptr %Ttigermain, %Ttigermain* %t, i32 0, i32 1
        store i64 9, i64* %a
        %r = load i64, i64* %a
        %s = add i64 100, %r
        %b = getelementptr %Ttigermain, %Ttigermain* %t, i32 0, i32 0
        store i64 %s, i64* %b
        ret i64 %s
    }

Then we run the emulator:

.. code:: bash

    $ llvm--emulator -a some_file.ll
    Parsing some_file.ll
    Beginning execution of some_file.ll
    Heap after globals are allocated:
    [None]

    Evaluating alloca %Ttigermain
    alloca {i64, i64, i64}  -->  allocating 3 cells
    %t <- 1

    Evaluating getelementptr %Ttigermain, %Ttigermain* %t, i32 0, i32 1
    Gep formula: 1 + 0 * 3 + (1)
    %a <- 2

    Evaluating store i64 9, i64* %a
    heap[2] <- 9

    Evaluating load i64, i64* %a
    load heap[2]
    %r <- 9

    Evaluating add i64 100, %r
    add 100, 9
    %s <- 109

    Evaluating getelementptr %Ttigermain, %Ttigermain* %t, i32 0, i32 0
    Gep formula: 1 + 0 * 3 + 0
    %b <- 1

    Evaluating store i64 %s, i64* %b
    heap[1] <- 109

    Evaluating ret i64 %s
    Returning 109

    Stepping done!
    Final ssa_env: {'U_mainSL_8': 1234, 'U_mainDummy_9': 5678, 't': 1, 'a': 2, 'r': 9, 's': 109, 'b': 1}
    Final heap: [None, 109, 9, <<Garbage>>]
    Program resulted in 109 after 8 steps

This shows which values variables have as they are encountered as well
as the order the instructions are evaluated.

Alternatives
------------

If the ``llvm--emulator`` script does not work for you, you can inspect
it in the ``path/to/emulator/repository/bin/`` folder (assuming you have
the source code. See the section 'Installation:Git Way', or look at the
code online on https://gitlab.com/cfreksen/llvm--emulator). It should be
clear enough what the script does, and if you know a bit of Python, you
should be able to tweak it to your needs.

Known Issues/Missing Features
=============================

Here some of the known major issues/missing features are listed. This
list might be updated, should the issues be fixed/the features
implemented:

Interactive mode
----------------

There is currently no support for stepping through the code one key
press at a time. Similarly, there is no support for inserting
breakpoints, or looking up the current values in memory/registers via
commands.

Builtin functions
-----------------

When generating LLVM code from Tiger code, there can be several calls to
functions defined in a file called ``runtime.c``. Many of these
functions are not implemented in the emulator. However, ``allocRecord``,
``initArray``, and ``print`` are so that will hopefully be enough for
the majority of your LLVM programs.

License
=======

The code in this project is licensed under GPLv3+. The full licensing
text can be found in the ``LICENSE`` file, while a small but descriptive
header is:

    LLVM-- Emulator -- A simple hacky emulator and debugger for LLVM--
    Copyright © 2017 Casper Freksen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see http://www.gnu.org/licenses/.

.. [1]
   I know the name is ugly, but Python packaging was not happy about the
   double dash in ``llvm--emulator``, and ``llvm-emulator`` makes it
   sound like it covers the entire LLVM IR language.
