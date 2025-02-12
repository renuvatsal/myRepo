#Python preparation
import json
from typing import List

class Marks:
    def __init__(self, maths, science, social):
        self.maths = maths
        self.science = science
        self.social = social

MarksList:List[Marks]=[]

class Students:
    def __init__(self, name, marks):
        self.name = name
        self.marks:List[Marks]=[]
        for mark in marks:
            if 'maths' in mark:
                maths = mark['maths']
            if 'science' in mark:
                science = mark['science']
            if 'social' in mark:
                social = mark['social']
        
        mark = Marks(maths,science,social)
        self.marks.append(mark)

StudentsList:List[Students]=[]

with open('mytestdata.json', 'r') as data:
    data=json.load(data)
    student=Students(name=data['name'], marks=data['marks'])
    StudentsList.append(student)

for student in StudentsList:
    print(student.name)
    for mark in student.marks:
        print(mark.maths,mark.science,mark.social)

'''
JSON data is here
{
    "name": "vatsal",
    "marks":[
        {
            "maths":90
        },
        {
            "science":90
        },
        {
            "social":70
        }
    ]
}
'''

Numlist=[i for i in range(1,101)]
c=34
cli=[i for i in Numlist[0:c]]
print(cli)

Numlist=list(range(1,101))
n=10

for i in range(0,len(Numlist),n):
    print([Numlist[j] for j in range(i,i+n)])

'''import decimal
string='5'
integer=5

print(type(decimal.Decimal(string)))
print(type(decimal.Decimal(integer)))

string="this this this what is this!"
print(string[::-1])
reversedText=''
for word in string:
    reversedText=word+reversedText
print(reversedText)

count=0
for word in string:
    if word=='i':
        count+=1

print(count)

LISTTest=['a','b','c','d','e']
print(''.join(LISTTest))

fib=[0,1]
for i in range(0,10):
    fib.append(fib[-1]+fib[-2])

print(fib)

numberList = [15, 85, 35, 89, 125, 2]
reqNumber= numberList[0]
for num in numberList:
    if reqNumber < num:
        reqNumber = num
print(reqNumber)
print(int(len(numberList)/2))

list1=[1,2,3]
list2=[4,5,6]
list3=[]
for i in range(0,len(list1)):
    list3.append(list1[i]+list2[i])

print(list3)'''

json_data='''{
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}'''
'''
import json

with open('sample.json','r') as f:
    data=json.load(f)

print(type(data))

print(type(json.loads(json_data)))

print(type(json.dumps(json_data)))
test=json.loads(json_data)
print(test['glossary']['GlossDiv']['GlossList']['GlossEntry'])

for i in test['glossary']['GlossDiv']['GlossList']['GlossEntry'].items():
    print(i)

x=lambda a,b:(a+b)*(a-b)
print(x(4,2))


class Person:
    def __init__(vatsal,name,age):
        vatsal.name=name
        vatsal.age=age
    
    def myFun(vatsal):
        print(f'Name is {vatsal.name} and age is {vatsal.age}')

p=Person('RV',27)
p.myFun()'''
