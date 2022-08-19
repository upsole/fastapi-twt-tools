import dotenv
import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from snscrape.base import ScraperException

from api.controllers import (
    delete_file_and_record,
    scrape_thread_to_pdf,
    serve_file,
    build_html,
    check_job_status,
    single_tweet,
    DOMAIN_NAME,
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

@app.get("/thread/{id}", status_code=202)
async def get_pdf(background_tasks: BackgroundTasks, id):
    if not is_valid_tweet(id):
        raise HTTPException(status_code=400, detail="Invalid tweet ID")

    try:
        await single_tweet(id)
        with session_scope() as s:
            new_job = insert_job(s, "pdf")
        background_tasks.add_task(scrape_thread_to_pdf, id, new_job["id"])

    except ScraperException:
        raise HTTPException(status_code=404, detail="Tweet not found")

    # TODO make this dev dependendant // In prod only return job object, no url
    return {"job": new_job, "url": DOMAIN_NAME + "/job/"+ str(new_job["id"])}

@app.get("/job/{job_id}", status_code=202)
async def check_job(job_id):
    try:
        res = await check_job_status(job_id)
        return res
    except:
        raise HTTPException(status_code=400, detail="Wrong id")

@app.get("/user", status_code=202)
async def get_user_html(background_tasks: BackgroundTasks, id, limit=10):
    if not is_valid_username(id):
        raise HTTPException(status_code=400, detail="Invalid username")

    try:
        with session_scope() as s:
            new_job = insert_job(s, "html")
        background_tasks.add_task(build_html, id, int(limit), new_job["id"])

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid username")
    except AttributeError:
        raise HTTPException(status_code=404, detail="User not found")

    except ScraperException:
        raise HTTPException(status_code=404, detail="Tweet not found")

    return {"job": new_job, "url": DOMAIN_NAME + "/job/"+ str(new_job["id"])}

@app.get("/file/{job_id}")
async def serve(background_tasks: BackgroundTasks, job_id):
    try:
        res = await serve_file(job_id)
        background_tasks.add_task(delete_file_and_record, job_id)
        return res
    except:
        raise HTTPException(status_code=400, detail="Wrong id")
