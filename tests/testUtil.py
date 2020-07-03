import os
import random
import string
import re
import tempfile

from time import sleep

from ipwb import replay
from ipwb import indexer
from ipwb import __file__ as moduleLocation

from multiprocessing import Process
from pathlib import Path

p = Process()


def createUniqueWARC():
    lines = []
    warcInFilename = 'frogTest.warc'
    ipwb_dir = str(Path(os.path.dirname(__file__)).parents[0])
    warcInPath = os.path.join(
        ipwb_dir +
        os.path.sep.join(['', 'samples', 'warcs', warcInFilename]))

    stringToChange = b'abcdefghijklmnopqrstuvwxz'
    randomString = getRandomString(len(stringToChange))
    randomBytes = str.encode(randomString)

    with open(warcInPath, 'rb') as warcFile:
        newContent = warcFile.read().replace(stringToChange, randomBytes)

    warcOutFilename = warcInFilename.replace('.warc', '_' +
                                             randomString + '.warc')
    warcOutPath = os.path.join(
        ipwb_dir +
        os.path.sep.join(['', 'samples', 'warcs', warcOutFilename]))

    print(warcOutPath)
    with open(warcOutPath, 'wb') as warcFile:
        warcFile.write(newContent)

    return warcOutPath


def getRandomString(n):
    return ''.join(random.SystemRandom().choice(
                   string.ascii_lowercase + string.digits) for _ in range(n))


def countCDXJEntries(cdxjData):
    urimCount = 0
    lines = cdxjData.strip().split('\n')
    for line in lines:
        if line[0] != '!':  # Exclude metadata from count
            urimCount += 1
    return urimCount


def startReplay(warcFilename):
    global p
    pathOfWARC = os.path.join(
        str(Path(os.path.dirname(__file__)).parents[0]) +
        os.path.sep.join(['', 'samples', 'warcs', warcFilename]))

    number_of_characters = 12
    character_set = string.ascii_uppercase + string.digits * 6

    tempFilePath = (
        f"{tempfile.gettempdir()}{os.path.sep}"
        f"{random.sample(character_set, number_of_characters)}.cdxj")

    open(tempFilePath, 'a').close()  # Create placeholder file for replay

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


def extractRelationEntriesFromLinkTimeMap(tm):
    matches = re.findall('rel=".*?"', tm)
    matches = map(lambda s: s[5:-1], matches)
    return matches
