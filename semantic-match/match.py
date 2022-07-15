import gensim.downloader as api
import torch
import pandas as pd
import sys
from gensim.parsing.preprocessing import remove_stopwords
import gensim

input_csv = sys.argv[1]
input_relations = sys.argv[2]
input_class_num = sys.argv[3]
# import torchtext
# api.BASE_DIR= 'D:\Work'
# print(list(api.info()['models'].keys()))
glove = api.load('glove-wiki-gigaword-50')
df = pd.read_csv(input_csv)
df = df.drop(df.columns[[0]],axis = 1)
df['relevant'] = '0'
with open(input_relations,'r') as f:
    actual_relations = f.readline().split(',')
    # print(actual_relations)
for i in range(df.shape[0]):
    if str(df['class_num'][i]) == str(input_class_num):
        relations = df['relation'][i].split(',')
        max_sim = 0
        max_sim_word = ""
        for actual_relation in actual_relations:
            sim = 0
            sim_word = ""
            filtered_relation_tokens = []
            for relation in relations:
                filtered_relation_tokens=  filtered_relation_tokens + (list(gensim.utils.tokenize(remove_stopwords(relation),deacc = True)))
            a = torch.from_numpy(glove[actual_relation]).unsqueeze(0)
            for token in filtered_relation_tokens:
                try:
                    b = torch.from_numpy(glove[token]).unsqueeze(0)
                except:
                    continue
                # sim = max(sim,float(torch.cosine_similarity(a,b)[0]))
                cosine_sim = torch.cosine_similarity(a,b)[0]
                if sim < float(cosine_sim) :
                    sim = float(cosine_sim)
                    sim_word = token
            if max_sim < sim:
                max_sim = max(max_sim,sim)
                max_sim_word = sim_word
            if(max_sim>=0.7):
                df['relevant'][i] = '1'
                df['relation'][i] = max_sim_word    
df.to_csv('../outputs/matched_output.csv')

