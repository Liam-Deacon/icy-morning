FROM public.ecr.aws/lambda/python:3.8
COPY ./app ./app
COPY ./requirements.txt ./requirements.txt
RUN pip install wheel && \
    pip install awslambdaric && \
    pip install -r ./requirements.txt
CMD ["app"]