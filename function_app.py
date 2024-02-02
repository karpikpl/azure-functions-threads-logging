import os
import azure.functions as func
from azure.monitor.opentelemetry import configure_azure_monitor


from threads_function import bp as http_threads
from futures_function import bp as http_futures
from asyncio_function import bp as http_asyncio

APPLICATIONINSIGHTS_CONNECTION_STRING = "APPLICATIONINSIGHTS_CONNECTION_STRING"
LOGGER_PREFIX = "myapp_logger"

if os.environ.get(APPLICATIONINSIGHTS_CONNECTION_STRING) is not None:
    configure_azure_monitor(
        connection_string=os.environ.get(APPLICATIONINSIGHTS_CONNECTION_STRING),
        logger_name=LOGGER_PREFIX,
    )

app = func.FunctionApp()
app.register_functions(http_threads)
app.register_functions(http_futures)
app.register_functions(http_asyncio)