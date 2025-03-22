from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

user_data_list: list[dict] = []
tasks_list: list[dict] = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # This allows all headers
)
class User(BaseModel):
    username: str
    password: str 

class Task(BaseModel):
    task: str
    deadline: str 
    user: str
    
@app.get("/login/", response_class=HTMLResponse)
async def get_login_page():
    with open("index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/register/", response_class=HTMLResponse)
async def get_register_page():
    with open("register.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200) 

@app.get("/main/", response_class=HTMLResponse)
async def get_main_page():
    with open("main.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/login/")
async def user_login(user: User):
    for existing_user in user_data_list:
        if existing_user["username"] == user.username:
            if existing_user["password"] == user.password:
                return JSONResponse({"status": "Logged in"})
            else:
                return JSONResponse({"status": "Incorrect password"})
    return JSONResponse({"status": "User not found"})

@app.post("/create_user/")
async def create_user(new_user: User):
    for user in user_data_list:
        if user["username"] == new_user.username:
            return {"status": "User already exists"}
    
    user_data_list.append({"username": new_user.username, "password": new_user.password})
    df = pd.DataFrame(user_data_list)
    df.to_csv("user_data.csv", index=False)
    return {"status": "User Created"}

@app.post("/create_task/")
async def create_task(task: Task):
    df = pd.read_csv(TASKS_FILE)
    df.loc[len(df)] = [task.task, task.deadline, task.user]
    df.to_csv(TASKS_FILE, index = False)    
    return {"status": "Task Created"}

@app.get("/get_tasks/")
async def get_tasks(name: str):
    df = pd.read_csv(TASKS_FILE)
    df = df[df["user"] == name]
    task_list = []
    for _, row in df.iterrows():
        task_list.append([row.task, row.deadline, row.user])
    
    return {"tasks": [task_list]}
