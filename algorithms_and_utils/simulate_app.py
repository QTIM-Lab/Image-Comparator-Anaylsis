import os, pandas as pd, numpy as np, pdb, random, sys
os.chdir('sorting_algorithms')
from insertionsort import insertionSort
sys.path.insert(1, '../couchdb_results')
from elo import EloRating


images = pd.read_csv("../couchdb_results/Cervix_Treatability/12-images/images.csv")
images['id'] = images.index + 1
images = images.loc[:,['id','image','class']]
jose_results = pd.read_csv("../couchdb_results/Cervix_Treatability/Jose.csv")
pairs = [(x,y) for x,y in zip(jose_results['image0'],jose_results['image1'])]
len(pairs) # 66

# Get Image IDs and mapping to original file name
image_list = pd.concat([jose_results[['image0','origin_0']].rename(columns={'image0':'image','origin_0':'origin'}),
                        jose_results[['image1','origin_1']].rename(columns={'image1':'image','origin_1':'origin'})], axis=0)
image_list = image_list.groupby(['image','origin']).size().reset_index()[['image','origin']]
image_ids = image_list['image']

def perform_pair_selection():
    database = {'list':arr, 'key':arr[1], 'key_index':1, 'other_element_index':0, 'sorted':False, 'pairs_seen':[]}
    # pdb.set_trace()
    def get_pair(database):
        arr = database['list']
        key_index = database['key_index']
        other_element_index = database['other_element_index']
        # pdb.set_trace()
        key = database['key']
        print(f"pair: [{key}, {arr[other_element_index]}]")
        return (key_index, other_element_index), (key, arr[other_element_index])

    # pair_indexes, pair = get_pair(database)

    def get_annotator_result(pair, pair_indexes):
        pair_result = jose_results[(jose_results['image0'] == pair[0]) & (jose_results['image1'] == pair[1])]
        if pair_result.shape[0] == 0:
            pair_result = jose_results[(jose_results['image0'] == pair[1]) & (jose_results['image1'] == pair[0])]
        # val = input("simulate getting user input: ")
        # pdb.set_trace()
        image0_index = pair_indexes[0] if pair_result['image0'].iloc[0] == pair[0] else pair_indexes[1]
        image1_index = pair_indexes[0] if pair_result['image1'].iloc[0] == pair[0] else pair_indexes[1]
        return {'image0':pair_result['image0'].iloc[0], 
                'image1':pair_result['image1'].iloc[0],
                'image0_index':image0_index,
                'image1_index':image1_index,
                'winner':pair_result['winner'].iloc[0]}

    # result = get_annotator_result(pair)

    # def adjust_database(database, result):
    #     # Answer Key:
    #     # 1 - image0 won (more treatable)
    #     # 0 - image1 won (more treatable)
    #     # -1 - Equally Treatable
    #     # -2 - Equally Not Treatable
    #     # pdb.set_trace()
    #     if result['winner'] == 1:
    #         if result['image0_index'] < result['image1_index']:
    #             database['list'][result['image0_index']] = result['image1']
    #             database['list'][result['image1_index']] = result['image0']
    #             print("A")
    #             pdb.set_trace()
    #         else:
    #             print("B")
    #             pdb.set_trace()
    #     elif result['winner'] == 0:
    #         print("C")
    #         pdb.set_trace()
    #     print("D")
    #     pdb.set_trace()
    #     database['key_index'] += 1
    #     database['other_element_index'] = database['key_index'] - 1
    #     database['pairs_seen'].append((result['image0'],result['image1']))
        
    # adjust_database(database, result, pair, pair_indexes)

    # Simulate asynchronous program and insertion sort
    for database_key_index in range(database['key_index'], len(database['list'])):
        database['key_index'] = database_key_index
        database['other_element_index'] = database['key_index'] - 1
        database['key'] = database['list'][database['key_index']]
        # if database['key_index'] == 12:
        #     pdb.set_trace()
        # pdb.set_trace()
        if database['key_index'] != len(arr):
            pair_indexes, pair = get_pair(database); print(f"pair_indexes, pair: {pair_indexes}, {pair}")
            key , key_index= pair[0], pair_indexes[0]; print(f"key, key_index: {key}, {key_index}")
            other_element , other_element_index= pair[1], pair_indexes[1]; print(f"other_element, other_element_index: {other_element}, {other_element_index}")
            result = get_annotator_result(pair, pair_indexes)
            # Who won between key and other element
            key_less_than_other_element = True if result['winner'] == 1 and key_index != result['image0_index'] else False
            print("A")
            database['pairs_seen'].append((result['image0'],result['image1']))
            print(database)
        while database['other_element_index'] >= 0 and key_less_than_other_element:
            print("B")
            database['list'][other_element_index+1] = other_element # key's old spot
            database['list'][other_element_index] = key
            database['key_index'] = other_element_index
            database['other_element_index'] -= 1
            if database['other_element_index'] != -1:
                pair_indexes, pair = get_pair(database); print(f"pair_indexes, pair: {pair_indexes}, {pair}")
                other_element , other_element_index= pair[1], pair_indexes[1]; print(f"other_element, other_element_index: {other_element}, {other_element_index}")
                result = get_annotator_result(pair, pair_indexes)
                database['pairs_seen'].append((result['image0'],result['image1']))
                print(database)
                # pdb.set_trace()
                key_less_than_other_element = True if result['winner'] == 1 and key_index != result['image0_index'] else False
        database['list'][database['other_element_index']+1] = key
        # MAke condition that allows the db to be "sorted"
        database['other_element_index'] = database['key_index'] - 1
    return database


arr = [i for i in image_ids]
arr = random.sample(list(image_ids), 12)

arr = [4, 12, 3, 11, 8, 9, 7, 2, 1, 5, 10, 6]
out = perform_pair_selection(); print(out['list']) # [12, 11, 9, 10, 4, 8, 3, 7, 6, 5, 2, 1]

arr = [4, 10, 2, 6, 12, 7, 9, 11, 8, 3, 5, 1]
out = perform_pair_selection(); print(out['list']) # [10, 6, 12, 9, 11, 4, 2, 7, 8, 5, 3, 1]

arr = [5, 2, 7, 3, 10, 6, 1, 11, 4, 12, 9, 8]
out = perform_pair_selection(); print(out['list']) # [10, 5, 2, 7, 4, 6, 8, 11, 12, 9, 3, 1]

arr = [1, 10, 3, 8, 6, 11, 4, 5, 9, 12, 2, 7]
out = perform_pair_selection(); print(out['list']) # [8, 5, 4, 10, 6, 11, 9, 12, 1, 3, 2, 7]

arr = [11, 7, 10, 4, 2, 1, 12, 8, 6, 5, 3, 9]
out = perform_pair_selection(); print(out['list']) # [11, 10, 12, 7, 4, 8, 5, 6, 9, 2, 1, 3]

arr = [5, 1, 11, 3, 8, 2, 9, 6, 12, 7, 10, 4]
out = perform_pair_selection(); print(out['list']) # [11, 9, 5, 8, 6, 12, 10, 1, 3, 2, 7, 4]

arr = [1, 8, 2, 12, 11, 6, 5, 4, 7, 3, 9, 10]
out = perform_pair_selection(); print(out['list']) # [12, 11, 8, 4, 5, 6, 9, 10, 1, 2, 7, 3]

arr = [7, 1, 12, 5, 3, 11, 2, 8, 6, 9, 10, 4]
out = perform_pair_selection(); print(out['list']) # [12, 11, 7, 5, 8, 4, 6, 9, 10, 1, 3, 2]

arr = [1, 9, 7, 10, 11, 3, 12, 5, 4, 8, 2, 6]
out = perform_pair_selection(); print(out['list']) # [9, 10, 11, 12, 1, 7, 4, 5, 8, 6, 3, 2]




arr = [4, 5, 2, 7, 1, 8, 10, 3, 6, 11, 12, 9]
out = perform_pair_selection(); print(out['list']) # [10, 5, 4, 2, 7, 8, 6, 11, 12, 9, 1, 3]
arr = [10, 5, 4, 2, 7, 8, 6, 11, 12, 9, 1, 3]
out = perform_pair_selection(); print(out['list']) # [10, 5, 4,   2, 7, 8,   6, 11, 12, 9, 1, 3]



def winner_id(row):
    # pdb.set_trace()
    if row['winner'] == 1:
        return row['image0']
    elif row['winner'] == 0:
        return row['image1']
    elif row['winner'] == -1:
        return 'ET'
    else:
        return 'ENT'


pair = (2,1)
pair = (3,2)
pair = (4,3)
pair = (4,2)
pair = (4,1)
pair = (5,3)
pair = (5,2)
pair = (5,4)
pair = (5,1)
pair = (6,3)
pair = (6,2)
pair = (6,4)
pair = (6,1)
pair = (6,5)
pair = (7,3)
pair = (8,7)
pair = (9,8)
pair = (9,7)
pair = (9,3)
jose_results['winner_id'] = jose_results.apply(winner_id, axis=1)
r = jose_results[(jose_results['image0'] == pair[0]) & (jose_results['image1'] == pair[1])][['image0','image1','winner','winner_id']]
if r.shape[0] == 0:
    r = jose_results[(jose_results['image0'] == pair[1]) & (jose_results['image1'] == pair[0])]

r[['image0','image1','winner','winner_id']]
# jose_results[['image0','image1','winner','winner_id']].to_csv("jose_temp.csv")


# Wins\Ties by id
images['wins'] = 0
images['ET'] = 0
images['ENT'] = 0
for id in images['id']:
    # pdb.set_trace()
    wins = jose_results[((jose_results['image0'] == id) | (jose_results['image0'] == id)) & (jose_results['winner_id'] == id)].shape[0]
    ET = jose_results[((jose_results['image0'] == id) | (jose_results['image0'] == id)) & (jose_results['winner_id'] == 'ET')].shape[0]
    ENT = jose_results[((jose_results['image0'] == id) | (jose_results['image0'] == id)) & (jose_results['winner_id'] == 'ENT')].shape[0]
    # pdb.set_trace()
    images.loc[images['id'] == id, 'wins'] = wins
    images.loc[images['id'] == id, 'ET'] = ET
    images.loc[images['id'] == id, 'ENT'] = ENT


images.sort_values('wins', ascending=False)


# Elo post
arr = [i for i in image_ids]
# arr = random.sample(list(image_ids), 12)

out = perform_pair_selection(); print(out['list']) 
out['pairs_seen']
