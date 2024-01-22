# About

Using Azure Functions to run code concurrently using threads, futures and asyncio.

## Motivation

Azure Functions use thread local to store invocation id, which causes logs to be dropped from multi-threaded applications.

This solution (based on stack overflow answer) shows how to add invocation id to keep logs from secondary threads.

## Sources

* Thanks to `Nizam` for his [Stack Overflow Response](https://stackoverflow.com/questions/55934085/how-to-redirect-logs-from-secondary-threads-in-azure-functions-using-python)
* [Azure Functions Worker Dispatcher](https://github.com/Azure/azure-functions-python-worker/blob/main/azure_functions_worker/dispatcher.py)
