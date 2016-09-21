from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError

FAKE_SECTION = 'asection'

class ConfFileUtil(SafeConfigParser):

    def get_option(self, option, raw=False, vars=None):
        res = None
        try:
            res = self.get(FAKE_SECTION, option, raw, vars)
        except NoSectionError as nse:
            print "calc_score: " + "NoSectionError " + nse.message
        except NoOptionError as noe:
            print "calc_score: " + "NoOptionError " + noe.message
        return res


    @staticmethod
    def read_from_conf_file(conf_file):
        parser = ConfFileUtil()
        parser.readfp(FakeSectionHead(open(conf_file)))
        return parser


class FakeSectionHead(object):
    def __init__(self, fp):
        self.fp = fp
        self.sechead = '['+FAKE_SECTION + ']\n'
    def readline(self):
        if self.sechead:
            try:
                return self.sechead
            finally:
                self.sechead = None
        else:
            return self.fp.readline()