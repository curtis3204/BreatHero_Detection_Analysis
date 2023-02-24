import matplotlib.ticker as mtick
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import os


##################################
Folder_name = 'FireBreath_bare/'
##################################


class Proper(object):
    def __init__(self):
        self.basic = {'Time' : [], 'Speed' : [], 'Flex' : [], }
        self.parameter = { 'Record' : [], 'Recordtime' : [], 'Action' : [], 'Actiontime' : []}


class Latency(object):
    def __init__(self):
        self.FireBreath_Action_Lantency = {'Inhale' : [], 'Exhale1' : [], 'Exhale2' : [], 'Exhale3' : [], 'Exhale4' : []}
        self.BoxBreath_Action_Lantency = {'Inhale' : [], 'Hold1' : [], 'Exhale' : [], 'Hold2' : []}
        self.FullBreath_Action_Lantency = {'Inhale' : [], 'Exhale' : []}


FireBreath = Latency()
BoxBreath = Latency()
FullBreath = Latency()


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

#Initiate Properties
def Init_all_Properties(object, raw):
    count = 0
    for i in range(len(raw['time'])):
        object.basic['Time'].append(raw['time'][i])
        object.basic['Flex'].append(raw['flex_sensor'][i])
        object.basic['Speed'].append(raw['speed_sensor'][i])

        if(raw['action_time'][i] != 'None' or raw['record_time'][i] == 'Yes'):
            if (raw['action_time'][i] != 'None'):
                object.parameter['Action'].append(raw['action_time'][i])
                object.parameter['Actiontime'].append(count)
            if (raw['record_time'][i] == 'Yes'):
                object.parameter['Record'].append(raw['record_time'][i])
                object.parameter['Recordtime'].append(count)
            count = count + 1
        else:
            count = count + 1
    print(object.parameter['Action'])
    print(object.parameter['Actiontime'])
    print(object.parameter['Record'])
    print(object.parameter['Recordtime'])

#Declare Objects
csv_files = Read_Files()
for i in range(0,len(csv_files)):
    globals()['File'+str(i)] = Proper()
    print('File'+str(i), ' = ', csv_files[i])

#Initiate Objects
for i in range(0,len(csv_files)):
    globals()['raw'+str(i)] = Read_csv(csv_files[i])
    print('\n''File'+str(i), ' : ')
    Init_all_Properties(globals()['File'+str(i)], globals()['raw'+str(i)])



for files in range(0,len(csv_files)):
    for i in reversed(range(len(globals()['File'+str(i)]['Actiontime']))):
        if (globals()['File'+str(i)]['Actiontime'][i] < globals()['File'+str(i)]['Recordtime'][i]):
            FireBreath.FireBreath_Action_Lantency['Inhale'][i] = (globals()['File'+str(i)]['Actiontime'][i] - globals()['File'+str(i)]['Recordtime'][i])
            

