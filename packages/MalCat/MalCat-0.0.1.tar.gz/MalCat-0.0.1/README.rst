MalCat
======

MalCat is a Python utility used as the backend for MalCat_, a CSS generator used for styling anime lists on MyAnimeList_.
It provides a quick and easy way to:

- fetch the contents of a user's anime/manga list
- format the list to a CSS template
- profit


Installation
------------

.. code:: bash

    $ pip install malcat


Usage
--------

.. code:: python

    from malcat.generator import MalCat

    generator = MalCat()
    css = generator.media('Doomcat55', 'anime', '#more$id { background-image: url($series_image); }')
    print(css)

Check MalCat's `MAL thread`__ for info on templates and parameters.

.. _MyAnimeList: https://myanimelist.net
.. _MalCat: https://myanimelist.net/forum/?topicid=1533260
__ MalCat_
