import string
import numpy as np
import pandas as pd


items = [
    'https://www.zara.com/eg/en/basic-slim-fit-t-shirt-p05584411.html?v1=157954762&v2=2032069',
    'https://www.zara.com/eg/en/basic-heavy-weight-t-shirt-p00526411.html?v1=174103357&v2=2032069',
    'https://www.zara.com/eg/en/knit-colour-block-t-shirt-p03284407.html?v1=148602456&v2=2032069',
    'https://www.zara.com/eg/en/basic-medium-weight-t-shirt-p01887401.html?v1=158099447',
    'https://www.zara.com/eg/en/knit-t-shirt-p04231410.html?v1=169542509&v2=2032069',
    'https://www.zara.com/eg/en/contrast-print-t-shirt-p00495431.html?v1=144410078&v2=2032069',
    'https://www.zara.com/eg/en/geometric-print-technical-t-shirt-p06224421.html?v1=157493299&v2=2032069',
    'https://www.zara.com/eg/en/long-length-t-shirt-p01887420.html?v1=144435377&v2=2032069',
    'https://www.zara.com/eg/en/textured-piqu--polo-shirt-p09240450.html?v1=164457785&v2=2032362',
    'https://www.zara.com/eg/en/basic-slim-fit-t-shirt-p05584340.html?v1=153714218&v2=2032069',
]

# product_id = np.random.randint(0, len(items))
# print(items[product_id])

users = pd.read_csv('users-dataset.csv')
users_arr = users.to_numpy()

interactions_arr = np.zeros((len(users_arr), 9), dtype=object)

count = 0
for user in users_arr:
    count += 1
    product_id = np.random.randint(0, len(items))

    # logic comes here

    interactions_arr[user[0]-1][0] = user[0]
    interactions_arr[user[0]-1][1] = product_id
    interactions_arr[user[0]-1][2] = user[3]
    interactions_arr[user[0]-1][3] = user[4]
    interactions_arr[user[0]-1][4] = user[5]
    # interactions_arr[user[0]-1][5] = "size_1"
    # interactions_arr[user[0]-1][6] = "presentage_1"
    # interactions_arr[user[0]-1][7] = "size_2"
    # interactions_arr[user[0]-1][8] = "presentage_2"
    if count > 10:
        break

print(interactions_arr)

iteractions = pd.DataFrame(interactions_arr, columns=[
                           'user_id', 'product_id', 'fit_preferences', 'weight', 'height', 'size_1', 'presentage_1', 'size_2', 'presentage_2'])
pd.DataFrame.to_csv(iteractions, 'interactions-dataset.csv', index=False)
