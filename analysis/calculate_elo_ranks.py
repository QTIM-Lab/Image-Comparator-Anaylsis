import os, pdb, pandas as pd

# Navigate to sorting algorithms directory for tools
## EloRating
from algorithms_and_utils.elo import EloRating
# IN = 'couchdb_results/Opthamology/RIM-ONE/compare_results_01_03_2023'

# Linux Tower 1
IN="/projects/Image-Comparator-Analysis/raw_annotations/opthamology_rim-one/opthamology_rim-one_50_CompareList"
DATA_OUT="/projects/Image-Comparator-Analysis/analysis"


# images = pd.read_csv(os.path.join('couchdb_results/Opthamology/RIM-ONE/',"images.csv")) # get actual images if needed
images = pd.read_csv(os.path.join('/projects/Image-Comparator-Analysis/raw_annotations/opthamology_rim-one',"images_opthamology_rim-one_app_images_key.csv")) # get actual images if needed
# Need to redesign merge and get_ranks around this data but for now they are used solely to get a full list of pair results for a "combined" user

results = {'Lazcano':  {'csv':'Lazcano_compare_results_01_03_2023.csv','ranks':[]},
           'Alryalat':  {'csv':'Alryalat_compare_results_01_03_2023.csv','ranks':[]},
           'Seibold':   {'csv':'Seibold_compare_results_01_03_2023.csv','ranks':[]},
           'Malik':  {'csv':'Malik_compare_results_01_03_2023.csv','ranks':[]},
           'Ittoop':  {'csv':'Ittoop_compare_results_01_03_2023.csv','ranks':[]},
           'Combined': {'csv':'Combined_compare.csv','ranks':[]}
          }



# Lazcano = pd.read_csv(os.path.join(IN, results['Lazcano']['csv']))
# Alryalat = pd.read_csv(os.path.join(IN, results['Alryalat']['csv']))
# Seibold = pd.read_csv(os.path.join(IN, results['Seibold']['csv']))
# Malik = pd.read_csv(os.path.join(IN, results['Malik']['csv']))
# Ittoop = pd.read_csv(os.path.join(IN, results['Ittoop']['csv']))

# Lazcano.shape
# Alryalat.shape
# Seibold.shape
# Malik.shape
# Ittoop.shape


def create_combined_list():
    results_Combined = pd.DataFrame()
    for person in results.keys():
        # pdb.set_trace()
        if person != "Combined":
            person_data = pd.read_csv(os.path.join(IN,results[person]['csv']))
            results_Combined = pd.concat([results_Combined, person_data], axis=0)
    results_Combined.to_csv(os.path.join(IN,"Combined_compare.csv"), index = None)
    return results_Combined


results_Combined = create_combined_list()
results_Combined.shape
results_Combined

def get_ranks(csv):
    data = pd.read_csv(os.path.join(IN,csv))
    pdb.set_trace()
    data.columns
    data.loc[50,['user','date','image0', 'image1', 'winner']]
    data[data['user'] == 'Lazcano'][['user','date','image0', 'image1', 'winner']]
    EloRating(45, 107, 30, 0)
    # pdb.set_trace()
    images = list(set(data['image_name_0']) | set(data['image_name_1']))
    # pdb.set_trace()
    images = {i:1000 for i in images} # initialize elo score
    def calc_elo(image_name_0, image_name_1, winner):
        # pdb.set_trace()
        if False: # winner == -1 or winner == -2: # uncomment to skip ties
            pass
        else:
            Ra, Rb = EloRating(images[image_name_0], images[image_name_1], 30, winner)
            images[image_name_0] = Ra
            images[image_name_1] = Rb
            # pdb.set_trace()
    data.apply(lambda row: calc_elo(row['image_name_0'], row['image_name_1'], row['winner']), axis=1)
    # pdb.set_trace()
    rows = {'images':list(images.keys()), 'elo':list(images.values())}
    # pdb.set_trace()
    ranks = pd.DataFrame(rows).sort_values('elo').reset_index()
    ranks['rank'] = ranks.index + 1
    return ranks


def merge_results(results):
    merge = pd.DataFrame()
    for person in results.keys():
        # pdb.set_trace()
        results[person]['ranks'] = get_ranks(results[person]['csv'])
        if merge.shape == (0,0):
            merge = pd.concat([merge, results[person]['ranks']]).rename(columns={'elo':f'Elo_{person}','rank':f'Ranks_{person}'}).drop('index',axis=1)
        else:
            # pdb.set_trace()
            new_table = results[person]['ranks'].rename(columns={'elo':f'Elo_{person}','rank':f'Ranks_{person}'}).drop('index',axis=1)
            merge = pd.merge(merge, new_table, on='images')
    # pdb.set_trace()
    return merge

results_c = {'Combined':results['Combined']}
merge = merge_results(results_c)

merge = merge_results(results)
os.remove(os.path.join(IN, "Combined_compare.csv")) # Delete so we don't have to worry about why it's there

merge.columns
header = ['images', 'Elo_Combined', 'Ranks_Combined', 'Elo_Lazcano', 'Ranks_Lazcano', 'Elo_Alryalat', 'Ranks_Alryalat', 'Elo_Seibold', 'Ranks_Seibold', 'Elo_Malik', 'Ranks_Malik', 'Elo_Ittoop', 'Ranks_Ittoop']

merge.sort_values("Ranks_Combined").to_csv(os.path.join(DATA_OUT,"elo_based_ranks.csv"), index=None)

