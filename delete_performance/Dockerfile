FROM public.ecr.aws/lambda/python:3.9
COPY delete_performance.py ${LAMBDA_TASK_ROOT}
CMD [ "delete_performance.lambda_handler" ]