pipeline{
    agent "any"
    stages{
        stage("Checkout"){
            steps{
                echo "======== executing git repository checkout ========"
                git branch: 'develop', url: "https://github.com/kevcalderon/AYD1-Proyecto1.git"
            }
        }
        /*stage("Test"){
            steps{
                echo "======== executing app tests ========"
                dir('backend'){
                    sh 'pytest --cov=controlador test_controlador.py'
                }
            }
            post{
                success{
                echo "======== tests stage executed successfully ========"
                }
                failure{
                    echo "======== tests stage execution failed ========"
                }
            } 
        }*/
        stage("App build"){
            steps{
                echo "======== executing app frontend build ========"
                dir('frontend'){
                    sh 'npm ci --silent'
                    sh 'npm run build'
                }
            }
        }
        stage("Docker image build backend"){
            steps{
                echo "======== executing app docker backend image build ========"
                dir('backend'){
                    script{
                        dockerImageB = docker.build "carlosmz87/proyecto_ayd1_backend"
                    }
                }
            }
        }
        stage("Docker image build frontend"){
            steps{
                echo "======== executing app docker frontend image build ========"
                dir('frontend'){
                    script{
                        dockerImageF = docker.build "carlosmz87/proyecto_ayd1_frontend"
                    }
                }
            }
        }
        stage("Deliver"){
            steps{
                echo "======== executing app deliver ========"
                script{
                    docker.withRegistry('', 'dockerhub'){
                        echo "DELIVER BACKEND"
                        dockerImageB.push('$BUILD_NUMBER')
                        dockerImageB.push('latest')
                        echo "DELIVER FRONTEND"
                        dockerImageF.push('$BUILD_NUMBER')
                        dockerImageF.push('latest')
                    }
                }      
            }
        }
    }
    post{
        success{
            echo "========pipeline executed successfully ========"
        }
        failure{
            echo "========pipeline execution failed========"
        }
    }
}

