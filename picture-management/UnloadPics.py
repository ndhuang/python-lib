#!/usr/bin/env python
# Unload pictures from the camera, without clobbering others
import argparse
from datetime import date
import mimetypes
import re
import os
import shutil
import sys
import pyexiv2
import numpy as np

def checkFiles(picList):
    mimetypes.init()
    mimetypes.add_type('image/x-nikon-nef', '.NEF')

    i = 0
    while i < len(picList):
        pic = picList[i]
        mt = mimetypes.guess_type(pic)[0]
        if mt == None:
            picList.remove(pic)
            continue
        mt = mt.split('/')
        if mt[0] != 'image':
            picList.remove(pic)
        else:
            i += 1
    return picList

def copyright(pic_file):
    # Add copyright info
    md = pyexiv2.ImageMetadata(pic_file)
    md.read()
    key = 'Exif.Image.Copyright'
    val = 'Copyright, Nicholas Huang %s. Licensed under CC-BY-NC 4.0.' %str(date.today().year)
    md[key] = pyexiv2.ExifTag(key, val)
    md.write()
    

def main(camPath = "/media/NIKON D7000/DCIM/100D5000/"):
    unloadPath = "/home/ndhuang/Pictures/CameraUnload/"
    if (not os.path.exists(camPath)):
        camPath = "/media/ndhuang/NIKON D7000/DCIM/100D7000/"
        if (not os.path.exists(camPath)):
            raise OSError('Insert camera SD card, or edit path ({})'.format(camPath))
    if (not os.path.exists(unloadPath)):
        raise OSError('Target directory does not exist; check path')
    newPics = sorted(checkFiles(os.listdir(camPath)))
    oldPics = sorted(checkFiles(os.listdir(unloadPath)))
    
    maxPic = 0
    for picture in oldPics:
        try:
            picNum = int(picture[4:8])
        except ValueError:
            print 'Invalid file name: ' + picture
            continue
        if (picNum > maxPic):
            maxPic = picNum

    i = maxPic
    for j, picture in enumerate(sorted(newPics)):
        done = float(j) / len(newPics)
        numPound = int(np.round(done * 40))
        print "[{}]{:3.0f}%".format("#" * numPound + " " * (40 - numPound), 
                                    round(done * 100)),
        sys.stdout.flush()
        extension = picture[len(picture) - 3:len(picture)]
        newName = "DSC_{0:04d}.{1}".format(i + 1, extension)
        shutil.copyfile(camPath + picture, unloadPath + newName)
        copyright(unloadPath + newName)
        i = i + 1
        print "\r",
    print ''

        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source_dir', type = str, default = "/media/NIKON D7000/DCIM/100D7000/")
    args = parser.parse_args()
    main(args.source_dir)
