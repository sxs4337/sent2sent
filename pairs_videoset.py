import os, csv
import pdb

path = '/home/sxs4337/itnas_ce_mil/datasets/__DO_NOT_MODIFY__Shagan_Sah_datasets/videoset_data/videoset_data/annotations/'

cats = os.listdir(path)
all_pairs = []
for cat in cats:
    videos = os.listdir(path+cat+'/')
    for video in videos:
        f = open(path+cat+'/'+video, 'rt')
        reader = csv.reader(f)
        rows = [row[2].lower() for row in reader]
        rows = rows[1:]
        pairs = [(x,rows[i+1]) for i, x in enumerate(rows[:-1]) if x != rows[i+1]]
        all_pairs.append(pairs)
all_pairs1 = [item for sublist in all_pairs for item in sublist]

pdb.set_trace()