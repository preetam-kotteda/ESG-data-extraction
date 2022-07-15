# eval "$(conda shell.bash hook)"
cd esg-bert
conda activate ESG
python3 prediction.py ../inputs/corpus.txt
cd ../openie
python3 re_openie.py ../outputs/classification_output.csv
cd ../semantic-match
python3 match.py ../outputs/relation_output.csv ../inputs/relations.txt 25
cd ../ner-spacy
python3 ner.py ../outputs/matched_output.csv
cd ../MBEM
python3 mbem.py ../outputs/ner_output.csv ../inputs/props.txt
cd ..
conda deactivate
