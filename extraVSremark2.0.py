#! /usr/bin/env python
#coding=utf-8

import sys
import re
from xml.etree import ElementTree

SOURCEFILE = "TEXT.xml"
DESTINATIONFILE = "TEXT.txt"
REGEXSTRING = "M:MsgService.IMsgService."

file = open(SOURCEFILE)
reload(sys)
sys.setdefaultencoding('utf-8')

fileHandler = open(DESTINATIONFILE,'w')
reload(sys)
sys.setdefaultencoding('utf-8')

root = ElementTree.fromstring(file.read()) 
eitor = root.getiterator("member")
for e in eitor:
    matches = [];
    for key, value in e.items():
        funcName = re.sub(REGEXSTRING,"",value);
        funcName = funcName.replace("System.","")
        
        match = re.search("(?<=\().*(?=\))",funcName)
        matches = re.split(",",match.group(0))
        i = 0
        for m in matches:
            tmp = re.search("(?<=\{).*(?=\})",m);
            if tmp != None:
                m = re.sub("Collections.Generic.List\{.*\}","List<"+tmp.group(0)+">",m)
                m = re.sub("Nullable\{.*\}",tmp.group(0)+"?",m)
            matches[i] = m;
            i=i+1   
        result = ""
        flag = 0
    
    i = 0
    try:
        valuematch = "";
        for subnode in e.getchildren():
            if str(subnode.tag) == "summary":
                result = result + "接口功能:%s\n" % ( subnode.text)
            elif str(subnode.tag) == "returns":
                result = result + "返回值:%s\n" % (subnode.text)
            else:
                if flag == 0:
                    result = result + "参数列表:\n"
                    flag = flag + 1
                for key,value in subnode.items():
                    result = result + "\t%s %s:%s\n" % (matches[i],value,subnode.text)
                    valuematch = valuematch + ("%s %s" % (matches[i],value))+","
                    i = i+1
            funcName = re.sub("(?<=\().*(?=\))",valuematch[:-1],funcName);
                
        result = "接口名称: %s" % (funcName)+"\n" + result + "\n"
        fileHandler.write(result)        
    except :
        fileHandler.write("\n\n问题出现:"+funcName+"请检查该函数\n\n")
 
fileHandler.close();
        ##fileHandler.write("%s:\n%s\n" % (subnode.tag, subnode.text))  
        
    

