from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from api.controllers import thread_json, thread_pdf, delete_pdf

app = FastAPI()

@app.get("/ok")
def health_route():
     return {"message": "Server is running!"}

@app.get("/json")
async def get_json(id):   
    res = await thread_json(id)
    return res

@app.get("/pdf", response_class=FileResponse)
async def get_pdf(background_tasks: BackgroundTasks, id):
    background_tasks.add_task(delete_pdf, id)
    res = await thread_pdf(id)
    return res

# TODO Scrap Only media files of thread
