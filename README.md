# InterPlanetary Wayback (ipwb)

This repo contains the code for the initial integration between [WARC](http://www.iso.org/iso/catalogue_detail.htm?csnumber=44717)s and [IPFS](https://github.com/ipfs/ipfs) as developed at the [Archives Unleashed Hackathon](http://archivesunleashed.ca) in Toronto, Canada in March 2016.

Two main components exist in the protype:
* **ipwbindexer.py** - takes a WARC input, extracts the HTTP headers, HTTP payload (response body), and relevant parts of the WARC header. Creates temp files of these. Pushes temp files into IPFS using a locally running ipfs daemon.
* **replay.py** - a very rudimentary replay script to resolve fetches for IPFS-content for on-demand replay in the browser. Plagued with [zombies](http://ws-dl.blogspot.com/2012/10/2012-10-10-zombies-in-archives.html). A placeholder until we get more familiar with modifying the [pywb](github.com/ikreymer/pywb) codebase for a truer replay system.

## Running ##
Before running the code, ipfs must be installed. See the [https://ipfs.io/docs/install/](Install IPFS) page to accomplish this. In the future, we hope to make this more automated. Once ipfs is installed, start the daemon:

```sh
$ ipfs daemon
```

### Indexing ###
In a separate terminal session (or the same if you started the daemon in the background), instruct ipwb to push a WARC into IPFS:

```sh
./ipwbindexer.py (path to warc or warc.gz)
```

...for example, from the root of the ipwb repository:

```sh
./ipwbindexer.py samples/warcs/sample-1.warc.gz
```

`indexer.py` parititions the WARC into WARC Records, extracts the WARC Response headers, HTTP response headers, and HTTP response body (payload). Relevant information is extracted from the WARC Response headers, temp files are created for the HTTP response headers and payload, and these two temp files are pushed into IPFS.

### Replaying ###

(TODO)
