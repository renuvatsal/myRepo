def call(String artifactoryBasePath, String artifactoryBrowserUrlProject,String buildOutputBin) {
   def tmpUserInput
   def userInputSWLabel = "NotSet"
   def userInputSWTTNR = "NotSet"

   def tmpTimestamp = env.BUILD_TIMESTAMP
   env._DATE = tmpTimestamp.substring(0, 10)
   println "env._DATE: ${env._DATE}"

   def tmpBuildNo = env.BUILD_NUMBER
   env._BUILDNO = tmpBuildNo.padLeft(8, '0')
   println "env._BUILDNO: ${env._BUILDNO}"

   env._PROJ_REPO_BRANCHNAME = env.BRANCH_NAME
   println "env._PROJ_REPO_BRANCHNAME: ${env._PROJ_REPO_BRANCHNAME}"
   env._PROJ_REPO_BRANCHNAME_NO_SLASH = env._PROJ_REPO_BRANCHNAME.replaceAll('/', '-')
   println "_PROJ_REPO_BRANCHNAME_NO_SLASH: ${env._PROJ_REPO_BRANCHNAME_NO_SLASH}"

   env._PLANNAME = 'NotSet'
   env._USERINPUTSWLABEL = 'NotSet'
   env._USERINPUTSWTTNR = 'NotSet'
   env._BUILDOUTPUTBIN = "${buildOutputBin}"
   if (env.BRANCH_NAME == 'master') {
        env._PLANNAME = 'nightly-build'
        env._ARTIFACTORY_URL = "${artifactoryBasePath}/${_PLANNAME}/${BRANCH_NAME}/${_DATE}-${_BUILDNO}"
        env._ARTIFACTORY_URL_LATEST = "${artifactoryBasePath}/${_PLANNAME}/${BRANCH_NAME}/0000-00-00-latest"
        env._ARTIFACTORY_URL_BROWSER = "${artifactoryBrowserUrlProject}/${_PLANNAME}/${BRANCH_NAME}/${_DATE}-${_BUILDNO}"
    } else if (env.BRANCH_NAME ==~ /PR-.*/ || env.BRANCH_NAME ==~ /feature.*/ || env.BRANCH_NAME ==~ /bugfix.*/) {
        env._PLANNAME = 'integration-build'
        env._ARTIFACTORY_URL = "${artifactoryBasePath}/${_PLANNAME}/${BRANCH_NAME}/${_DATE}-${_BUILDNO}"
        env._ARTIFACTORY_URL_BROWSER = "${artifactoryBrowserUrlProject}/${_PLANNAME}/${BRANCH_NAME}/${_DATE}-${_BUILDNO}"
   } else if (env.BRANCH_NAME ==~ /release.*/) {
       env._PLANNAME = 'release-candidate-build'
       def userInput
       timeout(time: 30, unit: "MINUTES") {
       tmpUserInput = input(id: 'userInput', message: 'SW logistic data:', parameters: [
                [$class: 'TextParameterDefinition', defaultValue: '${softwareLabelDefault}', description: 'SWLabel', name: 'swlabel'],
                [$class: 'TextParameterDefinition', defaultValue: '${swttnrDefault}', description: 'SWTTNR', name: 'swttnr']
          ])
        }
        env._USERINPUTSWLABEL = tmpUserInput['swlabel']
        env._USERINPUTSWTTNR = tmpUserInput['swttnr']
        println ("userInputSWLabel: "+env._USERINPUTSWLABEL)
        println ("userInputSWTTNR: "+env._USERINPUTSWTTNR)
        env._ARTIFACTORY_URL = "${artifactoryBasePath}/${_PLANNAME}/${_DATE}-${_USERINPUTSWLABEL}"
        env._ARTIFACTORY_URL_BROWSER = "${artifactoryBrowserUrlProject}/${_PLANNAME}/${_DATE}-${_USERINPUTSWLABEL}"
    }
    //println "env._PLANNAME: ${env._PLANNAME}"
    //println "env._BUILDOUTPUTBIN: ${env._BUILDOUTPUTBIN}"
    //println "env._ARTIFACTORY_URL: ${env._ARTIFACTORY_URL}"
    //println "env._ARTIFACTORY_URL_LATEST: ${env._ARTIFACTORY_URL_LATEST}"
    //println "env._ARTIFACTORY_URL_BROWSER: ${env._ARTIFACTORY_URL_BROWSER}"

    return [env._PLANNAME, env._BUILDOUTPUTBIN, env._ARTIFACTORY_URL, env._ARTIFACTORY_URL_LATEST, env._ARTIFACTORY_URL_BROWSER]
}