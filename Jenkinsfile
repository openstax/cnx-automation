pipeline {
    agent { dockerfile true}
    stages {
        stage('test') {
            steps {
                sh 'tox -- -m webview'
            }
        }
    }
}
