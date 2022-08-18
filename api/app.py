import dotenv
import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from snscrape.base import ScraperException


from api.controllers import (
    delete_pdf,
    scrape_thread_to_pdf,
    serve_thread_pdf,
    user_html,
    single_tweet,
)
from api.lib import is_valid_tweet, is_valid_username
from api.db.crud import session_scope, insert_job


dotenv.load_dotenv()
app = FastAPI()
ORIGIN = os.environ.get("CORS_ORIGIN")
origins = [ORIGIN]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET", "POST"])


@app.get("/ok")
def health_route():
    return {"message": "Server is running!"}


# TODO Thread HTML


@app.get("/thread/{id}", status_code=202)
async def get_pdf(background_tasks: BackgroundTasks, id):
    if not is_valid_tweet(id):
        raise HTTPException(status_code=400, detail="Invalid tweet ID")

    try:
        await single_tweet(id)
        with session_scope() as s:
            new_job = insert_job(s)
            print(new_job)
        background_tasks.add_task(scrape_thread_to_pdf, id, new_job["id"])

    except ScraperException:
        raise HTTPException(status_code=404, detail="Tweet not found")

    # json
    # TODO make this dev dependendant // In prod only return job object, no url
    return {"job": new_job, "url": "http://localhost:4000/pdf/"+ str(new_job["id"])}


@app.get("/pdf/{job_id}")
async def serve_pdf(background_tasks: BackgroundTasks, job_id):
    try:
        res = await serve_thread_pdf(job_id)
        background_tasks.add_task(delete_pdf, job_id)
        return res
    except:
        raise HTTPException(status_code=400, detail="Wrong id")


@app.get("/user/archive", response_class=HTMLResponse)
async def get_user_html(id, limit=10):
    if int(limit) > 500 or int(limit) == 0:
        limit = 500

    if not is_valid_username(id):
        raise HTTPException(status_code=400, detail="Invalid username")

    try:
        res = await user_html(id, int(limit))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid username")
    except AttributeError:
        raise HTTPException(status_code=404, detail="User not found")

    return res


# TODO Scrap Only media files of thread
