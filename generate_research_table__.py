# -*- coding: UTF-8 -*-
# ^^ Unicode Encoding ^^
import sys
import os
import pdb

reading_systems = ["Adobe","Amazon","Apple","B&N","Google","Kobo","Readium"] # Add more retail partners
if __name__ == '__main__':
    try:
        argvs = sys.argv
        argcs = len(argvs)
        if argcs <= 1:
            sys.stderr.write('Usage: python %s csv_file\n' % argvs[0])
            sys.exit(1)
        filenames = argvs[1:]
        for filename in filenames:
           table_contents = ""
           table_counter = 0
           counter = 0
           table_flag = False
           reading_system_name = []
           column_num = 0
           table_name = ''
           header_counter = 1
        with open(filename, 'r') as infile:
            filename_dir = os.path.dirname(filename)
            base_no_ext = os.path.basename(filename).split('.')[0]
            new_filename_ = os.path.join(filename_dir,base_no_ext+'_wiki.txt')
            new_filename = "temp.txt"
            with open(new_filename, 'w') as outfile:
                for line in infile:
                    if "Reading System" not in line and table_flag == False:
                        if '|-' not in line or '|}' not in line:
                            table_name +=  line.strip('\n').strip('\r').strip(',') + '\r\n'
                            header_counter += 1
                        elif '|-' in line:
                           table_name += line
                    if "Reading System" in line:
                        table_flag = True
                    line_array = list(line)               # line_array takes in every line from infile that is the last header
                    first_element_in_line = line_array[0] # plus the table content. A new line is added after every loop and the previous line is done away with
                    if first_element_in_line != ',':
                        first_element_in_line = ''
                        while (len(reading_system_name) == 0) or (reading_system_name[-1]) != ',': #reading_system_name contains the retail partner who's devices
                            for character in line_array:                                           #are being iterated through at the moment and being formatted into WikiML
                                reading_system_name.append(character) #characters are the elements in limne_array (every element is size 1 char)
                                if character == ',':
                                    break
                        reading_system_name.pop() #deletes the comma from the reading_system_name
                        for element in reading_system_name:
                            first_element_in_line += str(element)
                        reading_system_name = first_element_in_line.split(',')
                        reading_system_name = reading_system_name[0]
                        if reading_system_name in reading_systems:
                            first_element_in_line = reading_system_name
                            if counter == 0:
                                counter = 1
                            else:
                                outfile.write('|}')
                                outfile.write(((header) % (first_element_in_line, header_counter, column_num, table_name)))
                                table_counter += 1
                        if line_array[-2] != '\r' and line_array[-1] != '\n':
                           line_array.append('\r')
                           line_array.append('\n')
                        reading_system_name = [] #reinitializes reading_system_name as empty before next loop
                    for element in line_array:
                       table_contents += element
                    table_contents = table_contents.strip('\n')
                    if  '\r' in table_contents:
                        table_contents = table_contents.replace('\n','')
                        table_contents = table_contents + '\n|-\n'
                        array_of_table_contents = table_contents.split(",")
                        for index in range(len(array_of_table_contents)-1): #Deletes first element in array, which is either an empty string or the retail_partner's name
                             array_of_table_contents[index] = array_of_table_contents[index+1]
                        array_of_table_contents.pop()
                        table_contents = '' #Table contents is reinitialez for next loop
                        for element in array_of_table_contents: #The table contents is formatted for WikiML
                             if element == array_of_table_contents[0]:
                                table_contents +='|' + element
                             else:
                                table_contents +='||' + element
                        if "Reading System" in table_contents: #When there is a new table, create a new WikiML table header
                             counter == 1
                             header =('\n==Results → %s==\n{|class="wikitable" style=text-align:left; \n|-\n!rowspan ="%d"|Reading System||colspan ="%d" style="text-align:left;"|\n%s\n|-\n'+ table_contents)
                             total_headers = table_contents.split('||')
                             for element in total_headers:
                                 column_num += 1
                        counter += 1
                        outfile.write(table_contents)
                        table_contents = "" #Table contents is reinitialized
                outfile.write('|}')

        with open(new_filename, 'r') as infile:
             substitution_1 = '<span style="color:red">X</span>'
             substitution_2 = '<span style="color:green">&#10003;</span>'
             outfile = open(new_filename_, 'w')
             current_line = infile.readline()
             while "Results" not in current_line: # "Results" is used here as the beginning of the final output, everything before it will not be copied over from temp
                 last_line = infile.tell()
                 current_line = infile.readline()
             infile.seek(last_line)
             for line in infile:
                 if "Reading System" in line and 'rowspan' not in line: #Reading system in the header but not in the table contents
                     line = line.split('||')
                     for line_index in range (1,len(line)):
                         if '\r\n' in line[line_index]:
                             temp_line = list(line[line_index])
                             line[line_index] = ''
                             for two_iterations in range(2): #deletes last two elements
                                 temp_line.pop()
                             for temp_line_index in range(len(temp_line)):
                                 line[line_index] += str(temp_line[temp_line_index])
                             line[line_index] = '[[#' + line[line_index] + '|' + line[line_index] + ']]\r\n'
                         else:
                             line[line_index] = '[[#' + line[line_index] + '|' + line[line_index] + ']]||'
                     line.remove("|Reading System")
                     line[0] = '|' + line[0]
                 pre_substitution_array  = ''
                 for element in line:
                    pre_substitution_array += element
                 pre_substitution_array = pre_substitution_array.replace('\r','')
                 pre_substitution_array = pre_substitution_array.split('||')
                 for index in range (len(pre_substitution_array)):
                     if "unsupported" in pre_substitution_array[index]:
                         pre_substitution_array[index] = substitution_1
                     elif "supported" in pre_substitution_array [index]:
                         pre_substitution_array[index] = substitution_2
                 line = ''
                 for index in range (len(pre_substitution_array) - 1):
                    line += str(pre_substitution_array[index]) + '||'
                 line += pre_substitution_array[-1] + '\n'
                 characters_in_line = list(line)
                 for index in range (len(characters_in_line)-1):
                       if characters_in_line[index] == "&" and characters_in_line[index+1] != '#':
                           characters_in_line[index] = '&amp;'
                       #____________________________________________________________________________________________________________________________
                       #~~~~~~~~~~~~~~~~~~Use at your own peril, these lines of code exchange '>' and '<' for its WikiML formatted equivalent, but
                       #if any other substitution is made, you run the risk of changing the content of said substitution~~~~~~~~~~~~~~
                       #____________________________________________________________________________________________________________________________

                       # if characters_in_line[index] == '<' and ((characters_in_line[index+1] != '/' ) and (characters_in_line[index+1] != 's')):
                       #      characters_in_line[index] = '&lt;'
                       # if characters_in_line[index] == '>' and ((characters_in_line[index-1] != '/' ) and (characters_in_line[index-1] != 'n')):
                       #      characters_in_line[index] = '&gt;'

                 line = ''
                 for element in characters_in_line:
                     line += element
                 outfile.write(line)
             outfile.close()
             os.remove("temp.txt")
    except Exception as problem:
        print ("Error thrown: %s"  %problem)
        sys.exit()
