#!/usr/bin/env python3
import os
import sys
import pathlib
import argparse
import pyperclip
import re

# USER INTERFACE
parser = argparse.ArgumentParser(
    prog='rename-all',
    description='Take list of files separated by new line form the clipboard and rename the files from current directory in the ascending order')

parser.add_argument('--ext', default='*',
                    help="will only change name of files with this extension. Default all files")
args = parser.parse_args()
extension = args.ext


# FOR SORTING FILES
def extractFirstDigit(libObject):
    name = libObject.name
    digit = re.search(r"\d+", name)
    if not digit:
        return 0
    return int(digit.group(0))


# VARIABES
directory = pathlib.Path().resolve()
srcFiles = [item for item in directory.glob(
    f"*.{extension}") if item.is_file()]
srcFiles.sort(key=extractFirstDigit)


def summary(srcFiles, newNames):
    paths = []
    for src, name in zip(srcFiles, newNames):
        ext = src.suffix
        newName = name + ext
        dist = directory / newName
        paths.append((src, dist))
        print(f"{src.name}\t\t{dist.name}")

    return paths


def chageNames(paths):
    for src, dist in paths:
        os.rename(src, dist)


def main():
    clipboard = pyperclip.paste()
    newNames = clipboard.split('\n')

    print("The fallowing changes will occurs:")
    paths = summary(srcFiles, newNames)
    decision = input("If you want to continue type yes\n")
    if decision != 'yes':
        sys.exit()

    chageNames(paths)


main()
