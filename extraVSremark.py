#! /usr/bin/env python
#coding=utf-8

import sys
import re
from xml.etree import ElementTree

file = open("TEXT.xml")
reload(sys)
sys.setdefaultencoding('utf-8')

fileHandler = open("TEXT.txt",'w')
reload(sys)
sys.setdefaultencoding('utf-8')

root = ElementTree.fromstring(file.read()) 
eitor = root.getiterator("member")
for e in eitor:
    for key, value in e.items():
        fileHandler.write("接口名称:\n%s\n" % (re.sub("M:MsgService.IMsgService.","",value)))
        flag = 0
    for subnode in e.getchildren():
        if str(subnode.tag) == "summary":
            fileHandler.write("接口功能:%s\n" % ( subnode.text))
        elif str(subnode.tag) == "returns":
            fileHandler.write("返回值:%s\n" % (subnode.text)) 
        else:
            if flag == 0:
                fileHandler.write("参数列表:\n")
                flag = flag + 1
            for key,value in subnode.items():
                fileHandler.write("\t%s:%s\n" % (value,subnode.text))
    fileHandler.write("\n")
fileHandler.close();
        ##fileHandler.write("%s:\n%s\n" % (subnode.tag, subnode.text))  
        
    

