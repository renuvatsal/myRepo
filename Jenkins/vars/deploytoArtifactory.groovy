def call(String os, String NODE_NAME, String agentBuildPathAPPS, String buildType)
{   
    echo  "Build Type : ${buildType}"
    if ( os == 'win') {
        echo "Deploy to Artifactory on Node: ${NODE_NAME}"

        dir("${env.WORKSPACE}"){
            rtUpload (
                serverId: 'artifactory-al-prod',
                specPath: """app/artispecs/${buildType}-build/deploy.txt"""
            )
            script {
                currentBuild.description = """<a href="${env._ARTIFACTORY_URL_BROWSER}" target="_blank" rel="noopener noreferrer">Link to Artifactory</a>"""
            }
            
            if( buildType=='nightly' ){
                rtUpload (
                    serverId: 'artifactory-al-prod',
                    specPath: """app/artispecs/${buildType}-build/deploy-latest.txt"""
                )
            }
        }

        echo 'eval.bat'
        bat """
        cd ${env.WORKSPACE}\\app\\Support

        set PATH_TOOLSGENERIC=${agentBuildPathAPPS}
        rem call eval.bat

        echo ErrorLevel: %ERRORLEVEL%

        if %ERRORLEVEL% EQU 0 (
        echo eval.bat Success, ErrorLevel is: %ERRORLEVEL%
        exit /b %ERRORLEVEL%
        ) else (
        echo eval.bat Failure, ErrorLevel is: %ERRORLEVEL%
        exit /b %ERRORLEVEL%
        )
        """
    } else if ( os == 'linux') {
        echo "Deploy to Artifactory on Node: ${NODE_NAME}"
        echo "_ARTIFACTORY_URL: ${_ARTIFACTORY_URL}"
        echo "env._ARTIFACTORY_URL: ${env._ARTIFACTORY_URL}"

        dir("${env.WORKSPACE}"){
            rtUpload (
                serverId: 'artifactory-al-prod',
                specPath: """app/artispecs/${buildType}-build-linux/deploy.txt"""
            )
            script {
                currentBuild.description = """<a href="${env._ARTIFACTORY_URL_BROWSER}" target="_blank" rel="noopener noreferrer">Link to Artifactory</a>"""
            }
        }
    }
}