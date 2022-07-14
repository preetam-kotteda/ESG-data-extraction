import pandas as pd
import sys
from csv import writer
from csv import reader
import spacy
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English

nlp = spacy.load("en_core_web_sm")

input_csv = sys.argv[1]
input_props = sys.argv[2]

df = pd.read_csv(input_csv)
tokenizer = Tokenizer(nlp.vocab)
df = df.drop(df.columns[[0]],axis = 1)
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
        for token in doc:
            if token.lemma_ in actual_props_lemmatized:
                df['ontology_entry'][i] = str(token.lemma_)
            # print(token, token.lemma, token.lemma_)
df.to_csv('../outputs/final_output.csv')
