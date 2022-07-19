# Information extraction pipeline from ESG documents 

The project requires the user to have the latest version of conda and python installed in path. 

1. Create a new environment in Conda using the command

```
conda create -n <env> python==3.8

```

2.Install the dependencies using the requirements.txt file

```
conda activate <env>
pip install -r requirements.txt

```
3.Create an instance in neo4j Aura DB and get your DB credentials and save it in credentials.env 

4.Download the folder for the purpose of classification.The below mentioned link contains the pretrained weights of ESG BERT models:
  Create and folder with the name bert-models in the root directory and place the contents of the drive in it.

https://drive.google.com/drive/folders/1N7Biv16TCoK3LTFYihSPwHU6ZNrM6rvn?usp=sharing

5. Open localhost and enter the credentials for the database using the following command: 

```
cd Model
uvicorn api:app --reload

```
Now your webapplication gets hosted through localhost.

Enter your database credentials to enter to your database.

You should be redirected to Uploadfiles route where you need to upload all the input files.
* Input files:-
 - corpus.txt(Should be sentence tokenized)
 - relations.txt
 - props.txt
 
You will be redirected to aura db where you can play with the knowledge-graph using cypher commands.

6. Deactivate the environment once you are done. 
```
conda deactivate 

```

