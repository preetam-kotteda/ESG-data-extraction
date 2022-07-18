import pandas as pd
import sys
from csv import writer
from csv import reader
import spacy
from spacy.tokenizer import Tokenizer

from ner import entity_recog

def extract_data(input_corpus,input_relations,input_class_num,input_props):
    nlp = spacy.load("en_core_web_sm")
    # input_csv = sys.argv[1]
    # input_props = sys.argv[2]
    df = entity_recog(input_corpus,input_relations,input_class_num)
    # df = df.drop(df.columns[[0]],axis = 1)
    df['ontology_entry'] = 'NULL'

    with open(input_props,'r') as f:
        actual_props = f.readline().split(',')

    actual_props_lemmatized = []

    for prop in actual_props:
        prop_doc = nlp(prop)
        for token in prop_doc:
            actual_props_lemmatized.append(token.lemma_)

    for i in range(df.shape[0]):
        if str(df['relevant'][i]) == str(1):
            doc = nlp(df['sentence'][i])
            for j in range(len(doc)):
                if ((doc[j].lemma_.lower()) in actual_props_lemmatized) and (df['ontology_entry'][i] == "NULL"):
                    if(doc[j].lemma_.lower() == 'scope'):
                        df['ontology_entry'][i] = str(doc[j].lemma_) + str(doc[j+1].lemma_)
                    else:
                        df['ontology_entry'][i] = str(doc[j].lemma_)
            if df['ontology_entry'][i] == "NULL":
                df['relevant'][i] = '0'
                # print(token, token.lemma, token.lemma_)
    df = df.loc[lambda df: df['relevant'] == 1]
    df.to_csv('../outputs/final_output.csv')
    return None

# extract_data(r"D:\Work\full pipeline\ESG-extraction\inputs\corpus.txt",r"D:\Work\full pipeline\ESG-extraction\inputs\relations.txt","25",r"D:\Work\full pipeline\ESG-extraction\inputs\props.txt")
