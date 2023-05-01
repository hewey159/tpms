#Deriving the latest base image
FROM python:3.9.2


# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app/src

#to COPY the remote file at working directory in container
COPY . ./

COPY requirements.txt ./
RUN pip install -r requirements.txt

CMD [ "python", "./src/__main__.py"]