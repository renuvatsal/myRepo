import getopt
import sys
import csv
import os

## For any issues and enhancement contact renu.edevenkata@marelli.com

def parse_input(argv:str):
    try:
        opts,args=getopt.getopt(argv,'i:o:',['input=','output='])
    except getopt.GetoptError:
        print("Provide valid input and output files names.\nUsage: -i <inputfile> -o <outputfile>")
        sys.exit(2)

    for opt,arg in opts:
        if opt in ('-i','--input'):
            input=arg
        elif opt in ('-o','--output'):
            output=arg

    if not input or not output:
        print(f"Both input and output files are required.\nUsage: -i <inputfile> -o <outputfile>")
        sys.exit(2)

    if not os.path.isfile(input):
        print(f"The input file {input} does not exist.")
        sys.exit(2)
    
    output_extension = os.path.splitext(output)[1]
    if output_extension != '.csv':
        print(f"Warning: Output file extension '{output_extension}' is not expected. Using default '.csv'")
        output= os.path.splitext(output)[0] + '.csv'


    return input,output

if __name__=='__main__':

    input, output=parse_input(sys.argv[1:])

    headers=[]
    try:
        with open(input, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) >= 2:
                    headers.append(parts[1])
    except Exception as e:
        print(e)
    finally:
        file.close()

    if headers:
        try:
            with open(output, 'w', newline='', encoding='utf-8') as output_file:
                writer = csv.writer(output_file)
                writer.writerow(headers)
        except Exception as e:
            print(e)
        finally:
            output_file.close()
    else:
        print('No headers found')