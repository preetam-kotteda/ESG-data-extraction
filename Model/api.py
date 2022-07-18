from fastapi import FastAPI,Form,Request,status
from fastapi.middleware.cors import CORSMiddleware
from typing import Union , List
from fastapi import FastAPI, File, UploadFile
import pickle
from mbem import extract_data
from db import run_db,creds,authenticate_creds,reset_db
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from git import Repo

app = FastAPI()

origins = ['https://localhost:3000']

inputs_dir = "..\inputs\\"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})

@app.get("/",response_class=HTMLResponse)
def read_root(request:Request):
    return RedirectResponse(url = "/database-creds/")

# @app.get("/items/", response_class=HTMLResponse)
# async def read_items():
#     return index.html

@app.get("/database-creds/")
def getedentials(request:Request):
    return templates.TemplateResponse('index.html', context={'request': request})

@app.get("/uploadfiles/")
def get_upload_files(request:Request):
    return templates.TemplateResponse('uploadfiles.html', context={'request': request})

@app.post("/database-creds/")
def postcredentials(request:Request,uri:str= Form(),username:str = Form(),password:str = Form()):
    db_creds = authenticate_creds(uri,username,password)
    if db_creds:
        with open(inputs_dir+'creds_data.pkl', 'wb') as outp:
            pickle.dump(db_creds, outp, pickle.HIGHEST_PROTOCOL)
        return RedirectResponse("/uploadfiles/",status_code=status.HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse('invalidcreds.html',context = {'request':request})

@app.post("/uploadfiles/")
async def create_upload_files(request:Request,files: List[UploadFile]):
    if not files:
        return RedirectResponse(url = "/uploadfiles/")
    else:
        for file in files:
            try:
                contents = await file.read()
                with open(inputs_dir + file.filename, 'wb') as f:
                    f.write(contents)
            except Exception:
                return RedirectResponse(url = "/uploadfiles/")
            finally:
                await file.close()

    return RedirectResponse("/knowledge-graph/",status_code=status.HTTP_303_SEE_OTHER)


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
    return RedirectResponse("https://browser.neo4j.io/?connectURL=neo4j%2Bs%3A%2F%2Fneo4j%406a12d69e.databases.neo4j.io%2F")




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


