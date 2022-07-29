from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from api.controllers import thread_json, thread_pdf, delete_pdf, user_json, user_data

app = FastAPI()

@app.get("/ok")
def health_route():
     return {"message": "Server is running!"}

@app.get("/thread/json")
async def get_json(id):   
    res = await thread_json(id)
    return res

@app.get("/thread", response_class=FileResponse)
async def get_pdf(background_tasks: BackgroundTasks, id):
    background_tasks.add_task(delete_pdf, id)
    res = await thread_pdf(id)
    return res


# TODO
# @app.get("/user")
# async def get_user(id):
#     res = await user_data(id)
#     return res

@app.get("/user/archive")
async def get_json_archive(id, limit=10):
    res = await user_json(id, int(limit))
    return res
    

# TODO Scrap Only media files of thread
