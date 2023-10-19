from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import seaborn as sns
import numpy as np
import pandas as pd

#highlevel
df_high_level = pd.read_csv('/Users/nikonagengast/Desktop/weights/high_level.csv', index_col=0)
df_high_level = df_high_level.iloc[:,:3]

#mechanical
df_mechanical = pd.read_csv('/Users/nikonagengast/Desktop/weights/mechanical.csv', index_col=0)
df_mechanical = df_mechanical.iloc[:,:2]

#ecological
df_ecological= pd.read_csv('/Users/nikonagengast/Desktop/weights/ecology.csv', index_col=0)
df_ecological = df_ecological.iloc[:,:3]

#process
df_process= pd.read_csv('/Users/nikonagengast/Desktop/weights/process.csv', index_col=0)
df_process = df_process.iloc[:,:3]

#mechanical_0_degree
df_0_degree= pd.read_csv('/Users/nikonagengast/Desktop/weights/mechanical_0.csv', index_col=0)
df_0_degree = df_0_degree.iloc[:,:3]

#mechanical_90_degree
df_90_degree= pd.read_csv('/Users/nikonagengast/Desktop/weights/mechanical_90.csv', index_col=0)
df_90_degree = df_90_degree.iloc[:,:3]


ldf = [df_high_level, df_mechanical, df_0_degree, df_process, df_ecological, df_90_degree]
ldf_names = ['high_level', 'mechanical','mechanical_0' , 'process', 'ecology', 'mechanical_90']



lognorm = LogNorm(vmin=1.0 / 9.0, vmax=9.0)

fig, axs = plt.subplots(ncols=3, nrows=2, figsize=(12,4))

for i, e in enumerate(ldf):
    if i<3:
        print(i)
        axs[0,i]=sns.heatmap(e, annot=True, mask=e < 1 / 11, linewidths=.5,
                    norm=lognorm, cbar=None,
                    xticklabels=list(e.columns), yticklabels=list(e.columns), ax=axs[0,i])
        axs[0,i].set_title(ldf_names[i])
    else:
        axs[1, i-3] = sns.heatmap(e, annot=True, mask=e < 1 / 11, linewidths=.5,
                                norm=lognorm, cbar=None,
                                xticklabels=list(e.columns), yticklabels=list(e.columns), ax=axs[1,i-3])
        axs[1, i-3].set_title(ldf_names[i])

plt.tight_layout()
plt.subplots_adjust(hspace=1, wspace=0.6)
plt.show()