'''
This script aims to convert coco formated bounding box labels csv file to Yolo format.
The script takes a csv and returns a new csv.
The input csv is expected to have a column for the coco bbox annotations
    where each row is expected to contain single string formated
    as follow: '[x_min,y_min,width,height]',
    for example: '[2272.17, 1685.498, 837.912, 636.74088]'.
The output csv will contain all the columns in the input csv + yolo_bbox column
    where each row will contain single string formated
    as follow: '[x_center,y_center,bbox_width,bbox_height]'
'''

import csv
import pandas as pd

################################ Custom Functions ###########################################
def coco_to_yolo(x1, y1, w, h, image_w, image_h):
    # Takes coco bbox values (x_min,y_min,bbox_width,bbox_height) and image width and height
    # Returns yolo format bbox values as list [x_center,y_center,bbox_width,bbox_height]
    return [((2*x1 + w)/(2*image_w)) , ((2*y1 + h)/(2*image_h)), w/image_w, h/image_h]


############################ User Defined Variables #########################################
# The intial file with coco format bbox column
input_csv   = "input.csv"
# The coco format bbox column name
bbox_column_name = 'bbox'
# The output file that will hold the yolo format bbox column
output_csv  = "output.csv"

# Image width and height
# All images are expected to have the same dimensions
image_w, image_h = 4032,3024


################################ Core Operations ###########################################
if __name__ == "__main__":
    # Read the CSV that contains the coco_bbox annotations
    df=pd.read_csv(input_csv)

    # Extract the coco bbox string from the csv
    # Remove the brackets of the string
    # Convert the sting to a list of strings [x_min,y_min,width,height]
    # Cast the type to float
    coco_bbox= df[bbox_column_name].str.lstrip('[').str.rstrip(']').str.split(',',expand = True).astype('float')

    # Save the values of coco bbox elements separately
    coco_x_min=coco_bbox[0].to_numpy()
    coco_y_min=coco_bbox[1].to_numpy()
    coco_w=coco_bbox[2].to_numpy()
    coco_h=coco_bbox[3].to_numpy()

    # Reopen the coco bbox csv (input file)
    # Set the input file to be readable
    with open(input_csv,'r') as csvinput:
        # Create the new csv file to hold yolo bbox values (output file)
        # Set the output file to be writable
        with open(output_csv, 'w') as csvoutput:
            # Create writer for the output file
            writer = csv.writer(csvoutput)
            # Set the header row value to 'yolo_bbox'
            row0 = next(csv.reader(csvinput))
            writer.writerow(row0+['yolo_bbox'])
            # Create bbox row index holder
            i=0
            # Loop over the input csv rows
            for row in csv.reader(csvinput):
                # Calculate yolo bbox using custom function
                yolo_bbox=str(coco_to_yolo(coco_x_min[i],coco_y_min[i],
                                            coco_w[i],coco_h[i],image_w, image_h))
                # Write yolo bbox values to the output file
                writer.writerow(row + [yolo_bbox])
                i+=1
