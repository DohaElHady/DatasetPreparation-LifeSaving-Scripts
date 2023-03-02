'''
Each label in Yolo-formated annotations' text file is formated as follows:
    class_index    x_center    y_center    bbox_width   bbox_height

This script aims to delete certian class_index from  bulk of annotaions' files.
Example for when to use:
    If you have a dataset with dog vs cat vs frog annotaions indexed as follows:
    @ dog_index = 0 and cat_index = 1 and frog_index = 3
    and you want to combine it with another dataset of dog vs cat only
    and you want to remove the frog annotaions to be able to combine both datasets
    for dog vs cat problem, here comes the role of this script.

How to use:
1-  Edit the {intial_txt_dir} variable to the location of labels, the *.txt files.
2-  Optional: Edit the {new_txt_dir} variable.
2-  Set the class indices you want to delete: {delete_indices}
3-  Run the code.
4-  Find your new files at intial_txt_dir+'_v2' directory, or the location you chose.
'''

from os import listdir, getcwd,remove,rename, makedirs
from os.path import join, exists

############################ User Defined Variables #########################################
# The intial *.txt files directory
intial_txt_dir = 'new_dir/labels/coco_format_fish_data_seg'
# The new *.txt files directory to be saved
new_txt_dir = intial_txt_dir+'_v2'
# The indices of classes to be deleted
delete_indices = [3]


################################ Exceptions & Setup ##########################################
# Raise exception if the user selected the same location for {new_txt_dir} and {intial_txt_dir}
if intial_txt_dir == new_txt_dir:
    raise Exception("The directory of the new annotations must be different than the intial directory.")

# Create the new_txt_dir if it is not existed
if not exists(new_txt_dir):
    makedirs(new_txt_dir)

# {delete_indices} variable setup
delete_indices= list(map(str, delete_indices))


################################ Core Operations ###########################################
if __name__ == "__main__":
    # Loop over the text files in the intial directory
    for sample_name in listdir(intial_txt_dir):

        # Read the text in each file
        # Save it to {txt} variable
        txt_filename = join(intial_txt_dir, sample_name)
        txt_file=open(txt_filename,"r+")
        txt=txt_file.read()

        # Create holder variable for the txt of the new annotaions
        new_txt=''

        # Edit the index of each file line by line
        for line in txt.rsplit('\n'):
            # Check the line is not empty
            if len(line) !=0:
                # Capture the index as the first element in the annotaion line:
                # class_index    x_center    y_center    bbox_width   bbox_height
                class_index = str(line.rsplit()[0])
                # Check if the index should not be deleted
                # Else continue without writing it to the {new_txt}
                if not class_index in delete_indices:
                    # Paste the new line to the new_txt holder variable
                    new_txt= new_txt+line+'\n'

        # Create new file with the same name in the new directory
        new_txt_filename = join(new_txt_dir, sample_name)
        new_file = open(new_txt_filename, "w")
        # Write the {nex_txt} to the {new_file}
        new_file.write(new_txt[:-1])
        # Close the opened files
        new_file.close()
        txt_file.close()
