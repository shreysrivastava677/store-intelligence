import time
import uuid

from fastapi import Request

from app.logger import logger


async def logging_middleware(
    request: Request,
    call_next
):

    trace_id = str(
        uuid.uuid4()
    )

    start_time = time.time()

    response = await call_next(
        request
    )

    latency_ms = round(
        (
            time.time()
            - start_time
        ) * 1000,
        2
    )

    logger.info(
        {
            "trace_id": trace_id,
            "endpoint": request.url.path,
            "method": request.method,
            "status_code": response.status_code,
            "latency_ms": latency_ms
        }
    )

    response.headers[
        "X-Trace-ID"
    ] = trace_id

    return response