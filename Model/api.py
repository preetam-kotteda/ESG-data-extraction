from fastapi import FastAPI,Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Union , List
from fastapi import FastAPI, File, UploadFile
import pickle
from mbem import extract_data
from db import run_db,creds,authenticate_creds,reset_db
app = FastAPI()

origins = ['https://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

inputs_dir = "..\inputs\\"


@app.get("/")
def read_root():
    return {"message":"append /docs to url to view the fastapi interface"}



@app.post("/database-creds/")
async def postcredentials(uri:str= Form(),username:str = Form(),password:str = Form()):
    db_creds = authenticate_creds(uri,username,password)
    if db_creds:
        with open(inputs_dir+'creds_data.pkl', 'wb') as outp:
            pickle.dump(db_creds, outp, pickle.HIGHEST_PROTOCOL)
        return{"username":db_creds.username}
    else:
        return {"message":"Invalid creds"}




@app.post("/uploadfiles/")
async def create_upload_files(up_files: List[UploadFile]):
    if not up_files:
        return {"message": "No upload file sent"}
    else:
        for file in up_files:
            try:
                contents = await file.read()
                with open(inputs_dir + file.filename, 'wb') as f:
                    f.write(contents)
            except Exception:
                return {"message": "There was an error uploading the file(s)"}
            finally:
                await file.close()

    return {"message": f"Successfuly uploaded {[file.filename for file in up_files]}"}




@app.get("/knowledge-graph/")
async def get_knowledge_graph():
    try:
        # extract_data(inputs_dir+"corpus.txt",inputs_dir+"relations.txt","25",inputs_dir+"props.txt")
        print("extracted data")
    except:
        return {"message":"Failed in running model"}
    db_creds = None
    try:
        with open(inputs_dir+'creds_data.pkl', 'rb') as inp:
            db_creds = pickle.load(inp)
            print(db_creds.username)
    except:
        return{"message":"Unable to open pkl file"}
    if db_creds:
        try:
            run_db(db_creds)
            print("Ran db")
        except:
            return{"message":"Failed to enter data to db"}
    else:
        return{"message":"Please enter valid creds!"}
    return {"Sucessful knowledge graph!"}




@app.get("/reset-db")
async def reset():
    db_creds = None
    with open(inputs_dir+'creds_data.pkl', 'rb') as inp:
            db_creds = pickle.load(inp)
    try:
        reset_db(db_creds)
    except:
        return{"message":"Failed to reset db"}
    return{"message":"Sucessfull reset"}


