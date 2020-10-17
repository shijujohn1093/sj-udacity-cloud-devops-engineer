def image

pipeline {
    agent any

    stages {
        stage('Lint Dockerfile') {
            steps {
                script {
                    docker.image('hadolint/hadolint:latest-alpine').inside() {
                            sh 'hadolint ./application/Dockerfile | tee -a hadolint.txt'
                            sh '''
                                lintErrors=$(stat --printf="%s"  hadolint.txt)
                                if [ "$lintErrors" -gt "0" ]; then
                                    echo "Errors linting Dockerfile"
                                    cat hadolint.txt
                                    exit 1
                                else
                                    echo "Done linting Dockerfile"
                                fi
                            '''
                    }
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    image = docker.build("shijujohn1093/capstone", "-f application/Dockerfile application")
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                        image.push("${env.BUILD_NUMBER}")
                        image.push("latest")
                    }
                }
            }
        }

        stage('Apply deployment') {
            steps {
                dir('kubernetes') {
                    withAWS(credentials: 'aws-credentials', region: 'us-east-1') {
                            sh 'kubectl apply -f k8s.yaml'
                        }
                    }
            }
        }

        stage('Update deployment') {
            steps {
                dir('kubernetes') {
                    withAWS(credentials: 'aws-credentials', region: 'us-east-1') {
                            sh "kubectl set image deployments/capstone capstone=shijujohn1093/capstone:${BUILD_NUMBER}"
                        }
                    }
            }
        }

        stage('Wait for pods') {
            steps {
                withAWS(credentials: 'aws-credentials', region: 'us-east-1') {
                    sh '''
                        ATTEMPTS=0
                        ROLLOUT_STATUS_CMD="kubectl rollout status deployment/capstone"
                        until $ROLLOUT_STATUS_CMD || [ $ATTEMPTS -eq 60 ]; do
                            $ROLLOUT_STATUS_CMD
                            ATTEMPTS=$((attempts + 1))
                            sleep 10
                        done
                    '''
                }
            }
        }

        stage('Post deployment test') {
            steps {
                withAWS(credentials: 'aws-credentials', region: 'ap-southeast-2') {
                    sh '''
                        HOST=$(kubectl get service service-capstone | grep 'amazonaws.com' | awk '{print $4}')
                        curl $HOST -f
                    '''
                }
            }
        }

        stage("Prune docker") {
            steps {
                sh "docker system prune -f"
            }
        }
    }
}
