#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from genericpath import exists
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

from itertools import product


# In[ ]:


plt.rcParams.update({'font.size': 40, 'font.weight': 'bold'})
os.makedirs('Results', exist_ok = True)
os.makedirs('Results/1a', exist_ok = True)
os.makedirs('Results/1b', exist_ok = True)

# In[ ]:


def plot_multiple_complete_graphs(data, y_axis_label_data, matrix_size):
    title = f'Plot for Matrix Size {matrix_size} and Different Block Sizes'
    indexes = list(product(range(5), range(4)))
    length_i = len(indexes)
    fig, ax = plt.subplots(5, 4, sharex=True, figsize=(25, 25))
    last_value = None
    for a in fig.axes:
        a.tick_params( axis='x', which='both', bottom=True, top=False, labelbottom=True)    
    for index, label_name in enumerate(y_axis_label_data):
        index_pair = indexes[index]
        b = sns.barplot(data = data, x = "type", y = label_name, hue = "block_size",
                    ax = ax[index_pair[0], index_pair[1]], log=True)
        b.set_ylabel(label_name.split(':')[0], fontweight='bold')
        b.set_xlabel('')
        b.set_xticklabels(['ijk', 'ikj', 'kij'])
        b.get_legend().set_visible(False)
#         for container in b.containers:
#             b.bar_label(container)
        last_value = index
    for index in range(last_value+1, length_i):
        index_pair = indexes[index]
        ax[index_pair[0], index_pair[1]].axis('off')
    fig.text(0.5, 0.01, 'Loop Variant Type', ha='center', fontsize=30, fontweight='bold')
    plt.suptitle(title, fontsize=40)
    lines_labels = [fig.axes[0].get_legend_handles_labels()]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
    fig.legend(lines, labels, title='block sizes')
    plt.tight_layout()
    plt.show()


# In[ ]:


def save_multiple_complete_graphs(data, y_axis_label_data, matrix_size):
    title = f'Plot for Matrix Size {matrix_size} and Different Block Sizes'
    for index, label_name in enumerate(y_axis_label_data):
        sns.set(rc={'figure.figsize': (8,5)})
        b = sns.barplot(data = data, x = "type", y = label_name, hue = "block_size", log=True)
        b.set_ylabel(label_name.split(':')[0], fontweight='bold')
        file_name_to_save = f"{matrix_size}-{label_name.split(':')[0]}.png"
        path = os.path.join('Results/1b', file_name_to_save)
        b.set_xlabel('')
        b.set_xticklabels(['ijk', 'ikj', 'kij'])
        plt.title(title, fontweight='bold')
        plt.xlabel('Loop Variant Type', fontweight='bold')
        b.figure.savefig(path)
        plt.close()


# In[ ]:


def calculate_percent(data, df):
    misses_percent_columns = ['L1-dcache-load-misses-percent', 'LLC-loads-misses-percent',
                              'LLC-stores-misses-percent', 'dTLB-loads-misses-percent',
                              'dTLB-store-misses-percent']
    
    results = []
    for column in misses_percent_columns:
        results.append(100*data[column]/np.sum(df[column]))
    return results


# In[ ]:


def save_complete_graph(data_p, y_axis_label_data, matrix_size, block_size):
    old_data = data_p.copy(deep=True)
#     new_column_names = ['L1-dcache-load-misses-relative-percent',
#                         'LLC-loads-misses-relative-percent',
#                         'LLC-stores-misses-relative-percent',
#                         'dTLB-loads-misses-relative-percent',
#                         'dTLB-store-misses-relative-percent']
#     values = old_data.apply(lambda x: calculate_percent(x, old_data), axis=1)
#     relative_percent = pd.DataFrame(values.tolist(), columns = new_column_names)
    old_data.index = list(range(old_data.shape[0]))
#     relative_percent.index = list(range(relative_percent.shape[0]))
    data = old_data
#     pd.concat([old_data, relative_percent], axis=1)
    title = f'Plot for Matrix Size {matrix_size} and Block Size {block_size}'
    iter_label_data = y_axis_label_data
#     + new_column_names
    for index, label_name in enumerate(iter_label_data):
        sns.set(rc={'figure.figsize': (8, 5)})
        b = sns.barplot(data = data, x = "type", y = label_name, log=True)
        b.set_ylabel(label_name.split(':')[0], fontweight='bold')
        file_name_to_save = f"{matrix_size}-{block_size}-{label_name.split(':')[0]}.png"
        path = os.path.join('Results/1a', file_name_to_save)
        for container in b.containers:
            b.bar_label(container)
        b.set_xlabel('')
        b.set_xticklabels(['ijk', 'ikj', 'kij'])
        plt.xlabel('Loop Variant Type', fontweight='bold')
        plt.title(title, fontweight='bold')
        b.figure.savefig(path)
        plt.close()


# In[ ]:


def plot_complete_graph(data, y_axis_label_data, matrix_size, block_size):
    title = f'Plot for Matrix Size {matrix_size} and Block Size {block_size}'
    indexes = list(product(range(5), range(4)))
    length_i = len(indexes)
    fig, ax = plt.subplots(nrows=5, ncols=4, sharex=True, figsize=(25, 25))
    last_value = None
    for a in fig.axes:
        a.tick_params( axis='x', which='both', bottom=True, top=False, labelbottom=True)    
    for index, label_name in enumerate(y_axis_label_data):
        index_pair = indexes[index]
        b = sns.barplot(data = data, x = "type", y = label_name,
                    ax = ax[index_pair[0], index_pair[1]], log=True)
        b.set_ylabel(label_name.split(':')[0], fontweight='bold')
        b.set_xlabel('')
        b.set_xticklabels(['ijk', 'ikj', 'kij'])
#         for container in b.containers:
#             b.bar_label(container)
        last_value = index
    for index in range(last_value+1, length_i):
        index_pair = indexes[index]
        ax[index_pair[0], index_pair[1]].axis('off')
    fig.text(0.5, 0.01, 'Loop Variant Type', ha='center', fontsize=30, fontweight='bold')
    plt.suptitle(title, fontsize=40)
    plt.tight_layout()
    plt.show()


# In[ ]:


# def plot_complete_graph(data, y_axis_label_data, matrix_size, block_size):
#     title = f'Plot for Matrix Size {matrix_size} and Block Size {block_size}'
#     plt.figure(figsize=(25, 25))
#     plots_data = []
#     x_data = list(data['type'])
#     indexes = list(product(range(5), range(5)))
#     for index, label_name in enumerate(y_axis_label_data):
#         pair_index = indexes[index]
#         log_value = False
#         y_data = list(data[label_name])
#         if max(y_data) > 2000:
#             log_value = True
#         ax = plt.subplot2grid((5,5), pair_index)
#         ax.bar(x_data, y_data, log=log_value)
#         ax.set_ylabel(label_name.split(':')[0], fontweight='bold')
# #         ax.yaxis.label.set_size(15)
#         plots_data.append(ax)
#     plt.suptitle(title, fontsize=50)
#     fig.text(0.5, 0.01, 'Loop Variant Type', ha='center', fontsize=50, fontweight='bold')
#     plt.tight_layout()
#     plt.show()


# In[ ]:


final_data = pd.DataFrame()
for file in os.listdir('.'):
    if file.endswith('.log'):
        file_stats_data = file.split('_')
        n, block_size = int(file_stats_data[1]), int(file_stats_data[2])
        data = open(file).read()
        req_data = [x for x in data.strip().split('\n') if x != '']
        df_data  = {}
        for temp_data in req_data[1:]:
            number, column_name, *waste = temp_data.strip().split()
            number = number.replace(',', '')
            if column_name == 'seconds':
                column_name = 'time'
            df_data[column_name] = [number]
        temp_data = pd.DataFrame.from_dict(df_data)
        temp_data['matrix_size'] = n
        temp_data['block_size'] = block_size
        if file.startswith('ijk'):
            temp_data['type'] = 'ijk'
        if file.startswith('ikj'):
            temp_data['type'] = 'ikj'
        if file.startswith('kij'):
            temp_data['type'] = 'kij'
        final_data = final_data.append(temp_data, ignore_index=True)


# In[ ]:


column_data = final_data.columns
datatype_info = dict([(column_name, 'int') for column_name in column_data[:-1]]+ [('time', 'float64')])
final_data = final_data.astype(datatype_info)
group_by_columns = ['matrix_size', 'block_size', 'type']
agg_data = {key: 'mean' for key in final_data.columns[:-1]}
new_data = final_data.groupby(group_by_columns, as_index=False).agg(agg_data)
new_data = new_data.astype(datatype_info)


# In[ ]:


new_data['L1-dcache-load-misses-percent'] = 100*new_data['L1-dcache-load-misses']/new_data['L1-dcache-loads']
new_data['LLC-loads-misses-percent'] = 100*new_data['LLC-load-misses']/new_data['LLC-loads']
new_data['LLC-stores-misses-percent'] = 100*new_data['LLC-store-misses']/new_data['LLC-stores']
new_data['dTLB-loads-misses-percent'] = 100*new_data['dTLB-load-misses']/new_data['dTLB-loads']
new_data['dTLB-store-misses-percent'] = 100*new_data['dTLB-store-misses']/new_data['dTLB-stores']
new_data['avg-misses-percent'] = (new_data['L1-dcache-load-misses-percent'] + new_data['LLC-loads-misses-percent'] + new_data['LLC-stores-misses-percent'] + new_data['dTLB-loads-misses-percent'] + new_data['dTLB-store-misses-percent'])/5

# In[ ]:


useless_columns = ['cache-misses', 'cache-references', 'instructions', 
                  'L1-icache-load-misses', 'L1-dcache-stores']


# In[ ]:


new_data.drop(columns = useless_columns, inplace=True)
columns_data = list(new_data.columns)
columns_data.remove('matrix_size')
columns_data.remove('block_size')
columns_data += ['matrix_size', 'block_size']
new_data = new_data[columns_data]


# In[ ]:


new_data.to_csv('final_data.csv', sep=',',index=False)


# In[ ]:


matrix_sizes = [2048, 8192]
block_sizes = [32]
for matrix_size, block_size in product(matrix_sizes, block_sizes):
    plot_data = new_data[(new_data['matrix_size']==matrix_size)&(new_data['block_size']==block_size)]
    label_values = list(plot_data.columns[1:-2])
    save_complete_graph(plot_data, label_values, matrix_size, block_size)


# In[ ]:


for matrix_size in matrix_sizes:
    plot_data = new_data[(new_data['matrix_size'] == matrix_size)]
    label_values = list(plot_data.columns[1:-2])
    save_multiple_complete_graphs(plot_data, label_values, matrix_size)


# In[ ]:


# matrix_sizes = [2048, 8192]
# block_sizes = [32]
# for matrix_size, block_size in product(matrix_sizes, block_sizes):
#     plot_data = new_data[(new_data['matrix_size']==matrix_size)&(new_data['block_size']==block_size)]
#     label_values = list(plot_data.columns[1:-2])
#     plot_complete_graph(plot_data, label_values, matrix_size, block_size)


# In[ ]:


# for matrix_size in matrix_sizes:
#     plot_data = new_data[(new_data['matrix_size'] == matrix_size)]
#     label_values = list(plot_data.columns[1:-2])
#     plot_multiple_complete_graphs(plot_data, label_values, matrix_size)


# In[ ]:




