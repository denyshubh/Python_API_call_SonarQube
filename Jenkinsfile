pipeline {
  agent any
	stages {
	  stage('APP: Running Leand SDLC Quality Gate Creation') {
		  steps {
				withSonarQubeEnv('SonarQube') {
                                   sh 'env'
				   sh 'sudo chmod +x test.py'
				   sh 'sudo pip3 install -r requirements.txt'
				   sh 'python3 test.py'
				}
			}
       }
    }
}
	
