### Question 1: Basic Script Creation
**Question:** Write a shell script that takes a filename as an argument and displays "The file exists" if the file exists, otherwise it displays "The file does not exist".

**Answer:**
```bash
#!/bin/bash

if [ -e "$1" ]; then
    echo "The file exists"
else
    echo "The file does not exist"
fi
```

### Question 2: Loop and Conditions
**Question:** How do you write a shell script that prints the numbers from 1 to 10 using a `for` loop?

**Answer:**
```bash
#!/bin/bash

for i in {1..10}; do
    echo $i
done
```

### Question 3: File Content Search
**Question:** Create a shell script that searches for a specific word in all `.txt` files within a directory and prints the lines containing that word.

**Answer:**
```bash
#!/bin/bash

word=$1
for file in *.txt; do
    if grep -q "$word" "$file"; then
        echo "Found in $file:"
        grep "$word" "$file"
    fi
done
```

### Question 4: Argument Handling
**Question:** Write a script that accepts a list of numbers as arguments, calculates their sum, and prints the result.

**Answer:**
```bash
#!/bin/bash

sum=0
for num in "$@"; do
    sum=$((sum + num))
done
echo "The sum is: $sum"
```

### Question 5: Process Monitoring
**Question:** How can you write a shell script to check if a process is running, and if not, start it?

**Answer:**
```bash
#!/bin/bash

process_name="my_process"
if pgrep "$process_name" > /dev/null; then
    echo "$process_name is running"
else
    echo "$process_name is not running"
    /path/to/my_process &
    echo "Started $process_name"
fi
```

### Question 6: String Manipulation
**Question:** Write a shell script that takes a string as an argument and prints it in reverse order.

**Answer:**
```bash
#!/bin/bash

input=$1
echo "$input" | rev
```

### Question 7: File and Directory Management
**Question:** Create a script that creates a backup of a specified directory into a `.tar.gz` file named with the current date.

**Answer:**
```bash
#!/bin/bash

directory_to_backup=$1
backup_name="backup_$(date +%Y%m%d).tar.gz"
tar -czf "$backup_name" "$directory_to_backup"
echo "Backup completed: $backup_name"
```

### Question 8: User Input and Conditional Execution
**Question:** How can you write a script that prompts for a user’s name and exits if the user does not input anything?

**Answer:**
```bash
#!/bin/bash

read -p "Enter your name: " name
if [ -z "$name" ]; then
    echo "No name entered, exiting."
    exit 1
else
    echo "Hello, $name!"
fi
```

### Question 9: Log File Analysis
**Question:** Write a script to find the number of occurrences of a specific error message in a log file.

**Answer:**
```bash
#!/bin/bash

error_message=$1
log_file=$2
count=$(grep -c "$error_message" "$log_file")
echo "The error '$error_message' occurred $count times in $log_file."
```

### Question 10: Scheduled Tasks
**Question:** Explain how you can schedule a script to run every day at midnight using `cron`.

**Answer:**
- Open the crontab editor by typing `crontab -e` in the terminal.
- Add the following line to schedule the script:
  ```
  0 0 * * * /path/to/your/script.sh
  ```
  This line will execute `script.sh` every day at midnight.

### Question 11: Disk Usage Alert
**Question:** Write a shell script that checks the disk usage of the `/` directory and alerts if it exceeds 80%.

**Answer:**
```bash
#!/bin/bash

usage=$(df / | grep / | awk '{ print $5 }' | sed 's/%//g')
if [ "$usage" -gt 80 ]; then
    echo "Alert: Disk usage has exceeded 80%. Current usage is $usage%."
else
    echo "Disk usage is under control at $usage%."
fi
```

### Question 12: User Management
**Question:** Create a script that accepts a username and checks if the user exists on the system.

**Answer:**
```bash
#!/bin/bash

username=$1
if id "$username" >/dev/null 2>&1; then
    echo "User $username exists."
else
    echo "User $username does not exist."
fi
```

### Question 13: File Comparison
**Question:** Write a script to compare two files and print whether they are identical or not.

**Answer:**
```bash
#!/bin/bash

file1=$1
file2=$2
if cmp -s "$file1" "$file2"; then
    echo "Files are identical."
else
    echo "Files are different."
fi
```

### Question 14: Network Ping Test
**Question:** How can you write a shell script to ping a server 5 times and display "Server is up" if at least one ping is successful, otherwise display "Server is down"?

**Answer:**
```bash
#!/bin/bash

server=$1
if ping -c 5 "$server" | grep "1 received" > /dev/null; then
    echo "Server is up."
else
    echo "Server is down."
fi
```

### Question 15: Log Rotation
**Question:** Write a script to rotate a log file. Rename `app.log` to `app.log.1` and create a new, empty `app.log`.

**Answer:**
```bash
#!/bin/bash

logfile="app.log"
mv "$logfile" "$logfile.1"
touch "$logfile"
echo "Log rotated: $logfile renamed to $logfile.1"
```

### Question 16: Environment Variable Check
**Question:** Create a script that checks if a specific environment variable (e.g., `JAVA_HOME`) is set and prints its value.

**Answer:**
```bash
#!/bin/bash

variable_name="JAVA_HOME"
if [ -z "${!variable_name}" ]; then
    echo "$variable_name is not set."
else
    echo "$variable_name is set to ${!variable_name}."
fi
```

### Question 17: Archive and Extract
**Question:** Write a script to archive all `.log` files in the current directory into a `logs.tar.gz` file and extract them to a `logs` directory.

**Answer:**
```bash
#!/bin/bash

tar -czf logs.tar.gz *.log
mkdir -p logs
tar -xzf logs.tar.gz -C logs
echo "Logs archived and extracted to the 'logs' directory."
```

### Question 18: File Permission Modification
**Question:** Describe how you would write a script to make a file executable by the user, but no permissions for group and others.

**Answer:**
```bash
#!/bin/bash

file=$1
chmod u+x,g-rwx,o-rwx "$file"
echo "Permissions for $file updated: executable by user only."
```

### Question 19: Calculate and Print Factorial
**Question:** Write a shell script to calculate and print the factorial of a given number.

**Answer:**
```bash
#!/bin/bash

number=$1
factorial=1
for (( i=1; i<=number; i++ )); do
    factorial=$((factorial * i))
done
echo "The factorial of $number is $factorial."
```

### Question 20: Dynamic Text Replacement in Files
**Question:** How can you write a script to replace all occurrences of a string "foo" with "bar" in all `.txt` files within a directory?

**Answer:**
```bash
#!/bin/bash

find . -type f -name "*.txt" -exec sed -i 's/foo/bar/g' {} +
echo "Replaced 'foo' with 'bar' in all .txt files in the current directory."
```
