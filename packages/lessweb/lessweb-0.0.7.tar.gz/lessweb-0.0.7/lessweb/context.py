from typing import NamedTuple, Any, Callable, Optional, overload, Dict, List
import cgi
import json

from io import BytesIO

from lessweb.sugar import *
from lessweb.storage import Storage, global_data
from lessweb.webapi import UploadedFile


def _process_fieldstorage(fs):
    if isinstance(fs, list):
        return _process_fieldstorage(fs[0])  # 递归计算
    elif fs.filename is None:  # 非文件参数
        return fs.value
    else:  # 文件参数
        return UploadedFile(fs)


def _dictify(fs):
    # hack to make input work with enctype='text/plain.
    if fs.list is None:
        fs.list = []
    return dict([(k, _process_fieldstorage(fs[k])) for k in fs.keys()])


class Context(object):
    """
    Contextual variables:
        * environ a.k.a. env – a dictionary containing the standard WSGI environment variables
        * home – the base path for the application, including any parts "consumed" by outer applications http://example.org/admin
        * homedomain – ? (appears to be protocol + host) http://example.org
        * homepath – The part of the path requested by the user which was trimmed off the current app. That is homepath + path = the path actually requested in HTTP by the user. E.g. /admin This seems to be derived during startup from the environment variable REAL_SCRIPT_NAME. It affects what web.url() will prepend to supplied urls. This in turn affects where web.seeother() will go, which might interact badly with your url rewriting scheme (e.g. mod_rewrite)
        * host – the hostname (domain) and (if not default) the port requested by the user. E.g. example.org, example.org:8080
        * ip – the IP address of the user. E.g. xxx.xxx.xxx.xxx
        * method – the HTTP method used. E.g. GET
        * path – the path requested by the user, relative to the current application. If you are using subapplications, any part of the url matched by the outer application will be trimmed off. E.g. you have a main app in code.py, and a subapplication called admin.py. In code.py, you point /admin to admin.app. In admin.py, you point /stories to a class called stories. Within stories, web.ctx.path will be /stories, not /admin/stories. E.g. /articles/845
        * protocol – the protocol used. E.g. https
        * query – an empty string if there are no query arguments otherwise a ? followed by the query string. E.g. ?fourlegs=good&twolegs=bad
        * fullpath a.k.a. path + query – the path requested including query arguments but not including homepath. E.g. /articles/845?fourlegs=good&twolegs=bad
    """
    def __init__(self):
        self.status_code: int = 200
        self.reason: str = 'OK'
        self.headers: Dict = {}
        self.app_stack: List = []

        self.url_input: Dict = {}
        self.json_input: Optional[Dict] = None
        self._post_data: Optional[Dict] = None
        self._fields: Optional[Dict] = None
        self.pipe: Storage = Storage()

        self.environ: Dict = {}
        self.env: Dict = {}
        self.host: str = ''
        self.protocol: str = ''
        self.homedomain: str = ''
        self.homepath: str = ''
        self.home: str = ''
        self.realhome: str = ''
        self.ip: str = ''
        self.method: str = ''
        self.path: str = ''
        self.query: str = ''
        self.fullpath: str = ''

        self.me: Any = None
        self.db: Any = None
        self.will_commit: bool = False

    def __call__(self):
        return self.app_stack[-1](self)

    def set_header(self, header, value):
        """
        Example:

        """
        assert isinstance(header, str) and isinstance(value, str)
        if '\n' in header or '\r' in header or '\n' in value or '\r' in value:
            raise ValueError('invalid characters in header')
        self.headers[header] = value

    def get_header(self, header, default=None):
        """
        Example:

        """
        key = 'HTTP_' + header.replace('-', '_').upper()
        return self.env.get(key, default)

    def is_json_request(self):
        return self.json_input is not None or \
               'json' in self.env.get('CONTENT_TYPE', '').lower()

    @property
    def field_input(self):
        if self.json_input is not None:
            return self.json_input
        if self._fields is not None:
            return self._fields
        if self.is_json_request():
            try:
                self.json_input = json.loads(self.data().decode(global_data.app.encoding))
            except:
                self.json_input = {'__error__': 'invalid json received'}
            return self.json_input
        else:
            fp = BytesIO(self.data())
            try:
                # cgi.FieldStorage can raise exception when handle some input
                _ = cgi.FieldStorage(fp=fp, environ=self.env.copy(), keep_blank_values=1)
                self._fields = _dictify(_)
            except:
                self._fields = {'__error__': 'invalid fields received'}
        return self._fields

    def data(self):
        """
        Example:

        """
        if self._post_data is not None:
            return self._post_data
        try:
            cl = int(self.env.get('CONTENT_LENGTH'))
        except:
            cl = 0
        self._post_data = self.env['wsgi.input'].read(cl)
        return self._post_data

    def get_input(self, queryname, default=None):
        """
        Example:

        """
        ret = self.url_input.get(queryname, _nil)
        if ret is not _nil:
            return ret
        return self.field_input.get(queryname, default)
    # ~class Context

