from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    print("response.data",response.data)
    data = {}
    data['status'] = 0
    data['data'] =[]
    data['errors'] = [response.data.get('detail')]
    response.data = data
    return response
