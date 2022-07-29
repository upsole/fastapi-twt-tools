from twt_tools.thread import Thread
from twt_tools.user import User
from fastapi.responses import FileResponse
import os

async def thread_json(url):
    thread = Thread(url=url, thread_name=url, output_dir="")
    return thread.thread

async def thread_pdf(url):
    thread = Thread(url=url, thread_name=url, output_dir="")
    await thread.async_build_markdown()
    thread.build_pdf()
    thread.cleanup()

    filepath = f"{thread.thread_name}.pdf"
    return FileResponse(filepath)

def delete_pdf(name):
    os.remove(f"{name}.pdf")
