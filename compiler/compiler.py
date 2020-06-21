# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 13:35:06 2020

@author: 이민규
"""

import ActionGoToTable

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

class Parser:
    
    def __init__(self,_lexer):
        self.lexer = _lexer
        self.parserStack = []
        self.parserStack.append(0)
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
    
    
    def readFromTable(self,row,col):
    
#        try:        
#            col = self.actiongotoTableLabel.index(col)
#            row = int(row)
#        except ValueError:
#            print(" ******** Fatal Error: Token not found in Table\n")
#            raise ParsingError
##            return False
#    
        
        # GOTO인 경우 (헷갈리네)
        if not str(row).isdigit():
            col = self.actiongotoTableLabel.index(row)
            row = int(self.parserStack[-2])
        
        #액션 해야하는 경우
        else:
            col = self.actiongotoTableLabel.index(col)
            row = int(row)
            
             
        action = self.actiongotoTable[row][col]
        if(action == '' ):
            print(" ****** Parsing Error, reject\n")
            raise ParsingError
#            return False
        
        return str(action)
    
    
    def printStack_n_Input(self):
        

        print("Stack--> ",self.parserStack,end="  [")
        for i in self.parserInput:
            print(i.tokenToken, end=" ")
        print("] <--Input")
        
            
        pass
    
    def doAction(self,action):
        """
        가장 실질적인 parsing 담당하는 부분.
        GOTO,accept,shift,reduce 에 대해 처리함.
        어려우니까 주석 열심히 달아놓자
        """
        
        #여기 전에 readFromTable함수에서 이미 에러 났어야됨.
        print("ACTION: ",action)
        assert(action!='')

        actionType = action[0] #s12 이면 s, acc이면 a, goto면 숫자
        actionNum = action[1:] #s12 이면 12


        #accept인경우
        if(actionType=='a'):
            return "ACCEPT"
        
        #그냥 goto인경우
        elif(actionType.isdigit()):
            self.parseStack.append(action)
            return "RUNNING"
        
        #action인 경우
        ## shift
        elif (actionType == 's'):
            #shift var
            self.parserStack.append(self.parserInput.pop(0))
            #shift state
            self.parserStack.append(str(actionNum))
            
            return "RUNNING"
            
        ## reduce
        elif (actionType == 'r'):
            print("\n\nREDUCE!!!!!\n\n")
            raise ParsingError
            pass
            
            return "RUNNING"
        
        
            
            
        
        else:
            raise UnknownParsingError
        
        

    
    def parseOnce(self):
        
        stackTop = self.parserStack[-1]
        inputTop = self.parserInput[0].tokenType
        
        action = self.readFromTable(stackTop,inputTop)    
        actionResult = self.doAction(action)
               
        self.printStack_n_Input()
        
        return actionResult
    

# ************  main **************** #
        
if __name__ == '__main__':
    
    try:
        ## input Source Code
        inputStream = "__WORD__ ( ) { int __WORD__ , __WORD__ ; __WORD__ = __NUM__ ; RETURN __NUM__ ; } "
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