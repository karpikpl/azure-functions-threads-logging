import asyncio
import json
import azure.functions as func
import logging
from requests import get, Response
from opentelemetry import trace
from opentelemetry.propagate import extract

# import thread local storage
# from azure_functions_worker.dispatcher import (
#     _invocation_id_local as tls,
# )
class Dummy:
    def __init__(self):
        self.invocation_id = ""

tls = Dummy()
bp = func.Blueprint()

@bp.route(route="http_asyncio", auth_level=func.AuthLevel.FUNCTION)
async def http_asyncio(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        carrier = {
            "traceparent": context.trace_context.Traceparent,  # type: ignore
            "tracestate": context.trace_context.Tracestate,  # type: ignore
        }
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span(
            context.function_name,
            context=extract(carrier),
            attributes={
                "function_directory": context.function_directory,
                "invocation_id": context.invocation_id,
                "function_name": context.function_name,
            },
        ):
            logging.info('Python HTTP trigger function processed a request.')

            eventloop = asyncio.get_event_loop()

            logging.info("All threads started successfully!")
            tasks = [
                asyncio.create_task(
                    invoke_get_request(eventloop, no, context)
                ) for no in range(10)
            ]

            done_tasks, _ = await asyncio.wait(tasks)
            status_codes = [d.result().status_code for d in done_tasks]

            return func.HttpResponse(body=json.dumps(status_codes),
                                    mimetype='application/json') 

async def invoke_get_request(eventloop: asyncio.AbstractEventLoop, no: int, context: func.Context) -> Response:
    # Wrap requests.get function into a coroutine
    args = (no, context)
    single_result = await eventloop.run_in_executor(
        None,  # using the default executor
        foo2,  # each task call invoke_get_request
        *args
    )
    return single_result

def foo2(no: int, context: func.Context) -> Response:
    tls.invocation_id = context.invocation_id

    logging.info(f"Starting thread for arg {no}")
    response = get('https://www.google.com')
    logging.info(f"Thread {no} result: {response.status_code}")
    
    return response