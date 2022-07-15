# from pymysql import NULL
from openie import StanfordOpenIE
import pandas as pd
# https://stanfordnlp.github.io/CoreNLP/openie.html#api
# Default value of openie.affinity_probability_cap was 1/3.
import sys
input = sys.argv[1]

properties = {
    'openie.affinity_probability_cap': 2 / 3,
}

with StanfordOpenIE(properties=properties) as client:
    # text = 'Carbon emissions reduced by 20% in 2022'
    # print('Text: %s.' % text)
    # for triple in client.annotate(text):
        # print(type(triple))
        

    # graph_image = 'graph.png'
    # # client.generate_graphviz_graph(text, graph_image)
    # # print('Graph generated: %s.' % graph_image)
    df = pd.read_csv(input)
    # df_out = pd.DataFrame(columns= ['sentence','class_num','class_name','organization','subject','relation','object','Quantity','Year'])
    df_out = pd.DataFrame(columns= ['sentence','class_num','class_name','subject','relation','object'])
    df_out1 = pd.DataFrame(columns= ['sentence','class_num','class_name','relation'])
    for i in range(df.shape[0]):
        text = df['sentence'][i]
        relations_list = ""
        for triple in client.annotate(text):
            if relations_list == "":
                relations_list = triple['relation']
            else:
                relations_list = relations_list + "," + triple['relation']
            dict = {'sentence': [text],
                        'class_num':[df['class_num'][i]],
                        'class_name':[df['class_name'][i]],
                        # 'organization':['NULL'],
                        'subject':[triple['subject']],
                        'relation':[triple['relation']],
                        'object':[triple['object']],
                        # 'Quantity':[df['quantity'][i]],
                        # 'Year':[df['year'][i]]
                        }
            # print(dict)
            df_temp = pd.DataFrame(dict)
            # print(df_temp)
            df_out = pd.concat([df_out,df_temp],ignore_index=True)
        if relations_list != "":
            dict = {
                'sentence': [text],
                'class_num':[df['class_num'][i]],
                'class_name':[df['class_name'][i]],
                'relation':[relations_list]
            }
            df_temp = pd.DataFrame(dict)
            df_out1 = pd.concat([df_out1,df_temp],ignore_index=True)
    df_out1.to_csv('../outputs/relation_output.csv') 
    df_out.to_csv('../outputs/r&s&o.csv')
    # with open('corpus.txt', encoding='utf8') as r:
    #     corpus = r.read().replace('\n', ' ').replace('\r', '')

    # triples_corpus = client.annotate(corpus[0:5000])
    # print('Corpus: %s [...].' % corpus[0:80])
    # print('Found %s triples in the corpus.' % len(triples_corpus))
    # for triple in triples_corpus[:]:
    #     print('|-', triple)
    # print('[...]')