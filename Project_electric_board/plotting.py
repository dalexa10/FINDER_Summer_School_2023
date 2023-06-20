import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import os

# Recall to generate your own data before running this script
database_name = 'database_4.pkl'


try:
    with open('results/' + database_name, 'rb') as inp:
        ml_data = pickle.load(inp)
except NameError:
    print('No files found')

# Dataframe importing
data_df = pd.DataFrame.from_dict(ml_data, orient='index')
data_df_True = data_df[data_df['status'] == True]
data_df_False = data_df[data_df['status'] == False]


# Histogram plotting section
fig, ax = plt.subplots(2, 2)
ax[0, 0].hist(data_df_True['area'], bins=30, edgecolor='black')
ax[0, 0].set_xlabel('Area')
ax[0, 0].set_ylabel('Samples')
ax[0, 0].set_title('Area - Circuit Works')


ax[0, 1].hist(data_df_False['area'], bins=30, edgecolor='black')
ax[0, 1].set_xlabel('Area')
ax[0, 1].set_ylabel('Samples')
ax[0, 1].set_title('Area - Circuit Fails')


ax[1, 0].hist(data_df_True['perim'], bins=30, edgecolor='black')
ax[1, 0].set_xlabel('Perimeter')
ax[1, 0].set_ylabel('Samples')
ax[1, 0].set_title('Perimeter - Circuit Works')


ax[1, 1].hist(data_df_False['perim'], bins=30, edgecolor='black')
ax[1, 1].set_xlabel('Perimeter')
ax[1, 1].set_ylabel('Samples')
ax[1, 1].set_title('Perimeter - Circuit Fails')

plt.tight_layout()
plt.show()

# Second histogram plots
# Histogram plotting section
fig, ax = plt.subplots(1, 2)
ax[0].hist(data_df_False['area'], bins=30, edgecolor='black', alpha=0.3, label='Fails')
ax[0].hist(data_df_True['area'], bins=30, edgecolor='black', alpha=0.5, label='Works')
ax[0].set_xlabel('Area')
ax[0].set_ylabel('Samples')
ax[0].set_title('Area Histogram')
ax[0].legend(loc='best')


ax[1].hist(data_df_False['perim'], bins=30, edgecolor='black', alpha=0.3, label='Fails')
ax[1].hist(data_df_True['perim'], bins=30, edgecolor='black', alpha=0.5, label='Works')
ax[1].set_xlabel('Perimeter')
ax[1].set_ylabel('Samples')
ax[1].set_title('Perimeter Histogram')
ax[1].legend(loc='best')

plt.tight_layout()
plt.show()


# # Scatter plots
fig, ax = plt.subplots(2, 3)
ax[0, 0].scatter(data_df_True['l_LD'], data_df_True['l_LC'], c='g', alpha=0.5)
ax[0, 0].scatter(data_df_False['l_LD'], data_df_False['l_LC'], c='r', alpha=0.05)
ax[0, 0].set_xlabel('Distance LD')
ax[0, 0].set_ylabel('Distance LC')

ax[0, 1].scatter(data_df_True['l_LD'], data_df_True['l_LS'], c='g', alpha=0.5)
ax[0, 1].scatter(data_df_False['l_LD'], data_df_False['l_LS'], c='r', alpha=0.05)
ax[0, 1].set_xlabel('Distance LD')
ax[0, 1].set_ylabel('Distance LS')

ax[0, 2].scatter(data_df_True['l_LD'], data_df_True['l_DC'], c='g', alpha=0.5)
ax[0, 2].scatter(data_df_False['l_LD'], data_df_False['l_DC'], c='r', alpha=0.05)
ax[0, 2].set_xlabel('Distance LD')
ax[0, 2].set_ylabel('Distance DC')


ax[1, 0].scatter(data_df_True['l_LC'], data_df_True['l_LS'], c='g', alpha=0.5)
ax[1, 0].scatter(data_df_False['l_LC'], data_df_False['l_LS'], c='r', alpha=0.05)
ax[1, 0].set_xlabel('Distance LC')
ax[1, 0].set_ylabel('Distance LS')

ax[1, 1].scatter(data_df_True['l_DC'], data_df_True['l_DS'], c='g', alpha=0.5)
ax[1, 1].scatter(data_df_False['l_DC'], data_df_False['l_DS'], c='r', alpha=0.05)
ax[1, 1].set_xlabel('Distance DC')
ax[1, 1].set_ylabel('Distance DS')

ax[1, 2].scatter(data_df_True['l_DS'], data_df_True['l_CS'], c='g', alpha=0.5, label='Works')
ax[1, 2].scatter(data_df_False['l_DS'], data_df_False['l_CS'], c='r', alpha=0.05, label='Fails')
ax[1, 2].set_xlabel('Distance LD')
ax[1, 2].set_ylabel('Distance LC')
ax[1, 2].legend(loc='best')
plt.tight_layout()


# PLot correlation matrix



#
# fig, ax = plt.subplots()

# for i in range(len(ml_data)):
#     if ml_data[i]['status'] is True:
#         c = 'b'
#     else:
#         c = 'r'
#     ax.scatter(ml_data[i]['rel_dist']['l_LD'], ml_data[i]['rel_dist']['l_LC'], c=c)
#
# [ax.scatter(ml_data[i]['rel_dist']['l_LD'], ml_data[i]['rel_dist']['l_LC']) for i in range(len(ml_data))]
