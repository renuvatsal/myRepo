import getopt
import sys
import re
import logging

#Global Variables
cfilenames=[]
rownumbers=[]
messages=[]
references=[]
cfilenameKey='#cfilename#'
rownumberKey='#rownumber#'
messageKey='#message#'
referenceKey='#reference#'

def clearLists(bool:bool):
    if bool is True:
        cfilenames.clear()
        rownumbers.clear()
        messages.clear()
        references.clear() 


def misraManipulate(misraresultfile:str,misratemplatefile:str,output_file:str):
    if misraresultfile:
        with open(misraresultfile,'r') as input:
            content=input.readlines()
            for line in content:
                line=line.strip()
                if line.__contains__('.c'):
                    match=re.search('(.*\\.[cpp|c])',line)
                    if match:
                        cfilename=match.group()
                        cfilenames.append(cfilename)
                    match=re.search(':([0-9]+):',line)
                    if match:
                        rownumber=match.group(1)
                        rownumbers.append(rownumber)
                    match=re.search(r':[0-9]+:[0-9]+:\s*(.*?)\s*\(R',line)
                    if match:
                        message=match.group(1)
                        messages.append(message)
                    match=re.search(r']\s\(([^()]+)\)',line)
                    if match:
                        referencevalue=match.group(1)
                        split=referencevalue.split(' ')
                        RULEString=split[0]
                        RULEnumber=split[1].split('-')[1]
                        RULE=RULEString+'-'+RULEnumber
                        Misra=split[1].split('-')[0].split('C')[0].upper()
                        Year=split[1].split('-')[0].split('C')[1]
                        reference=Misra+' '+'C:'+Year+' '+RULE
                        references.append(reference)                      
    else:
        logging.error(f'{misraresultfile} doesnot exists')
        sys.exit(1)

    if cfilenames and rownumbers and messages and references:
        for (cfilename,rownumber,message,reference) in zip(cfilenames,rownumbers,messages,references):
            with open(misratemplatefile,'r') as template:
                concadContent=template.read()
                keys=[cfilenameKey,rownumberKey,messageKey,referenceKey]
                for value in keys:
                    if value==cfilenameKey:
                        concadContent=concadContent.replace(cfilenameKey,cfilename)
                    if value==rownumberKey:
                        concadContent=concadContent.replace(rownumberKey,rownumber)
                    if value==messageKey:
                        concadContent=concadContent.replace(messageKey,message)
                    if value==referenceKey:
                        concadContent=concadContent.replace(referenceKey,reference)
            with open(output_file,'a') as output:
                output.write(concadContent.strip()+'\n')
    else:
        logging.error('Unknown parsing issue occured')
        sys.exit(1)


def HISManipulate(HISresultfile:str,HIStemplatefile:str,output_file:str):
    if HISresultfile:
        with open(HISresultfile,'r') as input:
            content=input.readlines()
            for line in content:
                line=line.strip()
                if line.__contains__('.c'):
                    match=re.search('(.*\\.[cpp|c])',line)
                    if match:
                        cfilename=match.group()
                        cfilenames.append(cfilename)
                    match=re.search(':([0-9]+):',line)
                    if match:
                        rownumber=match.group(1)
                        rownumbers.append(rownumber)
                    match=re.search(r':\s(.*)',line)
                    if match:
                        message=match.group(1)
                        messages.append(message)                     
    else:
        logging.error(f'{HISresultfile} doesnot exists')
        sys.exit(1) 

    if HIStemplatefile:
        if cfilenames and rownumbers and messages:
            for (cfilename,rownumber,message) in zip(cfilenames,rownumbers,messages):
                with open(HIStemplatefile,'r') as template:
                    concadContent=template.read()
                    keys=[cfilenameKey,rownumberKey,messageKey,referenceKey]
                    for value in keys:
                        if value==cfilenameKey:
                            concadContent=concadContent.replace(cfilenameKey,cfilename)
                        if value==rownumberKey:
                            concadContent=concadContent.replace(rownumberKey,rownumber)
                        if value==messageKey:
                            concadContent=concadContent.replace(messageKey,message)
                with open(output_file,'a') as output:
                    output.write(concadContent.strip()+'\n')
        else:
            logging.error('Unknown parsing issue occured')
            sys.exit(1)
    else:
        logging.error(f'{HIStemplatefile} doesnot exists')
        sys.exit(1)
        
def parseInput(args:str):
    try:
        opts,args=getopt.getopt(args,'m:t:h:s:o:',['misrawarning=','misratemplate=','hiswarning=','histemplate=','output='])
    except getopt.GetoptError:
        logging.info(f'testResultsManipulate.py -m <misrawarning> -t <misratemplate> -h <hiswarning> -s <histemplate> -o <output>')
        sys.exit(2)

    for opt,arg in opts:
        if opt in ('-m','--misrawarning'):
            misrawarning=arg
        elif opt in ('-t','--misratemplate'):
            misratemplate=arg
        elif opt in ('-h','--hiswarning'):
            hiswarning=arg
        elif opt in ('-s','--histemplate'):
            histemplate=arg
        elif opt in ('-o','--output'):
            output=arg

    return misrawarning,misratemplate,hiswarning,histemplate,output

if __name__=='__main__':
    misrawarning,misratemplate,hiswarning,histemplate,output=parseInput(sys.argv[1:])
    misraManipulate(misrawarning,misratemplate,output)
    #misraManipulate('AXN_MisraWarnings.txt','misraResultsTemplate.txt')
    clearLists(True)
    HISManipulate(hiswarning,histemplate,output)
    #HISManipulate('AXN_HISWarnings.txt','HISResultsTemplate.txt')