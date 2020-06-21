# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 13:35:06 2020

@author: 이민규
"""

import ActionGoToTable
import sys
import time
import copy

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
class LexerError(Exception):
    pass
class CodeGenerationError(Exception):
    pass
class StringMultiplicationError(Exception):
    pass
class VariableRedefinitionError(Exception):
    pass
class UndefinedVariableError(Exception):
    pass
class EX101(Exception):
    pass
class EX102(Exception):
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
        self.tokenValue = _tokenToken
        self.tokenToken = _tokenToken
        self.tokenType = _tokenType
        
        self.childTokenList = []
        self.hasChild = False
        self.codeMade = False

    def __str__(self):
#        return "token("+self.tokenToken+")"
        return self.tokenToken
    
    def __repr__(self):
#        return "token("+self.tokenToken+")"
        return self.tokenToken
    
    
    
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
        print("\n*********  Inputs  *********\n")
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
                raise LexerError
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
    
    popStack = []

    
    
    @staticmethod
    def pop_stack_2n(_parser,n):
        Action.popStack = []
        for i in range(0,n):
            _parser.parserStack.pop()
            Action.popStack.append(_parser.parserStack.pop())
            
            
        
            
    @staticmethod
    def push_stack(_parser,_pushtoken):
        _pushtoken = Token(-1,_pushtoken,_pushtoken)
        _pushtoken.hasChild = True
        _pushtoken.childTokenList = copy.deepcopy(Action.popStack)
        _pushtoken.childTokenList.reverse()
        
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
        
        self.printStack_n_Input()
        stackTop = self.parserStack[-1]
        inputTop = self.parserInput[0]
        
        action = self.readFromTable(stackTop,inputTop)    
        actionResult = self.doAction(action)
               
        
        return actionResult
    
    def readFromTable(self,row,col):
        
#        print("inputROW:",row)
#        print("inputCOL:",col)
#        print("ROW--obj",row)
        
        # GOTO인 경우 (헷갈리네)
        if (not new_isdigit(row)):

            col = self.actiongotoTableLabel.index(row.tokenType)
            row = int(self.parserStack[-2])
            action = self.actiongotoTable[row][col]
        
        #액션 해야하는 경우
        else:
            col = self.actiongotoTableLabel.index(col.tokenType)
            row = int(row)
            action = self.actiongotoTable[row][col]                
            
#        print("ROW",row)
#        print("COL",col)
        print("ACTION", action)
            
        if action == '' :
            print(" ****** Parsing Error, reject\n")
            raise ParsingError
#            return False    
        
        elif action[0] == 'a' or action[0].isdigit() or action[0] == 's' or action[0] == 'r':
            return str(action)
        
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
        
        print("STACK---> ",self.parserStack, end="     ")
        print(self.parserInput,"<--- INPUT")
            
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

class Register:
    regi = 0
    
    def __init__(self,_regNum=0,_regValue=0):
        self.regNum = _regNum
        self.regValue = _regValue
    
    def Add(self):
        Register.regi += 1
        self.regNum = Register.regi
        
class CodeGenerator:
    
    code = []
    symbol = []
    reg = 0
    
    
    def __init__(self,_lexer,_parser):
        self.parser = _parser
        self.lexer = _lexer
        self.head = self.parser.parserStack[1]
    
    def printIntermediateCode(self):
        print("***** Intermediate Code *******")
        for i in self.code:
            print(i)
        print("")
        
    def printOutIntermediateCode(self,_filename):
        
        infile = open(_filename+'.code','w',encoding='UTF8')
        
        for i in self.code:
            infile.writelines(i + "\n")
    
        infile.close()
    
    def traverseTreeFront2Back(self,_token):

        #if token is leaf node
        if(type(_token)==str):
            return
#        
        if(not _token.codeMade):
            if(_token.tokenType == "__PROG__"):
                self.generateCode_Prog(_token)
            
        if(_token.hasChild):
            for i in _token.childTokenList:
                self.traverseTreeFront2Back(i)
            
        else:
            #print(_token)
            return
        
    def generateCode_Fact(self,_token):
        #print(" WOW FACT-->" , _token.childTokenList)
        
        if(_token.childTokenList[0].tokenType == "__NUM__"):
 
            regiMe = Register()
            regiMe.regValue = _token.childTokenList[0].tokenValue
            regiMe.Add()
            self.code.append("LD REG{0}, ${1}".format(regiMe.regNum,regiMe.regValue))
            
            return regiMe
            
        elif(_token.childTokenList[0].tokenType == "__WORD__"):
            
            regiMe = Register()
            regiMe.regValue = _token.childTokenList[0].tokenValue
            regiMe.Add()
            self.code.append("LD REG{0}, &{1}".format(regiMe.regNum,regiMe.regValue))
            
            return regiMe
        
        else:
            print("FACT generation ERROR");
            raise CodeGenerationError
        
    
    def generateCode_Term(self,_token):
        
        #print(" WOW TERM-->" , _token.childTokenList)
        
        if( len(_token.childTokenList) == 1):
            
            regiSon = self.generateCode_Fact(_token.childTokenList[0])
                        
            regiMe = Register()
            regiMe.regValue = regiSon.regValue
            regiMe.Add()
            
        
            self.code.append("LD REG{0}, REG{1}".format(regiMe.regNum,regiSon.regNum))

            
            return regiMe
        
        
        elif( len(_token.childTokenList) == 3):
        
            regiSon1 = self.generateCode_Fact(_token.childTokenList[0])
            regiSon2 = self.generateCode_Fact(_token.childTokenList[2])
            
            regiMe = Register()
            
            if (regiSon1.regValue).isdigit() and regiSon2.regValue.isdigit():
                regiMe.regValue = str(int(regiSon2.regValue) * int(regiSon1.regValue))
            
            else:
                raise StringMultiplicationError
            
            regiMe.Add()
            
            self.code.append("MUL REG{0}, REG{1}, REG{2}".format(regiMe.regNum,regiSon1.regNum,regiSon2.regNum))
            
            return regiMe
            
            
        else:
            print("FACT generation ERROR");
            raise CodeGenerationError
                
            
    def generateCode_Expr(self,_token):
        
        #print(" WOW EXPR-->" , _token.childTokenList)
        
        if( len(_token.childTokenList) == 1):
        
            regiSon = self.generateCode_Term(_token.childTokenList[0])
            
            regiMe = Register()
            regiMe.regValue = regiSon.regValue
            regiMe.Add()
            
            self.code.append("LD REG{0}, REG{1}".format(regiMe.regNum,regiSon.regNum))
            
            return regiMe        
        
        elif( len(_token.childTokenList) == 3):
        
            regiSon1 = self.generateCode_Term(_token.childTokenList[0])
            regiSon2 = self.generateCode_Term(_token.childTokenList[2])
            
            regiMe = Register()
            regiMe.regValue = regiSon1.regValue +regiSon2.regValue
            regiMe.Add()
            
            self.code.append("ADD REG{0}, REG{1}, REG{2}".format(regiMe.regNum,regiSon1.regNum,regiSon2.regNum))
            
            return regiMe
        
        
    def generateCode_Cond(self,_token):
        
        #print(" WOW COND-->" , _token.childTokenList)
        
        if( _token.childTokenList[1].tokenValue == ">" ):
        
            regiSon1 = self.generateCode_Expr(_token.childTokenList[0])
            regiSon2 = self.generateCode_Expr(_token.childTokenList[2])
            
            regiMe = Register()
            
            tmp = (regiSon1.regValue > regiSon2.regValue)
            
            if(tmp):
                regiMe.regValue = 1
            else:
                regiMe.regValue = 0
                
            regiMe.Add()
            
            self.code.append("LT REG{0}, REG{1}, REG{2}".format(regiMe.regNum,regiSon1.regNum,regiSon2.regNum))
            
            return regiMe        
        
        elif( _token.childTokenList[1].tokenValue == "==" ):
        
            regiSon1 = self.generateCode_Expr(_token.childTokenList[0])
            regiSon2 = self.generateCode_Expr(_token.childTokenList[2])
            
            regiMe = Register()
            
            tmp = (regiSon1.regValue == regiSon2.regValue)
            
            if(tmp):
                regiMe.regValue = 1
            else:
                regiMe.regValue = 0
                
            regiMe.Add()
            
            self.code.append("LT REG{0}, REG{1}, REG{2}".format(regiMe.regNum,regiSon1.regNum,regiSon2.regNum))
            
            return regiMe        

        
    def generateCode_Stat(self,_token):
        
        #print(" WOW STAT-->" , _token.childTokenList)
        
        #Stat -> IF cond THEN block ELSE block
        #Stat -> WHILE cond block
        #Stat -> RETURN expr ;
#        print(_token.childTokenList)
        if(_token.childTokenList[0].tokenType=="RETURN"):
                
            regiSon = self.generateCode_Expr(_token.childTokenList[1])
            regiMe = Register()
            regiMe.regValue = regiSon.regValue
            regiMe.Add()
            self.code.append("LD %eax{0}, REG{1}".format(regiMe.regNum,regiSon.regNum))
            self.storeSymbol(self.symbol[0][0].tokenValue, regiMe.regValue+" (%eax)")
            return regiMe
        #Stat -> Word  = Expr
        elif(_token.childTokenList[0].tokenType=="__WORD__"):
                
            regiSon = self.generateCode_Expr(_token.childTokenList[2])
#            regiMe = Register()
#            regiMe.regValue = regiSon.regValue
#            regiMe.Add()
            
            self.storeSymbol(_token.childTokenList[0].tokenValue,regiSon.regValue)
            self.code.append("ST &{0}, REG{1}".format(_token.childTokenList[0].tokenValue,regiSon.regNum))
            
#            return regiMe

    def generateCode_Decls(self,_token):
        
        #print(" WOW Decls-->" , _token.childTokenList)
        
        if(not _token.childTokenList):
            return
        
        else:
            self.generateCode_Decls(_token.childTokenList[0])
            self.generateCode_Decl(_token.childTokenList[1])
        
        return
    
    def generateCode_Decl(self,_token):
        
        #print(" WOW Decl-->" , _token.childTokenList)
        
        
        if(_token.childTokenList[0].childTokenList[0].tokenValue == "int"):
            tmp_type = "__INTEGER__"
        else:
            tmp_type = "__CHARACTER__"
            
        self.generateCode_Words(_token.childTokenList[1],tmp_type)
        
    
    def generateCode_Words(self,_token,_type):
        #print(" WOW Words-->" , _token.childTokenList)
        
        # Words -> Word
        if(_token.childTokenList[0].tokenType == "__WORD__"):
            self.generateCode_Word(_token.childTokenList[0],_type)
        
        # Words -> Words Word
        else:
            self.generateCode_Words(_token.childTokenList[0],_type)
            self.generateCode_Word(_token.childTokenList[2],_type)
        
    def generateCode_Word(self,_token,_type):

        if(self.checkRedundantSymbol(_token)):
            raise VariableRedefinitionError
            
        CodeGenerator.symbol.append([_token,_type,0])
                    
    def generateCode_Slist(self,_token):
        #print(" WOW Slist-->" , _token.childTokenList)
        
        # Slist -> Slist Stat
        if(_token.childTokenList[0].tokenType == "__SLIST__"):
            self.generateCode_Slist(_token.childTokenList[0])
            self.generateCode_Stat(_token.childTokenList[1])
        
        # Slist -> Slist
        else:
            self.generateCode_Stat(_token.childTokenList[0])
    
    def generateCode_Block(self,_token):
        
        self.generateCode_Decls(_token.childTokenList[1])
        self.generateCode_Slist(_token.childTokenList[2])

    def generateCode_Prog(self,_token):
     
        self.generateCode_Word(_token.childTokenList[0],"__FUNCTION__")
        self.generateCode_Block(_token.childTokenList[3])
    
    def checkRedundantSymbol(self,_token):
        
        for i in CodeGenerator.symbol:
            if(_token.tokenValue == i[0].tokenValue):
                print("\n\n***Redefinition of ",_token.tokenValue)
                return True
        return False
    
    def storeSymbol(self,_tokenName,_value):
        
        for i in CodeGenerator.symbol:
            if(_tokenName == i[0].tokenValue):
                i[2] = _value
                return
        
        raise UndefinedVariableError
    
    def printSymbolTable(self):
        
        print("\n****** Symbol Table ******")
        print("NAME".ljust(20),"TYPE".ljust(20),"VALUE".ljust(20))
        
        for i in self.symbol:
            print(i[0].tokenValue.ljust(20),i[1].ljust(20),str(i[2]).ljust(20))
    
    
    def printOutSymbolTable(self,_filename):
    
        infile = open(_filename+'.symbol','w',encoding='UTF8')
        
        infile.writelines("NAME".ljust(20)+"TYPE".ljust(20)+"VALUE".ljust(40)+"\n")
        for i in self.symbol:
            infile.writelines(i[0].tokenValue.ljust(20)+i[1].ljust(20)+str(i[2]).ljust(40)+"\n")
    
        infile.close()

class FileReader:
    
    @staticmethod
    def readFile(_filename):

        fileData = ""
        
        infile = open(_filename,'r',encoding='UTF8')
        lines = infile.readlines()
        for i in lines:
            fileData+=i
        infile.close()
        
        return fileData
        
# ************  main **************** #
if __name__ == '__main__':
    try:
        ## input Source Code
#        inputStream = "__WORD__ ( ) { int __WORD__ , __WORD__ ; __WORD__ = __NUM__ ; RETURN __NUM__ ; } "
        inputFile = sys.argv[1]
        inputStream = FileReader.readFile(inputFile)
        inputFile = inputFile.split('.')
        inputFile = inputFile[0]
#        inputStream = "myfunction ( ) { int numOne , numTwo  ; char Apple , Banana ; Banana = Yellow ; Apple = PenPineapple + ApplePen ; numOne = 7 ; RETURN 1010 * 2 ; }"
        
        
        ## Preprocessing.   
    
        preprocessor = Preprocessor(inputStream)
        inputStream = preprocessor.process()
    
        
        ## lexical analysis
        lexer = Lexer(inputStream)
        lexer.makeSplitTable() 
        lexer.printSplitTable()
        lexer.makeTokenTableAndCheckError(DISTINCT = False) #여기에서 오류검출함
        lexer.printTokenTable()
        
        ## Syntactic anlysis
        
        parser = Parser(lexer)
        parser.parse() #return only on success
        
        print("\nParsing Success... Ending Programm... \n2017314789 이민규\n2016313561 서운지\n\n")


        ## Code Generation
        codeGenerator = CodeGenerator(lexer,parser)
        codeGenerator.traverseTreeFront2Back(parser.parserStack[1])
        codeGenerator.printIntermediateCode()
        codeGenerator.printOutIntermediateCode(inputFile)
        codeGenerator.printSymbolTable()
        codeGenerator.printOutSymbolTable(inputFile)

        
        
        print(inputStream)
        time.sleep(10)

    except ParsingError:
        print("\nParsing Fail...  \n2017314789 이민규\n2016313561 서운지\n")
        time.sleep(10)
    except UnknownParsingError:
        print("\nFatal Parse Error... Something went wrong in source code... probably my mistake :( \n2017314789 이민규\n2016313561 서운지\n")
        time.sleep(10)
    except LexerError:
        print("\nLexer Error...\n2017314789 이민규\n2016313561 서운지\n")
        time.sleep(10)
    except CodeGenerationError:
        print("\nCodeGeneration Error...\n2017314789 이민규\n2016313561 서운지\n")
        time.sleep(10)
    except StringMultiplicationError:
        print("\nStringMultiplicationError! Can only multiply __NUM__ and __NUM__...\n2017314789 이민규\n2016313561 서운지\n")
        time.sleep(10)    
    except VariableRedefinitionError:
        print("VariableRedefinitionError! Can define Same variable only once...\n2017314789 이민규\n2016313561 서운지\n")
        time.sleep(10)
    except UndefinedVariableError:
        print("\nUndefinedVariableError! Tried to access or assign undefined variable\n2017314789 이민규\n2016313561 서운지\n")
        time.sleep(10)
        
        
    ##임시용    
    except EX101:
        print("\nEX101\n2017314789 이민규\n2016313561 서운지\n")
        time.sleep(10)
    except EX102:
        print("\nEX102\n2017314789 이민규\n2016313561 서운지\n")
        time.sleep(10)
        
        
        