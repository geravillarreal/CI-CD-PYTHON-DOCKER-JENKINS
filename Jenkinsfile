pipeline {
  agent any
  options { timestamps() }

  triggers {
    // Opción simple: revisar cada 2 min
    pollSCM('H/2 * * * *')
    // Si usas webhook, descomenta:
    // githubPush()
  }

  environment {
    APP_NAME  = 'myapp'
    APP_PORT  = '8000'
    IMAGE_REPO = "${env.APP_NAME}" // local
  }

  stages {

    stage('Tests') {
      steps {
        sh '''
          docker run --rm -v "$PWD":/app -w /app python:3.12-slim \
            bash -lc "pip install -r requirements.txt && pytest -q"
        '''
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          def shortCommit = sh(returnStdout: true, script: "git rev-parse --short HEAD").trim()
          sh """
            docker build -t ${IMAGE_REPO}:${shortCommit} -t ${IMAGE_REPO}:latest .
          """
        }
      }
    }

    stage('Deploy') {
      steps {
        sh '''
          (docker rm -f ${APP_NAME} || true)
          docker run -d --name ${APP_NAME} -p ${APP_PORT}:8000 ${IMAGE_REPO}:latest
          sleep 2
          docker ps --filter "name=${APP_NAME}"
        '''
      }
    }
  }

  post {
    success {
      echo "Listo: http://localhost:${APP_PORT}/health"
    }
    failure {
      echo "Falló el pipeline: revisa logs."
    }
  }
}
