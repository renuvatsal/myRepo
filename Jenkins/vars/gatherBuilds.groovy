def call() {
    echo env.WORKSPACE
    def data = readJSON file: "${env.WORKSPACE}\\app\\Jenkins\\manifest.json"
    def do_builds = []
    data.toolchains.each {
        def targets = it.targets
        if (!(targets instanceof List)) {
            targets = []
        }
        if (!targets.isEmpty()) {
            do_builds << it.name
            echo "${do_builds}"
        }
    }
   return do_builds
}