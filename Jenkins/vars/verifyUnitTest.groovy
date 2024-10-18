def call(String os)
{   
    if ( os == 'linux' ) {
        def result = sh(returnStdout: true,script: '''
                cat ../Bin/PROJ/PROJ.txt \
                | grep 'number_of_failed_asserts' | awk '{if ($2 == "0") print "true"; else print "false"}'
            '''
        ).trim()
        if (result == 'false') {
            echo "Unit test failed. Terminating the pipeline."
            error("Unit test failed")
        } else {
            echo "Unit test passed..."
        }
        script {
            try {
            sh '''
            echo " +++++ starting single file report generation ++++"
            currentDirectory=$(pwd)
            cd $currentDirectory/../../APPS/Support
            chmod +x ../../Build/VS/build.sh
            chmod -R 777 ./      
            ./some.sh
            '''
            } catch(Exception e) {
                echo "Deployment failed: ${e.getMessage()}"
            }
        }
    } else if ( os == 'win') {
        echo "Entered UntitTestWindows"
        dir("${env.WORKSPACE}") {
            def result = powershell(script: '''(Get-Content 'Build\\Bin\\PROJ\\PRJ.txt') -match 'number_of_failed_asserts' | ForEach-Object {
            $value = ($_ -split '\\s+')[1];
            if($value -eq '0') {
            Write-Output 'true'
            } else { Write-Output 'false'
            }
            }''', returnStdout: true).trim()
            echo "Result : ${result}"
            if (result == 'false' || result == null) {
            echo "Unit test failed .Terminating the pipeline."
            error("Unit test failed")
            } else {
            echo "Unit test Passed."
            }
        }
    }
}