
djangocms bootstrap grid
==================================

An opinionated implementation of a bootstrap grid plugin for djangocms.

Installation
------------

    pip install cmsplugin_ss_grid

In your settings.py

    INSTALLED_APPS = (
        ...
        'cmsplugin_ss_grid',
    )

Custom classes can be applied to both the background and the cells.  In settings.py:

    CMSPLUGIN_SS_GRID = dict(
        BACKGROUND_CLASSES=(
            ('', 'None'),
            ('background--light', 'Light'),
            ('background--dark', 'Dark')
        ),
        CELL_CLASSES=(
            ('', 'None'),
            ('some-style', 'Some Style')
        ),
        CELL_DEFAULT_CLASS='class-added-to-all-cells'
    )


Tested on
    * Python 2.7. 3.4, 3.5
    * Django 1.8, 1.9, 1.10
    * DjangoCms 3.4
