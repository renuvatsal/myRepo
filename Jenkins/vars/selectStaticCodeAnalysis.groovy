def call(Boolean axivionOption, Boolean qacOption) {
    String settingFilepath="${env.WORKSPACE}\\APPS\\Config\\settings.bat"
    String backupsettingFile="${env.WORKSPACE}\\APPS\\Config\\settings_backup.bat"
    String content = readFile(settingFilepath)
   
    if (fileExists(settingFilepath)) {
        if ( axivionOption ){
            boolean axnCheck = content.contains('SET OPTION_USE_AXIVION=0') || content.contains('SET OPTION_USE_AXIVION=1')
            if (axnCheck) {
                boolean axnEnableCheck = !content.contains('SET OPTION_USE_AXIVION=1')
                if (axnEnableCheck) {
                    bat "copy ${settingFilepath} ${backupsettingFile}"
                    String modifiedContent = content.replaceAll('SET OPTION_USE_AXIVION=0', 'SET OPTION_USE_AXIVION=1')            
                    writeFile(file: settingFilepath, text: modifiedContent)
                    println "StaticCodeAnalysis will be done by AXIVION"
                } else {
                    println "AXIVION is already enabled, no changes made to settings.bat"
                }
            } else {
                println "AXIVION configuration not found"
            }
        }
        
        if ( qacOption ){
            boolean qacCheck = content.contains('SET OPTION_USE_QAC=0') || content.contains('SET OPTION_USE_QAC=1')
            if (qacCheck) {
                boolean qacEnableCheck = !content.contains('SET OPTION_USE_QAC=1')
                if (qacEnableCheck) {
                    bat "copy ${settingFilepath} ${backupsettingFile}"
                    String modifiedContent = content.replaceAll('SET OPTION_USE_QAC=0', 'SET OPTION_USE_QAC=1')            
                    writeFile(file: settingFilepath, text: modifiedContent)
                    println "StaticCodeAnalysis will be done by QAC"
                } else {
                    println "QAC is already enabled, no changes made to settings.bat"
                }
            } else {
                println "QAC configuration not found"
            }
        }
        
        if ( axivionOption == false){
            boolean axnCheck = content.contains('SET OPTION_USE_AXIVION=0') || content.contains('SET OPTION_USE_AXIVION=1')
            if (axnCheck) {
                boolean axnEnableCheck = !content.contains('SET OPTION_USE_AXIVION=0')
                if (axnEnableCheck) {
                    bat "copy ${settingFilepath} ${backupsettingFile}"
                    String modifiedContent = content.replaceAll('SET OPTION_USE_AXIVION=1', 'SET OPTION_USE_AXIVION=0')            
                    writeFile(file: settingFilepath, text: modifiedContent)
                    println "StaticCodeAnalysis will be done by AXIVION"
                } else {
                    println "AXIVION is already disabled, no changes made to settings.bat"
                }
            } else {
                println "AXIVION configuration not found"
            }
        }
        
        if ( qacOption == false){
            boolean qacCheck = content.contains('SET OPTION_USE_QAC=0') || content.contains('SET OPTION_USE_QAC=1')
            if (qacCheck) {
                boolean qacEnableCheck = !content.contains('SET OPTION_USE_QAC=0')
                if (qacEnableCheck) {
                    bat "copy ${settingFilepath} ${backupsettingFile}"
                    String modifiedContent = content.replaceAll('SET OPTION_USE_QAC=1', 'SET OPTION_USE_QAC=0')            
                    writeFile(file: settingFilepath, text: modifiedContent)
                    println "StaticCodeAnalysis will be done by QAC"
                } else {
                    println "QAC is already disabled, no changes made to settings.bat"
                }
            } else {
                println "QAC configuration not found"
            }
        }
    } else {
        println "${env.WORKSPACE}\\APPS\\Config\\settings.bat doesnot exists"
    }
}
