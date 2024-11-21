#!/bin/sh

while getopts "a:c:" opt
do
   case "$opt" in
      a ) action="$OPTARG";;
      c ) core="$OPTARG" ;;
   esac
done

#current_ts=$(date '%Y-%m-%d-%H-%M')

PDCCORES=("PDC1E", "PDC1F", "PDC1AB", "PDC1E_PDC1AB", "PDC1F_PDC1AB")
BDCCORES=("PDC3E", "PDC3F", "PDC3AB", "PDC3E_PDC3AB", "PDC3F_PDC3AB")

trap 'echo "An error occured. Exiting."; exit 1;' ERR
set -e

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

cleanup(){
    rm -f $destConfigPath/*.conf_original
    #rm -f $destScriptPath/infa_server_env_original
}

if [ $action == "disable" ];
then
    for file in "ls -lrt $IMWPath/*.conf_IMW_$core"
    do
        destFileName="echo "$file" | awk -F "_" '{print $1}'"
        #Backup config files
        cp $destConfigPath/$destFileName $destConfigPath/${destFileName}_original
        #Copying config files from IMW path to config folder
        cp $IMWPath/$file $destConfigPath/$destFileName
    done

    infa_server_env_File="infa_server_env_IMW_$core"
    if [ -f $IMWPath/$infa_server_env_File ];
    then
        dest_infa_server_env_File="echo "$infa_server_env_File" | awk -F "_IMW_$core" '{print $1}'"
        #Backup infa env file
        cp $destScriptPath/$dest_infa_server_env_File $destScriptPath/${dest_infa_server_env_File}_original
        #Copying infa file from IMW path to scripts folder
        cp $IMWPath/$infa_server_env_File $destScriptPath/$dest_infa_server_env_File
    else
        echo "infa_server_env file doesnot exist for given core - ${core}"
    fi
elif [ $action == "enable" ];
then
    for file in "ls -lrt $destConfigPath/*.conf_original"
    do
        mainFileName="echo "$file" | awk -F"_" '{print $1}'"
        #Moving back to original state
        cp $destConfigPath/$file $destConfigPath/$mainFileName
    done
    
    for orgFile in "$destScriptPath"/infa*_original;
    do
        if [ -f "$orgFile" ]; then
        echo "$orgFile"
        fi

        infaFileName="echo "$infa_server_env_File" | awk -F "_original" '{print $1}'"
        #Moving back to original state
        cp $orgFile $infaFileName

    done
    cleanup()
fi
