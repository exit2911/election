#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 20:40:57 2019

@author: VyHo
"""

import pandas as pd
import numpy as np
from csv import reader
import matplotlib.pyplot as plt


cand_header = [r for r in reader(open('/Users/VyHo/Downloads/random_hackery-master/data/cn_header_file.csv','r'))]

cand_header

candidates = pd.read_csv('/Users/VyHo/Downloads/random_hackery-master/data/cn.txt', names = cand_header[0], sep = '|')

candidates.head()

candidates['CAND_NAME']

candidates['CAND_ELECTION_YR'] == 2016

#calling a table with selected columns and rows

candidates[candidates['CAND_ELECTION_YR'] == 2016 ][['CAND_ID','CAND_NAME']].head()

#checking the size

candidates.loc[6940:]

#showing the 3rd row

candidates.iloc[2]

candidates.dtypes

#search though rows

candidates[candidates['CAND_NAME'] == 'TRUMP, DONALD']

#cannot index with vectors contain null

candidates[candidates['CAND_NAME'].str.contains('TRUMPS')]

trump_table = candidates[candidates['CAND_NAME'].notnull() & candidates['CAND_NAME'].str.contains('TRUMP')]

donations_header = [r for r in reader(open('/Users/VyHo/Downloads/random_hackery-master/data/indiv_header_file.csv', 'r'))]

#calling first row

donations_header[0]

donations = pd.read_csv('data')

donations = pd.read_csv('/Users/VyHo/Downloads/random_hackery-master/data/itpas2.txt', names = donations_header[0], sep = '|')

donations.dtypes

donations.describe()

donations['TRANSACTION_AMT'].mean()

donations['TRANSACTION_AMT'].min()

donations['TRANSACTION_AMT'].max()

donations['TRANSACTION_AMT'].median()

plt.hist(donations['TRANSACTION_AMT'])

#check the candidates with political commitee 

candidates[candidates['CAND_PCC'].notnull()].shape

#donations.set_index('CMTE_ID').join(candidates.set_index('CAND_PCC'))

#donations.set_index('CMTE_ID').join(candidates.set_index('CAND_PCC'),how = 'right')
#we want to see candidates that donated, hence use inner join
cand_donations = donations.set_index('CMTE_ID').join(candidates.set_index('CAND_PCC'),how = 'inner')

cand_donations.describe()
cand_donations['TRANSACTION_AMT'].max()
#check rows with donations greater than 1M
#not working because the join is not returning any values
cand_donations[cand_donations['TRANSACTION_AMT'] > 1000000]['CAND_NAME'].values_counts() 

cand_donations[cand_donations['TRANSACTION_AMT']< 200]['CAND_NAME'].value_counts()

cand_donations.columns
#inserting the boolean series 
cand_donations = cand_donations[cand_donations['CAND_ELECTION_YR']==2016]

grouped = cand_donations.groupby('CAND_NAME')

grouped.sum()

#sum and aggregate
#aggregate and find sum and mean and count the # of timesthe candidates donated
#set() to create a set
grouped.agg({'TRANSACTION_AMT': [np.sum, np.mean], 'NAME': lambda x:len(set(x))})

#modify data based on a groupby

cand_donations['unique_donors'] = cand_donations.groupby('CAND_NAME')['NAME'].transform(lambda x: len(set(x)))

cand_donations['unique_donors']

sign_cand_donations = cand_donations[cand_donations['unique_donors'] > cand_donations['unique_donors'].mean()]

sign_cand_donations.shape

sign_cand_donations.groupby('CAND_NAME').sum()

cand_donations[cand_donations['CAND_NAME'].str.contains('TRUMP')]['unique_donors']

cand_donations[cand_donations['CAND_NAME'].str.contains('TRUMP')].describe()

sign_cand_donations = sign_cand_donations.append(cand_donations[cand_donations['CAND_NAME'].str.contains('TRUMP')])

sign_cand_donations.groupby('CAND_NAME').sum()['TRANSACTION_AMT']

sign_cand_donations.groupby('CAND_NAME').min()['unique_donors'].sort_values()
