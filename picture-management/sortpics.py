#!/usr/bin/python
from pyexiv2 import ImageMetadata
import numpy as np
import mimetypes
from os import path
import os, shutil, argparse, re

class Img:
    def __init__(self, path):
        self.path = path
        md = ImageMetadata(self.path)
        md.read()
        self.date = md['Exif.Image.DateTime'].value
        self.shutter = md['Exif.Nikon3.ShutterCount'].value

    def __cmp__(self, other):
        if not isinstance(other, Img):
            return -1
        if self.date < other.date:
            return -1
        elif self.date > other.date:
            return 1
        else:
            if self.shutter < other.shutter:
                return -1
            elif self.shutter > other.shutter:
                return 1
            else:
                return 0

    def __str__(self):
        return "%s: %s %d" %(self.path, 
                             self.date.strftime('%Y-%m-%d %H:%M:%S'), 
                             self.shutter)

def sort(dir, tmp_dir = path.abspath('/home/ndhuang/Pictures/'), all = False):
    mimetypes.init()
    mimetypes.add_type('image/x-nikon-nef', '.NEF')
    sort_dir = path.join(tmp_dir, 'sorting')

    img_files = os.listdir(dir)
    i = 0
    while i < len(img_files):
        img = img_files[i]
        if '.pp3' in img:
            img_files.remove(img)
            continue
        elif not all and not re.match('DSC_(\d){4}\.', img):
            img_files.remove(img)
            continue            
        mt = mimetypes.guess_type(img)[0]
        mt = mt.split('/')
        if mt[0] != 'image':
            raise RuntimeError('%s is not an image!' %img)
        else:
            i += 1

    os.mkdir(sort_dir)
    imgs = [[] for i in img_files]
    for i in range(len(img_files)):
        try:
            imgs[i] = Img(path.join(dir, img_files[i]))
        except KeyError:
            print '%s is missing EXIF data!' %img_files[i]
    # remove empty arrays
    while [] in imgs:
        imgs.remove([])
    imgs = sorted(imgs)
    
    pic_num = 1
    copies = 1
    for i, img in enumerate(imgs):
        ext = img.path[-3:]
        if i != 0 and imgs[i] == imgs[i - 1]:
            dst = path.join(sort_dir,
                            'DSC_%04d-%d.%s' %(pic_num - 1, copies, ext))
            copies += 1
        else:
            dst = path.join(sort_dir, 'DSC_%04d.%s' %(pic_num, ext))
            pic_num += 1
            copies = 1
        os.rename(img.path, dst)
        try:
            os.rename(img.path + '.out.pp3', dst + '.out.pp3')
        except OSError as err:
            pass
        try: 
            os.rename(img.path + '.pp3', dst + '.pp3')
        except OSError as err:
            pass

    for f in os.listdir(dir):
        os.rename(path.join(dir, f), path.join(sort_dir, f))
    os.rmdir(dir)
    os.rename(sort_dir, dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Sort pictures by time')
    parser.add_argument('directory', help = 'The directory to sort')
    parser.add_argument('--tmp-dir', help = 'Temporary storage directory')
    parser.add_argument('--all', help = 'Sort all image files, not just DSC_xxxx.* files', action = 'store_true')
    args = parser.parse_args()
    if args.tmp_dir == None:
        args.tmp_dir = path.abspath('/home/ndhuang/Pictures/')

    sort(args.directory, tmp_dir = args.tmp_dir, all = args.all)
