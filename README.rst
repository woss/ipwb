.. image:: https://raw.githubusercontent.com/oduwsdl/ipwb/master/docs/logo.png
    :target: https://pypi.python.org/pypi/ipwb

InterPlanetary Wayback (ipwb)
=============================
Peer-To-Peer Permanence of Web Archives
---------------------------------------

.. image:: https://api.travis-ci.org/oduwsdl/ipwb.png?branch=master
.. image:: https://img.shields.io/pypi/v/ipwb.svg

InterPlanetary Wayback (ipwb) facilitates permanence and collaboration in web archives by disseminating the contents of WARC files into the IPFS network. `IPFS`_ is a peer-to-peer content-addressable file system that inherently allows deduplication and facilitates opt-in replication. ipwb splits the header and payload of WARC response records before disseminating into IPFS to leverage the deduplication, builds a `CDXJ index`_ with references to the IPFS hashes returns, and combines the header and payload from IPFS at the time of replay. 

InterPlanetary Wayback primarily consists of two scripts:

- **ipwb/indexer.py** - archival indexing script that takes the path to a WARC input, extracts the HTTP headers, HTTP payload (response body), and relevant parts of the WARC-response record header from the WARC specified and creates byte string representations. The indexer then pushes the byte strings into IPFS using a locally running ipfs daemon then creates a `CDXJ`_ file with this metadata for `replay.py`.
- **ipwb/replay.py** - rudimentary replay script to resolve requests for archival content contained in IPFS for replay in the browser.

A pictorial representation of the ipwb indexing and replay process:

.. image:: https://raw.githubusercontent.com/oduwsdl/ipwb/master/docs/diagram_72.png

Installing
----------
ipwb can be run from source (see Indexing below) or installed via pip:

.. code-block:: bash

      $ pip install ipwb
       
...or from source in a virtual environment:

.. code-block:: bash

      $ virtualenv ipwb
      $ source ipwb/bin/activate
      (ipwb) $ pip install -r requirements.txt
      (ipwb) $ pip install ./

Setup
-----
The InterPlanetary Filesystem (ipfs) daemon must be installed and running before starting ipwb. See the `Install IPFS`_ page to accomplish this. In the future, we hope to make this more automated. Once ipfs is installed, start the daemon:

.. code-block:: bash

      $ ipfs daemon


If you encounter a conflict with the default API port of 5001 when starting the daemon, running the following prior to launching the daemon will change the API port to access to one of your choosing (here, shown to be 5002):

.. code-block:: bash

      $ ipfs config Addresses.API /ip4/127.0.0.1/tcp/5002

Indexing
--------
In a separate terminal session (or the same if you started the daemon in the background), instruct ipwb to push a WARC into IPFS:

.. code-block:: bash

      $ ipwb (path to warc or warc.gz)


...for example, from the root of the ipwb repository:

.. code-block:: bash

      ipwb samples/warcs/sample-1.warc.gz

Alternatively, if running from source without installation:

.. code-block:: bash

      (ipwb) $ ipwb/indexer.py (path to warc or warc.gz)


`indexer.py`, the default script called by the ipwb binary, parititions the WARC into WARC Records, extracts the WARC Response headers, HTTP response headers, and HTTP response body (payload). Relevant information is extracted from the WARC Response headers, temporary byte strings are created for the HTTP response headers and payload, and these two bytes strings are pushed into IPFS. The resulting CDXJ data is written to `stdout` by default but can be redirected to a file, e.g., 

.. code-block:: bash

      (ipwb) $ ipwb/indexer.py (path to warc or warc.gz) >> myArchiveIndex.cdxj

(TODO: add info about specifying the out file as a parameter)

Replaying
---------

(TODO: add more detailed info in this section, better sample data with more URIs in the repo for better demonstration of ipwb functionality)

The ipwb replay system can be launched with:

.. code-block:: bash

      (ipwb) $ ipwb/replay.py
	  
Once the daemon is started, the replay system web interface can be accessed through a web browser, e.g., `http://127.0.0.1:5000/http://www.cs.odu.edu/~salam/` with the sample CDXJ file.

(TODO: provide instructions on specifying a CDXJ file/directory to be read from the CDXJ replay system)

Project History
---------------
This repo contains the code for integrating `WARC`_\ s and `IPFS`_ as developed at the `Archives Unleashed Hackathon`_ in Toronto, Canada in March 2016. The project was also presented at:

* The `Joint Conference on Digital Libraries 2016`_ in Newark, NJ in June 2016.
* The `Web Archiving and Digital Libraries (WADL) 2016 workshop`_ in Newark, NJ in June 2016.
* The `Theory and Practice on Digital Libraries (TPDL) 2016`_ in Hannover, Germany in September 2016.

License
---------
MIT

.. _Contributor Friendly: https://github.com/ipfs/ipfs
.. _WARC: http://www.iso.org/iso/catalogue_detail.htm?csnumber=44717
.. _Joint Conference on Digital Libraries 2016: http://www.jcdl2016.org/
.. _Archives Unleashed Hackathon: http://archivesunleashed.ca
.. _Theory and Practice on Digital Libraries (TPDL) 2016: http://www.tpdl2016.org/
.. _Web Archiving and Digital Libraries (WADL) 2016 workshop: http://fox.cs.vt.edu/wadl2016.html
.. _CDXJ index: https://github.com/oduwsdl/ORS/wiki/CDXJ
.. _CDXJ: https://github.com/oduwsdl/ORS/wiki/CDXJ
.. _IPFS: https://ipfs.io/
.. _zombies: http://ws-dl.blogspot.com/2012/10/2012-10-10-zombies-in-archives.html
.. _pywb: https://github.com/ikreymer/pywb
.. _Install IPFS: https://ipfs.io/docs/install/
