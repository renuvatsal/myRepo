import getopt
import sys
import re
import logging

#Global Variables
cfilenames=[]
fullMessages=[]
warningMessages=[]
trimmedcfiles=[]
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

def fetchCertCWarnings(certCfile:str):
    if certCfile:
        try:
            with open(certCfile,'r') as input:
                content=input.readlines()
                for line in content:
                    line=line.strip()
                    if line.__contains__('.c'):
                        match=re.search('(.*\\.[cpp|c])',line)
                        if match:
                            cfilename=match.group()
                            trimmedcfile=re.search(r'(\\Src_AL\\[^\\]+(?:\\[^\\]+)*\.(?:cpp|c))',cfilename)
                            trimmedcfile=trimmedcfile.group()
                            trimmedcfiles.append(trimmedcfile)
                            cfilenames.append(cfilename)
                        match=re.search(r'\\Src_AL\\[^\\]+(?:\\[^\\]+)*(?=\(R)',line)
                        if match:
                            fullMessage=match.group()
                            fullMessages.append(fullMessage)
                        match=re.search(r':[0-9]+:[0-9]+:\s*(.*?)\s*\(R',line)
                        if match:
                            message=match.group(1)
                            warningMessages.append(message)
        except Exception as e:
            logging.ERROR(e)
    else:
        logging.ERROR(f'{certCfile} does not exist')

def prepareCertCWarnings(filenames:list,fullmessages:list,trimmedfilenames:list,warningmessages:list,certCTemplate:str,output_file:str):
    if filenames and fullmessages and trimmedfilenames and warningmessages:
        uniqueFile=countItems(filenames)
        uniqueMessage=countItems(warningmessages)
        conslidatedFileWarningsDict={i:trimmedcfiles.count(i) for i in trimmedcfiles}
        sorted_dict = {key: value for key, value in sorted(conslidatedFileWarningsDict.items(), key=lambda item: item[1], reverse=True)}
        max_key_length = max(len(key) for key in sorted_dict.keys()) + 2
        table_str = ""
        table_str += f"{'filename':<{max_key_length}} count\n"
        table_str += f"{'-' *  max_key_length} {'------':<6}\n"

        for key, value in sorted_dict.items():
            table_str += f"{key:<{max_key_length}} {value:<6}\n"

        try:
            with open(certCTemplate,'r') as template:
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
        logging.ERROR(f'Issue with prepareCertCWarnings method')    

def detailedReport(messages:list,output_file:str):
    warning={}
    for msg in messages:
        filepath, message = msg.split(':', 1)
        if filepath not in warning:
            warning[filepath] = []
        warning[filepath].append(message.strip())
    
    with open(output_file,'a') as output:
        pass#output.write("\n\n[Details Report]\n")
        pass#output.write("----------------------------------------------------------------------------------------\n")
        for filename in sorted(warning):
            output.write("[filename]: " + filename + "\n")
            for message in warning[filename]:
                output.write(f"{filename}:{message}\n")
                pass
            output.write("\n")

def parse_input(args:str):
    try:
        opts,args=getopt.getopt(args,'w:t:o:',['certwarning=','certtemplate=','output_file='])
    except getopt.GetoptError:
        logging.info(f'certCwarning.py -w <certwarning> -t <certtemplate> -o <output_file>')
        sys.exit(2)

    for opt,arg in opts:
        if opt in ('-w','--certwarning'):
            certwarning=arg
        elif opt in ('-t','--certtemplate'):
            certtemplate=arg
        elif opt in ('-o','--output'):
            output_file=arg

    return certwarning,certtemplate,output_file

if __name__=='__main__':

    certCfile, certCTemplate, output_file=parse_input(sys.argv[1:])
                    
    fetchCertCWarnings(certCfile)
    prepareCertCWarnings(cfilenames,fullMessages,trimmedcfiles,warningMessages,certCTemplate,output_file)
    detailedReport(fullMessages,output_file)