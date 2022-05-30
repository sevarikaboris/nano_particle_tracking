import os
import numpy as np
import scipy
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import VGG16
from PIL import Image
from scipy.io import loadmat
import time
from multiprocessing import Pool
import random
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
vgg16_model = VGG16(include_top=False, input_shape=(224, 224, 3))


#change these values
basepath = "E:/Analyzed/" #path where experiments are located
model = load_model("C:/Users/sevar/OneDrive/Documents/OneNote/OneDrive/Архив/Research/MIT Project/Microrheology/MPT - new/BorisBoris.h5") #path of used h5 model
dedrift = False
probability = 0.1 




def evaluate_table(mat_file_path):
    #print("processing: " + mat_file_path)

    if not dedrift:
        file_name = '/tracked_particles.mat'
    elif dedrift:
        file_name = '/tracked_particles_dedrift.mat'

    mat_file = loadmat(mat_file_path + file_name)
    concat_ptcl2 = mat_file['concat_ptcl'] #read the file
    
    video_folder_list = list()
    counter_fov = 1
    for videos_fov_dir in os.listdir(mat_file_path):
        if(not os.path.isdir(mat_file_path + videos_fov_dir)):
            continue
        
        number = counter_fov
        if(counter_fov == 1):
            number = 1
        elif(counter_fov == 2):
            number = 10
        else:
            number = counter_fov -1

        video_folder_list.append("fov" + str(number))
        counter_fov += 1
    #print(video_folder_list)

    #"E:\Particle Set 2\100 nm - C 1.0 - 1\fov1\fov1_0001.tif"
    
    row, col = concat_ptcl2.shape               #get rows and cols of mat_file
    table_with_result = np.zeros(shape=(row,6)) #initializing resulting table. it is faster to fill the array with zeros beforehand, than appending and copying tables
    table_with_result_index = 0                 #navigating index 



    for concat_row in concat_ptcl2:
        p = Pool()
        result = p.starmap(process_mat_file_row, [table_with_result, 
                        table_with_result_index, 
                        concat_row,
                        mat_file_path,
                        video_folder_list])
        p.close()
        p.join()   
        
        
    scipy.io.savemat(mat_file_path + 'test_mat'+'.mat',mdict={'concat_ptcl': table_with_result})

def process_mat_file_row(table_with_result, 
                        table_with_result_index, 
                        concat_row,
                        mat_file_path,
                        video_folder_list):

    if(random.random()>probability):
        for i in range(6):
            table_with_result[table_with_result_index][i] = concat_row[i]
            table_with_result[table_with_result_index][5] = 10.0
            table_with_result_index += 1
            continue

    picture_number = int(concat_row[2])
    if picture_number <10:
        number = '_000' + str(picture_number)
    elif picture_number <100:
        number = '_00' + str(picture_number)
    else:
        number = '_0' + str(picture_number)

    img2Name = basepath + mat_file_path + video_folder_list[int(concat_row[4])-1] + "/" +  video_folder_list[int(concat_row[4])-1] + number + '.tif'
    
    x = process_image(img2Name, concat_row[0], concat_row[1], 40)

    for i in range(5):
        table_with_result[table_with_result_index][i] = concat_row[i]
    table_with_result[table_with_result_index][5] = x
    table_with_result_index += 1

def process_image(img2Name, x_coord, y_coord, crop_image_size):
    img = Image.open(img2Name)
    left = x_coord-(crop_image_size/2)
    top = y_coord-(crop_image_size/2)
    right = left + crop_image_size
    bottom =top + crop_image_size
    imgSel = img.crop((left, top, right, bottom))
    imgSel = imgSel.resize((224, 224), Image.LANCZOS)
    imgSel = np.asarray(imgSel).reshape(1, 224, 224, 3)
    image = preprocess_input(imgSel)
    X_after_vgg = vgg16_model.predict(image)
    X_after_vgg.shape
    x = model.predict(X_after_vgg)
    return x

if __name__ == '__main__':

    mat_file_dirs = list()
    for experiment_dir in os.listdir(basepath):
        experiment_dir += "/"
        print("processing: " + experiment_dir)
        mat_file_dirs.append(experiment_dir)
        mat_file_dirs = basepath + experiment_dir
        evaluate_table(mat_file_dirs)

    