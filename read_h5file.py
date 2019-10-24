import h5py

f = 'C:/share_VM/work/Project_PPI/model_weights.h5'
file = h5py.File(f,'r')
for key in file.keys():
    for value in file[key]:
        print(value)
 # print(file[key].name)
 # print(file[key].shape)
 # print(file[key].value)