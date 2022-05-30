import numpy as np
import pandas as pd
import random

# reading the data
interactions = pd.read_csv('all-interactions-no-false-data.csv')
sorted = interactions.sort_values(by=['user_id'], ascending = True)


# preprocessing interactions
sizes = ['S', 'M', 'L', 'XL', 'XXL']
sorted['percentage_1'] = sorted['percentage_1'].str.rstrip('%').astype('float') / 100.0
sorted['percentage_2'] = sorted['percentage_2'].str.rstrip('%').astype('float') / 100.0
sorted['size_3'] = sorted['size_2']

for i, row in sorted.iterrows():
    size = random.choice([x for x in range(len(sizes))])
    while (sizes[size] == sorted.iloc[i,5] or sizes[size] == sorted.iloc[i,7]):
        size = random.choice([x for x in range(len(sizes))])
    sorted.iloc[i,9] = sizes[size]

sorted['percentage_3'] = 1- sorted['percentage_1']
sorted['m_product_id_1'] = sorted['product_id'].astype('string') + '_' + sorted['size_1']
sorted['m_product_id_2'] = sorted['product_id'].astype('string') + '_' + sorted['size_2']
sorted['m_product_id_3'] = sorted['product_id'].astype('string') + '_' + sorted['size_3']


# creating a new df for interactions
m_interactions = pd.DataFrame(columns=['user_id', 'product_id', 'rating'], index=np.arange(len(sorted)))
m_interactions.fillna(0, inplace=True)


i = 0
count = 0
id = ''
for interaction in sorted.iterrows():
    user_id = interaction[1]['user_id'] 
    if id == user_id :
        count += 1
    else:
        id = user_id
        count = 0
    
    if count == 0:
        product_id = interaction[1]['m_product_id_1']
        rating = interaction[1]['percentage_1']
        m_interactions.iloc[i, 0] = user_id
        m_interactions.iloc[i, 1] = product_id
        m_interactions.iloc[i, 2] = rating

    elif count == 1:
        product_id = interaction[1]['m_product_id_3']
        rating = interaction[1]['percentage_3']
        m_interactions.iloc[i, 0] = user_id
        m_interactions.iloc[i, 1] = product_id
        m_interactions.iloc[i, 2] = rating

    elif count == 2:
        product_id = interaction[1]['m_product_id_2']
        rating = interaction[1]['percentage_2']
        m_interactions.iloc[i, 0] = user_id
        m_interactions.iloc[i, 1] = product_id
        m_interactions.iloc[i, 2] = rating

    i += 1

# m_interactions.to_csv('m_interactions.csv', index=False)


# rating matrix
ratings = m_interactions.pivot_table(index=['user_id'], columns=['product_id'], values='rating')
ratings.fillna(0, inplace=True)
# ratings.to_csv('ratings.csv')

