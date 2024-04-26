import os
import numpy as np

from sklearn.metrics import ndcg_score
from crowdkit.aggregation import DawidSkene
from crowdkit.datasets import load_dataset
from crowdkit.aggregation import BradleyTerry, NoisyBradleyTerry
import pandas as pd

df = pd.read_csv('http://www-personal.umich.edu/~kevynct/datasets/wsdm_rankagg_2013_readability_crowdflower_data.csv', dtype=str)
df.shape
df.head()
df[['_worker_id','passage_a','passage_b']]

# make label column for winner - notice the for loop is for when either a or b is more difficult
for column, status in (('passage_a', 'Passage A is more difficult.'), ('passage_b', 'Passage B is more difficult.')):
    df.loc[df['please_decide_which_passage_is_more_difficult'] == status, 'label'] = df.loc[df['please_decide_which_passage_is_more_difficult'] == status, column]

df.rename(columns={
    '_worker_id': 'performer', # pair-wise id
    'passage_a': 'left', # image 0 
    'passage_b': 'right' # image 1 
}, inplace=True)

df[['performer','left','right']]
df.dropna(subset=['label'], inplace=True)

# Enter Bradley-Terry
agg_bt = BradleyTerry(n_iter=100).fit_predict(df)
agg_noisybt = NoisyBradleyTerry(n_iter=10).fit_predict(df)

gt_levels = {}

for _, row in df.iterrows():
    gt_levels[row['left']] = int(row['label_level_a'])
    gt_levels[row['right']] = int(row['label_level_b'])

gt = pd.Series(gt_levels.values(), index=gt_levels.keys())

# df_agg = pd.DataFrame({'bt': agg_bt, 'noisybt': agg_noisybt, 'gt': gt}).reset_index()
df_agg = pd.DataFrame({'bt': agg_bt, 'gt': gt}).reset_index()
df_agg.rename(columns={'index': 'passage'}, inplace=True)
df_agg


np.random.seed(0)

df_agg['bt_rank'] = df_agg['bt'].rank().astype(int)
# df_agg['noisybt_rank'] = df_agg['noisybt'].rank().astype(int)
df_agg['random_rank'] = np.random.permutation(range(len(df_agg)))

df_agg

ndcg_score(df_agg['random_rank'].values.reshape(1, -1), df_agg['gt'].values.reshape(1, -1), k=10)
ndcg_score(df_agg['bt_rank'].values.reshape(1, -1), df_agg['gt'].values.reshape(1, -1), k=10)
# ndcg_score(df_agg['noisybt_rank'].values.reshape(1, -1), df_agg['gt'].values.reshape(1, -1), k=10)

# df_agg[['bt_rank', 'noisybt_rank', 'random_rank', 'gt']].corr()
df_agg[['bt_rank', 'random_rank', 'gt']].corr()

df_agg.sort_values('bt_rank', ascending=False, inplace=True)
df_agg