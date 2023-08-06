================
Playlist Kreator
================

Create playlists easily from a list of artists, using their top songs.

Currently supported: Google Music.

Requirements
------------

This project requires python 3+

Installation
------------

TODO

::

    pip install playlist-kreator

Example
-------

::

    playlist-kreator artists big_four_thrash.txt "Big Four of Thrash" --max-songs-per-artist=10

This will create a playlist called "Big Four of Thrash".
The playlist will be composed of 10 top songs for each artist listed in the file `big_four_thrash.txt`.
Content of `big_four_thrash.txt`:

::

    Anthrax
    Megadeth
    Metallica
    Slayer

You can find more examples in the ``example_artists`` folder

Known limitations
-----------------

- Google Music needs an application password, you can set it here: https://myaccount.google.com/apppasswords
- Google Music has a limit of 1000 songs per playlist
- THe search can be wrong sometimes, a better solution is in progress

Contributing
------------

Pull requests are welcome!

Running locally
```````````````

::

    pip install -r requirements.txt

Inspiration
-----------

Kreator is amazing. 🤘

|Kreator|

.. |Kreator| image:: http://kreator-terrorzone.de/images/releases/thumbs/cover_gods.jpg
