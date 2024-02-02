# About

Using Azure Functions to run code concurrently using threads, futures and asyncio.

## Motivation

Azure Functions use thread local to store invocation id, which causes logs to be dropped from multi-threaded applications.

This solution (based on stack overflow answer) shows how to add invocation id to keep logs from secondary threads.

## Sources

* Thanks to `Nizam` for his [Stack Overflow Response](https://stackoverflow.com/questions/55934085/how-to-redirect-logs-from-secondary-threads-in-azure-functions-using-python)
* [Azure Functions Worker Dispatcher](https://github.com/Azure/azure-functions-python-worker/blob/main/azure_functions_worker/dispatcher.py)


## Local settings

`local.settings.json`:

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "APPLICATIONINSIGHTS_CONNECTION_STRING": "InstrumentationKey=xxx",
    "OTEL_SERVICE_NAME":"python-threaded-logging",
    "OTEL_EXPERIMENTAL_RESOURCE_DETECTORS": "azure_app_service",
    "OTEL_PYTHON_LOG_CORRELATION": "true"
  }
}
```