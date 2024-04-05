import os
import re
import shutil
from typing import List
import math
import concurrent.futures
import subprocess

class buildFile:
    def __init__(self,fullFileName,fileName):
        self.fullFileName=fullFileName
        self.fileName=fileName


#Globals
currentDirectory=os.getcwd()
buildDir=rf'{currentDirectory}\DirectoryName'
os.chdir(buildDir+'\\'+'required')
requiredDir=os.getcwd()
requiredList=requiredDir+'\\'+'_required_list.txt'

#Lists Declaration
buildFileList:List[buildFile]=[]
requiredFolderNamesList=[]
newFoldersList=[]
filesCountPerFolder=[]
consolidatedDatarequiredList=[]
batFileList=[]



print(f'Template directory {currentDirectory}')
print(f'current working directory changed is to {requiredDir} and buildDirectory is {buildDir}')

#buildrequiredFileList Creation
try:
    with open(requiredList, 'r') as requiredList:
        for _ in range(2):
            next(requiredList)
    
        for fullFileName in requiredList:
            fullFileName=fullFileName.rstrip()
            pattern=r'[^\\]+\.c$'
            #pattern=r'[A-Za-z_]+\.c$'
            match=re.search(pattern,fullFileName)
            if match:
                fileName=match.group()
            buildFileList.append(buildFile(fullFileName,fileName))
except Exception as e:
    print(f'{requiredList} is not available: {e}')

print(f'length is {len(buildFileList)}')

#Complete _required_list.txt file and folders creation
def required_list_creation(count:int,path:str):
    if count>10:
        requiredfoldersCount=math.ceil(count/10)

    desiredFolderCount=0
    while desiredFolderCount!=requiredfoldersCount:
        desiredFolderCount+=1
        folderName=path+'\\'+'required_'+str(desiredFolderCount)
        newFoldersList.append(folderName)
        try:
            os.mkdir(folderName)
            shutil.copy(currentDirectory+'\\'+'requiredListTemplate.txt',folderName+'\\'+'_required_list.txt')
            requiredFolderNamesList.append(folderName+'\\'+'_required_list.txt')
            with open(folderName+'\\'+'_required_list.txt','r') as file:
                content=file.read()
            content=content.replace('#folderName#',folderName)
            with open(folderName+'\\'+'_required_list.txt','w') as op:
                op.write(content)
            if desiredFolderCount==requiredfoldersCount:
                return True
        except Exception as e:
            print('ERROR: Directory already exists',e)
            return False
    else:
        print(f'Total files in _required_list.txt is less than 10 or there is some problem')


def required_list_concad(count:int,status:bool):
    if status is True:
        try:
            for i in range(0,count,10):
                    data=[item.fullFileName for item in buildFileList[i:i+10]]
                    filesCountPerFolder.append(len(data))
                    consolidatedDatarequiredList.append(data)

            for dataSet,folderName in zip(consolidatedDatarequiredList,requiredFolderNamesList):
                for each in dataSet:
                    with open(folderName,'a') as file:
                        file.write('\n'+each.strip())
            
            return True
        except Exception as e:
            print(f'ERROR: {e}')
            return False
    else:
        print(f'Total files in _required_list.txt is less than 10 or there is some problem')



def buildAnalyzeBatFile(buildFileList:list,foldersList:list,filesCountPerFolder:list,requiredDir:str):
    
    index=0
    if len(buildFileList)>10 and len(foldersList)==len(filesCountPerFolder):
        try:
            for folder,countPerFiles in zip(foldersList,filesCountPerFolder):
                folderName='#folderName#'
                fileCount='#count#'
                fullfilename='#fullfilename#'
                filename='#filename#'

                shutil.copy(currentDirectory+'\\'+'buildAnalyzeTemplate.txt',folder+'\\'+'batFileName.bat')
                batFileList.append(folder+'\\'+'batFileName.bat')

                with open(folder+'\\'+'batFileName.bat','r') as file:
                    batContent=file.read()
                    replacablesForBatCreation=[folderName,fileCount]
                    for r in replacablesForBatCreation:
                        if r==folderName:
                            batContent=batContent.replace(folderName,str(folder))
                        elif r==fileCount:
                            batContent=batContent.replace(fileCount,str(countPerFiles))
                with open(folder+'\\'+'batFileName.bat','w') as op:
                    op.write(batContent)
                
                while countPerFiles!=0:
                    for row in buildFileList[index:index+1]:
                        with open(currentDirectory+'\\'+'buildFileTemplate.txt','r') as file:
                            conCadContent=file.read()
                            replacablesForBatConcad=[fullfilename,filename,folderName]
                            for value in replacablesForBatConcad:
                                if value==fullfilename:
                                    conCadContent=conCadContent.replace(fullfilename,row.fullFileName)
                                elif value==folderName:
                                    conCadContent=conCadContent.replace(folderName,folder)
                                elif value==filename:
                                    conCadContent=conCadContent.replace(filename,row.fileName+'.txt')
                        with open(folder+'\\'+'batFileName.bat','a') as file:
                            file.write(conCadContent)
                    countPerFiles-=1
                    index+=1

            return True
        except Exception as e:
            print(f'ERROR: {e}')
            return False
    else:
        print(f'Total files in _required_list.txt is less than 10 or new folders are not created')
        return False

def runBatchFile(batfilepath:list):
    subprocess.call(batfilepath,shell=True)

def copyrequiredCfg(foldersList:list,dir:str):
    try:
        for folder in foldersList:
            shutil.copy(dir+'\\'+'_required_cfg.txt',folder+'\\'+'_required_cfg.txt')
        
        return True
    except Exception as e:
        print(f'ERROR: {e}')
        return False
    


requiredstatus=required_list_creation(len(buildFileList),buildDir)
if requiredstatus is True:
    requiredconcadstatus=required_list_concad(len(buildFileList),requiredstatus)
    copyStatus=copyrequiredCfg(newFoldersList,requiredDir)
    if requiredconcadstatus and copyStatus is True:
        batstatus=buildAnalyzeBatFile(buildFileList,newFoldersList,filesCountPerFolder,requiredDir)
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(batFileList)) as executor:
                run=[executor.submit(runBatchFile,batfile) for batfile in batFileList]
                concurrent.futures.wait(run)
        except Exception as e:
            print(f'Error: {e}')
        finally:    
            executor.shutdown(wait=False)
