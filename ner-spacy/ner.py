import spacy
from spacy import displacy
import pandas as pd 
import sys

from csv import writer
from csv import reader

input = sys.argv[1]

NER = spacy.load("en_core_web_sm")
df = pd.read_csv(input)
df = df.drop(df.columns[[0]],axis = 1)
df['quantity'] = "NULL"
df['year'] = "NULL"
df['organization'] = "NULL"
df['amount'] = "NULL"
for i in range(df.shape[0]):
    if (str(df['relevant'][i]) == '1'):    
        text = df['sentence'][i]
        text1= NER(text)
        for word in text1.ents:
            # print(word.label)
            if(word.label_== "PERCENT" ):
                df['quantity'][i] = word.text
            if(word.label_ == "ORG"):
                if(df['organization'][i] == "NULL"):
                    df['organization'][i] = word.text
                else:
                    df['organization'][i] = df['organization'][i] +' '+word.text
            if(word.label_== "DATE"):
                df['year'][i] = word.text
        token_list = text.split(' ')
        for j in range(len(token_list)):
            if token_list[j].isdigit():
                if j>1 and token_list[j] != df['quantity'][i] and token_list[j] != df['year'][i] and token_list[j-1].lower() != 'scope':
                    df['amount'][i] = token_list[j]
                elif (j == 0) and token_list[j] != df['quantity'][i] and token_list[j] != df['year'][i]:
                    df['amount'][i] = token_list[j]
    # if df['object'][i] == str(df['quantity'][i]) or  df['object'][i] == str(df['year'][i]) :
    #     df['relevant'][i] = '0'  
df.to_csv('../outputs/ner_output.csv')
# text2 = NER("Gender Diversity is maintained in Socgen")
# for word in text2.ents:
#     print(word.text , word.label_)
# raw_text = "Shnieder reduced carbon emissions by 20% in 2022."
