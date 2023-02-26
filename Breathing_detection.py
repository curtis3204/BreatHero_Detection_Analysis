import matplotlib.ticker as mtick
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import os
from scipy import stats
from scipy.interpolate import make_interp_spline


fig, ax1 = plt.subplots()
fig.set_size_inches(18, 8)
# fig.tight_layout()
ax2 = ax1.twinx()

class Proper(object):
    def __init__(self):
        self.basic = {'Time' : [], 'Speed' : [], 'Flex' : [], }
        self.parameter = { 'Record' : [], 'Recordtime' : [], 'Action' : [], 'Actiontime' : []}



##################################
Folder_name = 'BoxBreath_jacket/'
##################################
num = 0

x_lim = 25

#BoxBreath_bare 5 25
#BoxBreath_jacket 0 25
#FireBreath_jacket 1 12
#FireBreath_bare 8 12
#FullBreath_bare 10 17
#FullBreath_jacket 3 17


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



#False Analysis
def False_Calcuate(object, breath):
    if (breath == 'FireBreath'):
        false_number = abs(len(object.parameter['Record']) - 5)
        return false_number
    elif (breath == 'BoxBreath'):
        false_number = abs(len(object.parameter['Record']) - 4)
        return false_number
    elif (breath == 'FullBreath'):
        false_number = abs(len(object.parameter['Record']) - 2)
        return false_number



#Smooth Process
def smooth(x, y):
    spl = make_interp_spline(x, y, k=2)
    x_smooth = np.linspace(x.min(), x.max(), 200) 
    y_smooth = spl(x_smooth)
    return x_smooth, y_smooth


#################### Main ######################

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


#Accuracy Analysis
false_total = 0
for i in range(0,len(csv_files)):
    false_total = false_total + False_Calcuate(globals()['File'+str(i)], 'BoxBreath')

print('\nfalse_total: ', false_total)
accuracy_num = ((4 * len(csv_files))-false_total) / (4 * len(csv_files))
print('accuracy_num: ',Folder_name, accuracy_num)
print('\n')


# for i in range(0,len(csv_files)):
#     #Plot All Files' Figure in background
#     ax1_x = np.arange(0,len(globals()['File'+str(i)].basic['Flex']))
#     ax1_x = ax1_x/60
#     ax1_y = globals()['File'+str(i)].basic['Flex']
#     s_ax1, s_ay1 = smooth(ax1_x, ax1_y)
#     ax1.plot(s_ax1, s_ay1, color='tab:blue', alpha=0.15, linewidth=0.55)

#     ax2_x = np.arange(0, len(globals()['File'+str(i)].basic['Speed']))
#     ax2_x = ax2_x/60
#     ax2_y = globals()['File'+str(i)].basic['Speed']
#     s_ax2, s_ay2 = smooth(ax2_x, ax2_y)
#     ax2.plot(s_ax2, s_ay2, color='tab:orange', alpha=0.15,linewidth=0.55)

##Plot Single Figure
#################### 10 11

selected_object = globals()['File'+str(num)]
####################

ax1_x = np.arange(0,len(selected_object.basic['Flex']))
ax1_x = ax1_x/60
ax1_y = selected_object.basic['Flex']
s_ax1, s_ay1 = smooth(ax1_x, ax1_y)
ax1.plot(s_ax1, s_ay1, color='tab:blue', alpha=0.85, linewidth=2)

ax2_x = np.arange(0, len(selected_object.basic['Speed']))
ax2_x = ax2_x/60
ax2_y = selected_object.basic['Speed']
s_ax2, s_ay2 = smooth(ax2_x, ax2_y)
ax2.plot(s_ax2, s_ay2, color='tab:orange', alpha=0.85,linewidth=2)



# ax1.set_xlabel('Time', fontsize=30, color='tab:gray')
ax1.tick_params(axis='x', labelsize=25, labelcolor='tab:gray')

#Plot Flex
# ax1.set_ylabel('flex_sensor (Ω)', color='#80C8E8', fontsize = 35, alpha=0.85)
ax1.tick_params(axis='y', labelsize=30, labelcolor='#80C8E8')
ax1.set_ylim(10000, 15000)
ax1.set_xlim(0, x_lim)

#Plot Speed
# ax2.set_ylabel('speed_sensor', color='#F7B081', fontsize = 35, alpha=0.85)
ax2.tick_params(axis='y', labelsize=30, labelcolor='#F7B081')
ax2.set_ylim(0, 30)


#Action / Record Vertical Line
for i in range(len(selected_object.parameter['Actiontime'])):
    ax1.vlines(selected_object.parameter['Actiontime'][i]/60, ymin = 10000, ymax = 15000, 
            color = 'red', linestyles='dashed', alpha=0.65, linewidth=3.5)

for i in range(len(selected_object.parameter['Recordtime'])):
    ax1.vlines(selected_object.parameter['Recordtime'][i]/60, ymin = 10000, ymax = 15000, 
            color = 'green', linestyles='dashed', alpha=0.65, linewidth=3.5)


ax1.spines[:].set_alpha(0.2)
ax2.spines[:].set_alpha(0.2)

Figure_name = (csv_files[num].split('\\')[1]).split('.')[0]

save_name = str(str(Figure_name)+'_'+Folder_name.split('_')[1].split('/')[0])

plt.title(save_name, fontsize = 20, pad = 10)
plt.savefig(Folder_name+save_name+'.png')

    
# plt.show()


#FireBreath_bare/ 0.8571428571428571
#FireBreath_jacket/ 0.7142857142857143
#BoxBreath_bare/ 0.9791666666666666
#BoxBreath_jacket/ 1.0
#FullBreath_bare/ 1.0
#FullBreath_jacket/ 0.9583333333333334
