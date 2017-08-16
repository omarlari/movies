node {

   stage 'Checkout'
   git 'https://github.com/omarlari/movies.git'

   stage 'Build Dockerfile'
   docker.build('movies')

   stage 'Push to ECR'
   docker.withRegistry('https://${ECS_REPO}', 'ecr:us-west-2:aws') {
       docker.image('movies').push('${BUILD_NUMBER}')
   }

   stage 'update ECS Task Def'

   parallel(
        ecs: {node {
        docker.image('omarlari/awscli').inside{
            git 'https://github.com/omarlari/movies.git'
            sh 'sed -i s/BUILD/${BUILD_NUMBER}/g tdmovies001.json'
            sh 'aws ecs register-task-definition --cli-input-json file://tdmovies001.json --family ${TASK_DEF} --region us-west-2'
        }
        }},
        kubernetes: { node {
        docker.image('omarlari/alpine-kubectl').inside("--volume=/home/core/.kube:/config/.kube"){
            sh 'kubectl set image deployment/${K8S_DEPLOYMENT} movies=${ECS_REPO}/movies:${BUILD_NUMBER}'
            }
        }},
        swarm: { node {
            sh "echo deploying to swarm"
        }}
   )


   stage 'update ECS service'
   docker.image('anigeo/awscli').inside{
       sh 'aws ecs update-service --cluster ${ECS_CLUSTER} --service ${ECS_SERVICE} --task-definition ${TASK_DEF} --region us-west-2'
   }
}
