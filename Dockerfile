FROM ubuntu:latest
MAINTAINER Joe Costanzo "joe@joeco.info"
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
EXPOSE 5000
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]