import pickle
import bz2
import argparse
import pandas as pd
import os


S='S';T='T';K='K';L='L'

def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-ls', '--list', help = 'list of file names', default='', required = True)
    parser.add_argument('-pk', '--pkl', help = 'import pickle file', default = '', required = True)
    parser.add_argument('-o2', '--out2', help = 'list of species total reads', default = '', required = True)
    parser.add_argument('-sp', '--splist', help = 'abundant species list', default = '', required = True)
    args = parser.parse_args()
    return args

def samplelist(list):
    samplelist=[]
    with open(list) as f:
        line = f.readlines()
    for sample in line:
        samplelist.append(sample[:-1])
    return samplelist

def MakeDataStructure(list,db,sp):
    DS = {}; DS[S]={}
    DS[T] = {}; DS[K] = {}; DS[L] = {}
    for sample in list:
        DS[T][sample] = 0
        with open(sample) as f:
            content = f.readlines()
            DS[K][sample] = {}
            for line in content[1:]:
                ## 1. update T
                DS[T][sample] += int(line.split('\t')[1][:-1])
                ## 2. update S
                marker = line.split('\t')[0]
                if db['markers'][marker]['clade'] in sp:
                    clade = db['markers'][marker]['clade']
                ## 3. update K
                    if DS[K][sample].has_key(clade) == False:
                        DS[K][sample][clade] = {}
                    if DS[K][sample][clade].has_key(marker) == False:
                        DS[K][sample][clade][marker] = 0
                    DS[K][sample][clade][marker] += int(line.split('\t')[1][:-1])
                ## 4. update L
                    if DS[L].has_key(clade) == False:
                        DS[L][clade] = {}
                    if DS[L][clade].has_key(marker) == False:
                        DS[L][clade][marker] = db['markers'][marker]['len']
        print sample
    return DS




args = parse_args()

with open(args.pkl, 'rb') as ifile:
    db = pickle.loads(bz2.decompress(ifile.read()))
splist = samplelist(list = args.splist)
list = samplelist(list = args.list)
DS = MakeDataStructure(list=list,db=db,sp=splist)

with open(args.out2, 'wb') as handle:
    pickle.dump(DS, handle)

