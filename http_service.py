# http_service.py
import json
from werkzeug import Response
from nameko.web.handlers import http


class HttpService:
    name = "http_service"

    @http('POST', '/send_report')
    def get_method(self, request):
        print(request)
        # тут была бы итерация по книгам создание csv файла и отправка на почту через какой нибудь SendGrid:)
        response = Response(
            json.dumps({
                'message': 'done',
            }),
            status=200,
            mimetype='application/json'
        )
        return response
