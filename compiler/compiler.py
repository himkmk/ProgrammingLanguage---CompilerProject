# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 13:35:06 2020

@author: 이민규
"""

import ActionGoToTable

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
        validTokenListOperation = ["=",">","*","==","+","-",";"]
        validTokenListControlStatement = ["IF","THEN","ELSE","ENDIF","WHILE","RETURN"]
        validTokenListTypeDef = ["int","char"]

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
                
        #그 외 기타 문자열 및 숫자
        elif self.tokenToken.isalpha():
            self.tokenType = "__WORD__"
            return True
        
        elif self.tokenToken.isdigit():
            self.tokenType = "__NUM__"
            return True    
        
        else:
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
        for i in self.splitTable:
            
            
            _tokenCount = indexCounter
            _tokenToken = i
            _tokenType = "defaultType"
            token = Token(_tokenCount,_tokenToken,_tokenType)
            
            #오류인 경우
            if (not token.checkAndAssignTokenType()):
#                오류 위치 출력
                return False
            
            #정상인 경우
            elif (not DISTINCT or self.checkDistinctToken(token)):
                self.tokenTable.append(token)
                
                
            indexCounter+=1
        #end for
        return True
    
    def printTokenTable(self):
        print("\n*********  TOKEN TABLE  *********\n")
        print("Count", "\t", "Token" , "\t" , "Type","\n")
        for i in self.tokenTable:
            print(i.tokenCount, "\t", i.tokenToken , "\t" , i.tokenType)
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
        
            
        self.gotoTable = ActionGoToTable.generateTable()
        self.gotoTableLabel = ActionGoToTable.generateLabel()
    
    def readFromTable(self,row,col):
        pass

    def parseOnce(self):
        stackTop = self.parserStack[-1]
        inputTop = self.parserInput[0].tokenType
        
        try: 
            gotoTable_j = self.gotoTableLabel.index(inputTop)
            gotoTable_i = stackTop
        
        except ValueError:
            print("Fatal Error: Cannot Parse, invalid token type")
            return False
        
        print("Stack--> ",self.parserStack,end="  [")
        for i in self.parserInput:
            print(i.tokenToken, end=" ")
        print("] <--Input")
        pass
    
    

# ************  main **************** #
        
if __name__ == '__main__':
    
    ## input Source Code
    inputStream = "#define k tmp \n #define num 7 \n IF \
    k == 0 THEN ( k = k + num \t ) ELSE k = k - num ENDIF"

    
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

    while(parser.parseOnce()):
        pass
    
    
    print("\nEnding program...\n2017314789 이민규\n")
