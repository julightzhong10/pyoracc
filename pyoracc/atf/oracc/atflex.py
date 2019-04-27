from pyoracc.atf.common.atflex import AtfLexer


class AtfOraccLexer(AtfLexer):

    def __init__(self, skip, debug, log):
        super(AtfOraccLexer, self).__init__(skip, debug, log)
