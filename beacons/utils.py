from beacons.thread_local import get_current_request
from beacons.settings import MEDIA_URL, PUBLIC_URL


def absolute_url(url=''):
    request = get_current_request()
    return 'http://%s' % request.get_host() + url

def media_url(url):
    return PUBLIC_URL + MEDIA_URL + url
