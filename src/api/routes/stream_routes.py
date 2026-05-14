from fastapi import APIRouter
from fastapi.responses import StreamingResponse

import json
import time


router = APIRouter()


def fake_stream():

    for i in range(5):

        payload = {

            "step": i,

            "status": "running"
        }

        yield f"data: {json.dumps(payload)}\n\n"

        time.sleep(1)


@router.get("/stream")
def stream_endpoint():

    return StreamingResponse(

        fake_stream(),

        media_type="text/event-stream"
    )