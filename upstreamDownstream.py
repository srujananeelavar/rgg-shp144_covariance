# READ ME
# This program works with the output of blastParser.py.
# However, any Excel file that contains the column names ID, Contig, Subject Start, and Subject End can also
# be used as an input.

import os
import pandas as pd

from Bio.Seq import Seq
# from Bio.Alphabet import generic_dna

#takes in the input Excel file and creates dictionary
def Excel_to_dict(file):
	df = pd.read_excel(file)

	#keep only the rows that contain ID, Contig, Subject Start, Subject End
	df = df[['ID', 'Contig', 'Subject Start', 'Subject End']]

	out = dict()
	for index, row in df.iterrows():
		ID, contig, start, end = row
		if ID in out:
			out[ID].append((str(contig), int(start), int(end)))
		else:
			out[ID] = [(str(contig), int(start), int(end))]

	return out

#takes in the input data and finds sequences either upstream or downstream the given data for a given length
#the output is a fas file, where each sequence is labeled by its fas ID, contig found, and start position
#the sequences can either be outputed either as a nucleotide or amino acid sequence
#a divider can also be added to separate the orginal data and the found upstream/downstream data
def findUpDown(data, fas_dir, direction, length, output_type, divider, output_file):
	#dictionary to hold all the sequences
	out = []
	for ID in data:
		file = fas_dir + ID + '.fasta'
		#open file
		inputFile = open(file, 'r')
		inputString = inputFile.readlines()
		inputFile.close()
		for option in data[ID]:
			#find sequence
			seq = findSeq(option, inputString, direction, length, output_type, divider)
			out.append((ID, option[0], option[1], seq))

	#output as fas file
	f = open(output_file + '.fasta', 'w')
	for ID, contig, start, seq in out:
		f.write('>' + str(ID) + ' ' + contig + ' ' + str(start) + '\n')
		f.write(seq + '\n')
	f.close()

#takes in the sequence information and finds the sequence in the indicated direction and length
def findSeq(option, inputString, direction, length, output_type, divider):
	contig, start, end = option
	label = '>' + contig + '\n'

	#find contig
	startContig = inputString.index(label)
	gene = inputString[startContig+1].strip('\n')
	for line in inputString[startContig+2:]:
		#stop at next contig
		if '>' in line:
			break
		gene += line.strip('\n')

	#make sure length is divisible by 3
	while length%3 != 0:
		length += 1

	#find seq as well as upstream/downstream
	if start < end:
		#account for zero indexing
		og = gene[start-1:end]

		if direction == 'up':
			#upstream
			more = start-length-1
			while more < 0:
				more += 3
			new = gene[more:start-1]
		else:
			#downstream
			more = end+length
			while more > len(gene):
				more -= 3
			new = gene[end:more]

	else:
		#account for zero indexing
		og = gene[end-1:start]

		if direction == 'up':
			#upstream
			more = start + length
			while more > len(gene):
				more -= 3
			new = gene[start:more]
		else:
			#downstream
			more = end - length - 1
			while more < 0:
				more += 3
			new = gene[more:end-1]

	og = Seq(og)
	new = Seq(new)
	#reverse complement if on opposite strand
	if start > end:
		og = og.reverse_complement()
		new = new.reverse_complement()

	#change to amino acid if necessary
	if output_type == 'aa':
		og = og.translate()
		new = new.translate()

	#combine the two sequences
	if direction == 'up':
		if divider == 'y':
			final_seq = str(new) + '|' + str(og)
		else:
			final_seq = str(new) + str(og)
	else:
		if divider == 'y':
			final_seq = str(og) + '|' + str(new)
		else:
			final_seq = str(og) + str(new)

	return final_seq

def grabSeq(data, fas_dir, output_type, output_file):
	#dictionary to hold all the sequences
	out = []
	for ID in data:
		file = fas_dir + ID + '.fas'
		#open file
		inputFile = open(file, 'r')
		inputString = inputFile.readlines()
		inputFile.close()
		for option in data[ID]:
			#find sequence
			seq = findSeqOnly(option, inputString, output_type)
			out.append((ID, option[0], option[1], seq))

	#output as fas file
	f = open(output_file + '.fas', 'w')
	for ID, contig, start, seq in out:
		f.write('>' + str(ID) + ' ' + contig + ' ' + str(start) + '\n')
		f.write(seq + '\n')
	f.close()

#takes in the sequence information and finds the sequence in the indicated direction and length
def findSeqOnly(option, inputString, output_type):
	contig, start, end = option
	label = '>' + contig + '\n'

	#find contig
	startContig = inputString.index(label)
	gene = inputString[startContig+1].strip('\n')
	for line in inputString[startContig+2:]:
		#stop at next contig
		if '>' in line:
			break
		gene += line.strip('\n')

	#find sequence
	if start < end:
		gene = gene[start-1:end+200]
	else:
		end -= 200
		if end < 0:
			end = 0
		gene = gene[end:start]

	gene = Seq(gene)
	#reverse complement if on opposite strand
	if start > end:
		gene = gene.reverse_complement()

	#translate
	seq = gene.translate(to_stop=True)

	if output_type == 'aa':
		return str(seq)
	else:
		#change back to nucleotides
		length = len(seq)
		return str(gene[:length*3])

if __name__ == '__main__':
	data_file = input('Enter name of input Excel file: ')
	fas_dir = input('Enter the path to the fas directory: ')
	while fas_dir[-1] != '/':
		print("Make sure to add a '/' to the end of your directory")
		fas_dir = input('Enter the path to the fas directory: ')
	direction = input('Would you like to look upstream (up), downstream (down), or just grab the sequences (seq)?: ')
	while direction != 'up' and direction != 'down' and direction != 'seq':
		print("Invalid direction entered.")
		direction = input('Would you like to look upstream (up), downstream (down), or just grab the sequences (seq)?: ')

	if direction == 'seq':
		output_type = input('Would you like the output to be in nucleotides (n) or amino acids (aa)?: ')
		while output_type != 'n' and output_type != 'aa':
			print('Invalid output type.')
			output_type = input('Would you like the output to be in nucleotides (n) or amino acids (aa)?: ')
	else:
		length = int(input('How far would you like to go in that direction?: '))
		output_type = input('Would you like the output to be in nucleotides (n) or amino acids (aa)?: ')
		while output_type != 'n' and output_type != 'aa':
			print('Invalid output type.')
			output_type = input('Would you like the output to be in nucleotides (n) or amino acids (aa)?: ')
		divider = input('Would you like to add a divider "|"? (y/n): ')
		while divider != 'y' and divider != 'n':
			print('Invalid input.')
			divider = input('Would you like to add a divider "|"? (y/n): ')

	output_file = input('Enter the name you want for the output fas file: ')

	data = Excel_to_dict(data_file)
	if direction == 'seq':
		grabSeq(data, fas_dir, output_type, output_file)
	else:
		findUpDown(data, fas_dir, direction, length, output_type, divider, output_file)