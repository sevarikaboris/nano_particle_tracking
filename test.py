
from email.mime import base
import math
import os
from turtle import left, right
import numpy as np
from scipy.io import loadmat
from PIL import Image
import tables
from scipy.io import loadmat

def transpose_matrix(matrix):
    return list(map(list, zip(*matrix)))

#for root, dirs, files in os.walk("C:/Users/Jerome's Laptop/Desktop/Hauptordner", topdown=False):
#   for name in files:
#      print(os.path.join(root, name))
#   for name in dirs:
#      print(os.path.join(root, name))



#for root, dirs, files in os.walk("C:/Users/Jerome's Laptop/Desktop/Hauptordner", topdown=False):
#    print(dirs)
#    dir_list = dirs

#print("files:")
#print(dir_list)

#result = len(os.listdir("C:/Users/Jerome's Laptop/Desktop/Hauptordner"))
#print(result)

#file = tables.open_file('tracked_particles_dedrift.mat')
file = loadmat('tracked_particles_dedrift.mat')
lists = file['concat_ptcl2']
#print(lists)
#print(lists[4])
tr = list(map(list, zip(*lists)))
fov_index_list = list() #fov_index_list[video_nr][i] = index

min_of_series = int(min(tr[4]))
max_of_series = int(max(tr[4]))
fov_index_list = [[] for y in range(max_of_series)]

for index, value in enumerate(tr[4]):
    fov_index_list[int(value)-1].append(index)
#print(fov_index_list)

#print(fov_index_list[9])
#print(max(tr[4]))

for fovs in fov_index_list:
    FOV = list()
    for index in fovs:
        FOV.append(lists[index])

    FOV = list(map(list, zip(*FOV)))
    bevor = 1
    for particleid in FOV[3]:
        if(bevor != particleid):
            print(particleid)
            bevor = particleid

#for fov in range(int(min(tr[4])),int(max(tr[4])+1)): #fov zelle mit partikel
#    print(fov)

indices = tr[4].index(1)
#print(indices)
