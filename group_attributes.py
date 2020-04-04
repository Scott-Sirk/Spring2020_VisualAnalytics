#goal - get grouped counts of attributes

from collections import Counter
from collections import defaultdict

def file_to_dict(file_name):
    #make dictionary like {sp_id:[list of values]...}
    dictionary = defaultdict(list)
    #open file and read as list into memory
    with open(file_name, 'rb') as my_file:
        lines = my_file.readlines()
    #for every line in the file - skipping the headers
    for line in lines[1:]:
        #unpack the tab delim. file
        sp_id, data_point = line.split(b'\t')
        #and append value to running list for that jey - strippin out any extra new lines
        dictionary[sp_id].append(data_point.strip(b'\n').strip(b'\r'))
    return dictionary

def group_attributes(dict1, dict2):
    #keep a running dict formatted like {dict1_value:[list of dict 2 values]}
    master_dict = defaultdict(list)
    #for everything in dict1
    for key, value in dict1.items():
        #for every value in the value list in dict 1
        for data_point in value:
            #get all the same attributes for that person(sp id) in dict 2
            for attribute in dict2[key]:
                #and add all the values for that person to a running list
                ##for the current value being used from dict 1
                ##it will being to look like...
                ###{Voltare:[general, farmer, wife, general...]}
                ###if dict 1 was networks and dict2 was occupation
                master_dict[data_point].append(attribute)
    #return the dictionary
    return master_dict

def count_attributes(master_dict):
    #change the list on values [general, farmer, wife, general]
    ##into a dictionary {general:2, farmer:1, wife:1}
    ##and save that change to the dictionary
    for key, value_list in master_dict.items():
        master_dict[key] = Counter(value_list)
    return master_dict

def main():
    #vars...
    file1 = r'output\egonetworkscombined.tsv'
    file2 = r'output\occupation.tsv'

    #run...
    ##read files into mempry
    dict1 = file_to_dict(file1)
    dict2 = file_to_dict(file2)
    ##get attributes in dict 2 grouped by dict 1 attributes
    attributes = group_attributes(dict1, dict2)
    ##change a list of attributes into a dictionary of counts
    final_dictionary = count_attributes(attributes)
    #final dictionary is formatted like...
    ##{dict1_value:{dict2_value1:value1_count, dict2_value2:value2_count...}...}

    ###display the outcome...
    for key, value in final_dictionary.items():
        print(key)
        for attribute, count in value.items():
            print('\t', attribute, ':', count)

if __name__ == '__main__':
    main()
