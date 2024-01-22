import azure.functions as func
import logging
import threading

# import thread local storage
from azure_functions_worker.dispatcher import (
    _invocation_id_local as tls,
)
bp = func.Blueprint()

@bp.route(route="http_threads", auth_level=func.AuthLevel.FUNCTION)
def http_threads(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    thread1 = threading.Thread(
        target=foo,
        args=(
            context,
            "one arg",
        ),
    )
    thread2 = threading.Thread(
        target=foo,
        args=(
            context,
            "another arg",
        ),
    )
    thread3 = threading.Thread(
        target=foo,
        args=(
            context,
            "yet another arg",
        ),
    )
    thread1.start()
    thread2.start()
    thread3.start()
    logging.info("All threads started successfully!")

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

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

    tls.invocation_id = context.invocation_id

    logging.info(f"Starting thread for arg {st}")
    return context.invocation_id