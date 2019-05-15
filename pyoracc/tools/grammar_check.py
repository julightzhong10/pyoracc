
class GrammarCheck(object):
    def __init__(self):
        self.errors = [] #error list
        self.errors_str = [] #error list

        self.orig_line = 0
        self.orig_input = ''

        self.ids = [] # id lines, e.g. &P123456 = AB 78, 910
        self.lans = [] # language lines, e.g. #atf: lang akk 
        self.objs = [] # objects lines, e.g. @tablet
        self.surfaces = [] # surfarces lines, e.g. @column 2
        self.trans = [] # transliterration lines, e.g. 1. dub-sar
        self.dollars = [] # $ comment lines, e.g. $ blank space 


    def print_test(self):
        self.structure_check(0)
        print('----(GrammarCheck----')
        print(self.ids)
        print(self.lans)
        print(self.objs)
        print(self.surfaces)
        print(self.trans)
        print(self.dollars)
        print(self.errors_str)
        print('----GrammarCheck)----')


    def add_id(self,idn):
        '''
        :params id: int, the line number in segmented file
        :return: N/A

        add line number of atf id line (e.g. &P010032 = CT 50, 019) to the self.ids
        '''
        self.ids.append(idn)

    def add_lan(self,lan):
        '''
        :params lan: int, the line number in segmented file
        :return: N/A

        add line number of language protocal line (e.g. #atf: lang akk) to the self.lans
        '''
        self.lans.append(lan)

    def add_objs(self,obj):
        '''
        :params obj: int, the line number in segmented file
        :return: N/A

        add line number of object type line (e.g. @tablet) to the self.objs
        '''
        self.objs.append(obj)

    def add_surfaces(self,surface):
        '''
        :params surface: int, the line number in segmented file
        :return: N/A

        add line number of surface line (e.g. @reverse) to the self.surfaces
        '''
        self.surfaces.append(surface)

    def add_trans(self,tran_id,tran_line):
        '''
        :params tran_id: str, transliterration id
        :params tran_line: int, the line number in segmented file
        :return: N/A

        add id and line number of transliterration line (e.g. 4. szu nam-ti-la-ni) to the self.trans as a tuple (tran_id,tran_line)
        '''
        self.trans.append((tran_id,tran_line))

    def add_dollars(self,dollar):
        '''
        :params dollar: int, the line number in segmented file
        :return: N/A

        add line number of dollar comments line (e.g. $ blank space) to the self.dollars
        '''
        self.dollars.append(dollar)
    
    def structure_check(self,):
        '''
        :return: N/A

        check different rules and append error message to self.error
        '''
        
        '''check ID line'''
        if len(self.ids)<1:
            self.errors_str.append(u"PyOracc Error: First line of a text should always start with like \"&P123456 = AB 78, 910\"")
        elif len(self.ids)>1:
            tmp_error_str=u"PyOracc Error: Mutiple ID lines (e.g. &P123456 = AB 78, 910) at line "
            for i in range(len(self.ids)):
                tmp_error_str+=str(self.orig_line+self.ids[i])
                tmp_error_str+=', ' if i<(len(self.ids)-1) else ''
            self.errors_str.append(tmp_error_str)
        
        '''check language line'''
        if len(self.lans)<1:
            self.errors_str.append(u"PyOracc Error: Missing language line (e.g. #atf: lang akk)")
        elif len(self.lans)>1:
            tmp_error_str=u"PyOracc Error: Mutiple languages lines (e.g. #atf: lang akk) at line "
            for i in range(len(self.lans)):
                tmp_error_str+=str(self.orig_line+self.lans[i])
                tmp_error_str+=', ' if i<(len(self.lans)-1) else ''
            self.errors_str.append(tmp_error_str)

        '''check objects line'''
        if len(self.objs)<1:
            self.errors_str.append(u"PyOracc Error: Missing object line (e.g. @tablet)")
        elif len(self.objs)>1:
            tmp_error_str=u"PyOracc Error: Mutiple object lines (e.g. @tablet) at line "
            for i in range(len(self.objs)):
                tmp_error_str+=str(self.orig_line+self.objs[i])
                tmp_error_str+=', ' if i<(len(self.objs)-1) else ''
            self.errors_str.append(tmp_error_str)

        '''check $comment or transliterration line'''
        if len(self.dollars)<1 and len(self.surfaces)<1 and len(self.trans)<1:
            self.errors_str.append(u"PyOracc Error: at least 1 dollar comment line (e.g. $ blank space) or 1 surface line (e.g. @column 2) with 1 transliterration line (e.g. 1. dub-sar)")
        
        '''check surface and transliterration sequence'''
        for i in range(len(self.))
