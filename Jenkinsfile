@Library('jenkins-pipeline-scripts') _
pipeline {
    agent none
    triggers {
        pollSCM('*/3 * * * *')
    }
    options {
        // Keep the 50 most recent builds
        buildDiscarder(logRotator(numToKeepStr:'50'))
    }
    stages {
        stage('Build') {
            agent any
            steps {
                sh 'make docker-image'
            }
        }
        stage('Push image to registry') {
            agent any
            steps {
                pushImageToRegistry (
                    env.BUILD_ID,
                    "imio/memory"
                )
            }
        }
        stage('Deploy to prod') {
            agent any
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                // sh "mco shell run 'docker pull docker-staging.imio.be/imio/memory:$BUILD_ID' -I /^staging.imio.be/"
                // sh "mco shell run '/srv/docker_scripts/website-update-all-images.sh' -t 1200 --tail -I /^staging.imio.be/"
                sh "echo 'deploy to prod'"
            }
            // steps {
            //     deployToProd (
            //         env.BUILD_ID,
            //         'imio/memory',
            //         '/role::docker::sites$/',
            //         '/srv/docker_scripts/website-update-all-images.sh',
            //     )
            // }
        }
    }
}
