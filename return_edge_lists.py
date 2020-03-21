#given a data file you want to make edge lists for
##return a dictionary where the key is SP ID and the value is the edge list

from collections import defaultdict
from itertools import combinations

def read_file(raw_data_file):
    #read file in as list of lines
    with open(raw_data_file, 'rb') as my_file:
        content = my_file.readlines()
    #return the content
    return content

def return_edge_lists(data):
    #assume that the SP ID is at index pos. 0
    #assume the value is at index pos. 1
    dictionary = defaultdict(list)
    #for every value in the data we've read into memory
    for i in range(len(data)):
        #split the data into its columns(id and value)
        columns = data[i].split(b'\t')
        #append values associated with SP ID to a list
        dictionary[columns[0]].append(columns[1].strip(b'\n').strip(b'\r'))
    #take the lists made by CSV values above and make edge lists using
    ##Tim's example w/ itertools.combinations()
    for key, val_list in dictionary.items():
        dictionary[key] = list(combinations(val_list, 2))
    #return the dictionary {SP ID:[edge_list], ...}
    return dictionary

def main():
    #vars...
    ##given on of the split files we can build an edge list
    input_file = r'output\egonetworkscombined.tsv'

    #run...
    ##read the file in
    data = read_file(input_file)
    ##return the edge list
    edge_list_dict = return_edge_lists(data)

##    #display the edge list data
##    for key, val_list in edge_list_dict.items():
##        print(key)
##        for val in val_list:
##            print('\t', val)
##        print()

if __name__ == '__main__':
    main()
