pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
  }

  environment {
    // Tag images per build so you can roll back if needed
    IRIS_IMAGE_TAG = "${env.BUILD_NUMBER}"

    // Local venv path in workspace
    VENV_DIR = ".venv"

    // Nginx entrypoint
    BASE_URL = "http://127.0.0.1:8081"
  }

  stages {

    stage('Checkout SCM') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python + Install') {
      steps {
        powershell '''
          $ErrorActionPreference = "Stop"

          python --version

          if (Test-Path $env:VENV_DIR) {
            Remove-Item -Recurse -Force $env:VENV_DIR
          }

          python -m venv $env:VENV_DIR

          .\\$env:VENV_DIR\\Scripts\\python -m pip install --upgrade pip
          .\\$env:VENV_DIR\\Scripts\\pip install -r requirements.txt
        '''
      }
    }

    stage('Train Model Artifact') {
      steps {
        powershell '''
          $ErrorActionPreference = "Stop"

          if (!(Test-Path "artifacts")) {
            New-Item -ItemType Directory -Path "artifacts" | Out-Null
          }

          # Change this command to your actual training entrypoint
          .\\$env:VENV_DIR\\Scripts\\python service\\train_local.py

          if (!(Test-Path "artifacts\\iris_model.joblib")) {
            throw "Model artifact not found at artifacts\\iris_model.joblib"
          }

          Write-Output "Model artifact created: artifacts\\iris_model.joblib"
        '''
      }
    }

    stage('Unit + API Tests') {
      steps {
        powershell '''
          $ErrorActionPreference = "Stop"

          # If you have pytest tests
          if (Test-Path "tests") {
            .\\$env:VENV_DIR\\Scripts\\pytest -q
          } else {
            Write-Output "No tests folder found, skipping pytest."
          }

          # Optional quick import check
          .\\$env:VENV_DIR\\Scripts\\python -c "import fastapi; print('FastAPI import OK')"
        '''
      }
    }

    stage('Build Docker Image') {
      steps {
        powershell '''
          $ErrorActionPreference = "Stop"

          Write-Output "Building with tag: $env:IRIS_IMAGE_TAG"

          # Compose will use IRIS_IMAGE_TAG in docker-compose.yml if you added it
          docker compose build
        '''
      }
    }

    stage('Deploy Blue-Green') {
      steps {
        powershell '''
          $ErrorActionPreference = "Stop"

          # Ensure compose sees the env var for image tag
          $env:IRIS_IMAGE_TAG = "$env:IRIS_IMAGE_TAG"

          # Your requirement: deploy via down + up
          .\\deploy\\deploy_stack.ps1
        '''
      }
    }

    stage('Smoke Test') {
      steps {
        powershell '''
          $ErrorActionPreference = "Stop"
          .\\deploy\\smoke_test.ps1 -BaseUrl "$env:BASE_URL"
        '''
      }
    }

    stage('Switch To Green') {
      steps {
        powershell '''
          $ErrorActionPreference = "Stop"

          .\\deploy\\switch_to_green.ps1

          # Verify again after switching traffic
          .\\deploy\\smoke_test.ps1 -BaseUrl "$env:BASE_URL"
        '''
      }
    }
  }

  post {
    always {
      powershell '''
        Write-Output "Docker compose status:"
        docker compose ps
      '''
      archiveArtifacts artifacts: 'artifacts/**/*', fingerprint: true
    }

    failure {
      // Optional: auto rollback to blue if green switch fails
      powershell '''
        if (Test-Path ".\\deploy\\switch_to_blue.ps1") {
          Write-Output "Rolling back to BLUE..."
          .\\deploy\\switch_to_blue.ps1
        }
      '''
    }
  }
}
