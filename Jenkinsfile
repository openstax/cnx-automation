pipeline {
    agent none
    stages {
        stage('test') {
            agent {
                docker{
                    dockerfile true
                }
            }
            steps {
                sh 'tox -- -m webview --headless'
            }
        }
    }
}
