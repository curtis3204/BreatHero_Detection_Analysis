from matplotlib.colors import ListedColormap
import matplotlib.ticker as mtick
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import warnings
from scipy.interpolate import make_interp_spline
from scipy import stats

# Fixing random state for reproducibility
np.random.seed(2022)

# set figure properties
fig, axes = plt.subplots(3,5)
fig.tight_layout()
fig.set_size_inches(18, 8)
plt.subplots_adjust(wspace=0.5, hspace=0.5)

# paramter class
class Param(object):
    def __init__(self, x=[]):
        self.x = x
        self.norm = {'Stiffness':[], 'Size':[], 'Weight':[], 'Speed':[],'Magnitude':[]}
Pattern = Param(x=np.array([50,100,150,200]))
Duration = Param(x=np.array([180,240,300,360]))
Intensity = Param(x=np.array([0.6,0.9,1.2,1.5]))
colors = ['#528E58', '#455173', '#BB4430']  # color GBR
fade_colors = ['#76A579', '#6D7B99', '#CC6E64'] # fade color GBR
units = ['(ms)', '(ms)', '(N)']
cols = [col for col in Duration.norm.keys()]
rows = [row for row in ['Rise Time (ms)', 'Duration (ms)', 'Amplitude (N)']]

# read data
raw = pd.read_csv('output_newton.csv')
y_aggr = np.ones(4)
for i in range(raw.shape[0]//4):
    user = raw['id'][4*i]
    prop = raw['properties'][4*i]
    param = raw['parameters'][4*i]
    data = raw[['real', 'normalize']][4*i:4*(i+1)].to_numpy()
    data = data[data[:, 0].argsort()]
    if param=='VibrationDuration':
        Duration.norm[prop].append(data[:,1])
    elif param=='VibrationIntensity':
        Intensity.norm[prop].append(data[:,1])
    elif param=='VibrationPattern':
        Pattern.norm[prop].append(data[:,1])
print("prop!!!!!!!!!!!!!!:", prop)


#########
class Proper(object):
    def __init__(self):
        self.para = {'rise_time':[], 'duration':[], 'amplitude':[]}

Stiffness = Proper()
Size = Proper()
Weight = Proper()
Speed = Proper()
Magnitude = Proper()

# raw = pd.read_csv('regress model.csv')
# print(raw)

Stiffness.para = {'rise_time':[1.915,1.04,1.765,1.69], 'duration':[0.868,0.94,1.012,1.084], 'amplitude':[0.5665,0.85,1.1335,1.417]}
Size.para = {'rise_time':[1.12,1.04,0.96,0.88], 'duration':[0.6344,0.8744,1.1144,1.3544], 'amplitude':[0.509,0.827,1.145,1.463]}
Weight.para = {'rise_time':[1.105,1.03,0.955,0.88], 'duration':[0.6701,0.8801,1.0901,1.3001], 'amplitude':[0.5622,0.8448,1.1274,1.41]}
Speed.para = {'rise_time':[1.1,1.03,0.96,0.89], 'duration':[0.795,0.915,1.035,1.155], 'amplitude':[0.5535,0.8376,1.1217,1.4058]}
Magnitude.para = {'rise_time':[1.09,1.03,0.97,0.91], 'duration':[0.757,0.907,1.057,1.207], 'amplitude':[0.5513,0.8414,1.1315,1.4216]}

print(Stiffness.para.values())
# raw = np.genfromtxt('regress model.csv', delimiter=',')

# Stiffness, Size, Weight, Speed, Magnitude = [], [], [], [], [], []
# for i, prop in enumerate([Stiffness, Size, Weight, Speed, Magnitude]):
#     for j in range(3):
#         prop[i].para[j] = raw[(i)*(j)]


def smooth(x, y):
    spl = make_interp_spline(x, y, k=2)
    x_smooth = np.linspace(x.min(), x.max(), 4) 
    y_smooth = spl(x_smooth)
    return x_smooth, y_smooth



 
# plot 
for i,param in enumerate([Pattern, Duration, Intensity]):
    # print("i:", i, "\n")

    for j,prop in enumerate(param.norm.keys()):
        case = param.norm[prop]
        x = param.x
        # print("prop:", prop)
        # print("x:",x)
        # print("case:", case)
        # print("case_len", len(case))
        
        y_aggr = 1
        index = 5*i+j
        axes[i,j].set_xlim([x.min()-(x.max()-x.min())*0.05, x.max()+(x.max()-x.min())*0.05])
        axes[i,j].set_ylim([0.2, 1.8])
        axes[i,j].xaxis.set_ticks(x)
        axes[i,j].yaxis.set_ticks([0.5,1.,1.5])
        axes[i,j].tick_params(axis='both', colors='#383838')
        axes[i,j].yaxis.set_major_formatter(mtick.PercentFormatter(1))
        axes[i,j].tick_params(axis='both', labelsize=11)
        axes[i,j].xaxis.set_ticks_position('none') 
        axes[i,j].yaxis.set_ticks_position('none') 
        label = axes[i,j].set_xlabel(units[i], color='#939393', fontsize=11, loc="right")
        axes[i,j].xaxis.set_label_coords(1.2, -0.05)
        # axes[i,j].set_ylabel(cols[j])
        # axes[i,j].set_xlabel(rows[i], color='#515151')
        axes[i,j].spines[:].set_alpha(0)
        axes[i,j].grid(axis='both', alpha=0.7, linewidth=0.5)

        a, b, c, d = [], [], [], []
        e, f, g, h = [], [], [], []

        for k in range(len(case)):
            y = case[k]
            # print("y", y)

            y_aggr *= y
            # print("y_aggr", y_aggr)
            
            xs,ys = smooth(x, y)
            axes[i,j].plot(xs, ys, '-', color=colors[i], linewidth=0.35, alpha=0.2, zorder=1)
            axes[i,j].scatter(x, y, s=2.0, color=colors[i], alpha=0.6, zorder=3)
            a.append(y[0])
            b.append(y[1])
            c.append(y[2])
            d.append(y[3])
        
        a_str_dev = np.std(a)
        b_str_dev = np.std(b)
        c_str_dev = np.std(c)
        d_str_dev = np.std(d)

        str_dev = [a_str_dev, b_str_dev, c_str_dev, d_str_dev]    

        y_avg = y_aggr**(1/len(case))

        #fill_between "Inside"
        axes[i,j].plot(xs, y_avg+str_dev, '--', color=colors[i], linewidth=0.35, alpha=1, zorder=1)
        axes[i,j].plot(xs, y_avg-str_dev, '--', color=colors[i], linewidth=0.35, alpha=1, zorder=1)
        axes[i,j].fill_between(xs, y_avg-str_dev, y_avg+str_dev, color=colors[i], alpha=0.1)

        #regression linear line
        axes[i,j].plot(xs, y_avg-str_dev, '--', color=colors[i], linewidth=0.35, alpha=1, zorder=1)


        ##fill_between "Outside"
        # axes[i,j].plot(xs, y_avg+str_dev, '--', color=colors[i], linewidth=0.35, alpha=1, zorder=1)
        # axes[i,j].fill_between(xs, y_avg+str_dev, 1.8, color=colors[i], alpha=0.085)
        # axes[i,j].plot(xs, y_avg-str_dev, '--', color=colors[i], linewidth=0.35, alpha=1, zorder=1)
        # axes[i,j].fill_between(xs, 0, y_avg-str_dev, color=colors[i], alpha=0.085)
       
        # axes[i,j].plot(xs, y_avg+str_dev, '-x', color=colors[i], linewidth=0.35, alpha=1, zorder=1)
        # axes[i,j].plot(xs, y_avg-str_dev, '-x', color=colors[i], linewidth=0.35, alpha=1, zorder=1)

        # axes[i,j].errorbar(xs, y_avg, str_dev, fmt = '', ecolor = colors[i], elinewidth = 1.5, capsize = 3, capthick = 2, alpha=0.5)

        # axes[i,j].scatter(x, y_avg+str_dev, s=5, facecolors='#FFFFFF', color=colors[i], linewidth=1.2, alpha=0.7, zorder=3)
        # axes[i,j].scatter(x, y_avg-str_dev, s=5, facecolors='#FFFFFF', color=colors[i], linewidth=1.2, alpha=0.7, zorder=3)
        # axes[i,j].fill_between(xs, y_avg-str_dev, y_avg+str_dev, color=colors[i], alpha=0.2)

        xs,ys = smooth(x, y_avg)
        # axes[i,j].plot(xs, ys, '-', color=colors[i], linewidth=1.8, alpha=1, zorder=4)
        axes[i,j].scatter(x, y_avg, s=22, facecolors='#FFFFFF', color=colors[i], linewidth=1.9, alpha=1, zorder=5)
        
        # numpy polynomial
        # z = np.polyfit(x, y_avg, 1)
        # p = np.poly1d(z)
        # slope, intercept, r, p, se = stats.linregress(x, y_avg)
        # print(z, r)
        # axes[i,j].plot(xs, p(xs), '-', color='#D58632', linewidth=1.2, alpha=1, zorder=1)


# plot label
# y_coor = [0.68, 0.365, 0.05]

for ax in axes[:,0]:
    ax.set_ylabel('Estimated Magnitudes', color='#939393', size=13)

# #Title for each column
# for ax, col in zip(axes[0], cols):
#     ax.set_title(col, color='#515151', size=23)

for i, (ax, row) in enumerate(zip(axes[:,0], rows)):
    ax.annotate(row, xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - 5, 0),
                xycoords=ax.yaxis.label, textcoords='offset points',
                size=22, ha='right', va='center', color=colors[i], rotation=90,)

# for i, (ax, row) in enumerate(zip(axes[:,2], rows)):
#     ax.set_xlabel(row, color=colors[i], size=14)
#     plt.figtext(0.5,y_coor[i], row, ha="center", va="top", fontsize=14, color=colors[i])

# save & show
plt.savefig('MagnitudeEstimation.png')
plt.show()