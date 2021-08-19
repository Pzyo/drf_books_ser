
from rest_framework.views import APIView
from api import models
from api.ser import BookModelSerializer
from utils.response import APIResponse

class BookAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # 查询单个和查询所有, 合在一起
        # 查所有
        if not kwargs.get('pk', None):
            book_list = models.Book.objects.all().filter(is_delete=False)
            book_list_ser = BookModelSerializer(book_list, many=True)
            return APIResponse(data=book_list_ser.data)
        # 查一个
        else:
            book = models.Book.objects.filter(pk=kwargs.get('pk', None), is_delete=False).first()
            book_ser = BookModelSerializer(book)
            return APIResponse(data=book_ser.data)


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
            book_ser = BookModelSerializer(instance=book, data=request.data, partial=True)
        else:
            book_list = []
            modify_data = []
            for item in request.data:
                pk = item.pop('id')
                book = models.Book.objects.get(pk=pk)
                book_list.append(book)
                modify_data.append(item)
            # 批量修改, 方案1, for循环
            # for i, si_data in enumerate(modify_data):
            #     book_ser = BookModelSerializer(instance=book_list[i], data=si_data)
            #     book_ser.is_valid(raise_exception=True)
            #     book_ser.save()

            # 方案2, 重写ListSerializer的update方法, 在序列化类中编写
            book_ser = BookModelSerializer(instance=book_list, data=modify_data, many=True)

        book_ser.is_valid(raise_exception=True)
        book_ser.save()

        return APIResponse(data=book_ser.data)

    def delete(self, request, *args, **kwargs):
        # 单删与批量删
        pk = kwargs.get('pk')

        pks = []
        if pk:
            pks.append(pk)
        else:
            pks = request.data.get('pks')
        # ret返回受影响的行数
        ret = models.Book.objects.filter(pk__in=pks, is_delete=False).update(is_delete=True)
        if ret:
            return APIResponse()
        else:
            return APIResponse(code=110, msg='没有要删除的数据')

from rest_framework.generics import ListAPIView
class BookView(ListAPIView):
    queryset = models.Book.objects.all()
    serializer_class = BookModelSerializer