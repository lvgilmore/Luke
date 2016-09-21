from ConfigParser import SafeConfigParser


class ConfFileUtil(object):

    @staticmethod
    def read_from_conf_file(conf_file):
        parser = SafeConfigParser()
        parser.readfp(FakeSectionHead(open(conf_file)))
        return parser


class FakeSectionHead(object):
    def __init__(self, fp):
        self.fp = fp
        self.sechead = '[asection]\n'

    def readline(self):
        if self.sechead:
            try:
                return self.sechead
            finally:
                self.sechead = None
        else:
            return self.fp.readline()
