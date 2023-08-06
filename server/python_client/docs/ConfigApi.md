# http_client.ConfigApi

All URIs are relative to *http://localhost:9000/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_config**](ConfigApi.md#get_config) | **GET** /config/connector/{id} | GetConfig


# **get_config**
> ApiResponse get_config(id, connector)

GetConfig

Get connector config.

### Example

* Api Key Authentication (ca_key):

```python
import time
import http_client
from http_client.api import config_api
from http_client.model.api_response import ApiResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:9000/api
# See configuration.py for a list of all supported configuration parameters.
configuration = http_client.Configuration(
    host = "http://localhost:9000/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ca_key
configuration.api_key['ca_key'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ca_key'] = 'Bearer'

# Enter a context with an instance of the API client
with http_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = config_api.ConfigApi(api_client)
    id = "id_example" # str | Connector Id, e.g. sfexpress.test
    connector = "connector_example" # str | Connector-self Name
    cache = "cache_example" # str | Cache that customer ID and name is matched. If the value is `disable`, the cache will not be checked (optional)

    # example passing only required values which don't have defaults set
    try:
        # GetConfig
        api_response = api_instance.get_config(id, connector)
        pprint(api_response)
    except http_client.ApiException as e:
        print("Exception when calling ConfigApi->get_config: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # GetConfig
        api_response = api_instance.get_config(id, connector, cache=cache)
        pprint(api_response)
    except http_client.ApiException as e:
        print("Exception when calling ConfigApi->get_config: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Connector Id, e.g. sfexpress.test |
 **connector** | **str**| Connector-self Name |
 **cache** | **str**| Cache that customer ID and name is matched. If the value is &#x60;disable&#x60;, the cache will not be checked | [optional]

### Return type

[**ApiResponse**](ApiResponse.md)

### Authorization

[ca_key](../README.md#ca_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User ID and Name has been checked successfully. |  -  |
**400** | Invalid input. |  -  |
**404** | id check failed. |  -  |
**500** | id retrieval failed. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

