[![image](https://raw.githubusercontent.com/oduwsdl/ipwb/master/docs/logo.png)](https://pypi.python.org/pypi/ipwb)

InterPlanetary Wayback (ipwb)
-----------------------------

### Peer-To-Peer Permanence of Web Archives

![travis](https://travis-ci.org/oduwsdl/ipwb.svg?branch=master)
![pypi](https://img.shields.io/pypi/v/ipwb.svg)
![codecov](https://codecov.io/gh/oduwsdl/ipwb/branch/master/graph/badge.svg)

InterPlanetary Wayback (ipwb) facilitates permanence and collaboration
in web archives by disseminating the contents of
[WARC](http://www.iso.org/iso/catalogue_detail.htm?csnumber=44717) files
into the IPFS network. [IPFS](https://ipfs.io/) is a peer-to-peer
content-addressable file system that inherently allows deduplication and
facilitates opt-in replication. ipwb splits the header and payload of
WARC response records before disseminating into IPFS to leverage the
deduplication, builds a [CDXJ
index](https://github.com/oduwsdl/ORS/wiki/CDXJ) with references to the
IPFS hashes returned, and combines the header and payload from IPFS at
the time of replay.

InterPlanetary Wayback primarily consists of two scripts:

-   **ipwb/indexer.py** - archival indexing script that takes the path
    to a WARC input, extracts the HTTP headers, HTTP payload (response
    body), and relevant parts of the WARC-response record header from
    the WARC specified and creates byte string representations. The
    indexer then pushes the byte strings into IPFS using a locally
    running IPFS daemon then creates a
    [CDXJ](https://github.com/oduwsdl/ORS/wiki/CDXJ) file with this
    metadata for replay.py.
-   **ipwb/replay.py** - rudimentary replay script to resolve requests
    for archival content contained in IPFS for replay in the browser.

A pictorial representation of the ipwb indexing and replay process:

![image](https://raw.githubusercontent.com/oduwsdl/ipwb/master/docs/diagram_72.png)

### Installing

InterPlanetary Wayback requires Python 2.7+ though we are working on
having it work on Python 3 as well (see
[\#51](https://github.com/oduwsdl/ipwb/issues/51)).

The latest release of ipwb can be installed using pip:

``` {.sourceCode .bash}
$ pip install ipwb
```

The latest development version containing changes not yet released can
be installed from source:

``` {.sourceCode .bash}
$ git clone https://github.com/oduwsdl/ipwb
$ cd ipwb
$ pip install -r requirements.txt
$ pip install ./
```

### Setup

The InterPlanetary Filesystem (ipfs) daemon must be installed and
running before starting ipwb. See the [Install
IPFS](https://ipfs.io/docs/install/) page to accomplish this. In the
future, we hope to make this more automated. Once ipfs is installed,
start the daemon:

``` {.sourceCode .bash}
$ ipfs daemon
```

If you encounter a conflict with the default API port of 5001 when
starting the daemon, running the following prior to launching the daemon
will change the API port to access to one of your choosing (here, shown
to be 5002):

``` {.sourceCode .bash}
$ ipfs config Addresses.API /ip4/127.0.0.1/tcp/5002
```

### Indexing

In a separate terminal session (or the same if you started the daemon in
the background), instruct ipwb to push a WARC into IPFS:

``` {.sourceCode .bash}
$ ipwb index (path to warc or warc.gz)
```

\...for example, from the root of the ipwb repository:

``` {.sourceCode .bash}
$ ipwb index ipwb/samples/warcs/salam-home.warc
```

The ipwb indexer parititions the WARC into WARC Records and extracts the
WARC Response headers, HTTP response headers, and the HTTP response
bodies (payloads). Relevant information is extracted from the WARC
Response headers, temporary byte strings are created for the HTTP
response headers and payload, and these two bytes strings are pushed
into IPFS. The resulting CDXJ data is written to stdout by default but
can be redirected to a file, e.g.,

``` {.sourceCode .bash}
$ ipwb index (path to warc or warc.gz) >> myArchiveIndex.cdxj
```

### Replaying

An archival replay system is also included with ipwb to re-experience
the content disseminated to IPFS . The replay system can be launched
using the provided sample data with:

``` {.sourceCode .bash}
$ ipwb replay
```

A CDXJ index can also be provided and used by the ipwb replay system by
specifying the path of the index file as a parameter to the replay
system:

``` {.sourceCode .bash}
$ ipwb replay <path/to/cdxj>
```

ipwb also supports using an IPFS hash or any HTTP location as the source
of the CDXJ:

``` {.sourceCode .bash}
$ ipwb replay http://myDomain/files/myIndex.cdxj
$ ipwb replay QmYwAPJzv5CZsnANOTaREALhashYgPpHdWEz79ojWnPbdG
```

Once started, the replay system\'s web interface can be accessed through
a web browser, e.g., <http://localhost:5000/> by default.

### Using Docker

A pre-built Docker image is made available that can be run as following:

``` {.sourceCode .bash}
$ docker container run -it --rm -p 5000:5000 oduwsdl/ipwb
```

The container will run an IPFS daemon, index a sample WARC file, and
replay it using the newly created index. It will take a few seconds to
be ready, then the replay will be accessible at <http://localhost:5000/>
with a sample archived page.

To index and replay your own WARC file, bind mount your data folders
inside the container using -v (or \--volume) flag and run commands
accordingly. The provided docker image has designated /data directory,
inside which there are warc, cdxj, and ipfs folders where host folders
can be mounted separately or as a single mount point at the parent /data
directory. Assuming that the host machine has a /path/to/data folder
under which there are warc, cdxj, and ipfs folders and a WARC file at
/path/to/data/warc/custom.warc.gz.

``` {.sourceCode .bash}
$ docker container run -it --rm -v /path/to/data:/data oduwsdl/ipwb ipwb index -o /data/cdxj/custom.cdxj /data/warc/custom.warc.gz
$ docker container run -it --rm -v /path/to/data:/data -p 5000:5000 oduwsdl/ipwb ipwb replay /data/cdxj/custom.cdxj
```

If the host folder structure is something other than
/some/path/{warc,cdxj,ipfs} then these volumes need to be mounted
separately.

To build an image from the source, run the following command from the
directory where the source code is checked out.

``` {.sourceCode .bash}
$ docker image build -t ipwb .
```

### Help

Usage of sub-commands in ipwb can be accessed through providing the -h
or \--help flag, like any of the below.

``` {.sourceCode .bash}
$ ipwb -h
usage: ipwb [-h] [-d DAEMON_ADDRESS] [-o OUTFILE] [-v] {index,replay} ...

InterPlanetary Wayback (ipwb)

optional arguments:
  -h, --help            show this help message and exit
  -d DAEMON_ADDRESS, --daemon DAEMON_ADDRESS
                        Location of ipfs daemon (default 127.0.0.1:5001)
  -o OUTFILE, --outfile OUTFILE
                        Filename of newly created CDXJ index file
  -v, --version         Report the version of ipwb

ipwb commands:
  Invoke using "ipwb <command>", e.g., ipwb replay

  {index,replay}
    index               Index a WARC file for replay in ipwb
    replay              Start the ipwb replay system
```

``` {.sourceCode .bash}
$ ipwb index -h
usage: ipwb [-h] [-e] [-c] [--compressFirst] [-o OUTFILE] [--debug]
            index <warcPath> [index <warcPath> ...]

Index a WARC file for replay in ipwb

positional arguments:
  index <warcPath>      Path to a WARC[.gz] file

optional arguments:
  -h, --help            show this help message and exit
  -e                    Encrypt WARC content prior to adding to IPFS
  -c                    Compress WARC content prior to adding to IPFS
  --compressFirst       Compress data before encryption, where applicable
  -o OUTFILE, --outfile OUTFILE
                        Path to an output CDXJ file, defaults to STDOUT
  --debug               Convenience flag to help with testing and debugging
```

``` {.sourceCode .bash}
$ ipwb replay -h
usage: ipwb replay [-h] [-P [<host:port>]] [index]

Start the ipwb relay system

positional arguments:
  index                 path, URI, or multihash of file to use for replay

optional arguments:
  -h, --help            show this help message and exit
  -P [<host:port>], --proxy [<host:port>]
                        Proxy URL
```

### Project History

This repo contains the code for integrating
[WARC](http://www.iso.org/iso/catalogue_detail.htm?csnumber=44717)s and
[IPFS](https://ipfs.io/) as developed at the [Archives Unleashed: Web
Archive Hackathon]() in Toronto, Canada in March 2016. The project was
also presented at:

-   The [Joint Conference on Digital Libraries
    2016](http://www.jcdl2016.org/) in Newark, NJ in June 2016.
-   The [Web Archiving and Digital Libraries (WADL) 2016
    workshop](http://fox.cs.vt.edu/wadl2016.html) in Newark, NJ in
    June 2016.
-   The [Theory and Practice on Digital Libraries (TPDL)
    2016](http://www.tpdl2016.org/) in Hannover, Germany in
    September 2016.
-   The [Archives Unleashed 4.0: Web Archive Datathon]() in London,
    England in June 2017.
-   The [International Internet Preservation Consortium (IIPC) Web
    Archiving Conference (WAC) 2017](http://netpreserve.org/wac2017/) in
    London, England in June 2017.

License
-------

MIT

> target
>
> :   <https://travis-ci.org/oduwsdl/ipwb>
