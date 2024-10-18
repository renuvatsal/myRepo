def call() {
    echo "Entered into finishCheckout"
    //withBotCreds() {
        def project_name = getProjectName()
        startCheckout(project_name, false)
    //}
}