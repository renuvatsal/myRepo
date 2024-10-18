def call(project_name, wipe_workspace){
    echo "Entered into startCheckout: ${project_name}"
    if(wipe_workspace){
       dir(env.workspace) {
           deleteDir()
       }
    }
    scmVars = checkout([
        $class: 'GitSCM',
        branches: scm.branches,
        extensions: scm.extensions + [[$class: 'GitLFSPull'],
                                      [$class: 'CheckoutOption', timeout: 45],
                                      [$class: 'CloneOption', timeout: 45, noTags: false, reference: 'D:/Mirror/proj.git', shallow: false],
                                      [$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: true, recursiveSubmodules: true, reference: '', timeout: 45, trackingSubmodules: false],
                                      [$class: 'RelativeTargetDirectory', relativeTargetDir: project_name]],
        userRemoteConfigs: scm.userRemoteConfigs
    ])
    echo "startCheckout: Completed checkout"
	return scmVars    
}