from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def test_connection():
    return {"status": "okay"}

@app.websocket('/ws')
async def web_socket(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(data)


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
