InterPlanetary Wayback (ipwb)
=============================

This repo contains the code for the initial integration between `WARC <http://www.iso.org/iso/catalogue_detail.htm?csnumber=44717>`_\ s and `IPFS <https://github.com/ipfs/ipfs>`_ as developed at the `Archives Unleashed Hackathon <http://archivesunleashed.ca>`_ in Toronto, Canada in March 2016.

Two main components exist in the protype:

- **ipwbindexer.py** - takes the path to a WARC input, extracts the HTTP headers, HTTP payload (response body), and relevant parts of the WARC response header from the WARC specified. Creates temp files of these. Pushes temp files into IPFS using a locally running ipfs daemon. Creates a `CDXJ <https://github.com/oduwsdl/ORS/wiki/CDXJ>`_ file with this metadata for `replay.py`.
- **replay.py** - a very rudimentary replay script to resolve fetches for IPFS-content for on-demand replay in the browser. Plagued with `zombies <http://ws-dl.blogspot.com/2012/10/2012-10-10-zombies-in-archives.html>`_. A placeholder until we get more familiar with modifying the `pywb <https://github.com/ikreymer/pywb>`_ codebase for a truer replay system.

Install
-------
ipwb can be run from source (see Indexing below) or installed via pip:

::

      $ pip install ipwb
       
...or from source in a virtual environment

::

      $ virtualenv ipwb
      $ source ipwb/bin/activate
      (ipwb) $ pip install -r requirements.txt

Running
-------
Before running the code, ipfs must be installed. See the `Install IPFS <https://ipfs.io/docs/install/>`_ page to accomplish this. In the future, we hope to make this more automated. Once ipfs is installed, start the daemon:

::

      $ ipfs daemon


Indexing
--------
In a separate terminal session (or the same if you started the daemon in the background), instruct ipwb to push a WARC into IPFS:

::

      $ ipwb (path to warc or warc.gz)


...for example, from the root of the ipwb repository:

::

      ipwb samples/warcs/sample-1.warc.gz

Alternatively, if running from source:

::

      (ipwb) $ ipwb/indexer.py (path to warc or warc.gz)


`indexer.py`, the default script called by the ipwb binary, parititions the WARC into WARC Records, extracts the WARC Response headers, HTTP response headers, and HTTP response body (payload). Relevant information is extracted from the WARC Response headers, temp files are created for the HTTP response headers and payload, and these two temp files are pushed into IPFS.

Replaying
---------

(TODO)
