# Thumbnailer

Creates thumbnails from images found in source directory

### Usage:

From commandline: `thumbnailer.py [-h] [-r] [--width W] [--height H] [-e EXT] [dir]`


```
positional arguments:
  dir                set to change source directory. Defaults to current
                     directory.

optional arguments:
  -h, --help         show this help message and exit
  -r, --recursive    process images in subdirectories
  --width W          maximal width of the thumbnail
  --height H         maximal height of the thumbnail
  -e EXT, --ext EXT  process only images with given extension
```