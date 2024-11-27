from fastapi import FastAPI

app = FastAPI()


@app.get("/api/chatrooms/")
async def list_chatrooms():
    return {"chatrooms": ["Room1", "Room2"]}
