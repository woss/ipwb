import sys, os
import pywb.warc.cdxindexer
import md5
import json
#import ordereddict
from pywb.warc.archiveiterator import ArchiveIterator, DefaultRecordParser
from pywb.utils.loaders import LimitReader

from pywb.warc.recordloader import ArcWarcRecordLoader
#from pywb.warc.cdxindexer import CDXJ

from surt import surt
from pywb.utils.bufferedreaders import DecompressingBufferedReader
from pywb.utils.statusandheaders import StatusAndHeadersParser


from io import BytesIO
import ipfsApi

IP = '127.0.0.1'
PORT = '5001'

IPFS_API = ipfsApi.Client(IP, PORT)

def main():
  options = {"cdxj": True, "include_all": False, "surt_ordered": False}
  cdxLines = ""

  # Read WARC file
  loader = ArcWarcRecordLoader(verify_http=True)

  #warcFileFullPath = '/Users/machawk1/Desktop/testWarc.warc.gz'
  warcFileFullPath = '/Users/machawk1/Desktop/testWarc.warc.gz'

  with open(warcFileFullPath, 'rb') as warc:
    iter = TextRecordParser(**options)
    idx = 0
    for entry in iter(warc):
      if entry.record.rec_type == "response":  
        if entry.get('mime') in ('text/dns', 'text/whois'):  continue
      
        hdrs = entry.record.status_headers
        hstr = hdrs.protocol + ' ' + hdrs.statusline
        for h in hdrs.headers:
          hstr += "\n" + ": ".join(h)
        
        statusCode = hdrs.statusline.split()[0]
        
        if not entry.buffer: return
        
        entry.buffer.seek(0)
        payload = entry.buffer.read()
        
        tmpFilePath = '/tmp/ipfs/'
        fileHash = md5.new(hstr).hexdigest()
        
        hdrfn = tmpFilePath + 'header_' + fileHash
        pldfn = tmpFilePath + 'payload_' + fileHash
        
        writeFile(hdrfn, hstr)
        writeFile(pldfn, payload)
        
        # Retry if IPFS gives errors then give up on record
        hdrHash = ''
        pldHash = ''
        retryCount = 0
        while retryCount < 5:
          try:
            hdrHash = pushToIPFS(hdrfn)
            pldHash = pushToIPFS(pldfn)
            break
          except:
            logError("IPFS failed on " + entry.get('url'))
            retryCount += 1
        
        if retryCount >= 5: 
          logError("Skipping "+entry.get('url'))
          
          continue
        
        
        uri = surt(entry.get('url'))
        timestamp = entry.get('timestamp')
        mime = entry.get('mime')
        
        encrKey = "" #TODO
        
        obj = {"header_digest": hdrHash, "payload_digest": pldHash, "status_code": statusCode, "mime_type": mime, "encryption_key": encrKey}
        objJSON = json.dumps(obj);
        
        cdxjLine = '{0} {1} {2}'.format(uri, timestamp, objJSON) 
        cdxLines += cdxjLine
        print cdxjLine
        
        resHeader = pullFromIPFS(hdrHash)
        resPayload = pullFromIPFS(pldHash)
        
        warcContents = resHeader + '\n\n' + resPayload
        
  #print "Writing cdxj string to testWARC.cdxj"
  #with open("testWARC.cdxj", "w") as cdxjFile:
  #  cdxjFile.write(cdxLines)

def logError(errIn):
  print >> sys.stderr, errIn
   
def pullFromIPFS(hash):
  global IPFS_API
  return IPFS_API.cat(hash)

def pushToIPFS(path):
  global IPFS_API
  res = IPFS_API.add(path)
  return res['Hash']

def writeFile(filename, content):
  with open(filename, "w") as tmpFile:
    tmpFile.write(content) 
  
#os.remove(filename)
#print api.cat('QmbRZEuSFqT214MNZg2iSifq7DCdc9PNbcpb3rDHAHdhyv')
#print api.id()
#sys.exit()

class TextRecordParser(DefaultRecordParser):
    def create_payload_buffer(self, entry):
        # can add conditionals on when to buffer
        #mime = entry.get('mime')
        # if mime and ('text/' in mime):
        #     return BytesIO()
        # else:
        #     return None
        # or, always buffer
        return BytesIO()
    
if __name__ == '__main__':
  main()      