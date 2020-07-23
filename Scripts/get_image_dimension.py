# getting image dimension using img_name
# image_height, image_width = get_image_dimensions(img_name)
import os

def read_image_dimensions(csv_file_path):
    
    # create an empty dictionary
    # read the csv line by line. 
    # for each line, you create one key and value pair. 
    
    results = {}
    csv_file = open(csv_file_path, 'r') 
    lines = csv_file.readlines() 

    # strips the newline character 
    for line in lines: 
        good_line = line.strip()
        good_line_ls = good_line.split(',')
        name = good_line_ls[0]
        width = good_line_ls[1]
        height = good_line_ls[2]
        
        results[name] = {
            'width': width,
            'height': height
        }
    
    csv_file.close()
    return results
    
if __name__ == '__main__':
    # read a csv
    here = os.getcwd()
    file_name = 'image_dimensions_corrected.csv'
    results = read_image_dimensions(os.path.join(here, file_name))
    print(results)