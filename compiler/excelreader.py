# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 23:13:33 2020

@author: 이민규
"""

def genActionGoToTable():
    table=[]
    infile = open('table.csv','r',encoding='UTF8')
    while True:
         line = infile.readline()
         if not line: break
         line = line.replace(",,",",-,-").replace(",\n",",-").strip()
         line = line.split(",")
         
         table.append(line)
    
    infile.close()
    table[0][0]='0'
    
    return table

tmp = genActionGoToTable()