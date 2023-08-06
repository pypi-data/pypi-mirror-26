Diamond-Patterns
================

**Diamond-Patterns** are scaffolds for knowledge work.  Use patterns to go faster.

Installation
------------

UNIX
^^^^

Install on Linux, BSD, or OS X.  Supports system-wide installation and python virtual environments.

::

    pip install diamond-patterns

OS X
^^^^

Install system-wide with Homebrew.

::

    brew install https://raw.github.com/iandennismiller/diamond-patterns/master/etc/diamond-patterns.rb

Windows
^^^^^^^

Diamond-patterns installs system-wide with Administrator privileges.

::

    start-process powershell –verb runAs
    easy_install -U mr.bob==0.1.2
    pip install diamond-patterns

Usage
^^^^^

::

    mkdir ~/Documents/my-article
    cd ~/Documents/my-article
    diamond --skel article scaffold
