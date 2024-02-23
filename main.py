from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils import *
import uvicorn, logging

app = FastAPI()
logging.basicConfig(filename="logs/api_log.log",level=logging.DEBUG,
                    format='%(asctime)s - %(name)s -%(threadName)s - %(levelname)s - %(message)s')

class chatbot(BaseModel):
    input_condition : str

@app.post("/askAI")
async def ask_ai(input:chatbot):
    input_condition = input.input_condition
    answer = get_disease_classification(input_condition=input_condition)
    return answer

# if __name__ == '__main__':
#     # uvicorn.run(app=app, host = "0.0.0.0",
#     #             port = 8080, server_header = False,
#     #             timeout_keep_alive = 10, workers = 4, log_level = 'debug')
#     uvicorn.run(app=app)


