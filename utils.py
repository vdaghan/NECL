import feedparser
import pathlib
import os
import subprocess
import sys
import urllib
from urllib.request import urlretrieve


def parseRSS(url):
    NewsFeed = feedparser.parse("https://cppcast.com/feed.rss")
    parseResults = [(entry['links'][1]['href'], entry['title']) for entry in NewsFeed['entries']]
    return parseResults


def getCurrentFolder():
    return str(pathlib.Path().absolute())


def getFilenames(link):
    mp3Filename = urllib.parse.urlparse(link).path
    mp3Filename = os.path.split(mp3Filename)[1]

    currentFolder = getCurrentFolder()

    downloadedFolder = currentFolder + '\\downloaded\\'
    mp3FilenameWithPath = downloadedFolder + mp3Filename

    fileName = pathlib.Path(mp3FilenameWithPath).stem

    wavFolder = currentFolder + '\\tmp\\'
    if not os.path.isdir(wavFolder):
        os.makedirs(wavFolder)

    wavFilenameWithPath = wavFolder + fileName + '.wav'
    jsonFilenameWithPath = downloadedFolder + fileName + '.json'

    return {'stem': fileName, 'link': link, 'mp3': mp3FilenameWithPath, 'wav': wavFilenameWithPath, 'json': jsonFilenameWithPath}


def downloadPodcast(filenames):
    if not pathlib.Path(filenames['mp3']).exists():
        print('Downloading file:', filenames['mp3'])
        downloadedFile, headers = urlretrieve(filenames['link'], filenames['mp3'])
    return filenames['mp3']


def convertMP3ToWav(filenames):
    wavFolder = getCurrentFolder() + '\\tmp\\'
    if not os.path.isdir(wavFolder):
        os.makedirs(wavFolder)

    if not pathlib.Path(filenames['wav']).exists():
        conversionResult = subprocess.run(['ffmpeg', '-i', filenames['mp3'], filenames['wav']])
        # conversionResult = subprocess.run(['ffmpeg', '-ss', '0', '-t', '60', '-i', mp3FilenameWithPath, wavFilenameWithPath])
        if 0 != conversionResult.returncode:
            print("Could not convert mp3 file to wav file: " + filenames['mp3'] + " -> " + filenames['wav'])
            print(conversionResult)
            sys.exit()
