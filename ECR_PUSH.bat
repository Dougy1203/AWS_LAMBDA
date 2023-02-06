:: check if connection is valid with login success
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>

:: docker fun stuff
docker compose up -d

:: create AWS ECR Repository
aws ecr create-repository --repository-name <REPOSITORY_NAME> --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE

:: tags and pushes to ecr
docker tag audition:1.0 <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:audition
docker tag cast:1.0 <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:cast
docker tag cdirector:1.0 <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:cdirector
docker tag cperformer:1.0 <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:cperformer
docker tag cperformance:1.0 <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:cperformance
docker tag dperformance:1.0 <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:dperformance
docker tag pperformance:1.0 <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:pperformance
docker tag sperformance:1.0 <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:sperformance
docker push <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:audition
docker push <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:cast
docker push <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:cdirector
docker push <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:cperformer
docker push <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:cperformance
docker push <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:dperformance
docker push <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:pperformance
docker push <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:sperformance

aws lambda create-function --function-name <FUNCTION_NAME> \
--image <YOUR_ACCOUNT_NUMBER>.dkr.ecr.us-east-1.amazonaws.com/<REPOSITORY_NAME>:audition
pause