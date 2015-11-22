from beacons.thread_local import get_current_request
from beacons.settings import MEDIA_URL


def absolute_url(url=''):
    request = get_current_request()
    return 'http://%s' % request.get_host() + url

def media_url(url):
    return absolute_url(MEDIA_URL + url)
