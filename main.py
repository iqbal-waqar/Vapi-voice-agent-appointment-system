from fastapi import FastAPI, Request
import logging

from backend.routes.appointment import router
from backend.database.database import init_db


logging.basicConfig(level=logging.INFO)

app = FastAPI()


init_db()


@app.middleware("http")
async def log_requests(request: Request, call_next):

    if request.url.path == "/schedule_appointment":

        body = await request.body()

        logging.info(f"Raw request body: {body.decode()}")

    response = await call_next(request)

    return response


app.include_router(router)



if __name__=="__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=4444,
        reload=True
    )
