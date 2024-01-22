import azure.functions as func

from threads_function import bp as http_threads
from futures_function import bp as http_futures
from asyncio_function import bp as http_asyncio

app = func.FunctionApp()
app.register_functions(http_threads)
app.register_functions(http_futures)
app.register_functions(http_asyncio)