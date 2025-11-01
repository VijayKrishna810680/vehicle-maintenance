pipeline {
  agent any
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Build Backend') {
      steps {
        sh 'docker build -t vehicle-backend:latest backend'
      }
    }
    stage('Deploy (example)') {
      steps {
        echo 'Add deployment steps (ssh, kubectl, terraform) here'
      }
    }
  }
}
