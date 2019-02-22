
projectName = "bunny"
@Library('jenkins-slack-messenger') 
import main.slack.SlackController;
SlackController slack = new SlackController(this);

try { 
    slack.sendStartMessage()
    node {

        stage('clone repo') { 
            git url: "https://github.com/NewKnowledge/${projectName}.git", 
                credentialsId: '055e98d5-ce0c-45ef-bf0d-ddc6ed9b634a', 
                branch: "${BRANCH_NAME}"

            sh "git rev-parse HEAD > .git/commit-id"
            commitId = readFile('.git/commit-id').trim()
            cleanBranchName = BRANCH_NAME.replaceAll("/", "-")
            println commitId
        }

        stage("publish docker image") { 
            withCredentials ([sshUserPrivateKey(
                    credentialsId: 'e7d90e91-9e58-4a60-abc9-26b8d9987ce9',
                    keyFileVariable: 'keyfile')]) {
                acrDomain = "newknowledge.azurecr.io"
                acrRepo = "${acrDomain}/${projectName}"
                sh "eval `ssh-agent -s` && ssh-add ${keyfile} && DOCKER_BUILDKIT=1 docker build -t ${projectName} --ssh default ."
                docker.withRegistry("https://${acrDomain}", 'acr-creds') {
                    sh "docker tag ${projectName} ${acrRepo}:${cleanBranchName}"
                    sh "docker tag ${projectName} ${acrRepo}:${commitId}"
                    sh "docker push ${acrRepo}:${cleanBranchName}"
                    sh "docker push ${acrRepo}:${commitId}"
                    if ("${BRANCH_NAME}" == "master") {
                        sh "docker tag ${projectName} ${acrRepo}:latest"
                        sh "docker push ${acrRepo}:latest"
                    }
                }
            }
        }

        /* Kick off another job to use the newly registered images */
        stage ("deploy on K8s") {
            // cat file on a machine where cat/shell is available
            devValues = sh (script: "cat ./values.dev.yaml", returnStdout: true, encoding: 'UTF-8')
            prodValues = sh (script: "cat ./values.prod.yaml", returnStdout: true, encoding: 'UTF-8')

            // Branches to deploy
            def buildableBranches = ["dev", "master"]
            if (!buildableBranches.contains(BRANCH_NAME)) {
                currentBuild.result = 'SUCCESS'
                return
            }

            // Different configs for different branches
            def devMap  = [namespace: "quorum-dev", 
                clusterId: "mario-monitor", 
                releaseName: "${projectName}-dev", 
                valueFile: devValues]
            def prodMap  = [namespace: "quorum-prod", 
                clusterId: "prod", 
                releaseName: "${projectName}-prod", 
                valueFile: prodValues]

            // Select "active" map
            def activeMap
            if ("${BRANCH_NAME}" == "master") {
                activeMap = prodMap
            } else {
                activeMap = devMap
            }
            // Run k8s jobs with config
            build job: "deploy-k8s-from-file", parameters: [
                string(name: "imageTag", value: "${commitId}"),
                string(name: "chartName", value: "nk.kafka-singleton"),
                string(name: "valueFileString", value: "${activeMap.valueFile}"),
                string(name: "namespace", value: "${activeMap.namespace}"),
                string(name: "clusterId", value: "${activeMap.clusterId}"),
                string(name: "releaseName", value: "${activeMap.releaseName}")
            ]
        }
    }
    slack.sendFinishMessage()
} catch(Exception e) { 
    slack.sendErrorMessage(e)
    error(e)
}
