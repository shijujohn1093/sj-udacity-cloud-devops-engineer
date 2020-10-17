aws cloudformation create-stack \
--stack-name "capstone-project-user" \
--template-body file://user.yaml \
--region=us-east-1 \
--capabilities CAPABILITY_NAMED_IAM \
