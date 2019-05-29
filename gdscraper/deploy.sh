#!/bin/bash
SECONDS=0

# Taken from: https://www.davidhoeck.com/automated-deployment-for-vue-applications/

SSH_USERNAME="root"
SSH_HOST="138.68.175.93"
SSH_KEY="/Users/puiggm/.ssh/gd"

DEPLOY_BRANCH="master"
PROD_PATH="/var/www/automation/londongdautomation/gdscraper"


echo "Commiting the changes to the Repo..."
git add .
git commit -m "[RELEASE] commit for deployment - IMPORTANT: this commit is auto-generated by the deploy script"
git push origin ${DEPLOY_BRANCH} --force


# -- LOG IN VIA SSH TO REMOTE --
ssh  ${SSH_USERNAME}@${SSH_HOST} "

    cd ${PROD_PATH}

    docker stop apigd;
    docker rm apigd;
    docker run -p 9080:9080 -tid --restart unless-stopped --name apigd -v ${PROD_PATH}:/scrapyrt/project scrapinghub/scrapyrt



";
duration=$SECONDS
echo "Deployment Finished in "
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds."

exit
