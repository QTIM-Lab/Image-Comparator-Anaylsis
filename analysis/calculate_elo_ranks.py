import os, pdb, pandas as pd

# Navigate to sorting algorithms directory for tools
## EloRating
from sorting_algorithms.elo import EloRating
WKDIR = 'couchdb_results/Opthamology/RIM-ONE/compare_results_01_03_2023'

images = pd.read_csv(os.path.join('couchdb_results/Opthamology/RIM-ONE/',"images.csv")) # get actual images if needed

# Need to redesign merge and get_ranks around this data but for now they are used solely to get a full list of pair results for a "combined" user

results = {'Lazcano':  {'csv':'Lazcano_compare_results_01_03_2023.csv','ranks':[]},
           'Alryalat':  {'csv':'Alryalat_compare_results_01_03_2023.csv','ranks':[]},
           'Seibold':   {'csv':'Seibold_compare_results_01_03_2023.csv','ranks':[]},
           'Malik':  {'csv':'Malik_compare_results_01_03_2023.csv','ranks':[]},
           'Combined': {'csv':'Combined_compare.csv','ranks':[]}
          }

def create_combined_list():
    results_Combined = pd.DataFrame()
    for person in results.keys():
        # pdb.set_trace()
        if person != "Combined":
            person_data = pd.read_csv(os.path.join(WKDIR,results[person]['csv']))
            results_Combined = pd.concat([results_Combined, person_data], axis=0)
    results_Combined.to_csv(os.path.join(WKDIR,"Combined_compare.csv"), index = None)
    return results_Combined


results_Combined = create_combined_list()

def get_ranks(csv):
    data = pd.read_csv(os.path.join(WKDIR,csv))
    # pdb.set_trace()
    images = list(set(data['image_name_0']) | set(data['image_name_1']))
    # pdb.set_trace()
    images = {i:1000 for i in images} # initialize elo score
    def test(image_name_0, image_name_1, winner):
        # pdb.set_trace()
        if winner == -1 or winner == -2:
            pass
        else:
            Ra, Rb = EloRating(images[image_name_0], images[image_name_1], 30, winner)
            images[image_name_0] = Ra
            images[image_name_1] = Rb
            # pdb.set_trace()
    data.apply(lambda row: test(row['image_name_0'], row['image_name_1'], row['winner']), axis=1)
    rows = {'images':list(images.keys()), 'elo':list(images.values())}
    # pdb.set_trace()
    ranks = pd.DataFrame(rows).sort_values('elo').reset_index()
    ranks['rank'] = ranks.index + 1
    return ranks


def merge_results(results):
    merge = pd.DataFrame()
    for person in results.keys():
        results[person]['ranks'] = get_ranks(results[person]['csv'])
        if merge.shape == (0,0):
            merge = pd.concat([merge, results[person]['ranks']]).rename(columns={'elo':f'Elo_{person}','rank':f'Ranks_{person}'}).drop('index',axis=1)
        else:
            # pdb.set_trace()
            new_table = results[person]['ranks'].rename(columns={'elo':f'Elo_{person}','rank':f'Ranks_{person}'}).drop('index',axis=1)
            merge = pd.merge(merge, new_table, on='images')
    # pdb.set_trace()
    return merge


merge = merge_results(results)
os.remove(os.path.join(WKDIR, "Combined_compare.csv")) # Delete so we don't have to worry about why it's there

header = ['images', 'Elo_Combined', 'Ranks_Combined', 'Elo_Lazcano', 'Ranks_Lazcano', 'Elo_Alryalat', 'Ranks_Alryalat', 'Elo_Seibold', 'Ranks_Seibold', 'Elo_Malik', 'Ranks_Malik']

merge.sort_values("Ranks_Combined").to_csv(os.path.join(WKDIR,"elo_based_ranks.csv"), index=None)

