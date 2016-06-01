"""
The goal is to make a list of species, that have a max abundance across sample larger than 1%
"""
import argparse
import pandas as pd
import os

def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', help = 'list of file names', default='', required = True)
    parser.add_argument('-o1', '--out1', help = 'list of abundant species', default = '', required = True)
    parser.add_argument('-o2', '--out2', help = 'list of species total reads', default = '', required = True)
    args = parser.parse_args()
    return args

def samplelist(list):
    samplelist=[]
    with open(list) as f:
        line = f.readlines()
    for sample in line:
        samplelist.append(sample[:-1])
    return samplelist


def creatematrix(samplelist,out1,out2):
    outfile1 = open(out1,'w')
    outfile2 = open(out2,'w')
    splist = []
    for sample in samplelist:
        with open(sample) as f:
            content = f.readlines()
            for line in content:
                Line = line.split('\t')
                if Line[0] == 'k__Bacteria':
                    outfile2.write(sample+'\t'+Line[4]+'\n')
                if len(Line[0].split('|')) == 7:
                    if float(Line[1])>1 and (not Line[0].split('|')[6] in splist):
                        sp = Line[0].split('|')[6]
                        splist.append(sp)
                        outfile1.write(sp+'\n')
                        os.system('nohup python ~/dev/metaphlan2/metaphlan2/metaphlan2.py -t clade_specific_strain_tracker --min_ab 0.0 --clade '+ sp + ' ../HMPdata/'+sample[:-4]+ ' --input_type bowtie2out > ../HMPsp/' + sp + ' --mpa_pkl ~/dev/metaphlan2/metaphlan2/db_v20/mpa_v20_m200.pkl &')
    return splist


args = parse_args()
samplelist = samplelist(list = args.list)
splist = creatematrix(samplelist=samplelist,out1=args.out1,out2=args.out2)
