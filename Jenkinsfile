pipeline {
    agent {
    dockerfile true
    args '--tmpfs /.config'
    }
    stages {
        stage('test') {
            steps {
                sh 'tox -- -m webview --headless'
            }
        }
    }
}
