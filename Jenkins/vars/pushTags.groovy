def call(String remoteRepoUrl, String pathToCFGID ){                    
                    bat """
                        git status
                        git stash

                        git checkout ${env.BRANCH_NAME}

                        git stash apply
                        git status

                        git config --list

                        git remote add central ${remoteRepoUrl}

                        echo set configurations
                        git config --global user.email ""
                        git config --global user.name "Jenkins Agent"

                        git fetch central

                        echo create and push tag
                        git tag -a ${env._USERINPUTSWLABEL} -m "Created by Jenkins Agent"
                        git push central --tags

                        git status
                    """
                    bat """
                        REM Tailor: adapt path to CfgId folder of Your project
                        cd ${pathToCFGID}
                        echo "${env._USERINPUTSWLABEL}" > CFGID_CfgInfoVersion.txt.h
                        echo "${env.userInputSWTTNR}" > CfgId_CfgInfoPartNo.txt.h
                        """
}                    