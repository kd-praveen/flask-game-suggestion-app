# pull official base image
FROM python:3.8

# set work directory
WORKDIR /alocai-app

# install dependencies
RUN apt-get update && apt-get install -y netcat
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY ./web ./web

# run entrypoint.sh
ENTRYPOINT ["/alocai-app/entrypoint.sh"]