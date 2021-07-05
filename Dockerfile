# Download base image ubuntu 18.04
FROM ubuntu:18.04

MAINTAINER Weecology "https://github.com/weecology/retriever"

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

# Manually install tzdata to allow for non-interactive install
RUN apt-get install -y --force-yes tzdata

RUN apt-get install -y --force-yes build-essential wget git locales locales-all > /dev/null &&\
    apt-get install -y --force-yes postgresql-client mariadb-client > /dev/null &&\
    apt-get install -y --force-yes libpq-dev

# Set encoding
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Remove python2 and install python3
RUN apt-get remove -y python && apt-get install -y python3  python3-pip curl &&\
    rm -f /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python &&\
    rm -f /usr/bin/pip && ln -s /usr/bin/pip3 /usr/bin/pip

RUN echo "export PATH="/usr/bin/python:$PATH"" >> ~/.profile &&\
    echo "export PYTHONPATH="/usr/bin/python:$PYTHONPATH"" >> ~/.profile &&\
    echo "export PGPASSFILE="~/.pgpass"" >> ~/.profile

# Add permissions to config files
RUN chmod 0644 ~/.profile

RUN pip install pymysql &&\
    pip install psycopg2-binary -U &&\
    pip install codecov -U &&\
    pip install pytest-cov -U &&\
    pip install pytest-xdist -U &&\
    pip install pytest &&\
    pip install yapf &&\
    pip install pylint &&\
    pip install flake8 -U &&\
    pip install h5py &&\
    pip install Pillow &&\
    pip install kaggle &&\
    pip install inquirer

# Install Postgis after Python is setup
RUN apt-get install -y --force-yes postgis

COPY . ./retriever
RUN chmod 0755 /retriever/cli_tools/entrypoint.sh
ENTRYPOINT ["/retriever/cli_tools/entrypoint.sh"]


WORKDIR ./retriever

RUN pip install -e .
# Add permissions to config files
# Do not run these cmds before Entrypoint.
RUN export PGPASSFILE="~/.pgpass" &&\
    chmod 600 cli_tools/.pgpass &&\
    chmod 600 cli_tools/.my.cnf

CMD ["bash", "-c", "python --version"]
