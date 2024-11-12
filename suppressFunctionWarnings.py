import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, help='Provide file.txt filename')
    parser.add_argument('-f', '--functions', type=lambda s: s.split(','),help='Comma-separated list of function names')

    args = parser.parse_args()

    input_file = args.input_file
    string_list = args.functions

    removeFunctions(input_file,string_list)

def removeFunctions(input:str,functions:list):
    with open(input, 'r') as file:
        lines = file.readlines()
    
    with open(input, 'w') as file:
        for line in lines:
             if not any(function in line for function in functions):
                file.write(line)

if __name__ == "__main__":
    main()