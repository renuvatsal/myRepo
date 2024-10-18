import getopt
import sys
import re
import logging


def generateFile(complier,includes,clist,outputfile):
    dict={}
    try:
        with open(clist,'r') as file:
                dataCheck = file.read(1)    
                if dataCheck:
                    file.seek(0)
                    content=file.readlines()
                    for line in content:
                        fullfilepath=line.strip()
                        print(fullfilepath)
                        match=re.search(r'([^/]+)(?=\.c$|\.cpp$)',line)
                        if match:
                            cfilenamewithoutext=match.group(1)
                            if fullfilepath not in dict:
                                dict[fullfilepath] = cfilenamewithoutext
    except FileNotFoundError:
        print(f"File not found: {clist}")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    max_key_length = max(len(key) for key in dict.keys()) + 2           
    max_value_length = max(len(value) for value in dict.values()) + 2

    for key,value in dict.items():
        try:
            with open(outputfile,'a') as output:
                #objfiles_path = Path(".") / "_his_temp" / "obj" / "_objfiles.txt"
                objfiles_path = ".\\_his_temp\\obj\\_objfiles.txt"
                cfile = f"{value}.o"
                output_str = f"{complier} @{includes}   -c {key:{max_key_length}}   -o ./_his_temp/obj/{cfile:{max_value_length}}   &&   echo ./_his_temp/obj/{cfile:{max_value_length}}   >>   {objfiles_path}\n"
                output.write(output_str)
        except Exception as e:
            print(f"An error occurred while writing to {outputfile}: {e}")


def parse_input(args:str):
    try:
        opts,args=getopt.getopt(args,'c:i:l:o:',['complier=','includes=','clist=','output_file='])

        for opt,arg in opts:
            if opt in ('-c','--complier'):
                complier=arg
            elif opt in ('-i','--includes'):
                includes=arg
            elif opt in ('-l','--clist'):
                clist=arg
            elif opt in ('-o','--output_file'):
                output_file=arg

    except getopt.GetoptError:
        logging.info(f'generate_cc_files.py -c <complier> -i <includes> -l <clist> -o <output_file>')
        sys.exit(2)

    return complier,includes,clist,output_file

if __name__=='__main__':

    complier, inc, clist, output_file=parse_input(sys.argv[1:])
    #inc='_build_easy_axivion_flags_ARM_AXN.txt'
    #clist='_compile_files.txt'
    #output_file='tst.txt'
    #complier="test"
    generateFile(complier,inc,clist,output_file)
    