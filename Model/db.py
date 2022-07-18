from re import L
from neo4j import GraphDatabase
import pickle
from git import Repo
class creds:
    def __init__(self,uri,username,password):
        self.uri = uri
        self.username = username
        self.password = password

def authenticate_creds(uri,username,password):
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        print("connected: {}".format(driver.verify_connectivity()))
        driver.close()
        db_creds = creds(uri,username,password)
        return db_creds
    except:
        return None

def run_db(db_creds):
    driver = GraphDatabase.driver(db_creds.uri, auth=(db_creds.username,db_creds.password))
    def run_code(tx,n):
        for i in range(n):
            with open("../neofiles/neo"+ str(i+1)+".txt",'r') as f:
                query = ""
                while True:
                    line = f.readline() 
                    if not line:
                        break
                    query = query + line
                tx.run(query)

    with driver.session() as session:
        session.write_transaction(run_code,5)

    driver.close()

def reset_db(db_creds):
    driver = GraphDatabase.driver(db_creds.uri, auth=(db_creds.username,db_creds.password))
    def run_code(tx):
        with open("../neofiles/reset1.txt",'r') as f:
            query = ""
            while True:
                line = f.readline() 
                if not line:
                    break
                query = query + line
            tx.run(query)

        with open("../neofiles/reset2.txt",'r') as f:
            query = ""
            while True:
                line = f.readline() 
                if not line:
                    break
                query = query + line
            tx.run(query)

    with driver.session() as session:
        session.write_transaction(run_code)

    driver.close()

# inputs_dir = "..\inputs\\"
# db_creds = None
# with open(inputs_dir+'creds_data.pkl', 'rb') as inp:
#     db_creds = pickle.load(inp)
# run_db(db_creds)
PATH_OF_GIT_REPO = r'D:\Work\full pipeline\ESG-extraction'
COMMIT_MESSAGE = "lastes commit 1"
def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')    

git_push()