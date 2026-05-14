from fastapi import FastAPI

from src.api.routes.chat_routes import (
    router as chat_router
)

from src.api.routes.stream_routes import (
    router as stream_router
)

from src.api.routes.feedback_routes import (
    router as feedback_router
)

from src.feedback.feedback_database import (
    initialize_feedback_database
)

initialize_feedback_database()

app = FastAPI(

    title="Industrial Agentic AutoML",

    version="1.0.0"
)

app.include_router(chat_router)

app.include_router(stream_router)

app.include_router(feedback_router)


@app.get("/")
def root():

    return {

        "message": "Industrial Agentic AutoML API"
    }