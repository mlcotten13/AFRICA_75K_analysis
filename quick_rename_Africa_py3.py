#!/usr/local/bin/python
import sys
import os.path
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from io import StringIO
import csv

#input tsv tables from GISAID (nice they put all the details in multiple tables, why not just one table? 
# create GISAID id, details dictionary 

print('quick_rename_Africa_py3.py running')	

if len(sys.argv)!=4:
	print("Usage: python quick_rename_Africa_py3.py seq_to_rename.fasta sequence_tech_table dates_location_table ")
	sys.exit()	
All_entries = sys.argv[1]
outprefix = os.path.splitext(All_entries)[0]

sequence_tech_table = sys.argv[2]
dates_location_table = sys.argv[3]


def remove_space(string):
	return "".join(string.split())


all_details_dict1 = {}
	
with open(dates_location_table) as this_file:
	tsv_file = csv.reader(this_file, delimiter="\t")	
	next(tsv_file)
	for row in tsv_file:
		this_ID = str(row[0])
		
		this_collection_date = str(row[1])
		this_submission_date = str(row[2])
		location_all = str(row[3])
		pieces = location_all.split("/")
		if len(pieces)>= 2:
			country = remove_space(str(pieces[1]))
			country_clean = country.replace(',','')
		else:
			print("messed up id")
			country_clean= "NA"
		all_details_dict1[this_ID]=(country_clean+"|"+this_collection_date+"|"+this_submission_date)
this_file.close()

print(all_details_dict1)

all_details_dict2 = {}
with open(sequence_tech_table) as this_file2:
	tsv_file2 = csv.reader(this_file2, delimiter="\t")
	next(tsv_file2)
	for row in tsv_file2:
		this_virus_name = str(row[0])
		this_virus_name_pieces = this_virus_name.split("/")
		this_sample = this_virus_name_pieces[2]
		this_ID = str(row[1])
		old_value = all_details_dict1.get(this_ID)
		this_technology = remove_space(row[8])
		this_technology_clean = this_technology.replace(',','')		
		new_value= old_value +"|"+this_sample+"|"+this_technology_clean
		all_details_dict2[this_ID]=new_value

this_file.close()

print(all_details_dict2)
print(str(len(all_details_dict2)))

f2 = open(outprefix+"_nn.fasta", "w")
for record in SeqIO.parse(open(All_entries, "rU"), "fasta"):
	id_pieces = (str(record.id)).split("|")
	g_id = id_pieces[1]
	new_id = g_id+"|"+(all_details_dict2.get(g_id, 'Not_here'))	
	print('>'+'%s' % new_id, file=f2)
	print(record.seq, file=f2)
f2.close()

print('That\'s All Folks!')
sys.exit()
