# -*- coding: UTF-8 -*-
# ^^ Unicode Encoding ^^
import sys
import os
import pdb

reading_systems = ["Adobe","Amazon","Apple","B&N","Google","Kobo","Readium"]
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
           col_count = 1
        with open(filename, 'r') as infile:
            filename_dir = os.path.dirname(filename)
            base_no_ext = os.path.basename(filename).split('.')[0]
            new_filename_ = os.path.join(filename_dir,base_no_ext+'_wiki.txt')
            new_filename = "temp.txt"
            with open(new_filename, 'w') as outfile:
                for line in infile:
                    if "Reading System" not in line and table_flag == False:
                        if '|-' not in line or '|}' not in line:
                            table_name =  line.strip('\n')
                            table_name = table_name.strip('\r')
                            table_name = table_name.replace(',', '')
                            table_name = table_name + '\r\n|-\n!'
                            header_counter += 1
                        elif '|-' in line:
                           table_name += line
                    if "Reading System" in line:
                        for element in line:
                            if element ==',':
                                col_count += 1
                        print line
                        if table_flag == False:
                            outfile.write(('\n{|class="wikitable" style=text-align:left; \n|-\n!colspan ="%d" style="text-align:left;"|'+ table_name) %col_count)
                        table_flag = True
                    line_array = list(line)               # line_array takes in every line from infile that is the last header
                    first_element_in_line = line_array[0] # plus the table content. A new line is added after every loop and the previous line is done away with
                    if first_element_in_line == ',':
                        first_element_in_line = ' ,'
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
                        #for index in range(len(array_of_table_contents)-1): #Deletes first element in array, which is either an empty string or the retail_partner's name
                             #array_of_table_contents[index] = array_of_table_contents[index+1]
                        #array_of_table_contents.pop()
                        table_contents = '' #Table contents is reinitialized for next loop
                        #print table_contents
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
                        if table_flag == True:
                            outfile.write(table_contents)
                        table_contents = "" #Table contents is reinitialized
                outfile.write('|}')

    except Exception as problem:
        print ("Error thrown: %s"  %problem)
        sys.exit()
