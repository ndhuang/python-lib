#!/usr/bin/python
import sys
import os
import shutil
import re
import argparse
import mimetypes

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

def main(srcPath, destPath, min = None, max = None):
    if srcPath[-1] != '/':
        srcPath += '/'
    if destPath[-1] != '/':
        destPath += '/'
    if (not os.path.exists(srcPath)):
        print 'Source directory does not exist'
        exit(1)
    if (not os.path.isdir(srcPath)):
        print 'Source is not a directory'
        exit(1)
    if (not os.path.exists(destPath)):
        print destPath + 'does not exist; check path'
        exit(2)
    if (not os.path.isdir(destPath)):
        print destPath + ' is not a director'
    newPics = sorted(checkFiles(os.listdir(srcPath)))
    oldPics = sorted(checkFiles(os.listdir(destPath)))

    # find the highest picture number in the destination directory
    maxPic = 0
    for picture in oldPics:
        try:
            picNum = int(picture[4:8])
            if (picNum > maxPic):
                maxPic = picNum
        except ValueError:
            print 'Invalid file name: ' + picture
            continue

    # find all the used numbers in the destination dir
    used = [False for unused in range(maxPic + 1)]
    for picture in oldPics:
        try:
            picNum = int(picture[4:8])
            used[picNum] = True
        except ValueError:
            print 'Invalid file name: ' + picture
            continue

    i = 0
    for picture in newPics:
        if min and max:
            try:
                picNum = int(picture[4:8])
                if picNum < min:
                    continue
                elif picNum > max:
                    break
                
            except ValueError:
                print 'Invalid file name: ' + picture
                continue
            
        while (i < len(used) and used[i]):
            i = i + 1
        extension = picture[len(picture) - 3:len(picture)]
        num = "{0:04d}".format(i + 1)
        newName = "DSC_%s.%s" %(num, extension)
        shutil.move(srcPath + picture, destPath + newName)
        # try to move RawTherapee profile with the image
        try:
            shutil.move(srcPath + picture + '.pp3',
                        destPath + newName + '.pp3')
        except IOError:
            pass
        try:
            shutil.move(srcPath + picture + '.out.pp3',
                        destPath + newName + '.out.pp3')
        except IOError:
            pass
        i = i + 1
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Move pictures sensibly')
    parser.add_argument('src', type = str)
    parser.add_argument('dest', type = str)
    parser.add_argument('-r', '--range', type = str)
    args = parser.parse_args()
    if args.range:
        match = re.match('(\d+).(\d+)', args.range)
        if not match:
            raise ValueError('Bad range: %s' %args.range)
        min = int(match.group(1))
        max = int(match.group(2))
    else:
        min = None
        max = None
    main(args.src, args.dest, min, max)
