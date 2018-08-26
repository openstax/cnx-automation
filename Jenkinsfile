pipeline {
    agent {
        {
            docker {
                label 'docker'
                dockerfile true
            }
        }
    stages {
        stage('test') {
            steps {
                sh 'tox -- -m webview --headless'
            }
        }
    }
}
