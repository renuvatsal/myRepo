def call(agentBuildPathToolsGeneric){
    bat """
    cd ${env.WORKSPACE}\\${project_name}\\proj\\Support

    set PATH_APPS=${agentBuildPathToolsGeneric}
    set PROJECTNAME_AXIVION=CLN1-${env._PROJ_REPO_BRANCHNAME_NO_SLASH}
    call some.bat
    """

    def result = powershell(script: """
    (Get-Content 'some\\path\\proj\\result.txt') -match 'number_of_failed_asserts' | ForEach-Object {
        \$value = (\$_ -split '\\s+')[1];
        if(\$value -eq '0') {
            Write-Output 'true'
        } else {
            Write-Output 'false'
        }
    }
    """, returnStdout: true).trim()
    echo "Result : ${result}"
    if (result == 'false') {
     echo "Unit test failed. Terminating the pipeline."
     error("Unit test failed")
    } else {
     echo "Unit test Passed."
    }

    bat """
    echo ErrorLevel: %ERRORLEVEL%
    if %ERRORLEVEL% EQU 0 (
        echo some.bat Success, ErrorLevel is: %ERRORLEVEL%
    ) else (
        echo some.bat Failure, ErrorLevel is: %ERRORLEVEL%
        exit /b %ERRORLEVEL%
    )
    """
}
