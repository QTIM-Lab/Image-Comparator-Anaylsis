import os, choix, pdb, random
import networkx as nx
import numpy as np, pandas as pd
from sklearn.linear_model import LinearRegression
from itertools import combinations, permutations

import matplotlib.pyplot as plt # BB

# Older (Dropbpx MGH)
WKDIR='couchdb_results/Opthamology/RIM-ONE/compare_results_01_03_2023'
# Linux Tower 1
WKDIR="/projects/Image-Comparator-Analysis/raw_annotations/opthamology_rim-one/opthamology_rim-one_50_CompareList"

DATA_OUT="/projects/Image-Comparator-Analysis/analysis"

# Dropbox again
# images = pd.read_csv(os.path.join('couchdb_results/Opthamology/RIM-ONE/',"images.csv")) # get actual images if needed

# Linux Tower 1
images = pd.read_csv(os.path.join('/projects/Image-Comparator-Analysis/raw_annotations/opthamology_rim-one',"images_opthamology_rim-one_app_images_key.csv")) # get actual images if needed
images.app_image_id.max() # 158
images.app_image_id.min() # 1

def make_data_pairs(row, min_id):
    # 1 - image0 won
    # 0 - image1 won
    # -1 - Equally Treatable
    # -2 - Equally Not Treatable (edited) 
    if row['winner'] == 1:
        left = row['image0']
        right = row['image1']
    elif row['winner'] == 0:
        left = row['image1']
        right = row['image0']
    elif row['winner'] == -1 or row['winner'] == -2:
        left = 'tie'
        right= 'tie'
        return(left, right)
    # return(left, right)
    # if int(right)-min_id == -1:
    #     pdb.set_trace()
    return (int(left)-min_id, int(right)-min_id)

results_Lazcano = pd.read_csv(os.path.join(WKDIR, "Lazcano_compare_results_01_03_2023.csv"))
results_Alryalat = pd.read_csv(os.path.join(WKDIR, "Alryalat_compare_results_01_03_2023.csv"))
results_Seibold = pd.read_csv(os.path.join(WKDIR, "Seibold_compare_results_01_03_2023.csv"))
results_Malik = pd.read_csv(os.path.join(WKDIR, "Malik_compare_results_01_03_2023.csv"))
results_Ittoop = pd.read_csv(os.path.join(WKDIR, "Ittoop_compare_results_01_03_2023.csv"))


# .sort_values('date')[['user','origin_0','origin_1','image0','image1','date']] # To view
results = {
           'Lazcano':results_Lazcano,
           'Alryalat':results_Alryalat,
           'Seibold':results_Seibold,
           'Malik':results_Malik,
           'Ittoop':results_Ittoop,
           }

def create_fake_ids(image_ids):
    # print("create_fake_ids: \n"); pdb.set_trace()
    image_ids = list(image_ids)
    image_ids = pd.DataFrame({"image_ids":image_ids}).sort_values("image_ids")
    image_ids.reset_index(inplace=True)
    image_ids['fake_ids'] = image_ids.index + 1
    image_ids.drop(columns=['index'], inplace=True)
    return image_ids 

temp_params = {'A': [], 'M': [],'I': [], 'L': []} # For debugging
def compute_ranks(df, name):
    # Create Fake IDS
    image_ids = set(np.concatenate((df.image0.unique(),df.image1.unique())))
    fake_ids = create_fake_ids(image_ids)
    min_id = min(fake_ids['fake_ids']) # adjusted image_ids min_id
    # image 0
    fake_df = pd.merge(fake_ids, df[['image0','image1','winner']], left_on="image_ids", right_on="image0")
    fake_df.rename(columns={'fake_ids':'image0_fake'}, inplace=True)
    fake_df.drop('image_ids', axis=1, inplace=True)
    # image 1
    fake_df = pd.merge(fake_df, fake_ids, left_on="image1", right_on="image_ids")
    fake_df.rename(columns={'fake_ids':'image1_fake'}, inplace=True)
    fake_df.drop('image_ids', axis=1, inplace=True)
    df['data_pairs'] = fake_df[['image0_fake','image1_fake','winner']].rename(columns={'image0_fake':'image0','image1_fake':'image1'}).apply(lambda x: make_data_pairs(x, min_id), axis=1)
    n_items = len(image_ids)
    # Make choix ranks
    # pairs have to be fed in winner first: (winner, loser)...so ties don't exist, maybe we can pass in (winner,loser) and (loser,winner)
    non_ties = df[df['data_pairs'].str[0] != 'tie'] # removes some ids so total count wont be 596
    data = non_ties['data_pairs'].to_list()
    r_data = random.sample(data, len(data))
    params = choix.ilsr_pairwise(n_items, r_data, alpha=0.01)
    ranks_low_to_high = np.argsort(params)+min_id
    ################################ Fill Temp Params ##########################################
    if name == 'Alryalat':
        temp_params['A'].append(ranks_low_to_high)
    elif name == 'Malik':
        temp_params['M'].append(ranks_low_to_high)
    elif name == 'Ittoop':
        temp_params['I'].append(ranks_low_to_high)
    elif name == 'Lazcano':
        temp_params['L'].append(ranks_low_to_high)
    ################################ Fill Temp Params ##########################################
    # Double checked on 01/04/2023 and I still think this is right.
    # np.argsort(params) returns ids in order from worst to best.
    # https://notebook.community/lucasmaystre/choix/notebooks/intro-pairwise
    df_ranks = pd.DataFrame({'user':['Ranks_'+name]*len(ranks_low_to_high),
                             'id':ranks_low_to_high,
                             'ranks':range(1,len(ranks_low_to_high)+1)})
    # print("compute_ranks: \n"); pdb.set_trace()
    # Return Ids to their original form
    df_ranks = pd.merge(fake_ids, df_ranks, left_on='fake_ids', right_on='id')[['user','image_ids','ranks']]
    return df_ranks


# quick() # literally so I don't have to highlight it each time to test.

def quick():
# Get each annotators ranks from choix
    all = pd.DataFrame()
    ranks = pd.DataFrame()
    for name in results.keys():
        df = results[name]
        # pdb.set_trace()
        df_ranks = compute_ranks(df, name)
        # pdb.set_trace()
        # Concat individual results
        all = pd.concat([all, df], axis=0)
        ranks = pd.concat([ranks, df_ranks], axis=0)
        # len(data) # some amount, down from 598
    return all, ranks


all, ranks = quick()

# Get combined annotator ranks from choix by using all data available from all annotators
combined_ranks = compute_ranks(all, 'Combined')
ranks = pd.concat([ranks, combined_ranks], axis=0)
ranks[ranks['user'] == 'Ranks_Combined'].sort_values('image_ids', ascending=True)

Ranks = ranks.pivot(index=['image_ids'], columns=["user"], values='ranks').reset_index()
Ranks = pd.merge(images, Ranks, left_on='app_image_id', right_on='image_ids')
Ranks.columns
header = ['app_image_id','image_name', 'Ranks_Combined', 'Ranks_Ittoop', 'Ranks_Alryalat', 'Ranks_Lazcano', 'Ranks_Malik', 'Ranks_Seibold']
Ranks[header].sort_values('Ranks_Combined').to_csv(os.path.join(DATA_OUT,"choix_based_ranks.csv"), index=False)


Ranks.head()
I = Ranks[['image_ids', 'Ranks_Ittoop']]; I.sort_values('image_ids', inplace=True);
A = Ranks[['image_ids', 'Ranks_Alryalat']]; A.sort_values('image_ids', inplace=True);
M = Ranks[['image_ids', 'Ranks_Malik']]; M.sort_values('image_ids', inplace=True);
L = Ranks[['image_ids', 'Ranks_Lazcano']]; L.sort_values('image_ids', inplace=True);
S = Ranks[['image_ids', 'Ranks_Seibold']]; S.sort_values('image_ids', inplace=True);
C = Ranks[['image_ids', 'Ranks_Combined']]; C.sort_values('image_ids', inplace=True);


Annotators=[f'Ranks_{a}' for a in results.keys()] + ['Ranks_Combined']

plots = [i for i in combinations(Annotators, 2)]
len([i for i in combinations(Annotators, 2)])# 15


def make_plot(X, Y):
    # pdb.set_trace()
    X_df = Ranks[['image_ids', X]]; X_df.sort_values('image_ids', inplace=True)
    Y_df = Ranks[['image_ids', Y]]; Y_df.sort_values('image_ids', inplace=True)
    x = np.array([X_df[X]])
    y = np.array([Y_df[Y]])
    plt.scatter(x, y); plt.savefig(os.path.join(DATA_OUT,f"{X}_v_{Y}_plot.png"))
    plt.title(f'{X} vs {Y}')
    plt.xlabel(f'{X}')
    plt.ylabel(f'{Y}')
    model = LinearRegression()
    model.fit(x.T, y.T)
    y_new = model.predict(x.T)
    plt.scatter(x, y_new); plt.savefig(os.path.join(DATA_OUT,f"{X}_v_{Y}_plot.png"))
    plt.clf()

# Manual
make_plot('Ranks_Ittoop', 'Ranks_Alryalat')
# Auto
for x_, y_ in plots:
    make_plot(x_, y_)


# Randomise data
# r_data = random.sample(data, len(data))
# params = choix.ilsr_pairwise(n_items, r_data) # doesn't work as graph doesn't converge or something...need alpha
# params = choix.ilsr_pairwise(n_items, r_data, alpha=0.01)
# print(params)
# print("ranking (worst to best):", np.argsort(params)+1)

# See ranks evolve game by game
# def calc_ranks(DATA):
#     for pair_num in range(1,len(DATA)+1):
#         print(pair_num)
#         params = []
#         temp_data = set(sum(DATA[0:pair_num],()))
#         data_ids = set(sum(DATA,()))
#         temp_n_items = len(temp_data)
#         # ID ADJUSTMENT
#         # max(temp_data)
#         # if pair_num == 300:
#         #     pdb.set_trace()
#         # pdb.set_trace()
#         # params = choix.ilsr_pairwise(temp_n_items, DATA[0:pair_num], alpha=0.1)
#         params = choix.ilsr_pairwise(max(temp_data)+1, DATA[0:pair_num], alpha=0.01)
#         # if len(set(params)) == len(data_ids):
#         #     pdb.set_trace()
#         # if pair_num % 50 == 0:
#         #     pdb.set_trace()
#         # if pair_num == 568:
#         #     pdb.set_trace()
#         #     graph = nx.DiGraph(incoming_graph_data=data)
#         #     nx.draw(graph, with_labels=True)
#         #     plt.show()
#             # break
#         print(params)
#         print("ranking (worst to best):", np.argsort(params)+1)
#     return params

# calc_ranks(r_data)


# prob_1_wins, prob_4_wins = choix.probabilities([1, 4], params)
# print("Prob(1 wins over 4): {:.2f}".format(prob_1_wins))


# Visualize graph
# graph = nx.DiGraph(incoming_graph_data=data)
# nx.draw(graph, with_labels=True)
# plt.show()
# data

# Counting distinct pairs
# found = []
# for l,r in data:
#     if l not in found:
#         found.append(l)
#     if r not in found:
#         found.append(r)
# len(set(found))

# Sample data
# n_items = 5
# data = [
#     (1, 0), (0, 4), (3, 1),
#     (0, 2), (2, 4), (4, 3),
# ]



# Try different alphas
# for alpha in [i for i in [0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01]]:
#     print(alpha)
#     params = choix.ilsr_pairwise(n_items, r_data, alpha=alpha)
#     print("ranking (worst to best):", np.argsort(params)+1)

# Force new numbers to the front without randomizing, but byt choosing explicitly
# Doesn't work that well right now...more investigation later
# Data = []
# # seen_i = []
# # seen_j = []
# back_of_Data = []
# for i,j in data:
#     # if i == 3 and j ==1:
#     #     pdb.set_trace()
#     print(i,j)
#     max_index = 1
#     if len(Data) != 0:
#         max_index = max([max(I,J) for I,J in Data])
#     # pdb.set_trace()
#     if i not in [D[0] for D in Data] and j not in [D[1] for D in Data] and i <= max_index and j <= max_index:# and True:
#         Data.append((i,j))
#     else:
#         back_of_Data.append((i,j))
#     # if i not in seen_i:
#     #     seen_i.append(i)
#     #     if j not in seen_j:
#     #         seen_j.append(j)
#     #         Data.append((i,j))
#     #     else:
#     #         back_of_Data.append((i,j))
#     # else:
#     #     back_of_Data.append((i,j))
# len(Data + back_of_Data)
# pdb.set_trace()

