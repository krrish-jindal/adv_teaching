from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    import  main_video.py	
    return {"message": "Hello World"}
