import base64
from support import random_generator as rg


class Headers(object):

    def __init__(self, header_type, header_version=150):
        self.header_type = header_type
        self.header_version = header_version

    def _create_browser_headers_static(self, header_name, header_version):
        headers = {
            'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) {header_name}/{header_version} Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip',
            'DNT': '1',
            'Connection': 'close'
        }
        self.header_name = header_name
        self.header_version = header_version
        self.headers = headers
        return headers

    def _create_browser_headers_random(self):
        random_browser_version = rg.create_random_browser_version()
        random_browser_header = self._create_browser_headers_static('Chrome', 'random')
        if self.header_version == 'random':
            self.header_version = random_browser_version
            self.random_browser_header = random_browser_header




