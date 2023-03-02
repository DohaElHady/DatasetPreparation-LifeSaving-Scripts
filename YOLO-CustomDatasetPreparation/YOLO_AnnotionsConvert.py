'''
Each label in Yolo-formated annotations' text file is formated as follows:
    class_index    x_center    y_center    bbox_width   bbox_height

This script aims to edit the label class_index in a bulk of annotaions' files.
Example for when to use:
    If you have a dataset with dog vs cat annotaions indexed as follows:
    @ dog_index = 0 and cat_index = 1
    and you want to combine it with another dataset of dog vs cat too
    however this dataset is indexed as follows:
    @ dog_index = 1 and cat_index = 0
    then you need to convert the annotations of one of them inorder to
    be able to combine both datasets, here comes the role of this script.

How to use:
1-  Edit the {intial_txt_dir} variable to the location of labels, the *.txt files.
2-  Optional: Edit the {new_txt_dir} variable.
3-  Set the {no_of_calsses} variable.
4-  Edit the class indices to the order you want:
        Ex: intial labels are [0,1,2] and you want it to be [2,1,0]
        Then set the {new_indices} variable to [2,1,0].
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
# The new indices values
new_indices = [2,1,0]
# Number of classes in the dataset
no_of_calsses = 3


################################ Exceptions & Setup ##########################################
# Raise exception if the user selected the same location for {new_txt_dir} and {intial_txt_dir}
if intial_txt_dir == new_txt_dir:
    raise Exception("The directory of the new annotations must be different than the intial directory.")
# Raise exception if the user missed an index
if len(new_indices) != no_of_calsses:
    raise Exception("There is an error in formating {new_indices} variable.")

# Create the new_txt_dir if it is not existed
if not exists(new_txt_dir):
    makedirs(new_txt_dir)

# {new_indices} variable setup
new_indices= list(map(str, new_indices))



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
                # Capture the old index as the first element in the annotaion line:
                # class_index    x_center    y_center    bbox_width   bbox_height
                class_index = line.rsplit()[0]
                # Replace the old class_index with new index
                # Keep the rest of the line as it is
                line=line.replace(class_index ,new_indices[int(class_index)] ,1)
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
