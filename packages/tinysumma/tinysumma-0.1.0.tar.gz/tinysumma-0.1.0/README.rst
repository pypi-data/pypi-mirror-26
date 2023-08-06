tinysumma 0.1.0: summarize tinyletter statistics
================================================

Python package providing a friendly command-line interface to summarize tinyletter email newsletter statistics.

Built on top of `tinyapi`_, which wraps around TinyLetter's API, which is publicly accessible but undocumented—so, no guarantees.

.. _tinyapi: https://github.com/jsvine/tinyapi

Usage
-----

``tinysumma`` runs as a command-line script. Sample usage:

::

	>>tinysumma --help
	usage: tinysumma [-h] [-l] [-n NUMBEREDISSUE] [-u LETTERNAME]
					 [--datadir DATADIR]

	optional arguments:
	  -h, --help            show this help message and exit
	  -l, --latestissue     print stats latest issue
	  -n NUMBEREDISSUE, --numberedissue NUMBEREDISSUE
							print stats for numbered issue (first=1)
	  -u LETTERNAME, --updateletter LETTERNAME
							download latest stats to *.csv
	  --datadir DATADIR     data directory (if not current dir)

	>>tinysumma --updateletter mytinyletter
	Password:

	>>tinysumma --latestissue
	Your issue, 'Issue Title', was opened by 42 unique subscribers.
	That's a 75.0% open rate!
	The most popular url was https://github.com/awbirdsall/tinysumma,
	with 17 total clicks.
	A total of 9 urls were clicked.

Every time that ``tinysumma --updateletter mytinyletter`` is run, it writes three csv files: ``messages.csv``, ``urls.csv`` and ``subscribers.csv`` (default: current directory, unless other path passed in with ``--datadir`` flag). The command overwrites existing files with those names, without requiring confirmation! All summary data reported by other commands are taken from those files.

The csv files provide a lot more information than what ``tinysumma`` summarizes! A more in-depth analysis can always be performed outside of ``tinysumma`` (e.g., starting with ``pandas.read_csv()``).

Installation
------------

Install using ``pip``.

Install from PyPI:

::

    pip install tinysumma

Install most recent Github commit (stability not guaranteed):

::

    pip install git+https://github.com/awbirdsall/tinysumma

Dependencies
------------

Tested on Python 3.5.

Requires ``tinyapi`` and ``pandas`` (installation of which should be automatically handled by ``pip``).

Running the tests requires ``pytest``.

Testing
-------

Tests are located in the ``tests/`` subfolder and can be run using ``py.test``.

Development
-----------

Posting issues or pull requests to the `github page`_ is welcome!

.. _github page: https://github.com/awbirdsall/pyvap
