#!/bin/sh

core=$1

PDCCORES=("PDC1E", "PDC1F", "PDC1AB", "PDC1E_PDC1AB", "PDC1F_PDC1AB")
BDCCORES=("PDC3E", "PDC3F", "PDC3AB", "PDC3E_PDC3AB", "PDC3F_PDC3AB")


if [[ "${PDCCORES[*]}" == *$core* ]];
then 
    IMWPath=/pdcnexus/emc/apps/config/IMW
    destScriptPath=/pdcnexus/emc/apps/scripts
    destConfigPath=/pdcnexus/emc/apps/config
elif [[ "${BDCCORES[*]}" == *$core* ]];
then
    IMWPath=/bdcnexus/emc/apps/config/IMW
    destScriptPath=/bdcnexus/emc/apps/scripts
    destConfigPath=/bdcnexus/emc/apps/config
fi

for file in "ls -lrt $IMWPath/*.conf_IMW_$core"
do
    destFileName="echo "$file" | awk -F "_" '{print $1}'"
    
    destFileCheck = $(cksum $destConfigPath/$destFileName)
    IMWFileCheck = $(cksum $IMWPath/${destFileName}_original)
    if [ $destFileCheck != $IMWFileCheck ];
    then
        diff $destConfigPath/$destFileName $IMWPath/${destFileName}_original
    fi
done

infa_server_env_File="infa_server_env_IMW_$core"
if [ -f $IMWPath/$infa_server_env_File ];
then
    dest_infa_server_env_File="echo "$infa_server_env_File" | awk -F "_IMW_$core" '{print $1}'"
    
    destFileCheck = $(cksum $destScriptPath/$dest_infa_server_env_File)
    IMWFileCheck = $(cksum $IMWPath/${infa_server_env_File}_original)
    if [ $destFileCheck != $IMWFileCheck ];
    then
        diff $destConfigPath/$destFileName $IMWPath/${destFileName}_original
    fi
else
    echo "infa_server_env file doesnot exist for given core - ${core}"
fi