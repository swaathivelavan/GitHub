import json

import uvicorn
import ast
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from db_setup import db
from schemas import Repository, RepositoryCollection

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/repositories", response_model=RepositoryCollection)
def get_repositories_from_GitHub(username: str):
    listUsers = username.split(",")
    list = []
    for user in listUsers:
        if not user:
            raise Exception("Unable to retrieve repositories - Empty Username")
        url = f"https://api.github.com/users/{user}/repos"
        response_information = requests.get(url)  # response is a byte object
        if response_information.status_code == 404:
            raise Exception("Username Invalid")
        dict_str = json.loads(response_information.content.decode('utf-8'))
        for repo in ast.literal_eval(str(dict_str)):
            repo = Repository(repository_name=repo['name'],repo_link=repo['git_url'])
            list.append(repo)
        db.child("Repository").child(user).set(json.loads(RepositoryCollection(repositories=list).json()))

    return RepositoryCollection(repositories=list, username=username)

@app.get("/db_repositories")
def get_repositories_from_database(username: str):
    if not username:
        raise Exception("Unable to retrieve repositories - Empty Username")
    ans = db.child("Repository").child(username).get()

    return ans.val()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run(app, port=8000, host="0.0.0.0")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
