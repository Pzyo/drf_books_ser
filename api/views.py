
from rest_framework.views import APIView
from api import models
from api.ser import BookModelSerializer
from utils.response import APIResponse

class BookAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # 查询单个和查询所有, 合在一起
        book_list = models.Book.objects.all().filter(is_delete=False)
        book_list_ser = BookModelSerializer(book_list, many=True)
        return APIResponse(data=book_list_ser.data)

    def post(self, request, *args, **kwargs):
        if isinstance(request.data, dict):
            book_ser = BookModelSerializer(data=request.data)
        elif isinstance(request.data, list):
            book_ser = BookModelSerializer(data=request.data, many=True)
        else:
            return APIResponse(code=400, msg='fail', status=400)

        book_ser.is_valid(raise_exception=True)
        book_ser.save()
        return APIResponse(data=book_ser.data)

    def put(self, request, *args, **kwargs):
        if kwargs.get('pk', None):
            book = models.Book.objects.filter(pk=kwargs.get('pk', None)).first()
            book_ser = BookModelSerializer(instance=book, data=request.data)
            book_ser.is_valid(raise_exception=True)
            book_ser.save()
            return APIResponse(data=book_ser.data)
        else:
            book_ser = BookModelSerializer(instance=book, data=request.data)

