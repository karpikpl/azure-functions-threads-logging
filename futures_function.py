import azure.functions as func
import logging
import concurrent.futures
from opentelemetry import trace
from opentelemetry.propagate import extract
from requests import get

bp = func.Blueprint()
tracer = trace.get_tracer(__name__)

# import thread local storage
from azure_functions_worker.dispatcher import (
    _invocation_id_local as tls,
)
# class Dummy:
#     def __init__(self):
#         self.invocation_id = ""

# tls = Dummy()

@bp.route(route="http_futures", auth_level=func.AuthLevel.FUNCTION)
def http_func(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        carrier = {
            "traceparent": context.trace_context.Traceparent,  # type: ignore
            "tracestate": context.trace_context.Tracestate,  # type: ignore
        }
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

            name = req.params.get('name')
            if not name:
                try:
                    req_body = req.get_json()
                except ValueError:
                    pass
                else:
                    name = req_body.get('name')


            with concurrent.futures.ThreadPoolExecutor() as executor:
                future1 = executor.submit(foo, context, "one arg")
                future2 = executor.submit(foo, context, "another arg")
                future3 = executor.submit(foo, context, "third arg")  # Add more futures as needed

                for future in concurrent.futures.as_completed([future1, future2, future3]):
                    try:
                        result = future.result()
                        logging.info(f"Thread result: {result}")
                        # process result if needed
                    except Exception as exc:
                        logging.error(f'Generated an exception: {exc}')

            if name:
                return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
            else:
                return func.HttpResponse(
                    "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
                    status_code=200
                )

def foo(context, st: str) -> str:
    # invocation_id_local = sys.modules[
    #     "azure_functions_worker.dispatcher"
    # ]._invocation_id_local
    # invocation_id_local.v = context.invocation_id
    with tracer.start_as_current_span(f"foo {st} operation", kind=trace.SpanKind.INTERNAL):

        tls.invocation_id = context.invocation_id

        logging.info(f"THREAD: Running thread for arg {st}")
        response = get('https://www.google.com')
        logging.info(f"THREAD: Thread {st} result: {response.status_code}")
        return context.invocation_id