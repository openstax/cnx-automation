@Library('pipeline-library') _

pipeline {
  agent { label 'docker' }
  environment {
    TESTING_CONTAINER_NAME = meta.getContainerName()
  }
  stages {
    stage('Test Against staging.cnx.org') {
      // all branches
      when { branch 'master' }
      steps {
        sh "mkdir -p ${env.WORKSPACE}/xml-report"
        sh "docker run -d --name ${env.TESTING_CONTAINER_NAME} -v ${env.WORKSPACE}/xml-report:/xml-report --env-file .jenkins/testing.env.list openstax/cnx-automation:latest"
        sh "docker exec ${env.TESTING_CONTAINER_NAME} pytest --new-first --failed-first -m 'webview or neb' --junitxml=report.xml"
      }
      post {
        always {
          // Move the report to a place that is both accessible and writable
          sh "docker exec -u root ${env.TESTING_CONTAINER_NAME} cp /code/report.xml /xml-report"
          // Destroy the testing container
          sh "docker stop ${env.TESTING_CONTAINER_NAME} && docker rm -f ${env.TESTING_CONTAINER_NAME}"
          // Report test results
          junit "xml-report/report.xml"
        }
      }
    }
  }
}
