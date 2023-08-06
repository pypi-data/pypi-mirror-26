darpy
=====

Distribute Archived Python

Install with ::

    pip install darpy


``darpy`` isn't better than shell scripting. It *is* shell scripting. No
illusions, no lies, no false abstractions.

Why?
----

1. Pre-baking a virtualenv and shipping it around is full of woes. (e.g.
   ``-relocatable`` only kind of works, but virtualenv may have abspaths in it)

2. Want to be able to bundle dependencies of an application so that you can
   have them openly specified in ``requirements.txt``, but reproducibly deploy
   the same exact dependencies

How?
----

Use ``tar``, ``pip download``, ``pip install``, to make python archives which
can unpack and install without network access.

Works best if you ``darpy pack`` and ``darpy unpack`` on the same platform
version, python version, and architecture. ``darpy pack`` may fetch arch or
platform-specific binary packages based on the platform where it runs.

Usage
-----

Pack it Up
~~~~~~~~~~

If you have a package in dir ``$HOME/myproject`` ::

    darpy pack --src "$HOME/myproject"

If you want to use a ``requirements.txt`` outside of ``setup.py`` ::

    darpy pack --requirements "$HOME/myproject/requirements.txt"

or use both ::

    darpy pack --src "$HOME/myproject" --requirements "$HOME/myproject/requirements.txt"


Unpack It
~~~~~~~~~

Works best if done on the same platform

Unpack into current virtualenv with ::

    darpy unpack darpy-pack.tgz

Unpack into target virtualenv with ::

    darpy unpack darpy-pack.tgz --virtualenv "$HOME/myvirtualenv"
