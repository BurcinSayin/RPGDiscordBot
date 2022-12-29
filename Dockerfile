FROM public.ecr.aws/lambda/python:3.9 AS build-stage

RUN mkdir /root/site-packages
RUN pip install pynacl -t /root/site-packages
RUN pip install boto3 -t /root/site-packages
RUN pip install gspread -t /root/site-packages

FROM scratch AS export-stage
COPY --from=build-stage /root/site-packages /
