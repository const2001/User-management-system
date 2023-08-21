pipeline {
    agent any


    stages {
        stage('Clone') {
            steps {
                // Clean up the workspace before starting the build
                deleteDir()

                // Clone the GitHub repository
                       git branch: 'main', url: 'https://github.com/const2001/User-management-system.git'

                     
            }
            
        }

        stage('Run Ansible Playbook') {
            steps {
                sh '''
                    cd ~/workspace/ansible-pipeline/
                    ansible-playbook ansible_playbook_flask_admin_setup.yml

                '''  
             
                }
            }
        }
    

    
}
