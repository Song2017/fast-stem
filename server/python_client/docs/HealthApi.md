# http_client.HealthApi

All URIs are relative to *http://localhost:9000/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_health**](HealthApi.md#get_health) | **GET** /health | health
[**get_metrics**](HealthApi.md#get_metrics) | **GET** /metrics | metrics


# **get_health**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} get_health()

health

### Example


```python
import time
import http_client
from http_client.api import health_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:9000/api
# See configuration.py for a list of all supported configuration parameters.
configuration = http_client.Configuration(
    host = "http://localhost:9000/api"
)


# Enter a context with an instance of the API client
with http_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = health_api.HealthApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # health
        api_response = api_instance.get_health()
        pprint(api_response)
    except http_client.ApiException as e:
        print("Exception when calling HealthApi->get_health: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | App service health status |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_metrics**
> str get_metrics()

metrics

### Example


```python
import time
import http_client
from http_client.api import health_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:9000/api
# See configuration.py for a list of all supported configuration parameters.
configuration = http_client.Configuration(
    host = "http://localhost:9000/api"
)


# Enter a context with an instance of the API client
with http_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = health_api.HealthApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # metrics
        api_response = api_instance.get_metrics()
        pprint(api_response)
    except http_client.ApiException as e:
        print("Exception when calling HealthApi->get_metrics: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | App metrics |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized: provided apikey is not valid |  -  |
**500** | Server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

