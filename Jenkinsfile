pipeline {
  agent any
  options { timestamps(); skipDefaultCheckout(true) }

  environment {
    APP_NAME   = 'myapp'
    APP_PORT   = '8000'
    IMAGE_REPO = "${env.APP_NAME}"
    JENKINS_CTN = 'jenkins' // nombre de tu contenedor (docker-compose lo creó así)
  }

  stages {
    stage('Checkout') {
      steps {
        deleteDir()
        git branch: 'main', url: 'https://github.com/geravillarreal/CI-CD-PYTHON-DOCKER-JENKINS.git'
        sh 'pwd && ls -la'               // Diagnóstico: aquí debes ver requirements.txt
      }
    }

    stage('Tests') {
      steps {
        // Monta el MISMO volumen que usa Jenkins y trabaja en la MISMA ruta
        sh """
          docker run --rm --volumes-from ${JENKINS_CTN} \
            -w "${WORKSPACE}" python:3.12-slim \
            bash -lc "ls -la; pip install -r requirements.txt && pytest -q"
        """
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          def shortCommit = sh(returnStdout: true, script: "git rev-parse --short HEAD").trim()
          // Usamos un contenedor con docker CLI; el contexto '.' sale del volumen compartido
          sh """
            docker run --rm --volumes-from ${JENKINS_CTN} \
              -v /var/run/docker.sock:/var/run/docker.sock \
              -w "${WORKSPACE}" docker:26.1-cli sh -lc \
              "docker build -t ${IMAGE_REPO}:${shortCommit} -t ${IMAGE_REPO}:latest ."
          """
        }
      }
    }

    stage('Deploy') {
      steps {
        sh """
          docker rm -f ${APP_NAME} || true
          docker run -d --name ${APP_NAME} -p ${APP_PORT}:8000 ${IMAGE_REPO}:latest
          docker ps --filter name=${APP_NAME}
        """
      }
    }
  }

  post {
    success { echo "Listo: http://localhost:${APP_PORT}/health" }
    failure { echo "Falló el pipeline: revisa logs." }
  }
}
