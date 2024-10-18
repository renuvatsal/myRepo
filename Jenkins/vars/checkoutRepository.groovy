def call(String os, String repo_name, boolean wipe_workspace){
    if(wipe_workspace){
       dir(env.workspace) {
           cleanWs()
       }
    }
    
    checkout([
        $class: 'GitSCM',
        branches: scm.branches,
        extensions: scm.extensions + [[$class: 'GitLFSPull'],
                                    [$class: 'CheckoutOption', timeout: 45],
                                    [$class: 'CloneOption', timeout: 45, noTags: false, reference: repo_name, shallow: false],
                                    [$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: true, recursiveSubmodules: true, reference: '', timeout: 45, trackingSubmodules: false]],
        userRemoteConfigs: scm.userRemoteConfigs
    ])
}