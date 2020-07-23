import os

import pandas as pd
from PIL import Image
import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
import time


def image_download():
    here = os.getcwd()
    os.listdir(here)

    file2 = open('image_dimensions.csv', 'a')

    data = pd.read_csv('export-2020-07-13T20_07_52.584Z.csv')
    n_total_data = len(data)

    here = os.getcwd()
    image_folder = 'img'
    image_folder_path = os.path.join(here, image_folder)

    print(image_folder_path)

    counter = 0
    success_counter = 0
    failed_counter = 0
    for idx, row in data.iterrows():
        time.sleep(0.1)
        file_name = row['ID'] + '-' + row['External ID']
        url = row['Labeled Data']

        response = requests.get(url)

        img_array = np.array(bytearray(response.content), dtype=np.uint8)
        # do not save data in this case
        if img_array.size == 0:
            print('got no image')
            failed_counter += 1
            continue
        img = cv2.imdecode(img_array, -1)        

        img_path = os.path.join(image_folder_path, file_name)
        try:
            cv2.imwrite(img_path, img)
            success_counter += 1
        except:
            print('could not save image')
            failed_counter += 1
            continue
        
        height, width, _ = img.shape

        line = file_name + "," + str(width) + "," + str(height)+'\n'
        file2.write(line)


        counter += 1
#         if counter > 15:
#             break
        print('currently at {} with total of {}. Succeeded {}; failed {} times.'.format(counter, n_total_data, success_counter, failed_counter))
    file2.close()

if __name__ == '__main__':
    image_download()

#     start_time = time.time()
#     response = requests.get(row['lb_url'])
#     if response.status_code == 200:  # !!!
#         img_array = np.array(bytearray(response.content), dtype=np.uint8)
#         if img_array.size == 0:
#             'could not get {}'.format(img_file_name)
#             return False
#         img = cv2.imdecode(img_array, -1)
#         # img = Image.open(BytesIO(response.content))

#         try:
#             cv2.imwrite(img_path, img)
#         except:
#             print('could not save image')
#             return False
#         time.sleep(0.1)
#         print('{} is saved'.format(img_file_name))
#         print('this took {} seconds'.format(time.time() - start_time))
#         return True
#     else:
#         print('could not get image for {}'.format(img_file_name))
#         return False
