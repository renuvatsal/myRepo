def call(String agentBuildPathAPPS, String projRepoBranchNameNoSlash, String workspace, String batfile){
    bat """
        cd ${workspace}\\app\\Support

        set PATH_APPS=${agentBuildPathAPPS}
        set PROJECTNAME_AXIVION=PROJ-${projRepoBranchNameNoSlash}
        call ${batfile}
    """
    verifyUnitTest('win')

    bat """
        echo ErrorLevel: %ERRORLEVEL%

        if %ERRORLEVEL% EQU 0 (
        echo bat.bat Success, ErrorLevel is: %ERRORLEVEL%
        ) else (
        echo bat.bat Failure, ErrorLevel is: %ERRORLEVEL%
        exit /b %errorlevel%
        )
    """
}                
