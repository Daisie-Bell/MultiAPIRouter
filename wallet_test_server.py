
import time
import uvicorn

from fastapi import FastAPI

from multiapi_routes.Routes.Wallet import Wallets

app = FastAPI()

app.include_router(Wallets())

# Run the FastAPI server in a thread
def run_server():
    uvicorn.run("wallet_test_server:app", host="0.0.0.0", port=8000)

run_server()
while True:
    time.sleep(1)