import matplotlib.ticker as mtick
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import os


##################################
Folder_name = 'FullBreath_bare/'
##################################


class Proper(object):
    def __init__(self):
        self.basic = {'Time' : [], 'Speed' : [], 'Flex' : [], }
        self.parameter = { 'Record' : [], 'Recordtime' : [], 'Action' : [], 'Actiontime' : []}


#Read Files
def Read_Files():
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(Folder_name, "*.csv"))
    print(' \nGet', len(csv_files)  ,'files')
    return csv_files


#Read csv
def Read_csv(path):
    raw = pd.read_csv(path)
    return raw



#Declare Objects
csv_files = Read_Files()
for i in range(0,len(csv_files)):
    raw = Read_csv(csv_files[i])
    print(csv_files[i])
    bool = raw['flex_sensor'].isnull()
    for i in range(len(raw['flex_sensor'])):
        if bool[i] == True:
            print(i)




# for i in range(0,len(csv_files)):
#     globals()['File'+str(i)] = Proper()
#     print('File'+str(i), ' = ', csv_files[i])