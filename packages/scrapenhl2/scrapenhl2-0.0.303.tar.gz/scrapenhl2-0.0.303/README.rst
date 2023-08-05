.. image:: https://travis-ci.org/muneebalam/scrapenhl2.svg?branch=master
    :target: https://travis-ci.org/muneebalam/scrapenhl2
.. image:: https://coveralls.io/repos/github/muneebalam/scrapenhl2/badge.svg?branch=master
    :target: https://coveralls.io/github/muneebalam/scrapenhl2?branch=master
.. image:: https://landscape.io/github/muneebalam/scrapenhl2/master/landscape.svg?style=flat
   :target: https://landscape.io/github/muneebalam/scrapenhl2/master
   :alt: Code Health
.. image:: https://badge.fury.io/py/scrapenhl2.svg
    :target: https://badge.fury.io/py/scrapenhl2
Introduction
------------

scrapenhl2 is a python package for scraping and manipulating NHL data pulled from the NHL website.

Installation
-------------
You need python3 and the python scientific stack (e.g. numpy, matplotlib, pandas, etc).
Easiest way is to simply use `Anaconda <https://conda.io/docs/user-guide/install/index.html>`_.
To be safe, make sure you have python 3.5+, matplotlib 2.0+, and pandas 0.20+.

After that, all you need to do is open up terminal or command line and enter::

    pip install scrapenhl2

(If you have multiple versions of python installed, you may need to alter that command slightly.)

For now, installation should be pretty quick, but in the future it may take awhile
(depending on how many past years' files I make part of the package).

As far as coding environments go, I recommend jupyter notebook or
`Pycharm Community <https://www.jetbrains.com/pycharm/download/#section=mac>`_.
Some folks also like the PyDev plugin in Eclipse. The latter two are full-scale applications, while the former
launches in your browser. Open up terminal or command line and run::

    jupyter notebook

Then navigate to your coding folder, start a new Python file, and you're good to go.

Use
---

*Note that because this is in pre-alpha/alpha, syntax and use may be buggy and subject to change.*

On startup, when you have an internet connection and some games have gone final since you last used the package,
open up your python environment and update::

    from scrapenhl2 import *
    autoupdate()

Autoupdate should update you regularly on its progress; be patient.

To get a game H2H, use::

    season = 2016
    game = 30136
    game_h2h(season, game)

.. image:: examples/WSH-TOR_G6.png

To get a game timeline, use::

    game_h2h(season, game)

.. image:: examples/WSH-TOR_G6_timeline.png

To get a player rolling CF% graph, use::

    player = 'Ovechkin'
    rolling_games = 25
    start_year = 2015
    end_year = 2017
    rolling_player_cf(player, rolling_games, start_year, end_year)

.. image:: examples/Ovechkin_rolling_cf.png

To launch the app to help you navigate use::

    runapp()

When the docs are up, you should look through them. Also always feel free to contact me with questions or suggestions.

Contact
--------
`Twitter
<http://www.twitter.com/muneebalamcu>`_.

Collaboration
-------------

I'm happy to partner with you in development efforts--just shoot me a message.
Please also let me know if you'd like to alpha- or beta-test my code.

Donations
---------
If you would like to support my work, please donate money to a charity of your choice. Many large charities do
great work all around the world (e.g. Médecins Sans Frontières),
but don't forget that your support is often more critical for local/small charities.
Also consider that small regular donations are sometimes better than one large donation.

You can vet a charity you're targeting using a `charity rating website <https://www.charitynavigator.org/>`_.

If you do make a donation, make me happy `and leave a record here <https://goo.gl/forms/tl1jVm0D7esLLbfm1>`_..
(It's anonymous.)

Change log
----------

10/21/17: Added basic front end. Committed early versions of 2017 logs.

10/16/17: Added initial versions of game timelines, player rolling corsi, and game H2H graphs.

10/10/17: Bug fixes on scraping and team logs. Started methods to aggregate 5v5 game-by-game data for players.

10/7/17: Committed code to scrape 2010 onward and create team logs; still bugs to fix.

9/24/17: Committed minimal structure.

Major outstanding to-dos
------------------------

* Front end with Flask
* Add more graph methods
* Add more data search methods
* Bring in old play by play and shifts from HTML