 def call(String WORKSPACE, String agentBuildPathAPPS, String projRepoBranchNameNoSlash)
            {
                    bat """
                            REM cd CI\\Support
                            cd ${WORKSPACE}\\CI\\Support

                            set PATH_TOOLSGENERIC=${agentBuildPathAPPS}
                            call eval.bat

                            echo ErrorLevel: %ERRORLEVEL%

                            if %ERRORLEVEL% EQU 0 (
                            echo eval.bat Success, ErrorLevel is: %ERRORLEVEL%
                            exit /b %ERRORLEVEL%
                            ) else (
                            echo eval.bat Failure, ErrorLevel is: %ERRORLEVEL%
                            exit /b %ERRORLEVEL%
                            )
                            """
  }