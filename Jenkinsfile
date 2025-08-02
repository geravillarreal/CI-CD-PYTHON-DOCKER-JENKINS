pipeline {
  agent any
  options { timestamps(); skipDefaultCheckout(true) }  // evita checkout implícito

  environment {
    APP_NAME   = 'myapp'
    APP_PORT   = '8000'
    IMAGE_REPO = "${env.APP_NAME}"
  }

  stages {
    stage('Checkout') {
      steps {
        deleteDir() // limpia el workspace por si quedó algo
        // Opción A: usa la config del job (Pipeline from SCM)
        // checkout scm

        // Opción B (recomendada ahora): checkout explícito directo al repo
        git branch: 'main', url: 'https://github.com/geravillarreal/CI-CD-PYTHON-DOCKER-JENKINS.git'
      }
    }

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
          sh "docker build -t ${IMAGE_REPO}:${shortCommit} -t ${IMAGE_REPO}:latest ."
        }
      }
    }

    stage('Deploy') {
      steps {
        sh '''
          (docker rm -f ${APP_NAME} || true)
          docker run -d --name ${APP_NAME} -p ${APP_PORT}:8000 ${IMAGE_REPO}:latest
        '''
      }
    }
  }

  post {
    success { echo "Listo: http://localhost:${APP_PORT}/health" }
    failure { echo "Falló el pipeline: revisa logs." }
  }
}
