from fastapi import FastAPI
# from fastapi.responses import JSON

app = FastAPI()

@app.get("/ok")
def health_route():
     return {"msg": "Server is running!"}
