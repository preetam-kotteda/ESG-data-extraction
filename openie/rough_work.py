from openie import StanfordOpenIE
import pandas as pd
properties = {
    'openie.affinity_probability_cap': 2 / 3,
}

with StanfordOpenIE(properties=properties) as client:
    text = 'We aim for achieving carbon neutrality in operations by 2050'
    print('Text: %s.' % text)
    for triple in client.annotate(text):
        print('|-', triple)