import uvicorn
import dotenv
import os
dotenv.load_dotenv()
from api.db.crud import _reset_db

PORT = int(os.environ.get("PORT"))
HOST = str(os.environ.get("HOST"))

if __name__ == "__main__":
    print("Setting up DB")
    _reset_db()
    print("Starting server...")
    uvicorn.run("api.app:app", host=HOST, port=PORT, reload=True, proxy_headers=True, workers=4)
