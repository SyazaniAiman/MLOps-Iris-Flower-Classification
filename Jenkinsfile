pipeline {
  agent { label 'windows' }

  options {
    disableConcurrentBuilds()
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Setup Python + Install') {
      steps {
        bat '''
          py -3.11 -m venv .venv
          call .venv\\Scripts\\activate.bat
          python -m pip install --upgrade pip
          python -m pip install -r service\\requirements.txt
        '''
      }
    }

    stage('Train Model Artifact') {
      steps {
        bat '''
          call .venv\\Scripts\\activate.bat
          if not exist artifacts mkdir artifacts
          python service\\train_local.py
          dir artifacts
          type artifacts\\metrics.txt
        '''
      }
    }

    stage('Unit + API Tests') {
      steps {
        bat '''
          call .venv\\Scripts\\activate.bat
          python -m pytest -q
        '''
      }
    }

    stage('Build Docker Image') {
      steps {
        bat '''
          docker build -t iris-api:jenkins -f service\\Dockerfile .
        '''
      }
    }

    stage('Deploy Blue-Green') {
      steps {
        bat '''
          docker compose down
          docker compose up -d
          docker compose ps
        '''
      }
    }

    stage('Smoke Test') {
      steps {
        bat '''
          curl.exe http://127.0.0.1:8081/health
          curl.exe -X POST http://127.0.0.1:8081/predict -H "Content-Type: application/json" -d "{\\"features\\":[5.1,3.5,1.4,0.2]}"
        '''
      }
    }

    stage('Switch To Green') {
      steps {
        bat '''
          powershell -ExecutionPolicy Bypass -File .\\deploy\\switch_to_green.ps1
          curl.exe http://127.0.0.1:8081/health
        '''
      }
    }
  }
}
