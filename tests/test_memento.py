import pytest

import testUtil as ipwbTest
from ipwb import replay
from ipwb import indexer
from ipwb import __file__ as moduleLocation
from time import sleep
import os
import subprocess
import urllib2
import random
import string
import re
from multiprocessing import Process

p = Process()

def getURIMsFromTimeMapInWARC(warcFilename):
    global p
    startReplay(warcFilename)

    tm = urllib2.urlopen('http://localhost:5000/timemap/link/memento.us/').read()

    urims = []
    for line in tm.split('\n'):
        isAMemento = len(re.findall('rel=".*memento"', line)) > 0
        if isAMemento:
            urims.append(re.findall('<(.*)>', line)[0])
    stopReplay()

    return urims


def startReplay(warcFilename):
    global p
    pathOfWARC = os.path.join(os.path.dirname(moduleLocation) +
                              '/samples/warcs/' + warcFilename)
    tempFilePath = '/tmp/' + ''.join(random.sample(
        string.ascii_uppercase + string.digits * 6, 6)) + '.cdxj'
    print('B2' + tempFilePath)
    p = Process(target=replay.start, args=[tempFilePath])
    p.start()
    sleep(5)

    cdxjList = indexer.indexFileAt(pathOfWARC, quiet=True)
    cdxj = '\n'.join(cdxjList)

    with open(tempFilePath, 'w') as f:
        f.write(cdxj)


def stopReplay():
    global p
    p.terminate()


def getRelsFromURIMSinWARC(warc):
    urims = getURIMsFromTimeMapInWARC(warc)
    startReplay(warc)

    # Get Link header values for each memento
    linkHeaders = []
    for urim in urims:
        linkHeaders.append(urllib2.urlopen(urim).info().getheader('Link'))
    stopReplay()

    relsForURIMs = []
    for linkHeader in linkHeaders:
      relForURIM = ipwbTest.extractRelationEntriesFromLinkTimeMap(linkHeader)
      relsForURIMs.append(relForURIM)

    stopReplay()
    return relsForURIMs


@pytest.mark.skip(reason='not implemented')
def test_mementoRelations_one():
    # ipwb replay ipwb/samples/warcs/2mementos.warc | ipwb replay
    # curl -i localhost:5000/timemap/link/memento.us
    # Parse two URI-Ms
    # For
    pass


@pytest.mark.mementoRelationTwoCount
def test_mementoRelations_two():
    relsForURIMs = getRelsFromURIMSinWARC('2mementos.warc')

    cond_firstMemento = False
    cond_lastNextMemento = False
    cond_firstPrevMemento = False
    cond_lastMemento = False
    for relArrayForURIM in relsForURIMs:
        for idx, rel in enumerate(relArrayForURIM):
            if 'memento' in rel:
                # Should probably check index, too
                # ...maybe filer before conditions?
                if 'first' in rel:
                    cond_firstMemento = True
                if 'last' in rel and 'next in rel':
                    cond_lastNextMemento = True
                if 'first' in rel and 'prev' in rel:
                    cond_firstPrevMemento = True
                if 'last' in rel:
                    cond_lastMemento = True
    assert cond_firstMemento and \
           cond_lastNextMemento and \
           cond_firstPrevMemento and \
           cond_lastMemento

@pytest.mark.mementoRelationThreeCount
def test_mementoRelations_three():
    pass


@pytest.mark.skip(reason='not implemented')
def test_mementoRelations_four():
    pass

@pytest.mark.skip(reason='not implemented')
def test_mementoRelations_five():
    pass


# TODO: Have unit tests for each function in replay.py
