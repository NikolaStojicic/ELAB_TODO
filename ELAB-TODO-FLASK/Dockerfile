FROM ubuntu


RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*


RUN apt update; \
    apt install -y software-properties-common; \
    add-apt-repository -y ppa:deadsnakes/ppa; \
    apt install -y python3.7;

RUN apt-get install -y python3-pip; 

WORKDIR /var/flask-app/elab-flask

COPY . .

RUN python3.7 -m pip install pipenv; \
    pipenv shell; \
    pipenv install; 

EXPOSE 5000

CMD [ "pipenv", "run","python3" ,"app.py" ]
