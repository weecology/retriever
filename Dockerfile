# Download base image ubuntu 18.04
FROM ubuntu:18.04

MAINTAINER Weecology "https://github.com/weecology/retriever"

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

# Manually install tzdata to allow for non-interactive install
RUN apt-get install -y --force-yes tzdata

RUN apt-get install -y --force-yes build-essential wget git locales locales-all > /dev/null
RUN apt-get install -y --force-yes postgresql-client mariadb-client > /dev/null

# Set encoding
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Remove python2 and install python3
RUN apt-get remove -y python && apt-get install -y python3  python3-pip curl
RUN rm -f /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python
RUN rm -f /usr/bin/pip && ln -s /usr/bin/pip3 /usr/bin/pip

RUN echo "export PATH="/usr/bin/python:$PATH"" >> ~/.profile
RUN echo "export PYTHONPATH="/usr/bin/python:$PYTHONPATH"" >> ~/.profile
RUN echo "export PGPASSFILE="~/.pgpass"" >> ~/.profile

# Add permissions to config files
RUN chmod 0644 ~/.profile

RUN pip install pymysql
RUN pip install psycopg2-binary -U
RUN pip install codecov -U
RUN pip install pytest-cov -U
RUN pip install pytest-xdist -U
RUN pip install pytest
RUN pip install yapf
RUN pip install pylint
RUN pip install flake8

# Install Postgis after Python is setup
RUN apt-get install -y --force-yes postgis

COPY . ./retriever
RUN chmod 0755 /retriever/cli_tools/entrypoint.sh
ENTRYPOINT ["/retriever/cli_tools/entrypoint.sh"]


WORKDIR ./retriever

RUN pip install -e .
# Add permissions to config files
# Do not run these cmds before Entrypoint.
RUN export PGPASSFILE="~/.pgpass"
RUN chmod 600 cli_tools/.pgpass
RUN chmod 600 cli_tools/.my.cnf

CMD ["bash", "-c", "Python --version"]
