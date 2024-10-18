def call(Map params = [:]) {
    def agentBuild = params.agentBuild ?: 'NodeValueNotProvided'
    def agentBuildPathAPPS = params.agentBuildPathAPPS ?: 'APPSPathNotProvided'
    def scmVars = params.scmVars ?: 'scmVarsNotProvided'
    def artifactoryProjectName = params.artifactoryProjectName ?: 'ProjectNameNotProvided'
    def projectRepoName = params.projectRepoName ?: 'RepoNameNotProvided'
    def agentBuildLinux = params.agentBuildLinux ?: 'LinuxNodeValueNotProvided'
    def artifactoryBrowserUrl = params.artifactoryBrowserUrl ?: 'BrowserUrNotProvided'
    def softwareLabelDefault = params.softwareLabelDefault ?: 'softwareLabelDefaultNotProvided'
    def swttnrDefault = params.swttnrDefault ?: 'swttnrDefaultNotProvided'
    def repoName =params.repoName ?: 'repoNameNotProvided'
    def pathToCFGID = params.pathToCFGID ?: 'pathToCFGIDNotProvided'
    def remoteRepoUrl = params.remoteRepoUrl ?: 'remoteRepoUrlNotProvided'
    def remoteRepository = params.remoteRepository ?: 'remoteRepositoryNotProvided'
    def buildOutputBin = params.buildOutputBin ?: 'buildOutputBinNotProvided'
    def buildType = params.buildType ?: 'buildTypeNotProvided'
    def jobName = params.jobName ?: 'jobNameNotProvided'
    def build_stage = params.build_stage ?: 'build_stageeNotProvided'
    def ut_stage = params.ut_stage ?: 'ut_stageNotProvided'
    def runAxivion = params.axivion ?: false
    def runQac = params.qac ?: false
    def record_stage = params.record_stage ?: 'record_stageNotProvided'

    // assembled artifactory url
    def artifactoryBasePath = "${artifactoryProjectName}/${projectRepoName}/application"
    def artifactoryBrowserUrlProject = "${artifactoryBrowserUrl}/${artifactoryBasePath}"
    g_do_builds = ['none'] // array that stores how to do builds

    pipeline {
        agent any

        options { 
            disableConcurrentBuilds() // Disallow concurrent executions, prevents simultaneous accesses to shared resources
            skipDefaultCheckout(true)
        }

        parameters {
            booleanParam(name: 'wipeout', defaultValue: false, description: 'Wipe out workspace before checkout')
            booleanParam(name: 'axivion', defaultValue: false, description: 'Enable axivion as analysis tool')
            booleanParam(name: 'qac', defaultValue: false, description: 'Enable qac as analysis tool')
        }

        stages {
            stage('Init') {
                when { beforeAgent true; expression {record_stage == true }}
                agent { label "${agentBuild}" }
                steps {
                    script {
                        cancelPreviousBuilds(jobName)
                    }
                }
            }

            stage("Prepare Variables") {
                when { beforeAgent true; expression {record_stage == true }}
                agent { label "${agentBuild}" }
                steps{
                    echo "On Node: ${NODE_NAME}"

                    echo "Initially prepare build variables"
                    script{
                        def variables = buildVariables(artifactoryBasePath, artifactoryBrowserUrlProject, buildOutputBin)
                        env._PLANNAME= variables[0]
                        env._BUILDOUTPUTBIN= variables[1]
                        env._ARTIFACTORY_URL= variables[2]
                        env._ARTIFACTORY_URL_LATEST= variables[3]
                        env._ARTIFACTORY_URL_BROWSER= variables[4]
                    }
                }
            }

            stage('Pull APPS') {
                when { beforeAgent true; expression {record_stage == true }}
                agent { label "${agentBuild}" }
                steps {
                    lock("${NODE_NAME}LockAPPSPull") {
                        echo 'Pull APPS'
                        echo "On Node: ${NODE_NAME}"

                        bat """
                        cd ${agentBuildPathAPPS}
                        git pull
                        """
                    }
                }
            }

            stage('Checkout project repository') {
                when { beforeAgent true; expression {record_stage == true }}
                parallel {
                    stage('Checkout project repo on Windows (default)') {
                        agent {label "${agentBuild}"}
                        steps {
                            checkoutRepository('win',repoName,params.wipeout)
                        }
                    }

                    stage('Checkout project repo on Linux') {
                        agent {label "${agentBuildLinux}"}
                        steps {
                            checkoutRepository('linux',repoName,params.wipeout)
                        }
                    }

                }
            }

            stage('Open task') {
                when { beforeAgent true; expression {record_stage == true }}
                agent { label "${agentBuild}" }
                steps {
                    script {
                        env.each { key, value ->
                            echo "${key}: ${value}"
                        }
                    }
                }
            }

            stage("Select Static Code Analysis Tool") {
                    when { beforeAgent true; expression {record_stage == true }}
                    agent { label "${agentBuild}" }
                    steps{
                        echo "On Node: ${NODE_NAME}"
                        echo "Select Static Code Analysis"
                        selectStaticCodeAnalysis(runAxivion, runQac)
                                
                    }
            }

            stage('Build and Integration') {
                when { beforeAgent true; expression {build_stage == true }}

                stages {
                    stage('Gather build stages') {
                        agent { label "${agentBuild}" }
                        steps {
                            script {
                                g_do_builds = gatherBuilds()
                            }
                        }
                    }

                    stage('Do build') {
                        when { beforeAgent true; expression { build_stage == true } }
                        parallel {
                            stage('Build target Windows/Cygwin') { // Compilation for Windows & cygwin
                                when { beforeAgent true; expression { g_do_builds.contains('win') } }
                                agent { label "${agentBuild}" }
                                options {
                                    timeout(activity: true, time: 30)
                                }
                                steps {
                                    ansiColor('xterm') {
                                        script {
                                            dir("${env.WORKSPACE}") {
                                                projectBuild('win', true,agentBuildPathAPPS,env._PROJ_REPO_BRANCHNAME_NO_SLASH)
                                            }
                                        }
                                    }
                                }
                                post {
                                    always {
                                        deploytoArtifactory('win',agentBuild,agentBuildPathAPPS,buildType)
                                    }
                                }
                            }

                            stage('Build target Linux32') { // Compilation for linux 32
                                when { beforeAgent true; expression { g_do_builds.contains('linux') } }
                                agent { label "${agentBuildLinux}" }
                                //agent {
                                //    docker {
                                //        alwaysPull true
                                //        image 'abc/linux-build'
                                //        label 'docker'
                                //        registryUrl 'https://docker.marelli.com/'
                                //    }
                                //}
                                options {
                                    timeout(activity: true, time: 30)
                                }
                                steps {  
                                    script {
                                        dir("${env.WORKSPACE}") {
                                            projectBuild('linux', false,null,env._PROJ_REPO_BRANCHNAME_NO_SLASH)
                                        }
                                    } 
                                } 
                                post {
                                    always {
                                        deploytoArtifactory('linux',agentBuild,agentBuildPathAPPS,buildType)
                                    }
                                }                
                            }
                        } 
                    }

                    stage('Integration'){
                        when { beforeAgent true; expression {build_stage == true }}
                        agent { label "${agentBuild}" }
                        steps{
                            script{
                                echo "Skipping Integration stage check Build stage"
                                env._PROJ_REPO_BRANCHNAME = env.BRANCH_NAME
                                println "env._PROJ_REPO_BRANCHNAME: ${env._PROJ_REPO_BRANCHNAME}"
                                env._PROJ_REPO_BRANCHNAME_NO_SLASH = env._PROJ_REPO_BRANCHNAME.replaceAll('/', '-')
                                println "_PROJ_REPO_BRANCHNAME_NO_SLASH: ${env._PROJ_REPO_BRANCHNAME_NO_SLASH}"
                                workspace="${env.WORKSPACE}"
                                //echo "${env._PROJ_REPO_BRANCHNAME_NO_SLASH} ${env.WORKSPACE}\\${project_name} ${agentBuildPathAPPS}"
                                //integration(agentBuildPathAPPS,env._PROJ_REPO_BRANCHNAME_NO_SLASH,workspace,'00_integration.bat')
                            }
                        }
                    }
                }   
            }
        }

        post {
            always {
                node( "${agentBuild}" ) {
                    echo 'One way or another, execution has finished'
                    cleanWs()
                }

            }
            success {
                echo 'I succeeded!'
            }
            unstable {
                echo 'I am unstable :/'
            }
            failure {
                echo 'I failed :('
            }
            changed {
                echo 'Things were different before...'
            }
        }
    }
}