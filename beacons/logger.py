import logging
import time
from django.http import JsonResponse
from beacons import settings
from django.db import connection
from django.utils import timezone
from datetime import datetime


class LoggingMiddleware(object):

    def process_request(self, request):
        self.start_time = time.time()

    def process_response(self, request, response):
        try:
            remote_addr = request.META.get('REMOTE_ADDR')
            if remote_addr in getattr(settings, 'INTERNAL_IPS', []):
                remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or remote_addr
            user_email = "-"
            extra_log = ""

            req_time = time.time() - self.start_time
            content_len = ''
            if hasattr(response, 'content'):
                content_len = len(response.content)

            if settings.DEBUG:
                sql_time = sum(float(q['time']) for q in connection.queries) * 1000
                extra_log += " (%s SQL queries, %s ms)" % (len(connection.queries), sql_time)

            if hasattr(request,'user'):
                user_email = getattr(request.user, 'username', '-')
                extra_log += " %s" % user_email

            current_time = datetime.strftime(timezone.now(), '%Y-%m-%d %H:%M:%S')
            logging.info("[%s] %s %s %s %s %s (%.02f seconds)%s" % (current_time, remote_addr, request.method, request.get_full_path(), response.status_code, content_len, req_time, extra_log))

            if isinstance(response, JsonResponse):
                if settings.LOG_HTTP_REQUESTS:
                    try:
                        logging.info(request.body)
                    except Exception, e:
                        logging.error("LoggingMiddleware Error: %s" % e)
                if settings.LOG_HTTP_RESPONSES:
                    logging.info(response.content)

        except Exception, e:
            logging.error("LoggingMiddleware Error: %s" % e)
        return response