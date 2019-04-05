#!/bin/python3
import glob
from PIL import Image
import os


valid_ext = ['.jpg', '.jpeg', '.png']


class ImageIsThumbnail(Exception):
    pass


class ThumbnailExists(Exception):
    pass


def parse_img_path(img_path):
    '''
    Returns tuple (fullpath, file_name, file_extension, dirpath), where
    file_name - file's name w/o extension
    '''
    dirpath, file_fullname = os.path.split(img_path)
    file_name, file_ext = os.path.splitext(file_fullname)
    return (img_path, file_name, file_ext, dirpath)


def img_scan(path="./", recursive=False, extension=None):
    '''
    Returns list of images in given path and, if recursive set to True,
    in its subdirectories.
    '''

    # prepare arguments for glob search
    if recursive:
        path = os.path.join(path, '**/*{ext}')
    else:
        path = os.path.join(path, '*{ext}')

    if extension:
        exts = [extension, ]
    else:
        exts = valid_ext

    # search images
    images = []
    for ext in exts:
        images_tmp = glob.glob(
            path.format(ext=ext),
            recursive=recursive
        )
        # for img in images_tmp:
        #     images.append(parse_img_path(img))
        images += images_tmp

    return images


def create_thumbnail(img_path, prefix="tn_", postfix="", size=(300, 300)):
    org_path, org_name, org_ext, org_dirname = parse_img_path(img_path)
    tn_name = "{pre}{name}{post}{ext}".format(
        pre=prefix,
        name=org_name,
        post=postfix,
        ext=org_ext
    )
    tn_path = os.path.join(org_dirname, tn_name)

    # Check if thumbnail already exists
    if org_name.startswith(prefix) and org_name.endswith(postfix):
        raise ImageIsThumbnail(
            "Image is already a thumbnail:\n\t{}".format(org_path)
        )
    if os.path.isfile(tn_path):
        raise ThumbnailExists(
            "Thumbnail already exists:\n\t{}".format(tn_path)
        )

    # Create thumbnail
    print("Creating thumbnail: " + tn_path)
    with Image.open(org_path) as img:
        img.thumbnail(size)
        img.save(tn_path)


if __name__ == "__main__":
    images = img_scan(recursive=True)
    total = len(images)
    print("Found {} images.".format(total))
    processed = 0
    ignored = 0
    for i in images:
        try:
            create_thumbnail(i)
        except ImageIsThumbnail as exc:
            print(exc)
            ignored += 1
        except ThumbnailExists as exc:
            print(exc)
            ignored += 1
        else:
            processed += 1

    print("Total:\t\t{}".format(total))
    print("Created:\t{}".format(processed))
    print("Ignored:\t{}".format(ignored))
