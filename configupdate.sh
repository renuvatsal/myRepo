#!/bin/sh

while getopts "a:f:p:" opt
do
   case "$opt" in
      a ) action="$OPTARG";;
      f ) filenames="$OPTARG" ;;
      p ) path="$OPTARG" ;;
   esac
done

if [ -z "$action" ] || [ -z "$filenames" ] || [ -z "$path" ]
then
   echo "Some or all of the input arguments are empty";
fi

# Convert the input filenames argument into an array
IFS=',' read -ra filenames <<< "$filenames"

# Goto path
cd $path

# Catch any error occurs while executiion of any command
trap 'echo "An error occured. Exiting."; exit 1;' ERR
set -e

# Running FOR LOOP for the filenames given as input
if [ "$action" == "start" ]
then
    for filename in "${filenames[@]}"; do
        if [ -f $filename ]
        then
            
            mv -f $filename ${filename}_original.txt
            echo "Moved $filename to ${filename}_original.txt"
            cp -f ${filename}_activity_specific_file.txt $filename
            echo "Copied ${filename}_activity_specific_file.txt to $filename"
        else
            echo "File does not exist"
            exit 1
        fi
    done
elif [ "$action" == "stop" ]
then
    for filename in "${filenames[@]}"; do
        if [ -f $filename ]
        then
            rm -f $filename
            echo "Removed activity specific $filename"
            mv -f ${filename}_original.txt $filename
            echo "Moved ${filename}_original.txt to $filename"
        else
            echo "File does not exist"
            exit 1
        fi
    done
fi