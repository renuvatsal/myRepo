import getopt
import sys
import re
import logging

#Global Variables
cfilenames=[]
warningMessages=[]
trimmedcfiles=[]
fullMessages=[]
tmp=[]

def countItems(list:list):
    count=0
    try:
        for item in list:
            if item not in tmp:
                count += 1
                tmp.append(item)
        uniqueCount=len(tmp)
    except Exception as e:
        logging.ERROR(e)
    finally:
        tmp.clear()
    return uniqueCount

def fetchHISWarnings(hisfile:str):
    if hisfile:
        try:
            with open(hisfile,'r') as input:
                content=input.readlines()
                for line in content:
                    line=line.strip()
                    if line.__contains__('.c'):
                        fullMessages.append(line)
                        match=re.search('(.*\\.[cpp|c])',line)
                        if match:
                            cfilename=match.group()
                            trimmedcfile=re.search(r'([^\\]+\.c)$',cfilename)
                            trimmedcfile=trimmedcfile.group(1)
                            trimmedcfiles.append(trimmedcfile)
                            cfilenames.append(cfilename)
                        match=re.search(r':[0-9]+:[0-9]+:\s*(.*)',line)
                        if match:
                            message=match.group(0)
                            warningMessages.append(message)
        except Exception as e:
            logging.ERROR(e)
    else:
        logging.ERROR(f'{hisfile} does not exist')

def prepareHISWarnings(filenames:list,warningmessages:list,hisTemplate:str,output_file:str):
    if filenames and warningmessages:
        uniqueFile=countItems(filenames)
        uniqueMessage=countItems(warningmessages)
        conslidatedFileWarningsDict={i:filenames.count(i) for i in filenames}
        sorted_dict = {key: value for key, value in sorted(conslidatedFileWarningsDict.items(), key=lambda item: item[1], reverse=True)}
        max_key_length = max(len(key) for key in sorted_dict.keys()) + 2
        table_str = ""
        table_str += f"{'filename':<{max_key_length}} count\n"
        table_str += f"{'-' *  max_key_length} {'------':<6}\n"

        for key, value in sorted_dict.items():
            table_str += f"{key:<{max_key_length}} {value:<6}\n"

        try:
            with open(hisTemplate,'r') as template:
                overide=template.read()
                overide=overide.replace('#uniqueFile#',str(uniqueFile))
                overide=overide.replace('#uniqueMessage#',str(uniqueMessage))
                overide=overide.replace('#data#',table_str)
        except Exception as e:
            logging.ERROR(e)

        try:
            with open(output_file,'a') as output:
                    output.write(overide.strip()+'\n\n\n')
        except Exception as e:
            logging.ERROR(e)
        finally:
            output.close()
            template.close()
    else:
        logging.ERROR(f'Issue with preparehisWarnings method')    

def detailedReport(messages:list,output_file:str):
    warning={}
    for msg in messages:
        filepath, message = msg.split('.c',1)
        filepath +='.c'
        if filepath not in warning:
            warning[filepath] = []
        warning[filepath].append(message.strip())
    
    with open(output_file,'a') as output:
        for filename in sorted(warning):
            output.write("[filename]: " + filename + "\n")
            for message in warning[filename]:
                output.write(f"Line{message}\n")
                pass
            output.write("\n")

def parse_input(args:str):
    try:
        opts,args=getopt.getopt(args,'w:t:o:',['hiswarning=','histemplate=','output_file='])
    except getopt.GetoptError:
        logging.info(f'hiswarning.py -w <hiswarning> -t <histemplate> -o <output_file>')
        sys.exit(2)

    for opt,arg in opts:
        if opt in ('-w','--hiswarning'):
            hiswarning=arg
        elif opt in ('-t','--histemplate'):
            histemplate=arg
        elif opt in ('-o','--output_file'):
            output_file=arg

    return hiswarning,histemplate,output_file

if __name__=='__main__':

    hisfile, hisTemplate, output_file=parse_input(sys.argv[1:])
    #hisfile, hisTemplate, output_file="..\\Tmp\\AXN_HISWarnings.txt","HISTemplate.txt","C:\\ALS_Repo\\THOR\\Build\\ToolsSpecific\\Cust\\Vw\\Vw099\\AXIVION\\HIS_Report\\HISReport.txt"
    
    with open(hisfile,'r') as file:
        dataCheck = file.read(1)
        if dataCheck:
            fetchHISWarnings(hisfile)
            prepareHISWarnings(cfilenames,warningMessages,hisTemplate,output_file)
            detailedReport(fullMessages,output_file)
        else:
            logging.WARNING('HIS warnings doesnot exists')