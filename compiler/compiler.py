# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 13:35:06 2020

@author: 이민규
"""

import ActionGoToTable

#isdigit 함수가 클래스 내부에서 제대로 작동 안해서 만듦
def new_isdigit(_s):
    
    if _s=='0'\
        or _s=='1'or _s=='2'or _s=='3'or _s=='4'or _s=='5'\
        or _s=='6'or _s=='7'or _s=='8'or _s=='9'or _s=='10'\
        or _s=='11'or _s=='12'or _s=='13'or _s=='14'or _s=='15'\
        or _s=='16'or _s=='17'or _s=='18'or _s=='19'or _s=='20'\
        or _s=='21'or _s=='22'or _s=='23'or _s=='24'or _s=='25'\
        or _s=='26'or _s=='27'or _s=='28'or _s=='29'or _s=='30'\
        or _s=='31'or _s=='32'or _s=='33'or _s=='34'or _s=='35'\
        or _s=='36'or _s=='37'or _s=='38'or _s=='39'or _s=='40'\
        or _s=='41'or _s=='42'or _s=='43'or _s=='44'or _s=='45'\
        or _s=='46'or _s=='47'or _s=='48'or _s=='49'or _s=='50':
    
        return True
    else:
        return False


class ParsingError(Exception):
    pass
class UnknownParsingError(Exception):
    pass

class Preprocessor:
    
    def __init__(self,_inputStream):
        self.inputStream = _inputStream
        
    
    def process(self):
        while("#define" in self.inputStream):
            macroStart = self.inputStream.find("#define")
            macroEnd = self.inputStream[macroStart:].find("\n") + macroStart
            macro = self.inputStream[macroStart:macroEnd].strip().split(" ")
            self.inputStream = self.inputStream[macroEnd:]
            self.inputStream = self.inputStream.replace(" "+macro[1]+" "," "+macro[2]+" ")
            self.inputStream = self.inputStream.strip()
                                                
        self.inputStream = self.inputStream.replace("\t", " ")
        self.inputStream = self.inputStream.replace("\n", " ")
    
        while ("  " in self.inputStream):
            self.inputStream = self.inputStream.replace("  "," ")
        
        return self.inputStream

class Token:
    
    def __init__(self,_count=-1,_tokenToken="",_tokenType=""):
        self.tokenCount = _count
        self.tokenToken = _tokenToken
        self.tokenType = _tokenType  

    def __str__(self):
#        return "token("+self.tokenToken+")"
        return self.tokenToken
    
    def __repr__(self):
#        return "token("+self.tokenToken+")"
        return self.tokenToken
    
    def isdigit():
        return false
    
    
    def checkAndAssignTokenType(self):

        #목록별 가능한 Token Type
        validTokenListBracket = ["{","}","(",")"]
        validTokenListOperation = ["=",">","*","==","+",",",";"]
        validTokenListControlStatement = ["IF","THEN","ELSE","ENDIF","WHILE","RETURN"]
        validTokenListTypeDef = ["int","char"]
        validTokenListNonTerminals = ["__FACT__", "__NUM__", "$", "__PROG__", "__DECLS__", "__DECL__",	"__WORDS__", "__VTYPE__",\
                                      "__BLOCK__",	"__SLIST__", "__STAT__", "__COND__",	"__EXPR__",	"__TERM__"]


        #지정해준 가능한 Token Type들
        if self.tokenToken in validTokenListBracket:
            self.tokenType = self.tokenToken
            return True
        
        elif self.tokenToken in validTokenListOperation:
            self.tokenType = self.tokenToken
            return True
        
        elif self.tokenToken in validTokenListControlStatement:
            self.tokenType = self.tokenToken
            return True
        
        elif self.tokenToken in validTokenListTypeDef:
            self.tokenType = self.tokenToken
            return True
        
        elif self.tokenToken in validTokenListNonTerminals:
            self.tokenType = self.tokenToken
            return True
                
        #그 외 기타 문자열 및 숫자
        elif self.tokenToken.isalpha():
            self.tokenType = "__WORD__"
            return True
        
        elif self.tokenToken.isdigit():
            self.tokenType = "__NUM__"
            return True    
        
        else:
            print("\n *** Error found in : ",self.tokenToken)
            print()
            return False

class Lexer:
    def __init__(self,_inputStream):
        self.splitTable = []
        self.tokenTable = []
        self.inputStream = _inputStream
        
    
    # 토큰테이블에 중복 값 안들어가게    
    def checkDistinctToken(self,_token) :
        for i in self.tokenTable:
            if i.tokenToken == _token.tokenToken:
                return False
            
        return True
            
    # inputStream 을 쪼개놓은 리스트 만들기
    def makeSplitTable(self):
        
        i=0
        j=0
        
        #inputStream 쭉 돌면서 (공백or탭or개행문자) or (끝에도달) 나오면 자르기
        while( i < len(self.inputStream)):
            for j in range (i,len(self.inputStream)):
                if (self.inputStream[j] == ' ' or \
                    self.inputStream[j] == '\t' or self.inputStream[j] == '\n') :
                    
                    self.splitTable.append(self.inputStream[i:j])
                    i = j
                    break
                
                elif (j == len(self.inputStream)-1):
                    self.splitTable.append(self.inputStream[i:])
                    i = j
                    break
            #end for
            i+=1
        #end while
            
    def printSplitTable(self):
        for i in self.splitTable:
            print(i)
    
    def getSplitTable(self):
        return self.splitTable
        
    #splitTalbe 기반으로 토큰테이블 만들기
    def makeTokenTableAndCheckError(self, DISTINCT):
        
        indexCounter = 0
        errorPlaceCounter = 0
        for i in self.splitTable:
            errorPlaceCounter += len(i)+1
            
            _tokenCount = indexCounter
            _tokenToken = i
            _tokenType = "defaultType"
            token = Token(_tokenCount,_tokenToken,_tokenType)
            
            #오류인 경우
            if (not token.checkAndAssignTokenType()):
                print("ToDo 오류 위치 출력 임시용: Error Location --> ",str(indexCounter)+"'s Token, ",str(errorPlaceCounter-len(i))+"'s character")
                raise ParsingError
                return False
            
            #정상인 경우
            elif (not DISTINCT or self.checkDistinctToken(token)):
                self.tokenTable.append(token)
                
                
            indexCounter+=1
        #end for
        return True
    
    def printTokenTable(self):
        print("\n*********  TOKEN TABLE  *********\n")
        print("Count".ljust(7),"Token".ljust(20),"Type","\n")
        for i in self.tokenTable:
            print(str(i.tokenCount).ljust(7),i.tokenToken.ljust(20), i.tokenType)
        print("")
    
    def getTokenTable(self):
        return self.tokenTable

class Action:
    
    def __init__(self):
        pass

    @staticmethod
    def pop_stack_2n(_parser,n):
        for i in range(0,2*n):
            _parser.parserStack.pop()
          
            
    @staticmethod
    def push_stack(_parser,_pushtoken):
        #Todo 이러면 다시 못찾으니까 tree만들때 다시 수정하자
        _pushtoken = Token(-1,_pushtoken,_pushtoken)
        _parser.parserStack.append(_pushtoken)
        
    @staticmethod
    def goto(_parser,_action):
        _parser.parserStack.append(_action)
    
    @staticmethod
    def shift(_parser,_actionNum):
            
            #shift var
            _parser.parserStack.append(_parser.parserInput.pop(0))
            #shift state
            _parser.parserStack.append(str(_actionNum))

    @staticmethod
    def reduce(_parser,_actionNum):
        """
        0) __START__ -> __PROG__
        1) __PROG__ -> __WORD__ ( ) __BLOCK__
        
        2) __DECLS__ -> __DECLS__ __DECL__
        3) __DECLS__ -> ''
        
        4) __DECL__ -> __VTYPE__ __WORDS__ ;
        
        
        5) __WORDS__ -> __WORDS__ , __WORD__
        6) __WORDS__ -> __WORD__
        
        7) __VTYPE__ -> int
        8) __VTYPE__ -> char
        
        9) __BLOCK__ -> { __DECLS__ __SLIST__ }
        10) __BLOCK__ -> ''
        
        11) __SLIST__ -> __SLIST__ __STAT__
        12) __SLIST__ -> __STAT__
        
        13) __STAT__ -> IF __COND__  THEN __BLOCK__ ELSE __BLOCK__
        14) __STAT__ -> WHILE __COND__ __BLOCK__
        15) __STAT__ -> __WORD__ = __EXPR__ ; 
        16) __STAT__ -> RETURN __EXPR__ ;
        
        17) __COND__ -> __EXPR__ > __EXPR__
        18) __COND__ -> __EXPR__ == __EXPR__
        
        19) __EXPR__ -> __TERM__
        20) __EXPR__ -> __TERM__ + __TERM__
        
        21) __TERM__ -> __FACT__
        22) __TERM__ -> __FACT__ * __FACT
        
        23) __FACT__ -> __NUM__
        24) __FACT__ -> __WORD__
        
        """
        
        case = int(_actionNum)
        if case == 0:
            Action.pop_stack_2n(_parser,1)
            Action.push_stack(_parser,"__START__")
        elif case == 1:
            Action.pop_stack_2n(_parser,4)
            Action.push_stack(_parser,"__PROG__")
            
        elif case == 2:
            Action.pop_stack_2n(_parser,2)
            Action.push_stack(_parser,"__DECLS__")
            
        elif case == 3:
            Action.pop_stack_2n(_parser,0)
            Action.push_stack(_parser,"__DECLS__")
            
        elif case == 4:
            Action.pop_stack_2n(_parser,3)
            Action.push_stack(_parser,"__DECL__")
            
        elif case == 5:
            Action.pop_stack_2n(_parser,3)
            Action.push_stack(_parser,"__WORDS__")
            
        elif case == 6:
            Action.pop_stack_2n(_parser,1)
            Action.push_stack(_parser,"__WORDS__")
            
        elif case == 7:
            Action.pop_stack_2n(_parser,1)
            Action.push_stack(_parser,"__VTYPE__")
            
        elif case == 8:
            Action.pop_stack_2n(_parser,1)
            Action.push_stack(_parser,"__VTYPE__")
            
        elif case == 9:
            Action.pop_stack_2n(_parser,4)
            Action.push_stack(_parser,"__BLOCK__")
            
        elif case == 10:
            Action.pop_stack_2n(_parser,0)
            Action.push_stack(_parser,"__BLOCK__")
            
        elif case == 11:
            Action.pop_stack_2n(_parser,2)
            Action.push_stack(_parser,"__SLIST__")
            
        elif case == 12:
            Action.pop_stack_2n(_parser,1)
            Action.push_stack(_parser,"__SLIST__")
            
        elif case == 13:
            Action.pop_stack_2n(_parser,6)
            Action.push_stack(_parser,"__STAT__")
            
        elif case == 14:
            Action.pop_stack_2n(_parser,3)
            Action.push_stack(_parser,"__STAT__")
            
        elif case == 15:
            Action.pop_stack_2n(_parser,4)
            Action.push_stack(_parser,"__STAT__")
            
        elif case == 16:
            Action.pop_stack_2n(_parser,3)
            Action.push_stack(_parser,"__STAT__")
            
        elif case == 17:
            Action.pop_stack_2n(_parser,3)
            Action.push_stack(_parser,"__COND__")
            
        elif case == 18:
            Action.pop_stack_2n(_parser,3)
            Action.push_stack(_parser,"__COND__")
            
        elif case == 19:
            Action.pop_stack_2n(_parser,1)
            Action.push_stack(_parser,"__EXPR__")
            
        elif case == 20:
            Action.pop_stack_2n(_parser,3)
            Action.push_stack(_parser,"__EXPR__")
            
        elif case == 21:
            Action.pop_stack_2n(_parser,1)
            Action.push_stack(_parser,"__TERM__")
            
        elif case == 22:
            Action.pop_stack_2n(_parser,3)
            Action.push_stack(_parser,"__TERM__")
            
        elif case == 23:
            Action.pop_stack_2n(_parser,1)
            Action.push_stack(_parser,"__FACT__")
            
        elif case == 24:
            Action.pop_stack_2n(_parser,1)
            Action.push_stack(_parser,"__FACT__")
            

class Parser:
    
    def __init__(self,_lexer):
        self.lexer = _lexer
        self.parserStack = []
        self.parserStack.append('0')
        self.parserInput = _lexer.getTokenTable()
        self.parserInput.append(Token(_tokenToken="$",_tokenType="$"))
        
            
        self.actiongotoTable = ActionGoToTable.generateTable()
        self.actiongotoTableLabel = ActionGoToTable.generateLabel()
    
    def parse(self):
        
        while(True):
            
            result = parser.parseOnce()
                    
            if (result == "RUNNING"):
                continue
            if (result == "ACCEPT"):
                break
            if (result == "ERROR"):
                raise ParsingError                        
            
        return

    def parseOnce(self):
        
        stackTop = self.parserStack[-1]
        inputTop = self.parserInput[0]
        
        action = self.readFromTable(stackTop,inputTop)    
        actionResult = self.doAction(action)
               
        self.printStack_n_Input()
        
        return actionResult
    
    def readFromTable(self,row,col):
        
        print("inputROW:",row)
        print("inputCOL:",col)
        
        # GOTO인 경우 (헷갈리네)
        print("ROW--obj",row)
        if (not new_isdigit(row)):
            print("here")
            col = self.actiongotoTableLabel.index(row.tokenType)
            row = int(self.parserStack[-2])
            action = self.actiongotoTable[row][col]
        
        #액션 해야하는 경우
        else:
            col = self.actiongotoTableLabel.index(col.tokenType)
            row = int(row)
            action = self.actiongotoTable[row][col]                
            
        print("ROW",row)
        print("COL",col)
        print("ACTION", action)
            
        if action[0] == 'a' or action[0].isdigit() or action[0] == 's' or action[0] == 'r':
            return str(action)
        
        elif action == '' :
            print(" ****** Parsing Error, reject\n")
            raise ParsingError
#            return False    
        else:
            raise UnknownParsingError
        
    
    
    def printStack_n_Input(self):
        

#        print("Stack--> [")
#        for i in self.parserStack:
#            print(i.tokenToken,end=" ")
#                         
#        print(self.parserStack,end="")
#        print("]",end="")
#        
#        print("[",end="")
#        for i in self.parserInput:
#            print(i.tokenToken, end=" ")
#        print("] <--Input")
        
        print("STACK: ",self.parserStack, end="     ")
        print(self.parserInput,": INPUT")
            
        pass
    
    def doAction(self,action):
        """
        가장 실질적인 parsing 담당하는 부분.
        GOTO,accept,shift,reduce 에 대해 처리함.
        어려우니까 주석 열심히 달아놓자
        """
        
        #여기 전에 readFromTable함수에서 이미 에러 났어야됨.
        assert(action!='')

        actionType = action[0] #s12 이면 s, acc이면 a, goto면 숫자
        actionNum = action[1:] #s12 이면 12


        #accept인경우
        if(actionType=='a'):
            return "ACCEPT"
        
        #그냥 goto인경우
        elif(actionType.isdigit()):
            Action.goto(self,action)
            return "RUNNING"
        
        #action인 경우
        ## shift
        elif (actionType == 's'):
            Action.shift(self,actionNum)
            return "RUNNING"
            
        ## reduce
        elif (actionType == 'r'):
            Action.reduce(self,actionNum)                    
            return "RUNNING"
        
        
            
            
        
        else:
            raise UnknownParsingError

    

# ************  main **************** #
        
if __name__ == '__main__':
    
    try:
        ## input Source Code
#        inputStream = "__WORD__ ( ) { int __WORD__ , __WORD__ ; __WORD__ = __NUM__ ; RETURN __NUM__ ; } "
        inputStream = "wordOne ( ) { int wordTwo , wordThree ; wordFour = 1111 ; RETURN 2222 ; }"
    
        
        ## preprocessing.   
    
        preprocessor = Preprocessor(inputStream)
        inputStream = preprocessor.process()
    
        
        ## lexical analysis
        lexer = Lexer(inputStream)
        lexer.makeSplitTable() 
        lexer.printSplitTable()
        assert(lexer.makeTokenTableAndCheckError(DISTINCT = False)) #여기에서 오류검출함
        lexer.printTokenTable()
    #    lexer.printTokenTable_CSV()
        
        ## syntactic anlysis
        
        parser = Parser(lexer)
        parser.parse() #return only on success
        
        print("\nParsing Success... Ending Programm... \n2017314789 이민규\n")



    except ParsingError:
        print("Parsing Fail...  \n2017314789 이민규\n")
    except UnknownParsingError:
        print("Fatal Parse Error... Something went wrong in source code... probably my mistake :( \n2017314789 이민규\n")