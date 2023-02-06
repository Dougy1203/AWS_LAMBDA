FROM public.ecr.aws/lambda/python:3.9
COPY create_performer.py ${LAMBDA_TASK_ROOT}
CMD [ "create_performer.lambda_handler" ]