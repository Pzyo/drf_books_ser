

from rest_framework.response import Response

class APIResponse(Response):
    def __init__(self, code=100, msg='success', data=None, status=None, headers=None, **kwargs):
        dic = {'code': code, 'msg': msg, 'data': data}
        if data:
            dic['data'] = data
        dic.update(kwargs)
        super().__init__(data=dic, status=status, headers=headers)
