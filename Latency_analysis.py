import matplotlib.ticker as mtick
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import os


########################## Select Folder ################################
Folder_name = 'FullBreath_jacket/'
########################## Select Folder ################################

class Latency(object):
    def __init__(self):
        self.FireBreath_Action_Lantency = {'Inhale' : [], 'Exhale1' : [], 'Exhale2' : [], 'Exhale3' : [], 'Exhale4' : []}
        self.BoxBreath_Action_Lantency = {'Inhale' : [], 'Hold1' : [], 'Exhale' : [], 'Hold2' : []}
        self.FullBreath_Action_Lantency = {'Inhale' : [], 'Exhale' : []}

class Proper(object):
    def __init__(self):
        self.basic = {'Time' : [], 'Speed' : [], 'Flex' : [], }
        self.parameter = { 'Record' : [], 'Recordtime' : [], 'Action' : [], 'Actiontime' : []}

def selected_breath(breath):
    if breath == 'FireBreath':
        FireBreath = Latency()
        Action_Lantency = FireBreath.FireBreath_Action_Lantency
        Action_Order = 4
        print('\n', breath)
        return Action_Lantency, Action_Order, breath
    elif breath == 'BoxBreath':
        BoxBreath = Latency()
        Action_Lantency = BoxBreath.BoxBreath_Action_Lantency
        Action_Order = 3
        print('\n', breath)
        return Action_Lantency, Action_Order, breath
    elif breath == 'FullBreath':
        FullBreath = Latency()
        Action_Lantency = FullBreath.FullBreath_Action_Lantency
        Action_Order = 1
        print('\n', breath)
        return Action_Lantency, Action_Order, breath

########################## Select Breath ################################
Action_Letency, Action_Order, Breath_name = selected_breath('FullBreath')
########################## Select Breath ################################


#FireBreath_bare/  All actionsLetency (ms) =  [160.25641025641025, 136.9047619047619, 140.47619047619048, 154.76190476190476, 157.14285714285714]
#FireBreath_jacket/  All actionsLetency (ms) =  [674.3589743589743, 140.47619047619048, 205.95238095238096, 75.0, 180.95238095238093]
#BoxBreath_bare/  All actionsLetency (ms) =  [290.2777777777778, 527.7777777777778, 519.4444444444445, 1984.722222222222]
#BoxBreath_jacket/  All actionsLetency (ms) =  [927.7777777777777, 676.3888888888889, 290.2777777777778, 573.6111111111111]
#FullBreath_bare/  All actionsLetency (ms) =  [389.3939393939394, 262.12121212121207]
#FullBreath_jacket/  All actionsLetency (ms) =  [761.1111111111111, 595.8333333333334]


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


#Calculate letancy
def Calculate_letency(Action_Letency, breath):
    letency_bracket = []
    for i in range (len(list(Action_Letency))):
        temp = Action_Letency[list(Action_Letency)[i]]
        Average_letancy = (sum(temp)/len(temp))/60*1000
        letency_bracket.append(Average_letancy)
    print(breath, ' All actionsLetency (ms) = ', letency_bracket)
    return letency_bracket



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



for file in range(0,len(csv_files)):
    order = Action_Order
    Actiontime = globals()['File'+str(file)].parameter['Actiontime']
    Recordtime = globals()['File'+str(file)].parameter['Recordtime']
    if (order == 0):
        continue
    else:
        for i in reversed(range(len(Actiontime))):
            for j in reversed(range(len(Recordtime))):
                if (Actiontime[i] > Recordtime[j]):
                    letency = Actiontime[i] - Recordtime[j]
                    temp_list = list(Action_Letency)
                    Action_Letency[temp_list[order]].append(letency)
                    order = order - 1
                    break
                elif ( i == 0 and Actiontime[0] < Recordtime[0]):
                    letency = 0
                    temp_list = list(Action_Letency)
                    Action_Letency[temp_list[order]].append(letency)
                    order = order - 1
                    break

print('\nAction_Letency : ', Action_Letency)
Calculate_letency(Action_Letency, Folder_name)





