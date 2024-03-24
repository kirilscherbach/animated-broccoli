FROM mageai/mageai:latest
USER root
#install pg client to run DB backups on schedule
RUN apt-get update
RUN apt-get install -y lsb-release
RUN sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get -y install postgresql-16
RUN apt-get clean all

ARG USER_CODE_PATH=/home/src/${PROJECT_NAME}

# Note: this overwrites the requirements.txt file in your new project on first run.
# You can delete this line for the second run :)
COPY requirements.txt ${USER_CODE_PATH}/requirements.txt

RUN pip3 install -r ${USER_CODE_PATH}/requirements.txt
