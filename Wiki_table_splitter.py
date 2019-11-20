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
            sys.stderr.write('Usage: python %s WikiML_file\n' % argvs[0])
            sys.exit(1)
        filenames = argvs[1:]
        for filename in filenames:
            table_count = 0
            header_counter = 1
            table_name = ''
            col_count = 0
        with open(filename, 'r') as infile:
            filename_dir = os.path.dirname(filename)
            base_no_ext = os.path.basename(filename).split('.')[0]
            new_filename = os.path.join(filename_dir,base_no_ext+'_table_split.txt')
            with open(new_filename, 'w') as outfile:
                for line in infile:
                    if "Reading System" not in line:
                            table_name +=  line
                            #header_counter += 1
                    if "Reading System" in line:
                        table_name += line
                        table_count += 1
                    line = line.split("||")
                    print line[0]
                    if line[0] in reading_systems:
                        table_count += 1
                        retail_partner = line[0]
                        #line.remove(retail_partner)
                        for element in line:
                            col_count += 1
                        if table_count > 1:
                            outfile.write('|}')
                        outfile.write(('\n==Results → %s==\n{|class="wikitable" style=text-align:left; \n|-\n!colspan ="%d" style="text-align:left;"|' + table_name) %(retail_partner, col_count))
                    str_line = ''
                    for index in range (len(line)-1):
                        str_line += line[index] + '||'
                        str_line += line[len(line)-1] + '\n'
                    outfile.write(str_line)
                outfile.write('|}')
    except Exception as problem:
        print ("Error thrown: %s"  %problem)
        sys.exit()
