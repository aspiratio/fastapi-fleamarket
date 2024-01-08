from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def example():
    return {"message": "Hello World!"}
