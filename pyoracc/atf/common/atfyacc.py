'''
Copyright 2015, 2016 University College London.

This file is part of PyORACC.

PyORACC is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyORACC is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyORACC. If not, see <http://www.gnu.org/licenses/>.
'''

import ply.yacc as yacc
from pyoracc import _pyversion
from pyoracc.atf.common.atflexicon import AtfLexicon

from pyoracc.model.comment import Comment
from pyoracc.model.composite import Composite
from pyoracc.model.line import Line
from pyoracc.model.link import Link
from pyoracc.model.link_reference import LinkReference
from pyoracc.model.milestone import Milestone
from pyoracc.model.multilingual import Multilingual
from pyoracc.model.note import Note
from pyoracc.model.oraccnamedobject import OraccNamedObject
from pyoracc.model.oraccobject import OraccObject
from pyoracc.model.ruling import Ruling
from pyoracc.model.score import Score
from pyoracc.model.state import State
from pyoracc.model.text import Text
from pyoracc.model.translation import Translation
from pyoracc.tools.logtemplate import LogTemplate
from pyoracc.tools.grammar_check import GrammarCheck
class AtfParser(object):
    tokens = AtfLexicon.TOKENS

    def __init__(self, debug=0, skip=False, log=yacc.NullLogger()):
        self.skip=skip
        self.errors=[] #error list
        self.parser = yacc.yacc(module=self, tabmodule='pyoracc.atf.parsetab',
                                debug=debug, debuglog=log)
        self.log_tmp=LogTemplate()
        self.cur_pos=0
        self.g_check=GrammarCheck()
        self.debug_mode=True
        self.detail_debug=False

    def p_codeline(self, p):
        "text_statement : AMPERSAND ID EQUALS ID newline"
        if self.debug_mode:
            print('p_codeline')
        p[0] = Text()
        p[0].code = p[2]
        p[0].description = p[4]


    def p_newline(self, p):
        """newline : NEWLINE
                   | newline NEWLINE"""
        if self.debug_mode:
            print('p_newline')
        self.cur_pos= p.lexpos(1) 


    def p_document(self, p):
        """document : text
                    | object
                    | composite"""
        if self.debug_mode:
            print('p_document')
        p[0] = p[1]



    def p_project_statement(self, p):
        "project_statement : PROJECT ID newline"
        if self.debug_mode:
            print('p_project_statement')
        p[0] = p[2]

    def p_project(self, p):
        "project : project_statement"
        if self.debug_mode:
            print('p_project')
        p[0] = p[1]

    def p_text_project(self, p):
        "text : text project"
        if self.debug_mode:
            print('p_text_project')
        p[0] = p[1]
        p[0].project = p[2]

    def p_code(self, p):
        "text : text_statement"
        if self.debug_mode:
            print('p_code')
            if self.detail_debug:
                print(p[1])
                print('---------')
        p[0] = p[1]

    def p_unicode(self, p):
        """skipped_protocol : ATF USE UNICODE newline
                            | ATF USE MATH newline
                            | ATF USE LEGACY newline
                            | ATF USE MYLINES newline
                            | ATF USE LEXICAL newline
                            | key_statement
                            | BIB ID newline
                            | BIB ID EQUALS ID newline
                            | lemmatizer_statement"""
        if self.debug_mode:
            print('p_unicode')

    def p_key_statement(self, p):
        """key_statement : key newline
                         | key EQUALS newline"""
        if self.debug_mode:
            print('p_key_statement')

    def p_key(self, p):
        "key : KEY ID"
        if self.debug_mode:
            print('p_key')

    def p_key_addendum(self, p):
        "key : key EQUALS ID"
        if self.debug_mode:
            print('p_key_addendum')

    def p_lemmatizer(self, p):
        "lemmatizer : LEMMATIZER"
        if self.debug_mode:
            print('p_lemmatizer')

    def p_lemmatizer_id(self, p):
        "lemmatizer : lemmatizer ID"
        if self.debug_mode:
            print('p_lemmatizer_id')


    def p_lemmatizer_statement(self, p):
        "lemmatizer_statement : lemmatizer newline "
        if self.debug_mode:
            print('p_lemmatizer_statement')

    def p_link(self, p):
        "link : LINK DEF ID EQUALS ID EQUALS ID newline"
        if self.debug_mode:
            print('p_link')
        p[0] = Link(p[3], p[5], p[7])

    def p_link_source(self, p):
        "link : LINK SOURCE ID EQUALS ID newline"
        # Not documented but fairly common ca 600
        # texts in the full corpus
        if self.debug_mode:
            print('p_link_source')
        p[0] = Link(code=p[3], description=p[5])

    def p_link_parallel(self, p):
        "link : LINK PARALLEL ID EQUALS ID newline"
        if self.debug_mode:
            print('p_link_parallel')
        p[0] = Link(None, p[3], p[5])

    def p_include(self, p):
        "link : INCLUDE ID EQUALS ID newline"
        if self.debug_mode:
            print('p_include')
        p[0] = Link("Include", p[2], p[4])

    def p_language_protoocol(self, p):
        "language_protocol : ATF LANG ID newline"
        if self.debug_mode:
            print('p_language_protoocol')
        self.g_check.add_lan(p.lineno(1))
        p[0] = p[4]

    def p_text_math(self, p):
        "text : text skipped_protocol"
        if self.debug_mode:
            print('p_text_math')
        p[0] = p[1]

    def p_text_link(self, p):
        "text : text link"
        if self.debug_mode:
            print('p_text_link')
        p[0] = p[1]
        p[0].links.append(p[2])

    def p_text_language(self, p):
        "text : text language_protocol"
        if self.debug_mode:
            print('p_text_language')        
        p[0] = p[1]
        p[0].language = p[2]

    def p_text_object(self, p):
        """text : text object %prec OBJECT"""
        if self.debug_mode:
            print('p_text_object')   
        p[0] = p[1]
        p[0].children.append(p[2])

    def p_text_surface(self, p):
        """text : text surface %prec OBJECT
                | text translation %prec TRANSLATIONEND"""
        if self.debug_mode:
            print('p_text_surface')   
        p[0] = p[1]
        # Find the last object in the text
        # If there is none, append a tablet and use that
        # Default to a tablet

        # Has a default already been added?
        if not p[0].objects():
            p[0].children.append(OraccObject("tablet"))
        p[0].objects()[-1].children.append(p[2])

    def p_text_surface_element(self, p):
        """text : text surface_element %prec OBJECT"""
        if self.debug_mode:
            print('p_text_surface_element')   
        p[0] = p[1]
        if not p[0].objects():
            p[0].children.append(OraccObject("tablet"))
        # Default to obverse of a tablet
        p[0].objects()[-1].children.append(OraccObject("obverse"))
        p[0].objects()[-1].children[0].children.append(p[2])

    def p_text_composite(self, p):
        """text : text COMPOSITE newline"""
        if self.debug_mode:
            print('p_text_composite')   
        p[0] = p[1]
        p[0].composite = True

    def p_text_text(self, p):
        """composite : text text"""
        if self.debug_mode:
            print('p_text_text')   
        # Text must be a composite
        p[0] = Composite()
        if not p[1].composite:
            # An implicit composite
            pass
        p[0].texts.append(p[1])
        p[0].texts.append(p[2])

    def p_composite_text(self, p):
        """composite : composite text"""
        if self.debug_mode:
            print('p_composite_text')   
        # Text must be a composite
        p[0] = p[1]
        p[0].texts.append(p[2])

    def p_object_statement(self, p):
        """object_statement : object_specifier newline"""
        if self.debug_mode:
            print('p_object_statement')   
        p[0] = p[1]

    def p_flag(self, p):
        """ flag : HASH
                 | EXCLAIM
                 | QUERY
                 | STAR """
        if self.debug_mode:
            print('p_flag')   
        p[0] = p[1]

    def p_object_flag(self, p):
        "object_specifier : object_specifier flag"
        if self.debug_mode:
            print('p_object_flag')   
        p[0] = p[1]
        AtfParser.flag(p[0], p[2])

    @staticmethod
    def flag(target, flag):
        if flag == "#":
            target.broken = True
        elif flag == "!":
            target.remarkable = True
        elif flag == "?":
            target.query = True
        elif flag == "*":
            target.collated = True

    # These MUST be kept as a separate parse rule,
    # as the same keywords also occur
    # in strict dollar lines
    def p_object_nolabel(self, p):
        '''object_specifier : TABLET
                            | ENVELOPE
                            | PRISM
                            | BULLA
                            | SEALINGS'''
        if self.debug_mode:
            print('p_object_nolabel')   
        p[0] = OraccObject(p[1])

    def p_object_label(self, p):
        '''object_specifier : FRAGMENT ID
                            | OBJECT ID
                            | TABLET REFERENCE'''
        if self.debug_mode:
            print('p_object_label')   
        p[0] = OraccNamedObject(p[1], p[2])

    def p_object(self, p):
        "object : object_statement"
        if self.debug_mode:
            print('p_object')  
        p[0] = p[1]

    def p_object_surface(self, p):
        """object : object surface %prec SURFACE
              | object translation %prec TRANSLATIONEND """
        if self.debug_mode:
            print('p_object_surface')  
        p[0] = p[1]
        p[0].children.append(p[2])

    def p_object_surface_element(self, p):
        """object : object surface_element %prec SURFACE"""
        if self.debug_mode:
            print('p_object_surface_element')  
        p[0] = p[1]
        # Default surface is obverse
        p[0].children.append(OraccObject("obverse"))
        p[0].children[0].children.append(p[2])

    def p_surface_statement(self, p):
        "surface_statement : surface_specifier newline"
        if self.debug_mode:
            print('p_surface_statement')
        p[0] = p[1]

    def p_surface_flag(self, p):
        "surface_specifier : surface_specifier flag"
        if self.debug_mode:
            print('p_surface_flag')  
        p[0] = p[1]
        AtfParser.flag(p[0], p[2])

    def p_surface_nolabel(self, p):
        '''surface_specifier  : OBVERSE
                              | REVERSE
                              | LEFT
                              | RIGHT
                              | TOP
                              | BOTTOM'''
        if self.debug_mode:
            print('p_surface_nolabel')  
        p[0] = OraccObject(p[1])

    def p_surface_label(self, p):
        '''surface_specifier : FACE ID
                             | SURFACE ID
                             | COLUMN ID
                             | SEAL ID
                             | HEADING ID'''
        if self.debug_mode:
            print('p_surface_label')  
        p[0] = OraccNamedObject(p[1], p[2])

    def p_surface(self, p):
        "surface : surface_statement"
        if self.debug_mode:
            print('p_surface')  
        p[0] = p[1]

    def p_surface_element_line(self, p):
        """surface_element : line %prec LINE
                           | dollar
                           | note_statement
                           | link_reference_statement %prec LINE
                           | milestone"""
        if self.debug_mode:
            print('p_surface_element_line')  
        p[0] = p[1]

    def p_dollar(self, p):
        """dollar          : ruling_statement
                           | loose_dollar_statement
                           | strict_dollar_statement
                           | simple_dollar_statement"""
        if self.debug_mode:
            print('p_dollar') 
        p[0] = p[1]

    def p_surface_line(self, p):
        """surface : surface surface_element"""
        if self.debug_mode:
            print('p_surface_line') 
        p[0] = p[1]
        p[0].children.append(p[2])
        # WE DO NOT YET HANDLE @M=DIVSION lines.

    def p_linelabel(self, p):
        "line_sequence : LINELABEL ID"
        self.g_check.add_trans(str(p[1]),p.lineno(1))
        if self.debug_mode:
            print('p_linelabel')
            if self.detail_debug: 
                print(p[1])
                print(p[2])
                print('----------')
        p[0] = Line(p[1])
        p[0].words.append(p[2])

    # def p_linelabel_error(self, p):
    #     "line_sequence : error ID"
    #     if self.debug_mode:
    #         print('p_linelabel')
    #         if self.detail_debug: 
    #             print(p[1])
    #             print(p[2])
    #             print('----------')
    #     p[0] = Line(p[1])
    #     p[0].words.append(p[2])


    def p_scorelabel(self, p):
        "line_sequence : SCORELABEL ID"
        if self.debug_mode:
            print('p_scorelabel') 
        p[0] = Line(p[1])
        p[0].words.append(p[2])

    def p_line_id(self, p):
        "line_sequence : line_sequence ID"
        if self.debug_mode:
            print('p_line_id')
            if self.detail_debug:
                print(p[1])
                print(p[2])
                print('----------')
        p[0] = p[1]
        p[0].words.append(p[2])

    def p_line_reference(self, p):
        "line_sequence : line_sequence reference"
        if self.debug_mode:
            print('p_line_reference') 
        p[0] = p[1]
        p[0].references.append(p[2])

    def p_line_statement(self, p):
        "line_statement : line_sequence newline"
        if self.debug_mode:
            print('p_line_statement') 
        p[0] = p[1]

    def p_line(self, p):
        "line : line_statement"
        if self.debug_mode:
            print('p_line') 
        p[0] = p[1]

    def p_line_lemmas(self, p):
        "line : line lemma_statement  "
        if self.debug_mode:
            print('p_line_lemmas')
        p[0] = p[1]
        p[0].lemmas = p[2]

    def p_line_note(self, p):
        "line : line note_statement"
        if self.debug_mode:
            print('p_line_note')
        p[0] = p[1]
        p[0].notes.append(p[2])

    def p_line_interlinear_translation(self, p):
        "line : line interlinear"
        if self.debug_mode:
            print('p_line_interlinear_translation')
        p[0] = p[1]
        p[0].translation = p[2]

    def p_interlinear(self, p):
        "interlinear : TR ID newline"
        if self.debug_mode:
            print('p_interlinear')
        p[0] = p[2]

    def p_interlinear_empty(self, p):
        "interlinear : TR newline"
        if self.debug_mode:
            print('p_interlinear_empty')
        p[0] = ""

    def p_line_link(self, p):
        "line : line link_reference_statement"
        if self.debug_mode:
            print('p_line_link')
        p[0] = p[1]
        p[0].links.append(p[2])

    def p_line_equalbrace(self, p):
        "line : line equalbrace_statement"
        if self.debug_mode:
            print('p_line_equalbrace')
        p[0] = p[1]
        # Don't know what to do here

    def p_equalbrace(self, p):
        "equalbrace : EQUALBRACE"
        if self.debug_mode:
            print('p_equalbrace')

    def p_equalbrace_ID(self, p):
        "equalbrace : equalbrace ID"
        if self.debug_mode:
            print('p_equalbrace_ID')

    def p_equalbrace_statement(self, p):
        "equalbrace_statement : equalbrace newline"
        if self.debug_mode:
            print('p_equalbrace_statement')

    def p_line_multilingual(self, p):
        "line : line multilingual %prec MULTI"
        if self.debug_mode:
            print('p_line_multilingual')
        p[0] = Multilingual()
        p[0].lines[None] = p[1]
        p[0].lines[p[2].label] = p[2]
        # Use the language, temporarily stored in the label, as the key.
        p[0].lines[p[2].label].label = p[1].label
        # The actual label is the same as the main line

    def p_multilingual_sequence(self, p):
        "multilingual_sequence : MULTILINGUAL ID "
        if self.debug_mode:
            print('p_multilingual_sequence')
        p[0] = Line(p[2][1:])  # Slice off the percent

    def p_multilingual_id(self, p):
        "multilingual_sequence : multilingual_sequence ID"
        if self.debug_mode:
            print('p_multilingual_id')
        p[0] = p[1]
        p[0].words.append(p[2])

    def p_multilingual_reference(self, p):
        "multilingual_sequence : multilingual_sequence reference"
        if self.debug_mode:
            print('p_multilingual_reference')
        p[0] = p[1]
        p[0].references.append(p[2])

    def p_multilingual_statement(self, p):
        "multilingual_statement : multilingual_sequence newline"
        if self.debug_mode:
            print('p_multilingual_statement')
        p[0] = p[1]

    def p_multilingual(self, p):
        "multilingual : multilingual_statement"
        if self.debug_mode:
            print('p_multilingual')
        p[0] = p[1]

    def p_multilingual_lemmas(self, p):
        "multilingual : multilingual lemma_statement "
        if self.debug_mode:
            print('p_multilingual_lemmas')
        p[0] = p[1]
        p[0].lemmas = p[2]

    def p_multilingual_note(self, p):
        "multilingual : multilingual note_statement "
        if self.debug_mode:
            print('p_multilingual_note')
        p[0] = p[1]
        p[0].notes.append(p[2])

    def p_multilingual_link(self, p):
        "multilingual : multilingual link_reference_statement "
        if self.debug_mode:
            print('p_multilingual_link')
        p[0] = p[1]
        p[0].links.append(p[2])

    def p_lemma_list(self, p):
        "lemma_list : LEM ID"
        if self.debug_mode:
            print('p_lemma_list')
        p[0] = [p[2]]

    def p_milestone(self, p):
        "milestone : milestone_name newline"
        if self.debug_mode:
            print('p_milestone')
        p[0] = p[1]

    def p_milestone_name(self, p):
        "milestone_name : M EQUALS ID"
        if self.debug_mode:
            print('p_milestone_name')
        p[0] = Milestone(p[3])

    def p_milestone_brief(self, p):
        """milestone_name : CATCHLINE
                          | COLOPHON
                          | DATE
                          | EDGE
                          | SIGNATURES
                          | SIGNATURE
                          | SUMMARY
                          | WITNESSES"""
        if self.debug_mode:
            print('p_milestone_brief')
        p[0] = Milestone(p[1])

    def p_lemma_list_lemma(self, p):
        "lemma_list : lemma_list lemma"
        if self.debug_mode:
            print('p_lemma_list_lemma')
        p[0] = p[1]
        p[0].append(p[2])

    def p_lemma(self, p):
        "lemma : SEMICOLON"
        if self.debug_mode:
            print('p_lemma')

    def p_lemma_id(self, p):
        "lemma : lemma ID"
        if self.debug_mode:
            print('p_lemma_id')
        p[0] = p[2]

    def p_lemma_statement(self, p):
        "lemma_statement : lemma_list newline"
        if self.debug_mode:
            print('p_lemma_statement')
        p[0] = p[1]

    def p_ruling_statement(self, p):
        "ruling_statement : ruling newline"
        if self.debug_mode:
            print('p_ruling_statement')
        p[0] = p[1]

    def p_ruling(self, p):
        """ruling : DOLLAR SINGLE RULING
                  | DOLLAR DOUBLE RULING
                  | DOLLAR TRIPLE RULING
                  | DOLLAR SINGLE LINE RULING
                  | DOLLAR DOUBLE LINE RULING
                  | DOLLAR TRIPLE LINE RULING"""
        if self.debug_mode:
            print('p_ruling')
        counts = {
            'single': 1,
            'double': 2,
            'triple': 3,
        }
        p[0] = Ruling(counts[p[2]])

    def p_uncounted_ruling(self, p):
        "ruling : DOLLAR RULING"
        if self.debug_mode:
            print('p_uncounted_ruling')
        p[0] = Ruling(1)

    def p_flagged_ruling(self, p):
        "ruling : ruling flag"
        if self.debug_mode:
            print('p_flagged_ruling')
        p[0] = p[1]
        AtfParser.flag(p[0], p[2])

    def p_note(self, p):
        """note_statement : note_sequence newline"""
        if self.debug_mode:
            print('p_note')
        p[0] = p[1]

    def p_note_sequence(self, p):
        """note_sequence : NOTE """
        if self.debug_mode:
            print('p_note_sequence')
        p[0] = Note()

    def p_note_sequence_content(self, p):
        """note_sequence : note_sequence ID"""
        if self.debug_mode:
            print('p_note_sequence_content')
        p[0] = p[1]
        p[0].content += p[2]

    def p_note_sequence_link(self, p):
        """note_sequence : note_sequence reference"""
        if self.debug_mode:
            print('p_note_sequence_link')
        p[0] = p[1]
        p[0].references.append(p[2])

    def p_reference(self, p):
        "reference : HAT ID HAT"
        if self.debug_mode:
            print('p_reference')
        p[0] = p[2]



    def p_loose_dollar(self, p):
        "loose_dollar_statement : DOLLAR PARENTHETICALID newline"
        if self.debug_mode:
            print('p_loose_dollar')
        p[0] = State(loose=p[2])

    def p_strict_dollar_statement(self, p):
        "strict_dollar_statement : DOLLAR state_description newline"
        self.g_check.add_dollars(p.lineno(1))
        if self.debug_mode:
            print('p_strict_dollar_statement')
        p[0] = p[2]

    def p_state_description(self, p):
        """state_description : plural_state_description
                             | singular_state_desc
                             | brief_state_desc"""
        if self.debug_mode:
            print('p_state_description')
        p[0] = p[1]

    def p_simple_dollar(self, p):
        """simple_dollar_statement : DOLLAR ID newline
                                   | DOLLAR state newline"""
        if self.debug_mode:
            print('p_simple_dollar')
        p[0] = State(p[2])

    def p_plural_state_description(self, p):
        """plural_state_description : plural_quantifier plural_scope state
                                    | ID plural_scope state
                                    | ID singular_scope state
                                    | ID REFERENCE state"""
        if self.debug_mode:
            print('p_plural_state_description')
        # The singular case is an exception: "1 line broken" is semantically
        # the same as "2 lines broken"
        p[0] = State(p[3], p[2], p[1])

    def p_plural_state_description_unquantified(self, p):
        """plural_state_description : plural_scope state
        """
        if self.debug_mode:
            print('p_plural_state_description_unquantified')
        # This should probably not be allowed but is happening in the corpus
        # i.e. ""$ columns broken"
        p[0] = State(p[2], p[1])

    def p_plural_state_description_unquantified_reverse(self, p):
        """plural_state_description : state plural_scope
        """
        if self.debug_mode:
            print('p_plural_state_description_unquantified_reverse')
        # This should probably not be allowed but is happening in the corpus
        # i.e. ""$ blank lines"
        p[0] = State(p[1], p[2])

    def p_plural_state_range_description(self, p):
        """plural_state_description : ID MINUS ID plural_scope state"""
        if self.debug_mode:
            print('p_plural_state_range_description')
        p[0] = State(p[5], p[4], p[1] + "-" + p[3])

    def p_qualified_state_description(self, p):
        "plural_state_description : qualification plural_state_description"
        if self.debug_mode:
            print('p_qualified_state_description')
        p[0] = p[2]
        p[0].qualification = p[1]

    def p_singular_state_desc(self, p):
        """singular_state_desc : singular_scope state
                               | REFERENCE state
                               | REFERENCE ID state"""
        if self.debug_mode:
            print('p_singular_state_desc')
        text = list(p)
        p[0] = State(text[-1], " ".join(text[1:-1]))

    # This is reversed compared to the documentation but fairly common so
    # We have to implement it. I.e. cams/gkab/00atf/ctn_4_032.atf and others
    # http://oracc.museum.upenn.edu/doc/help/editinginatf/primer/structuretutorial/index.html
    # section $-lines
    def p_state_singular_desc(self, p):
        """singular_state_desc : state singular_scope"""
        if self.debug_mode:
            print('p_state_singular_desc')
        text = list(p)
        p[0] = State(state=text[1], scope=" ".join(text[2:]))

    def p_singular_state_desc_brief(self, p):
        """brief_state_desc : brief_quantifier state"""
        if self.debug_mode:
            print('p_singular_state_desc_brief')
        text = list(p)
        p[0] = State(text[-1], None, text[1])

    def p_partial_state_description(self, p):
        """singular_state_desc : partial_quantifier singular_state_desc"""
        if self.debug_mode:
            print('p_partial_state_description')
        p[0] = p[2]
        p[0].extent = p[1]

    def p_state(self, p):
        """state : BLANK
                 | BROKEN
                 | EFFACED
                 | ILLEGIBLE
                 | MISSING
                 | TRACES"""
        if self.debug_mode:
            print('p_state')
        p[0] = p[1]

    def p_plural_quantifier(self, p):
        """plural_quantifier : SEVERAL
                             | SOME"""
        if self.debug_mode:
            print('p_plural_quantifier')

    def p_singular_scope(self, p):
        """singular_scope : LINE
                          | CASE
                          | SPACE"""
        if self.debug_mode:
            print('p_singular_scope')
        p[0] = p[1]

    def p_plural_scope(self, p):
        """plural_scope : COLUMNS
                        | LINES
                        | CASES"""
        if self.debug_mode:
            print('p_plural_scope')
        p[0] = p[1]

    def p_brief_quantifier(self, p):
        """brief_quantifier : REST
                            | START
                            | BEGINNING
                            | MIDDLE
                            | END"""
        if self.debug_mode:
            print('p_brief_quantifier')
        p[0] = p[1]

    def p_partial_quantifier(self, p):
        """partial_quantifier : brief_quantifier OF"""
        if self.debug_mode:
            print('p_partial_quantifier')
        p[0] = " ".join(p[1:])

    def p_qualification(self, p):
        """qualification : AT LEAST
                         | AT MOST
                         | ABOUT"""
        if self.debug_mode:
            print('p_qualification')
        p[0] = " ".join(p[1:])

    def p_translation_statement(self, p):
        """translation_statement : TRANSLATION PARALLEL ID PROJECT newline
                                 | TRANSLATION LABELED ID PROJECT newline
        """
        if self.debug_mode:
            print('p_translation_statement')
        p[0] = Translation()

    def p_translation(self, p):
        "translation : translation_statement"
        if self.debug_mode:
            print('p_translation')
        p[0] = p[1]

    def p_translation_end(self, p):
        "translation : translation END REFERENCE newline"
        if self.debug_mode:
            print('p_translation_end')
        p[0] = p[1]
        # Nothing to do; this is a legacy ATF feature

    def p_translation_surface(self, p):
        "translation : translation surface %prec SURFACE"
        if self.debug_mode:
            print('p_translation_surface')
        p[0] = p[1]
        p[0].children.append(p[2])

    def p_translation_labeledline(self, p):
        "translation : translation translationlabeledline %prec LINE"
        if self.debug_mode:
            print('p_translation_labeledline')
        p[0] = p[1]
        p[0].children.append(p[2])

    def p_translation_dollar(self, p):
        "translation : translation dollar"
        if self.debug_mode:
            print('p_translation_dollar')
        p[0] = p[1]
        p[0].children.append(p[2])

    def p_translationlabelledline(self, p):
        """translationlabeledline : translationlabel NEWLINE
                                  | translationrangelabel NEWLINE
                                  | translationlabel CLOSER
                                  | translationrangelabel CLOSER
        """
        if self.debug_mode:
            print('p_translationlabelledline')
        p[0] = Line(p[1])

    def p_translationlabel(self, p):
        """translationlabel : LABEL
                            | OPENR"""
        if self.debug_mode:
            print('p_translationlabel')
        p[0] = LinkReference("||", None)
        if p[1][-1] == "+":
            p[0].plus = True

    def p_translationlabel_id(self, p):
        """translationlabel : translationlabel ID
                            | translationlabel REFERENCE"""
        if self.debug_mode:
            print('p_translationlabel_id')
        p[0] = p[1]
        p[0].label.append(p[2])

    def p_translationrangelabel(self, p):
        "translationrangelabel : translationlabel MINUS"
        if self.debug_mode:
            print('p_translationrangelabel')
        p[0] = p[1]

    def p_translationrangelabel_id(self, p):
        """translationrangelabel : translationrangelabel ID
                                 | translationrangelabel REFERENCE"""
        if self.debug_mode:
            print('p_translationrangelabel_id')
        p[0] = p[1]
        p[0].rangelabel.append(p[2])

    def p_translationlabeledline_reference(self, p):
        """translationlabeledline : translationlabeledline reference
                                  | translationlabeledline reference newline"""
        if self.debug_mode:
            print('p_translationlabeledline_reference')
        p[0] = p[1]
        p[0].references.append(p[2])

    def p_translationlabeledline_note(self, p):
        "translationlabeledline : translationlabeledline note_statement"
        if self.debug_mode:
            print('p_translationlabeledline_note')
        p[0] = p[1]
        p[0].notes.append(p[2])

    def p_translationlabelledline_content(self, p):
        """translationlabeledline : translationlabeledline ID
                                  | translationlabeledline ID newline"""
        if self.debug_mode:
            print('p_translationlabelledline_content')
        p[0] = p[1]
        p[0].words.append(p[2])

    def p_linkreference(self, p):
        "link_reference : link_operator ID"
        if self.debug_mode:
            print('p_linkreference')
        p[0] = LinkReference(p[1], p[2])

    def p_linkreference_label(self, p):
        """link_reference : link_reference ID
                          | link_reference COMMA ID"""
        if self.debug_mode:
            print('p_linkreference_label')
        p[0] = p[1]
        p[0].label.append(list(p)[-1])

    def p_link_range_reference_label(self, p):
        """link_range_reference : link_range_reference ID
                                | link_range_reference COMMA ID"""
        if self.debug_mode:
            print('p_link_range_reference_label')
        p[0] = p[1]
        p[0].rangelabel.append(list(p)[-1])

    def p_link_range_reference(self, p):
        """link_range_reference : link_reference MINUS"""
        if self.debug_mode:
            print('p_link_range_reference')
        p[0] = p[1]

    def p_linkreference_statement(self, p):
        """link_reference_statement : link_reference newline
                                    | link_range_reference newline
        """
        if self.debug_mode:
            print('p_linkreference_statement')
        p[0] = p[1]

    def p_link_operator(self, p):
        """link_operator : PARBAR
                         | TO
                         | FROM """
        if self.debug_mode:
            print('p_link_operator')
        p[0] = p[1]

    def p_comment(self, p):
        "comment : COMMENT ID NEWLINE"
        if self.debug_mode:
            print('p_comment')
        p[0] = Comment(p[2])

    def p_check(self, p):
        "comment : CHECK ID NEWLINE"
        if self.debug_mode:
            print('p_check')
        p[0] = Comment(p[2])
        p[0].check = True

    def p_surface_comment(self, p):
        "surface : surface comment %prec LINE"
        if self.debug_mode:
            print('p_surface_comment')
        p[0] = p[1]
        p[0].children.append(p[2])

    def p_translationline_comment(self, p):
        "translationlabeledline : translationlabeledline comment"
        if self.debug_mode:
            print('p_translationline_comment')
        p[0] = p[1]
        p[0].notes.append(p[2])

    def p_translation_comment(self, p):
        "translation : translation comment %prec LINE"
        if self.debug_mode:
            print('p_translation_comment')
        p[0] = p[1]
        p[0].children.append(p[2])

    def p_text_comment(self, p):
        "text : text comment %prec SURFACE"
        if self.debug_mode:
            print('p_text_comment')
        p[0] = p[1]
        p[0].children.append(p[2])

    def p_line_comment(self, p):
        "line : line comment"
        if self.debug_mode:
            print('p_line_comment')
        p[0] = p[1]
        p[0].notes.append(p[2])

    def p_multilingual_comment(self, p):
        "multilingual : multilingual comment"
        if self.debug_mode:
            print('p_multilingual_comment')
        p[0] = p[1]
        p[0].notes.append(p[2])

    def p_score(self, p):
        "score : SCORE ID ID NEWLINE"
        if self.debug_mode:
            print('p_score')
        p[0] = Score(p[2], p[3])

    def p_score_word(self, p):
        "score : SCORE ID ID ID NEWLINE"
        if self.debug_mode:
            print('p_score_word')
        p[0] = Score(p[2], p[3], True)

    def p_text_score(self, p):
        "text : text score"
        if self.debug_mode:
            print('p_text_score')
        p[0] = p[1]
        p[0].score = p[2]

    # There is a potential shift-reduce conflict in the following sample:
    """
      @tablet
      @obverse
      @translation
      @obverse
    """
    # where (object(surface,translation(surface))) could be read as
    # object(surface,translation(),surface)
    # These need to be resolved by making surface establishment and composition
    # take precedence over the completion of a translation

    # A number of conflicts are also introduced by the default rules:

    # A text can directly contain a line (implying obverse of a tablet) etc.
    #

    precedence = (
        # LOW precedence
        ('nonassoc', 'TRANSLATIONEND'),
        ('nonassoc', 'TABLET', 'ENVELOPE', 'PRISM', 'BULLA', 'SEALINGS',
         'FRAGMENT', 'OBJECT', 'MULTI'),
        ('nonassoc', 'OBVERSE', 'REVERSE', 'LEFT', 'RIGHT', 'TOP', 'BOTTOM',
         'FACE',
         'SURFACE', 'EDGE', 'COLUMN', 'SEAL', 'HEADING', 'LINE'),
        ('nonassoc', "LINELABEL", "DOLLAR", "LEM", "NOTE", 'COMMENT',
         'CATCHLINE', 'CHECK',
         'COLOPHON', 'DATE', 'SIGNATURES',
         'SIGNATURE', 'SUMMARY',
         'WITNESSES', "PARBAR", "TO", "FROM"),
        # HIGH precedence
    )

    def p_error(self, p):
        wrong_value=''
        for value in p.value:
            if value.isspace():
                break
            wrong_value += value
        # wrong_value=p.value[0]
        if self.skip:
            self.errors.append((wrong_value,p.lineno, p.lexpos-self.cur_pos, p.type))
            while True:
                tok = self.parser.token() # Get the next token  
                if not tok or tok.type == 'NEWLINE': 
                    break
            return
        else:
            error_mesg=self.log_tmp.yacc_default(wrong_value,p.lineno, p.lexpos-self.cur_pos, p.type) 
            raise SyntaxError(error_mesg)
        
        
        # All errors currently unrecoverable
        # So just throw
        # Add list of params so PyORACC users can build their own error msgs.
