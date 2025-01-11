# fake recoll, map to something else...
# incomplete, only aims to work with webrecoll
# HayStack, sqlite....
"""
Sample input


    GET /results?query=create&dir=%3Call%3E&after=&before=&sort=relevancyrating&ascending=0&page=1 HTTP/1.1" 200 2538

        recoll __init__.py:73 setAbstractParams() - DEBUG - got (500, 30)
        recoll __init__.py:48 sortby() - DEBUG - got ('relevancyrating', 0)
        recoll __init__.py:55 execute() - DEBUG - got ('create', 1, None, 0)


    "GET /results?query=create+file&dir=%3Call%3E&after=&before=&sort=relevancyrating&ascending=0&page=1 HTTP/1.1" 200 2556

        setAbstractParams() - DEBUG - got (500, 30)
        sortby() - DEBUG - got ('relevancyrating', 0)
        execute() - DEBUG - got ('create file', 1, None, 0)

    "GET /results?query=create+file&dir=%3Call%3E&after=2024-12-01&before=2025-01-01&sort=relevancyrating&ascending=0&page=1 HTTP/1.1" 200 2603

        setAbstractParams() - DEBUG - got (500, 30)
        sortby() - DEBUG - got ('relevancyrating', 0)
        execute() - DEBUG - got ('create file date:2024-12-01/2025-01-01', 1, None, 0)

sort by Date
    "GET /results?query=create+file&dir=%3Call%3E&after=2024-12-01&before=2025-01-01&sort=mtime&ascending=0&page=1 HTTP/1.1" 200 2600

        setAbstractParams() - DEBUG - got (500, 30)
        sortby() - DEBUG - got ('mtime', 0)
        execute() - DEBUG - got ('create file date:2024-12-01/2025-01-01', 1, None, 0)

sort by Size
    "GET /results?query=create+file&dir=%3Call%3E&after=2024-12-01&before=2025-01-01&sort=fbytes&ascending=0&page=1 HTTP/1.1" 200 2600

        setAbstractParams() - DEBUG - got (500, 30)
        sortby() - DEBUG - got ('fbytes', 0)
        execute() - DEBUG - got ('create file date:2024-12-01/2025-01-01', 1, None, 0)


sort by Path
    "GET /results?query=create+file&dir=%3Call%3E&after=2024-12-01&before=2025-01-01&sort=url&ascending=0&page=1 HTTP/1.1" 200 2600

        setAbstractParams() - DEBUG - got (500, 30)
        sortby() - DEBUG - got ('url', 0)
        execute() - DEBUG - got ('create file date:2024-12-01/2025-01-01', 1, None, 0)

sort by Filename
    "GET /results?query=create+file&dir=%3Call%3E&after=2024-12-01&before=2025-01-01&sort=filename&ascending=0&page=1 HTTP/1.1" 200 2600
        setAbstractParams() - DEBUG - got (500, 30)
        sortby() - DEBUG - got ('filename', 0)
        execute() - DEBUG - got ('create file date:2024-12-01/2025-01-01', 1, None, 0)

TODO search folder is All only at the moment
"""

import logging
import sys


JYTHON_RUNTIME_DETECTED = 'java' in sys.platform.lower() or hasattr(sys, 'JYTHON_JAR') or str(copyright).find('Jython') > 0




if sys.version_info >= (2, 5):
    # 2.5 added function name tracing
    logging_fmt_str = "%(process)d %(thread)d %(asctime)s - %(name)s %(filename)s:%(lineno)d %(funcName)s() - %(levelname)s - %(message)s"
else:
    if JYTHON_RUNTIME_DETECTED:
        # process is None under Jython 2.2
        logging_fmt_str = "%(thread)d %(asctime)s - %(name)s %(filename)s:%(lineno)d - %(levelname)s - %(message)s"
    else:
        logging_fmt_str = "%(process)d %(thread)d %(asctime)s - %(name)s %(filename)s:%(lineno)d - %(levelname)s - %(message)s"

log = logging.getLogger(__name__)
#logging.basicConfig()

formatter = logging.Formatter(logging_fmt_str)
ch = logging.StreamHandler()  # use stdio
ch.setFormatter(formatter)
log.addHandler(ch)


log.setLevel(level=logging.INFO)
log.setLevel(level=logging.DEBUG)



#recoll = rclextract = rclconfig = None
rclextract = None


fake_results = [
    {
        # these should map to real data from notes
        'title': 'fake title',
        'filename': 'fake_filename',
        'url': 'fake_url/dirname/path',
        'abstract': 'fake_abstract with simulated highlight. the <span class="search-result-highlight">cat</span> sat on the mat, with a dog and a bottle of jack',
        'mtime': str(1736036722),  # string version of regular mtime, number of seconds - 2025-01-04 16:25

        'author': 'fake_author',  # required, but not something I want to model
    },
    {
        # these should map to real data from notes
        'title': 'fake title2',
        'filename': 'fake_filename2',
        'url': 'http://google.com',
        'abstract': 'fake_abstract2',
        'mtime': str(1736036722 + 1024),  # string version of regular mtime, number of seconds - 2025-01-04 16:25

        'author': 'fake_author',  # required, but not something I want to model
    },
]


class AttributeDict(dict):  # FIXME collections named tuple maybe a better option, or easydict.EasyDict, https://github.com/bcj/AttrDict
    def __getattr__(self, attr):
        return self.get(attr)  # fixme default param?

class FakeRecolQuery:
    # https://www.recoll.org/usermanual/webhelp/docs/RCL.PROGRAM.PYTHONAPI.RECOLL.html#RCL.PROGRAM.PYTHONAPI.RECOLL.CLASSES.QUERY
    rowcount = 0
    _result_counter = 0

    def sortby(self, a, b):
        """Example:
                    sortby(q['sort'], q['ascending'])
        """
        log.debug('got %r', (a, b))

    def execute(self, query_string, stemmer, language, collapseduplicates=None):
        """Example:
                execute(qs, config['stem'], config['stemlang'],
                      collapseduplicates=config['collapsedups']
        from https://www.recoll.org/usermanual/webhelp/docs/RCL.PROGRAM.PYTHONAPI.RECOLL.html#RCL.PROGRAM.PYTHONAPI.RECOLL.CLASSES.QUERY
            Query.execute(query_string, stemming=1, stemlang="english", fetchtext=False, collapseduplicates=False)
        """
        log.debug('got %r', (query_string, stemmer, language, collapseduplicates))
        self.rowcount = 0
        #self.rowcount = 1  # debug, lie!
        self.rowcount = len(fake_results)  # debug, lie!
        self.next = 1  # debug, FIXME will not pick up changes from caller - caller may well be using iterator interface (in an odd way?)
        self._result_counter = len(fake_results)  # debug, FIXME will not pick up changes from caller - caller may well be using iterator interface (in an odd way?)

    # TODO
    #self.next = 1 # integer
    #def next(self, ):
    # really needs to be a setter and getter

    #def scroll(self, offset, mode='absolute'):  # mode can be relative or absolute.
    # docs indicate this API is PEP-249-like
    def fetchone(self):
        if self._result_counter >= 1:
            self._result_counter -= 1
            fake_result = AttributeDict(fake_results[self._result_counter])  # called expects attributes, not a dictionary
            return fake_result
        return None
        ########
        if self.next == -1:
            return None  # or raise StopIteration?
        #return None  # FIXME return a dict
        fake_result = {
            # these should map to real data from notes
            'title': 'fake title',
            'filename': 'fake_filename',
            'url': 'fake_url/dirname/path',
            'abstract': 'fake_abstract',
            'mtime': str(1736036722),  # string version of regular mtime, number of seconds - 2025-01-04 16:25

            'author': 'fake_author',  # required, but not something I want to model
        }
        """TODO review: fields from webui.py
            # doc fields
            FIELDS = [
                # exposed by python api
                'abstract',
                'author',
                'collapsecount',
                'dbytes',
                'dmtime',
                'fbytes',
                'filename',
                'fmtime',
                'ipath',
                'keywords',
                'mtime',
                'mtype',
                'origcharset',
                'relevancyrating',
                'sig',
                'size',
                'title',
                'url',
                # calculated
                'label',
                'snippet',
                'time',
            ]


        from https://www.recoll.org/usermanual/webhelp/docs/RCL.PROGRAM.PYTHONAPI.RECOLL.html#RCL.PROGRAM.PYTHONAPI.RECOLL.CLASSES.DOC

          * url the document URL but see also getbinurl()
          * ipath the document ipath for embedded documents.
          * fbytes, dbytes the document file and text sizes.
          * fmtime, dmtime the document file and document times.
          * xdocid the document Xapian document ID. This is useful if you want to access the document through a direct Xapian operation.
          * mtype the document MIME type.
          * text holds the document processed text, if the index itself is configured to store it (true by default) and if the fetchtext query execute() option was true. See also the rclextract module for accessing document contents.
          * Other fields stored by default: author, filename, keywords, recipient

        """
        fake_result = AttributeDict(fake_result)  # called expects attributes, not a dictionary
        self.next = -1
        return fake_result

    def makedocabstract(self, doc, methods=None):
        log.debug('got %r', (doc, methods))
        return None
        return 'Fake snippet'
        return doc

class FakeRecollDatabase:

    def __init__(self, confdir, extra_dbs=None):
        self.confdir = confdir
        self.extra_dbs = extra_dbs
        self.abstract_params = {}
        pass


    def query(self):
        return FakeRecolQuery()

    def setAbstractParams(self, key, value):
        """Example:
            setAbstractParams(config['maxchars'], config['context'])
        """
        log.debug('got %r', (key, value))
        self.abstract_params[key] = value


class FakeRecoll:
    def __init__(self):
        pass

    def connect(self, confdir, extra_dbs=None):
        # https://www.recoll.org/usermanual/webhelp/docs/RCL.PROGRAM.PYTHONAPI.RECOLL.html
        return FakeRecollDatabase(confdir, extra_dbs=extra_dbs)

recoll = FakeRecoll()
