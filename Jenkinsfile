pipeline {
    agent none
    stages {
        stage('test') {
            agent {
                dockerfile{
                    additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                }
            }
            steps {
                sh 'tox -- -m webview --headless'
            }
        }
    }
}
