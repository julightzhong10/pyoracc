from pyoracc.model.milestone import Milestone
from pyoracc import _pyversion
from pyoracc.model.oraccobject import OraccObject
from pyoracc.model.oraccnamedobject import OraccNamedObject
from pyoracc.atf.common.atfyacc import AtfParser
from pyoracc.model.state import State
from pyoracc.model.text import Text

from pyoracc.model.link_reference import LinkReference

from pyoracc.cdlimodel.structure import Structure

from pyoracc.cdlimodel.cdlitext import CDLIText

objStructure = Structure()


class AtfCDLIParser(AtfParser):
    
    tokens = AtfParser.tokens
    precedence = AtfParser.precedence

    def __init__(self, debug,skip, log):
        super(AtfCDLIParser, self).__init__(debug, skip,log)

    def p_document(self, p):
        """document : text
                    | object
                    | composite"""
        p[0] = p[1]

        objStructure.CheckSurfaceRules()
        objStructure.PrintResults()
        objStructure.ClearData()
        objStructure.ResetColumnCounter()

    def p_linkreference_label(self, p):
        """link_reference : link_reference ID
                          | link_reference COMMA ID
                          | link_reference REFERENCE
                          | link_reference ID QUERY"""
        p[0] = p[1]
        p[0].label.append(list(p)[-1])

    def p_simple_dollar(self, p):
        """simple_dollar_statement : DOLLAR ID newline
                                   | DOLLAR state newline
                                   | DOLLAR REFERENCE ID newline"""
        # print(p[2])
        p[0] = State(p[2])    

    # to remove later
    def p_version_protoocol(self, p):
        """version_protocol : VERSION ID newline"""
        p[0] = p[2]

    # to remove later
    def p_text_version(self, p):
        """text : text version_protocol"""
        p[0] = p[1]
        p[0].version = p[2]

    def p_codeline(self, p):
        """text_statement : AMPERSAND ID EQUALS ID newline
                            | AMPERSAND ID EQUALS ID QUERY newline
                            | AMPERSAND ID EQUALS ID EQUALS ID newline
                            | AMPERSAND ID EQUALS ID EQUALS ID EQUALS ID newline
                            | AMPERSAND ID EQUALS ID STAR newline"""
        p[0] = Text()
        p[0].code = p[2]
        p[0].description = p[4]

        # CDLI Code
        objText = CDLIText()
        value, status, errorValue = objText.CheckPMap(p[0].code)
        if errorValue:
            print(errorValue)

        if not objText.CheckPnumber(p[0].code):
            print("Incorrect Pnumber: " + str(p[0].code))

        global objStructure
        objStructure.UpdatePnumber(p[0].code)

        if objStructure.newtext_status:
            objStructure.newtext_status = False
        else:
            objStructure.CheckSurfaceRules()
            objStructure.PrintResults()
            objStructure.ClearData()
            objStructure.ResetColumnCounter()

    def p_object_nolabel(self, p):
        '''object_specifier : TABLET
                            | ENVELOPE
                            | PRISM
                            | BULLA
                            | SEALINGS'''
        p[0] = OraccObject(p[1])
        objStructure.SetObjectType(str(p[0]))
        # print "Test: %s" % p[0]

    def p_object_label(self, p):
        '''object_specifier : FRAGMENT ID
                            | OBJECT ID
                            | TABLET REFERENCE'''
        p[0] = OraccNamedObject(p[1], p[2])
        objStructure.SetObjectType(str(p[2]))

    def p_surface_nolabel(self, p):
        '''surface_specifier  : OBVERSE
                              | REVERSE
                              | LEFT
                              | RIGHT
                              | TOP
                              | BOTTOM
                              | EDGE'''
        p[0] = OraccObject(p[1])
        objStructure.SetSurface(str(p[0]))
        # print "%s" %p[0]

    def p_surface_label(self, p):
        '''surface_specifier : FACE ID
                             | SURFACE ID
                             | COLUMN ID
                             | SEAL ID
                             | HEADING ID'''
        p[0] = OraccNamedObject(p[1], p[2])
        if str(p[2]) == "column":
            objStructure.IncrementColumnCounter()
        else:
            objStructure.SetSurface(str(p[0]))
        # print "%s" %p[0]

    def p_milestone_brief(self, p):
        """milestone_name : CATCHLINE
                          | COLOPHON
                          | DATE
                          | SIGNATURES
                          | SIGNATURE
                          | SUMMARY
                          | WITNESSES"""
        p[0] = Milestone(p[1])

    def p_text_object_surface_broken(self, p):
        """text : text object surface DOLLAR BROKEN QUERY newline"""
        p[0] = p[1]

    def p_linkreference(self, p):
        """link_reference : link_operator ID
                        | link_operator ID QUERY"""
        p[0] = LinkReference(p[1], p[2])

    def p_dollar_erased(self, p):
        """text :  text object surface DOLLAR ID LINE ERASED newline
            | text object surface DOLLAR ID LINES ERASED newline"""
        # print(p[2])
        p[0] = p[1]