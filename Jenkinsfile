pipeline {
  agent any

  options {
    timestamps()
  }

  environment {
    IMAGE_NAME = "iris-api"
    PROXY_URL  = "http://127.0.0.1:8081"
    BLUE_URL   = "http://127.0.0.1:8082"
    GREEN_URL  = "http://127.0.0.1:8083"
  }

  stages {

    stage('Checkout SCM') {
      steps {
        checkout scm
      }
    }

    stage('Checkout') {
      steps {
        script {
          bat 'git rev-parse --short HEAD > .gitshort'
          env.GIT_SHORT = readFile('.gitshort').trim()
          echo "Commit: ${env.GIT_SHORT}"
        }
      }
    }

    stage('Setup Python + Install') {
      steps {
        bat '''
          py -3.11 -m venv .venv
          .venv\\Scripts\\python -m pip install --upgrade pip
          .venv\\Scripts\\pip install -r service\\requirements.txt
          .venv\\Scripts\\pip install -r service\\requirements-dev.txt
        '''
      }
    }

    stage('Train Model Artifact') {
      steps {
        bat '''
          .venv\\Scripts\\python service\\train.py
          dir artifacts
        '''
        archiveArtifacts artifacts: 'artifacts/**', fingerprint: true
      }
    }

    stage('Unit + API Tests') {
      steps {
        bat '''
          set PYTHONPATH=service\\app
          .venv\\Scripts\\pytest -q
        '''
      }
    }

    stage('Build Docker Image') {
      steps {
        bat """
          docker build -t %IMAGE_NAME%:%GIT_SHORT% -f service\\Dockerfile .
          docker image ls %IMAGE_NAME% --format "table {{.Repository}}\\t{{.Tag}}\\t{{.ID}}"
        """
      }
    }

    stage('Deploy Blue-Green') {
      steps {
        script {
          def active = "blue"
          if (fileExists("deploy/active_color.txt")) {
            active = readFile("deploy/active_color.txt").trim()
          }
          def newColor = (active == "blue") ? "green" : "blue"
          env.ACTIVE_COLOR = active
          env.NEW_COLOR = newColor
          echo "Active: ${env.ACTIVE_COLOR}, New: ${env.NEW_COLOR}"
        }

        bat '''
          docker network inspect iris-net >nul 2>nul || docker network create iris-net
          docker compose -f deploy\\docker-compose.proxy.yml up -d
        '''

        bat """
          set IMAGE_TAG=%GIT_SHORT% && docker compose -f deploy\\docker-compose.${env.NEW_COLOR}.yml up -d
        """

        bat 'docker ps --format "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}"'
      }
    }

    stage('Smoke Test') {
      steps {
        script {
          def url = (env.NEW_COLOR == "blue") ? env.BLUE_URL : env.GREEN_URL
          env.NEW_URL = url
          echo "Smoke testing ${env.NEW_COLOR} at ${env.NEW_URL}"
        }

        bat """
          curl.exe -s -o nul -w "health=%{http_code}\\n" %NEW_URL%/health
          curl.exe -s -o nul -w "docs=%{http_code}\\n" %NEW_URL%/docs
          curl.exe -s -X POST %NEW_URL%/predict -H "Content-Type: application/json" --data-binary "{\\"features\\":[5.1,3.5,1.4,0.2]}"
        """
      }
    }

    stage('Switch To Green') {
      steps {
        bat """
          powershell -ExecutionPolicy Bypass -File deploy\\switch_traffic.ps1 -Color ${env.NEW_COLOR}
        """

        bat """
          echo ${env.NEW_COLOR} > deploy\\active_color.txt
        """

        bat """
          curl.exe -s -o nul -w "proxy_health=%{http_code}\\n" %PROXY_URL%/health
          curl.exe -s -o nul -w "proxy_docs=%{http_code}\\n" %PROXY_URL%/docs
        """

        script {
          def oldColor = env.ACTIVE_COLOR
          echo "Cleaning up old color: ${oldColor}"
          env.OLD_COLOR = oldColor
        }

        bat """
          docker compose -f deploy\\docker-compose.${env.OLD_COLOR}.yml down
        """
      }
    }
  }

  post {
    failure {
      echo "Pipeline failed, leaving current production traffic as-is."

      script {
        if (env.NEW_COLOR != null) {
          echo "Attempting cleanup of NEW_COLOR=${env.NEW_COLOR}"
        }
      }

      bat """
        if exist deploy\\docker-compose.${env.NEW_COLOR}.yml (
          docker compose -f deploy\\docker-compose.${env.NEW_COLOR}.yml down
        )
      """
    }
  }
}
