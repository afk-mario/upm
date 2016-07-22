#!/usr/bin/python

import os
import sys, getopt
import tarfile
from operator import itemgetter

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print('Input file is "', inputfile)
    print('Output file is "', outputfile)
    InstallPack(inputfile, outputfile)

def InstallPack(i, o):
    print("Extracting")
    print(tarfile.is_tarfile(i))
    package = tarfile.open(i)
    members = package.getmembers()
    arrayOfFiles = []
    for member in members:
        if(member.isfile()):
            parent = member.name.split('/', -1)
            if(len(parent) > 1):
                parent = parent[1]
            else:
                parent = parent[0]
            name = member.name.split('/', 2)[-1]
            obj = {
                'parent': parent,
                'name': name,
                'member': member
            }
            arrayOfFiles.append(obj)
    arrayOfFiles = sorted(arrayOfFiles, key=itemgetter('parent'))
    arrayOfNewFiles = []
    checkParent = arrayOfFiles[0]['parent']
    tmpobj = {}
    for item in arrayOfFiles:
        if(item['parent'] != checkParent):
            checkParent = item['parent']
            tmpobj = {}
        if(item['name'] == 'asset'):
            tmpobj['asset'] = item['member']
        elif(item['name'] == 'pathname'):
            tmpobj['pathname'] = item['member']
        arrayOfNewFiles.append(tmpobj)
    CreateFiles(arrayOfNewFiles, o, package)

def CreateFiles(arr, o, package):
    for item in arr:
        # print(item)
        pathname = item.get('pathname', None)
        asset = item.get('asset', None)
        newPath = None
        print("-----------")
        print(pathname)
        print(asset)
        if(pathname is not None):
            nfile= package.extractfile(pathname)
            data = nfile.readline().decode()
            nfile.close()
            print(data)
            newPath = os.path.join(o, data)
        if(asset is None):
            filename, file_extension = os.path.splitext(newPath)
            print(file_extension)
            if not os.path.exists(newPath) and not file_extension:
                os.makedirs(newPath)
        else:
            gsset.name = newPath
            print("extracted fil :")
            print(asset.name)
            nfile = package.extract(asset)

if __name__ == "__main__":
    main(sys.argv[1:])
