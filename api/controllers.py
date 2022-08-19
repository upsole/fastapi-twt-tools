from twt_tools.thread import Thread
from twt_tools.lib.lib import scrape_tweet
from twt_tools.user import User
from fastapi.responses import FileResponse, HTMLResponse
from api.db.crud import session_scope, insert_job, update_job, query_job, delete_job
import os

FILES_DIR = "files/"
DOMAIN_NAME = str(os.environ.get("DOMAIN_NAME"))

async def thread_json(url):
    thread = Thread(url=url, thread_name=url, output_dir="")
    return thread.thread

async def single_tweet(url):
    return scrape_tweet(url)


def scrape_thread_to_pdf(url, job_id):
    try:
        thread = Thread(url=url, thread_name=url, output_dir=FILES_DIR)
        thread.build_markdown()
        thread.build_pdf()
        thread.cleanup()

        # filename = FILES_DIR+thread.thread_name+".pdf"
        filename = os.path.join(FILES_DIR, thread.thread_name + ".pdf")
        if os.path.isfile(filename):
            with session_scope() as s:
                update_job(s, job_id, file=filename, status="success")
        else:
            with session_scope() as s:
                update_job(s, job_id, status="failed")
    # if build panics -> set job to failed
    except:
        with session_scope() as s:
            update_job(s, job_id, status="failed")

async def check_job_status(job_id):
    with session_scope() as s:
        job = query_job(s, job_id)
    if job["status"] == "success": return {"status": job["status"], "format": job["format"], "downloadUrl": DOMAIN_NAME + "/file/"+ str(job["id"]) }
    return job

async def serve_file(job_id):
    with session_scope() as s:
        job = query_job(s, job_id)
    if job["status"] != "success": 
        raise BaseException("Job not finished or not found.")
    if job["format"] == "pdf":
        return FileResponse(job["file"])
    elif job["format"] == "html":
        with open(job["file"], "r") as file:
            html = file.read()
        return HTMLResponse(html)

def delete_file_and_record(job_id):
    with session_scope() as s:
        job = query_job(s, job_id)

    if job["status"] == "success":
        print("File sent, deleting job from DB and file")
        with session_scope() as s:
            delete_job(s, job_id)
        os.remove(job["file"])


async def _user_data(url):
    pass

def build_html(url, limit, job_id):
    try:
        archive = User(url, output_dir=FILES_DIR)
        filename = os.path.join(FILES_DIR, archive.get_user().username + ".html")
        archive.build_html(limit=limit)

        if os.path.isfile(filename):
            with session_scope() as s:
                update_job(s, job_id, file=filename, status="success")
        else:
            with session_scope() as s:
                update_job(s, job_id, status="failed")
    except:
    # if build panics -> set job to failed
        with session_scope() as s:
            update_job(s, job_id, status="failed")
