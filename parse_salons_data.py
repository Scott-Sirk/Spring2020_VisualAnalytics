#parse and normalize the data for the salons project
import lookup

def read_file(raw_data_file):
    #read file in as list of lines
    with open(raw_data_file, 'rb') as my_file:
        content = my_file.readlines()
    #return the content
    return content

def iter_over_data(data, output):
    #because of some weird encoding we read the file in as a binary string
    ##so when we manuplitate the string we need to add a b'' in front
    headers = []
    #list of columns that had CSV values
    csv_columns = (1, 2, 8, 9, 10, 12, 14, 15, 16, 18, 23, 30)
    #for all data in the file we read in
    for i in range(len(data)):
        columns = data[i].split(b'\t')
        #save the headers for using later - to name detail files
        if i == 0:
            for c in columns:
                headers.append(c)
        #for all the columns in a row - if they're a 1->M CSV values write them to a sep. file
        for j in range(len(columns)):
            #These columns has comma seperated values - write them to seperate file to "normalize" the data
            ##1 - source
            ##2 - Ego Networks
            ##8 - Occupation
            ##9 - political rank
            ##10 - military rank
            ##12 - aristo title
            ##14 - knowlege netowrk
            ##15 - social network
            ##16 - professional network
            ##18 - academies
            ##22 - salons
            ##29 - nationality
            if j in csv_columns:
                make_1_to_many_files(columns[j], columns[0], headers[j], output)
        #write remaining non 1->M. data
        other_data = b'\t'.join([ii for jj, ii in enumerate(columns) if jj not in csv_columns])
        with open(output + '\\main.tsv', 'ab') as main_file:
            main_file.write(other_data + b'\n')

def make_1_to_many_files(data_point, unique_id, column_name, output_locn):
    #make a valid/consistant file name
    fname = column_name.decode('utf8', 'ignore').lower().replace("'", ' ').replace(' ', '_').replace('?', '').lower().strip()
    #if there is data...
    if data_point != b'':
        #open the output file
        with open(output_locn + '\\' + fname + '.tsv', 'ab') as my_file:
            #split on a comma - change comma-space to just comma to make it catch more
            for dp in data_point.replace(b', ', b',').split(b','):
                #write the data to the 1->M file
                my_file.write(unique_id + b'\t'
                              + lookup.correct_spelling.get(dp.replace(b'"', b''), dp.replace(b'"', b''))
                              + b'\n')
                    
def main():
    #vars...
    input_file = 'salons_project_raw_data.tsv'
    output_location = 'output'

    #run...
    data = read_file(input_file)
    iter_over_data(data, output_location)

if __name__ == '__main__':
    main()
