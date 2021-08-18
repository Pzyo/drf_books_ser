
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status


def my_exception_handler(exc, context):
    response=exception_handler(exc, context)

    if not response:
        # 更细致的捕获异常
        if isinstance(exc, ZeroDivisionError):
            return Response(data={'status': 777, 'msg': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'status':999, 'msg':str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # return response
        return Response(data={'status':888, 'msg':response.data.get('detail')}, status=status.HTTP_400_BAD_REQUEST)