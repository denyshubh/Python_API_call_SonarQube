pipeline {
  agent none
	stages {
	  stage('APP: Running Leand SDLC Quality Gate Creation') {
		  steps {
				withSonarQubeEnv('sonarqube') {
           sh 'env'
				   sh 'pip3 install -r requirements.txt'
				   // sh 'python3 test.py'
				}
			}
    }
  }
}
	
