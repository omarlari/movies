node {

   stage 'Checkout'
   git 'https://github.com/omarlari/movies.git'

   stage 'Build Dockerfile'
   docker.build('movies')

   stage 'Push to ECR'
   docker.withRegistry('https://223171727691.dkr.ecr.us-west-2.amazonaws.com', 'ecr:us-west-2:aws') {
       docker.image('movies').push('${BUILD_NUMBER}')
   }

   stage 'update ECS Task Def'

   parallel(
      ecs: {node {
        docker.image('anigeo/awscli').inside{
            git 'https://github.com/omarlari/movies.git'
            sh 'sed -i s/BUILD/${BUILD_NUMBER}/g ./movies/tdmovies001.json'
            sh 'aws ecs register-task-definition --cli-input-json file://~/movies/tdmovies001.json --family $TASK_DEF --region us-west-2'
        }
        }},
        kubernetes: { node {
            sh "echo deploying to k8s"
        }},
        swarm: { node {
            sh "echo deploying to swarm"
        }}
   )


   stage 'update ECS service'
   sshagent (credentials: ['ssh']) {
       sh "ssh -o StrictHostKeyChecking=no -l core 10.99.254.67 docker run awscli aws ecs update-service --cluster $ECS_CLUSTER --service $ECS_SERVICE --task-definition $TASK_DEF --region us-west-2"
   }
}
