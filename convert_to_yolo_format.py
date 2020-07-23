import pandas as pd
import json
from get_image_dimension import read_image_dimensions
import os
# define a function to get categories and bbox
def get_category_bbox(path_to_csv, path_to_imgs):
    
    # read a csv
    here = os.getcwd()
    file_name = 'image_dimensions_corrected.csv'
    img_dimensions = read_image_dimensions(os.path.join(here, file_name))
    
    data = pd.read_csv(path_to_csv)
    counter = 0
    # loop through the images
    success_counter = 0
    no_object_counter = 0
    no_img_dimension_counter = 0
    for idx, row in data.iterrows():
        counter += 1
        print('processing {}'.format(counter))
        objects = json.loads(row['Label']).get('objects')
        img_name = row['ID'] + '-' + row['External ID']

        # if no object, contiue the loop
        if not objects:
            no_object_counter += 1
            old_path = os.path.join(path_to_imgs, img_name)
            new_path = os.path.join(here, 'not_used_imgs', img_name)
            os.rename(old_path , new_path)
            continue

        # getting image dimension using img_name
        img_shape_dict = img_dimensions.get(img_name)
        if not img_shape_dict:
            no_img_dimension_counter += 1 
            continue

        image_width = img_shape_dict['width']
        image_height = img_shape_dict['height']
    
    
        image_yolo_results = []
        # looping through objects
        for obj in objects:
            # look at one example
            title = obj['title']
            bbox = obj['bbox']
            width = bbox['width']
            top = bbox['top']
            height = bbox['height']
            left = bbox["left"]

            yolo_result = convert_to_yolo(image_height, image_width, width, top, height, left, title)
            image_yolo_results.append(yolo_result)

        # we can have multiple instances where you have 
        # image1.funny.jpg -> [image1, funny, jpg]
        # image1.txt instead of image1.funny.txt
        split_ls = img_name.split('.')
        new_list = split_ls[:-1]
        file_name = '.'.join(new_list) + '.txt'
        f = open(os.path.join(path_to_imgs, file_name), 'w')
        for yolo in image_yolo_results:
            for ele in yolo:
                f.write(str(ele) + ' ')
            f.write('\n')
        f.close()
        
        success_counter += 1
        
        print('success counter: {}. Total file to process is {}'.format(success_counter, len(data)))
        print('no image dimension is {}. No object counter is {}'.format(no_img_dimension_counter, no_object_counter))


def convert_to_yolo(image_height, image_width, box_width, box_top, box_height, box_left, title):


    # Determine the title of the box
    if title == 'tidy':
        title_int = 0
    else:
        title_int = 1
    
    box_top = float(box_top)
    box_left = float(box_left)
    box_width = float(box_width)
    box_height = float(box_height)
    image_width = float(image_width)
    image_height = float(image_height)
    # Formulas for YOLO format
    x = box_width / image_width
    y = box_height /image_height
    center_x = (box_left + box_width/2) / image_width
    center_y = (box_top + box_height/2) / image_height
    
    if x > 1 or y > 1 or center_x > 1 or center_y > 1:
        print('shit happens')
    return (title_int, center_x, center_y, x, y)

    
if __name__ == '__main__':
    here = os.getcwd()
    path_to_csv = 'export-2020-07-13T20_07_52.584Z.csv'
    path_to_imgs = os.path.join(here, 'img')
    # 0. call a function to get categories and bbox
    get_category_bbox(path_to_csv, path_to_imgs)



