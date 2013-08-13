#!/usr/bin/python
from datetime import date
import pyexiv2
import sys

pic = sys.argv[1]
md = pyexiv2.ImageMetadata(pic)
md.read()
key = 'Exif.Image.Copyright'                                            

val = 'Copyright, Nicholas Huang %s. This work is licensed under the Creative Commons CC-BY-NC-SA 3.0. See http://creativecommons.org/licenses/by-nc-sa/3.0/' %str(date.today().year)

md[key] = pyexiv2.ExifTag(key, val)                                     
md.write()                              
