from pathlib import Path
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI
from pydantic import BaseModel

folder = Path(__file__).resolve().parent
GETFILE = folder / "serviceAccountKey.json"
cred = credentials.Certificate(str(GETFILE))
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

class Msg(BaseModel):
    sender: str
    receiver:str
    content:str

@app.post("/send")
async def sendmsg(m:Msg):
    doc = db.collection("messages").document()
    doc.set({
      "sender": m.sender,
      "receiver": m.receiver,
      "content": m.content,
      "timestamp": firestore.SERVER_TIMESTAMP
    })

    return {"status: sent, id: doc.id"}