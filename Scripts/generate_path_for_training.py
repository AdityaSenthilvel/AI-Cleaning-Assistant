import os
import random

def gen_files(folder_path):
    here = os.getcwd()
    # this is where we are
    # iterate throught all the files
    messy = []
    tidy = []
    file_list = os.listdir(folder_path)
    random.shuffle(file_list)
    for f in file_list:
        if f.endswith('.txt'):
            f_path = os.path.join(folder_path, f)
            with open(f_path, 'r') as label_file:
                line = label_file.readline()
                if line[0] == '0':
                    tidy.append(f)
                else:
                    messy.append(f)
                    
    print('we have {} messy ones'.format(len(messy)))
    print('we have {} tidy ones'.format(len(tidy)))

    # split files into train, valid and test.
    trainw = open('train.txt', 'w')
    validw = open('valid.txt', 'w')
    testw = open('test.txt', 'w')
    n_valid = 0
    n_train = 0
    n_test = 0
    
    file_list = os.listdir(folder_path)
    random.shuffle(file_list)
    for idx, f in enumerate(file_list):
    # check file extension
        if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.jpeg'):
            if idx % 9 == 0:
                testw.write(os.path.join(folder_path, f) + '\n')
                n_test += 1
            elif idx % 7 == 0:
                validw.write(os.path.join(folder_path, f) + '\n')
                n_valid += 1
            else:
                trainw.write(os.path.join(folder_path, f) + '\n')
                n_train += 1

    print("There are {} file paths in valid.txt".format(n_valid))
    print("There are {} file paths in test.txt".format(n_test))
    print("There are {} file paths in train.txt".format(n_train))
    

    trainw.close()
    validw.close()
    testw.close()
    
    
if __name__ == '__main__':
    here = os.getcwd()
    img_folder_path = os.path.join(here, 'img')
    gen_files(img_folder_path)