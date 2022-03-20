#!/usr/local/bin/python

import sys
import os.path
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.SeqUtils.CheckSum import seguid
import csv
import sys
from Bio.Seq import Seq
from io import StringIO
import itertools
from itertools import combinations
import os
from collections import Counter

# Simple, takes fasta file, counts Ns, outputs CSV table

if len(sys.argv)!=2:
	print("Usage: python CountsNs_in_seq_py3.py contigs.fasta")
	sys.exit()
	
print("Running CountsNs_in_seq_py3.py")

input_genome_file = sys.argv[1]
outprefix = os.path.splitext(input_genome_file)[0]


f0 = open(outprefix+'_countNs.csv', 'w')#make empty file
header= 'genome_id,N_count'
print(header, file=f0)
f0.close()

for record in SeqIO.parse(open(input_genome_file, "rU"), "fasta"):
	this_sequence = (str(record.seq)).upper()
	this_id = str(record.id)
	N_count = this_sequence.count("N")
	f1 = open(outprefix+'_countNs.csv', 'a')#make empty file
	print(this_id+','+str(N_count), file=f1)
	f1.close()

print('That\'s All Folks!')