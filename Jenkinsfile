pipeline{
    agent "slave-1"
    tools {
        nodejs 'node'
    }
    stages{
        stage("Checkout"){
            steps{
                echo "======== executing git repository checkout ========"
            }
        }
        stage("Test"){
            steps{
                echo "======== executing app tests ========"
            }
            post{
                success{
                echo "======== tests stage executed successfully ========"
                }
                failure{
                    echo "======== tests stage execution failed ========"
                }
            } 
        }
        stage("App build"){
            steps{
                echo "======== executing app build ========"
            }
        }
        stage("Docker images build"){
            steps{
                echo "======== executing app docker images build ========"
            }
        }
        stage("Deliver"){
            steps{
                echo "======== executing app deliver ========"
            }
        }
        stage("Deploy"){
            steps{
                echo "======== executing app deliver ========"
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

