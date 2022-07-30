from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from api.controllers import thread_json, thread_pdf, delete_pdf, user_json, user_data

app = FastAPI()

origins = ["http://localhost:5173"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET", "POST"])

@app.get("/ok")
def health_route():
    return {"message": "Server is running!"}


@app.post("/thread/json")
async def get_json(id):
    res = await thread_json(id)
    return res


@app.post("/thread", response_class=FileResponse)
async def get_pdf(background_tasks: BackgroundTasks, id):
    background_tasks.add_task(delete_pdf, id)
    res = await thread_pdf(id)
    return res

# TODO
# @app.get("/user")
# async def get_user(id):
#     res = await user_data(id)
#     return res

@app.post("/user/archive")
async def get_json_archive(id, limit=10):
    res = await user_json(id, int(limit))
    return res

# TODO Scrap Only media files of thread
