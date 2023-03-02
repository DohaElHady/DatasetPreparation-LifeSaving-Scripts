'''
This script aims to disassemble bulk of executable files using 'objdump' or 'ndisasm'
command-line built-in linux tools.

How to use:
1-  Edit {directory} to the executable files *.exe location.
2-  Choose the disassembler: set {disassembler} to 'ndisasm' or 'objdump'.
3-  Run the code.
4-  Find the diassembled_{file-name}.txt files with the disassembled data in the same location.
'''

import subprocess
import os
############################ User Defined Variables #########################################
# Assign *.exe directory
directory = 'Open Source Projects'
# Choose the disassembler
disassembler = 'ndisasm' # set to 'ndisasm' or 'objdump'


################################ Core Operations ###########################################
if __name__ == "__main__":
    # Iterate over the *.exe files
    executable = os.listdir(directory)
    for filename in executable:
        # Check if the file is executable
        if filename.find(".exe")!=-1:
            # Implement the disassembling command
            if disassembler == 'ndisasm':
                list_files = subprocess.run(["ndisasm", "-b32", "{}/{}".format(directory,filename)], stdout=subprocess.PIPE, text=True)
            else:
                list_files = subprocess.run(["objdump", "-D", "{}/{}".format(directory,filename)], stdout=subprocess.PIPE, text=True)
            # Create text file to save the disassembled data in it
            f = open("diassembled_{}.txt".format(filename.replace(".exe", "")), "w")
            # Write the data
            f.write(list_files.stdout)
            # Close the file
            f.close()
