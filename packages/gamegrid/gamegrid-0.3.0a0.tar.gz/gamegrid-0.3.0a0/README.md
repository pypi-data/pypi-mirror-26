gamegrid
===============================

A Custom Jupyter Widget Library to display a simple grid for a game.

Each cell in the grid contains an image, and each image can have a state of selected or unselected.

Installation
------------

To install use pip:

    $ pip install gamegrid
    $ jupyter nbextension enable --py --sys-prefix gamegrid


For a development installation (requires npm),

    $ git clone https://github.com/N/A/gamegrid.git
    $ cd gamegrid
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix gamegrid
    $ jupyter nbextension enable --py --sys-prefix gamegrid
