import os
import xlwt

#parseDir takes a directory and places all files into a list and creates a list of the contents in the files
#the final output would be a dictionary of the following features:
#ID, contig, E-value, alignment length, percentage similarity, query start, subject start, subject end
def parseDir(directory, querys, blast_type, max_Eval, similarity, min_length):
    listOfInputs = []
    for file in os.listdir(directory):
        if "fasta.out" in file:
            listOfInputs.append((directory + file))

    dataParsed = dict()
    for file in listOfInputs:
        inputFile = open(file, "r")
        inputName = file.split('/')[-1].split('.')[0]
        inputString = inputFile.readlines() #returns a list containing all lines of file
        if querys == 1:
            dataParsed = parseBLAST(inputName, inputString, dataParsed, blast_type, max_Eval, similarity, min_length)
        else:
            dataParsed = parseBLAST_multi_query(inputName, inputString, dataParsed, blast_type, max_Eval, similarity, min_length)
        inputFile.close()

    return dataParsed

#parseBLAST takes the contents of the BLAST file and outputs a dictionary
#which contains ID, contig, eval, alignment length and percentage, query start, subject start and end
def parseBLAST(entryName, inputString, dataParsed, blast_type, max_Eval, similarity, min_length):
    out = dict()
    contigParsedLines = [[]] #create a list of lists currently size 1
    i = 0
    for line in inputString: #separate by contig
        if ">" in line:
            i += 1
            contigParsedLines.append([]) #append an empty list
        contigParsedLines[i].append(line) #contains list of from one contig to the next

    match = [[]]
    b = 0

    #separate by matches
    for entry in contigParsedLines[1:]:
        label = entry[0].split()[1:]
        contig = ' '
        for i in label:
            contig += i + ' '
        contig = contig.strip()
        for line in entry:
            if "Score" in line:
                b = b + 1
                match.append([])
                match[b].append(contig) #subject string name
            match[b].append(line)

    #for each match
    for item in match[1:]:
        contig = item[0]
        if blast_type == 'blastn':
            Eval = float(item[1].split("=")[-1].strip())
            strand = item[3].split("/")[-1] #reading frame
        elif blast_type == 'tblastn':
            Eval = float(item[1].split("=")[-1].split()[0].strip(','))
            strand = item[3].split("=")[-1]
        alignlen = int(item[2].split("/")[1].split()[0]) #alignment length
        percentage = int(item[2].split("/")[1].split("(")[1].split("%")[0]) #percentage similarity
        queryStart = int(item[5].split()[1]) #start position of query
        subStart = int(item[7].split()[1]) #start position of subject
        sequences = item[7:]
        seq = ''
        for line in sequences:
            if 'Sbjct' in line:
                seq += line.split()[2]

        if blast_type == 'blastn':
            if "Minus" in strand:
                subEnd = subStart - alignlen + 1 #keep in nucleotide sequence
            else:
                subEnd = subStart + alignlen - 1
        elif blast_type == 'tblastn':
            if "-" in strand:
                subEnd = subStart - (alignlen * 3) + 1 #keep in nucleotide sequence
            else:
                subEnd = subStart + (alignlen * 3) - 1

        if Eval < max_Eval and percentage >= similarity and alignlen >= min_length:
            if contig in out:
                out[contig].append((Eval, alignlen, percentage, queryStart, subStart, subEnd, seq))
            else:
                out[contig] = []
                out[contig].append((Eval, alignlen, percentage, queryStart, subStart, subEnd, seq))

    dataParsed[entryName] = out
    return dataParsed

#same as parseBlast but with multiple queries
#final dictionary contains:
# ID, query, contig, eval, alignment length and percentage, query start, subject start and end
def parseBLAST_multi_query(entryName, inputString, dataParsed, blast_type, max_Eval, similarity, min_length):
    out = dict()
    queryParsedLines = [[]] #create a list of lists currently size 1
    i = 0
    for line in inputString: #separate the queries
        if "Query=" in line:
            i += 1
            queryParsedLines.append([]) #append an empty list
        queryParsedLines[i].append(line) #contains list of from one Query= to the next Query=

    entryParsedLines = dict() #[q:entries,qlen]
    for queryGroup in queryParsedLines[1:]: #for each Query=
        entries = [[]]
        v = 0
        q = (queryGroup[0].split("= ")[1] + " " + queryGroup[1].strip()).strip("Query= ").strip()
        #separate by contig for each query
        for line in queryGroup[3:]:
            if ">" in line:
                v = v + 1
                entries.append([])
            entries[v].append(line) #contains information of only one contig
        entryParsedLines[q] = (entries)

    #separate by matches
    match = [[]]
    b=0
    for query in entryParsedLines.keys(): #for each query
        entries = entryParsedLines[query]
        for entry in entries[1:]:
            if entry != []:
                label = entry[0].split()[1:]
                contig = ' '
                for i in label:
                    contig += i + ' '
                contig = contig.strip()
            for line in entry:
                if "Score" in line:
                    b = b + 1
                    match.append([])
                    match[b].append(contig) #subject string name
                    match[b].append(query) #query peptide
                match[b].append(line)

    for item in match[1:]:
        contig = item[0]
        query = item[1]
        if blast_type == 'blastn':
            Eval = float(item[2].split("=")[-1].strip())
            strand = item[4].split("/")[-1] #reading frame
        elif blast_type == 'tblastn':
            Eval = float(item[2].split("=")[-1].split()[0].strip(','))
            strand = item[4].split("=")[-1]
        alignlen = int(item[3].split("/")[1].split()[0]) #alignment length in amino acid numbers
        percentage = int(item[3].split("/")[1].split("(")[1].split("%")[0]) #percentage similarity
        subStart = int(item[8].split()[1]) #starting position of subject
        sequences = item[8:]
        seq = ''
        for line in sequences:
            if 'Sbjct' in line:
                seq += line.split()[2]
        queryStart = int(item[6].split()[1]) #starting position of query

        if blast_type == 'blastn':
            if "Minus" in strand:
                subEnd = subStart - alignlen + 1 #keep in nucleotide sequence
            else:
                subEnd = subStart + alignlen - 1
        elif blast_type == 'tblastn':
            if "-" in strand:
                subEnd = subStart - (alignlen * 3) + 1 #keep in nucleotide sequence
            else:
                subEnd = subStart + (alignlen * 3) - 1

        if Eval < max_Eval and percentage >= similarity and alignlen >= min_length:
            if query in out:
                out[query].append((contig, Eval, alignlen, percentage, queryStart, subStart, subEnd, seq))
            else:
                out[query] = []
                out[query].append((contig, Eval, alignlen, percentage, queryStart, subStart, subEnd, seq))

    dataParsed[entryName] = out
    return dataParsed

def outputExcel(output, querys, file_name):
    book = xlwt.Workbook()
    sh = book.add_sheet('Peptide')

    if querys == 1:
        titles = ['ID', 'Contig', 'E-value', 'Alignment Length', 'Alignment Percentage', 'Query Start', 'Subject Start', 'Subject End', 'Sequence']
        for c, title in enumerate(titles):
            sh.write(0, c, title)

        #row counter
        r = 1
        for ID in output:
            for contig in output[ID]:
                for match in output[ID][contig]:
                    sh.write(r, 0, ID)
                    sh.write(r, 1, contig)
                    for c, info in enumerate(match, 2):
                        sh.write(r, c, info)
                    r += 1

    else:
        titles = ['ID', 'Query', 'Contig', 'E-value', 'Alignment Length', 'Alignment Percentage', 'Query Start', 'Subject Start', 'Subject End', 'Sequence']
        for c, title in enumerate(titles):
            sh.write(0, c, title)

        #row counter
        r = 1
        for ID in output:
            for query in output[ID]:
                for match in output[ID][query]:
                    sh.write(r, 0, ID)
                    sh.write(r, 1, query)
                    for c, info in enumerate(match, 2):
                        sh.write(r, c, info)
                    r += 1

    book.save(file_name.strip() + '.xls')

if __name__ == '__main__':
    #information for BLAST parsing
    directory = input('Enter BLAST directory: ')
    while directory[-1] != '/':
        print("Make sure to add a '/' to the end of your directory")
        directory = input('Enter BLAST directory: ')   
    querys = int(input('Enter the number of querys in your BLAST: '))
    blast_type = input('Enter the BLAST type (either blastn or tblastn): ')
    while blast_type != 'blastn' and blast_type != 'tblastn':
        print('Invalid BLAST type entered')
        blast_type = input('Enter the BLAST type (either blastn or tblastn): ')
    max_Eval = float(input('Enter the maximum E-value (default 10): '))
    similarity = int(input('Enter the minimum similarity percentage (default 0): '))
    min_length = int(input('Enter the minimum length of the match (default 0): '))

    #information for Excel file
    file_name = input('Enter the name you want for the output Excel file: ')

    # directory = '/Users/sient/python/src/small_peptide/test_blast/'
    # querys = 5
    # blast_type = 'tblastn'
    # max_Eval = 10
    # similarity = 0
    # min_length = 0
    # file_name = 'Test'

    #the code can be run without using the terminal if you have some type of text editor like Sublime Text
    #just comment out the above code and hardcode the inputs below
    output = parseDir(directory, querys, blast_type, max_Eval, similarity, min_length)

    #makes an Excel file from the parsed data
    outputExcel(output, querys, file_name)