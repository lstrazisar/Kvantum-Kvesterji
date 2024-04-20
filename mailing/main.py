from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
import uvicorn
from gmail.gmail_api import GmailApi 
from pydantic import BaseModel

class Message(BaseModel):
    receiver: str
    subject: str
    body: str


class Mailing_service:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.router.add_api_route("/send_message", self.send_message, methods=["POST"])
        self.gmail_service = GmailApi()
    
    
    def send_message(self, message: Message):

        self.gmail_service.send_message("huntthedeals@gmail.com", message.receiver, message.subject, message.body)

        return JSONResponse(
            status_code=200,
            content={"message": "Email sent successfully"},
        )
    

if __name__ == "__main__":
    app = FastAPI()
    mailing = Mailing_service()
    app.include_router(mailing.router)
    uvicorn.run(app, host="0.0.0.0", port=8000)