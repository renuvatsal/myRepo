def call( String buildTarget, boolean batch,String agentBuildPathAPPS,String proj_repo_branchname_no_slash  ) {
    // input data come from the manifest file (found in the project repo)
    def datas = readJSON file : "${env.WORKSPACE}/PROJ/Jenkins/manifest.json"
    def signingJobName = ''  
    workspace="${env.WORKSPACE}"
    env._PROJ_REPO_BRANCHNAME = env.BRANCH_NAME
    println "env._PROJ_REPO_BRANCHNAME: ${env._PROJ_REPO_BRANCHNAME}"
    env._PROJ_REPO_BRANCHNAME_NO_SLASH = env._PROJ_REPO_BRANCHNAME.replaceAll('/', '-')
    println "_PROJ_REPO_BRANCHNAME_NO_SLASH: ${env._PROJ_REPO_BRANCHNAME_NO_SLASH}"

    datas.toolchains.each{
        if (it.name == buildTarget) //target parameter
        {
            // Table to store the scan parameter
            def scans = []

            it.targets.each {
                def scan_tool = null
                echo "build name: ${it.name} with command ${it.command}"
                if (batch == true) {
                    script{
                        try {
                            integration(agentBuildPathAPPS,env._PROJ_REPO_BRANCHNAME_NO_SLASH,workspace,it.command)
                        } catch (Exception e) {
                            echo "The command failed, error: ${e.getMessage()}"
                        }
                    }
                }
                else {
                    dir("${env.WORKSPACE}/Build/VS"){
                        script {
                            try {
                                sh  label:"Build ${it.name} target", script: it.command
                                verifyUnitTest(buildTarget)
                            } catch (Exception e) {
                                echo "The command failed, error: ${e.getMessage()}"
                            }
                        }
                        
                        
                    }
                }
                if (buildTarget.startsWith('gcc')) {
                    scan_tool = gcc(id: "gcc-${it.name}", name: "GCC ${it.name}")
                }
                //scans << scanForIssues( tool: scan_tool ) // scanning log files for issues
            }
            if (it.post_build) {
                it.post_build.each {
                    if (batch == true) {
                        bat label:"Post Build ${it}", script: it
                    }
                    else {
                        sh label:"Post Build ${it}", script: it
                    }
                }
            }
        }
    }
}
