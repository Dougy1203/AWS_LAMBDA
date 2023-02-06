FROM public.ecr.aws/lambda/python:3.9
COPY create_performance.py ${LAMBDA_TASK_ROOT}
CMD [ "create_performance.lambda_handler" ]