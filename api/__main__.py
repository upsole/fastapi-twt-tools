import uvicorn
import dotenv
import os
dotenv.load_dotenv()

PORT = os.environ.get("PORT")
HOST = os.environ.get("HOST")

if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run("api.app:app", host=HOST, port=int(PORT), reload=True, proxy_headers=True)
