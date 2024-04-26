import os, pdb, pandas as pd

# Make pairs +-2 from origin
# Ex: 8 can be paired with anything in th 6-10 range

s1 = ['8a1','11a2','13a3','16a4','18a5','21a6']
s2 = ['8b7','11b8','13b9','16b10','18b11','21b12']
s3 = ['8c13','11c14','13c15','16c16','18c17','21c18']
s4 = ['8d19','11d20','13d21','16d22','18d23','21d24']
s5 = ['8e25','11e26','13e27','16e28','18e29','21e30']

#s6 = ['8d31','11d20','13d21','16d22','18d23','21d24']
#s7 = ['8e25','11e26','13e27','16e28','18e29','21e30']

pairs = [];
pairs_debug = [];
def make_pairs(l1,l2):
    for i,j in enumerate(l1):
        for k,l in enumerate(l2):
            # This is pretty shaky so don't rely on it without double checking
            for letter in "abcde":
                if j.find(letter) != -1: # we found the right letter          
                    left = int(j[j.find(letter)+1:])
                if l.find(letter) != -1: # we found the right letter          
                    right = int(l[l.find(letter)+1:])
            if abs(i-k) <= 1 and j != l and ( [left,right] not in pairs and [right,left] not in pairs):
                pairs.append([left,right])
                pairs_debug.append([j,l])


make_pairs(s1,s1);make_pairs(s1,s2);make_pairs(s1,s3);make_pairs(s1,s4);make_pairs(s1,s5)
make_pairs(s2,s2);make_pairs(s2,s3);make_pairs(s2,s4);make_pairs(s2,s5)
make_pairs(s3,s3);make_pairs(s3,s4);make_pairs(s3,s5)
make_pairs(s4,s4);make_pairs(s4,s5)
make_pairs(s5,s5);

print(len(pairs))
print(pairs)




images = pd.DataFrame([
    [1, 8], 
    [2,11], 
    [3,13], 
    [4,16], 
    [5,18], 
    [6,21], 
    [7,8], 
    [8,11], 
    [9,13], 
    [10,16], 
    [11,18], 
    [12,21], 
    [13,8], 
    [14,11], 
    [15,13], 
    [16,16], 
    [17,18], 
    [18,21], 
    [19,8], 
    [20,11], 
    [21,13], 
    [22,16], 
    [23,18], 
    [24,21], 
    [25,8], 
    [26,11], 
    [27,13], 
    [28,16], 
    [29,18], 
    [30,21]
    ], columns=header)
    # s1 = ['8a1','11a2','13a3','16a4','18a5','21a6']
    # s2 = ['8b7','11b8','13b9','16b10','18b11','21b12']
    # s3 = ['8c13','11c14','13c15','16c16','18c17','21c18']
    # s4 = ['8d19','11d20','13d21','16d22','18d23','21d24']
    # s5 = ['8e25','11e26','13e27','16e28','18e29','21e30']

header = ['id', 'slice_num']
images = pd.DataFrame(
 [[1,8],
  [2,14],
  [3,16],
  [4,18],
  [5,22],
  [6,9],
  [7,11],
  [8,14],
  [9,14],
  [10,16],
  [11,17],
  [12,18],
  [13,20]], columns=header
)

def make_pairs(frame = images):
    pairs = []
    for id_1 in images['id']:
        for id_2 in images['id']:
            id_1_index = id_1 - 1
            id_2_index = id_2 - 1
            id_1_slice_num = images.iloc[id_1_index]['slice_num']
            id_2_slice_num = images.iloc[id_2_index]['slice_num']
            # pdb.set_trace()
            if abs(id_1_slice_num - id_2_slice_num) <= 2 \
                and id_1 != id_2 \
                and ( [id_1, id_2] not in pairs \
                and [id_2, id_1] not in pairs):
                pairs.append([id_1,id_2])
                # pairs_debug.append([j,l])
    return pairs
pairs = make_pairs(frame=images)

# [[1, 6], [2, 3], [2, 8], [2, 9], [2, 10], [3, 4], [3, 8], [3, 9], [3, 10], [3, 11], [3, 12], [4, 10], [4, 11], [4, 12], [4, 13], [5, 13], [6, 7], [8, 9], [8, 10], [9, 10], [10, 11], [10, 12], [11, 12], [12, 13]]
