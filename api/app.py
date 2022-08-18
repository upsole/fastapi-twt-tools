import dotenv
import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from snscrape.base import ScraperException


from api.controllers import thread_json, scrape_thread_to_pdf, delete_pdf, user_json, user_data, user_html, single_tweet
from api.lib import is_valid_tweet, is_valid_username
from api.db.crud import session_scope, insert_job


dotenv.load_dotenv()
app = FastAPI()
ORIGIN= os.environ.get("CORS_ORIGIN")
origins = [ORIGIN]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET", "POST"])


@app.get("/ok")
def health_route():
    return {"message": "Server is running!"}


# TODO Thread HTML

@app.get("/thread/{id}")
async def get_pdf(background_tasks: BackgroundTasks, id):
    if not is_valid_tweet(id): 
        raise HTTPException(status_code=400, detail="Invalid tweet ID")

    try:
        # background_tasks.add_task(delete_pdf, "build_files/"+id)
        await single_tweet(id)
        # BUG it's still blocking wtf?
        background_tasks.add_task(scrape_thread_to_pdf, id)
        with session_scope() as s:
            new_job = insert_job(s, "build_files/"+id+".pdf")
            print(new_job)

    except ScraperException:
        raise HTTPException(status_code=404, detail="Tweet not found")
    # except:
    #     raise HTTPException(status_code=500, detail="Most useful error of your life")

    # TODO return job as JSON
    return {"job": new_job}

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
