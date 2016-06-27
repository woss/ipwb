.. image:: https://raw.githubusercontent.com/oduwsdl/ipwb/master/docs/logo.png
    :target: https://pypi.python.org/pypi/ipwb

InterPlanetary Wayback (ipwb)
=============================
Peer-To-Peer Permanence of Web Archives
---------------------------------------

InterPlanetary Wayback (ipwb) facilitates permanence and collaboration in web archives by disseminating the contents of WARC files into the IPFS network. IPFS is a peer-to-peer content-addressable file system that inherently allows deduplication and facilitates opt-in replication. ipwb splits the header and payload of WARC response records before disseminating into IPFS to leverage the deduplication, build a CDXJ index, and combine them at the time of replay. 

InterPlanetary Wayback primarily consists of two scripts:

- **ipwb/indexer.py** - takes the path to a WARC input, extracts the HTTP headers, HTTP payload (response body), and relevant parts of the WARC response header from the WARC specified. Creates temp files of these. Pushes temp files into IPFS using a locally running ipfs daemon. Creates a `CDXJ <https://github.com/oduwsdl/ORS/wiki/CDXJ>`_ file with this metadata for `replay.py`.
- **ipwb/replay.py** - a very rudimentary replay script to resolve fetches for IPFS-content for on-demand replay in the browser. Plagued with `zombies <http://ws-dl.blogspot.com/2012/10/2012-10-10-zombies-in-archives.html>`_. A placeholder until we get more familiar with modifying the `pywb <https://github.com/ikreymer/pywb>`_ codebase for a truer replay system.

.. image:: https://raw.githubusercontent.com/oduwsdl/ipwb/master/docs/diagram_72.png

Installing
----------
ipwb can be run from source (see Indexing below) or installed via pip:

::

      $ pip install ipwb
       
...or from source in a virtual environment:

::

      $ virtualenv ipwb
      $ source ipwb/bin/activate
      (ipwb) $ pip install -r requirements.txt

Setup
-----
The InterPlanetary Filesystem (ipfs) daemon must be installed and running before starting ipwb. See the `Install IPFS <https://ipfs.io/docs/install/>`_ page to accomplish this. In the future, we hope to make this more automated. Once ipfs is installed, start the daemon:

::

      $ ipfs daemon


If you encounter a conflict with the default API port of 5001 when starting the daemon, running the following prior to launching the daemon will change the API port to access to one of your choosing (here, shown to be 5002):

::

      $ ipfs config Addresses.API /ip4/127.0.0.1/tcp/5002

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


`indexer.py`, the default script called by the ipwb binary, parititions the WARC into WARC Records, extracts the WARC Response headers, HTTP response headers, and HTTP response body (payload). Relevant information is extracted from the WARC Response headers, temp files are created for the HTTP response headers and payload, and these two temp files are pushed into IPFS. The resulting CDXJ data is written to `stdout` by default but can be redirected to a file, e.g., 

::

      (ipwb) $ ipwb/indexer.py (path to warc or warc.gz) >> myArchiveIndex.cdxj

(TODO: add info about specifying the out file as a CLI parameter.)

Replaying
---------

(TODO: add more detailed inf in this section)
(TODO: add better sample data with more URIs in the repo for better demonstration of ipwb functionality.)

The ipwb replay system can be launched with:

::

      (ipwb) $ ipwb/replay.py
	  
Once the daemon is started, the replay system web interface can be accessed through a web browser, e.g., `http://127.0.0.1:5000/http://www.cs.odu.edu/~salam/` with the sample CDXJ file.

(TODO: provide instructions on specifying a CDXJ file/directory to be read from the CDXJ replay system)

Project History
---------------
This repo contains the code for the initial integration between `WARC <http://www.iso.org/iso/catalogue_detail.htm?csnumber=44717>`_\ s and `IPFS <https://github.com/ipfs/ipfs>`_ as developed at the `Archives Unleashed Hackathon <http://archivesunleashed.ca>`_ in Toronto, Canada in March 2016. The project was also presented at the `Joint Conference on Digital Libraries 2016 <http://www.jcdl2016.org/>`_ in Newark, NJ; the `Web Archiving and Digital Libraries (WADL) 2016 workshop <http://fox.cs.vt.edu/wadl2016.html>`_ in Newark, NJ; and will be presented at the `Theory and Practice on Digital Libraries (TPDL) 2016 <http://www.tpdl2016.org/>`_ in Hannover, Germany in September 2016.

License
---------
MIT
