FROM registry.git.equinor.com/sentry/decimate:latest
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app


# Install python/pip
RUN apt-get update -y && apt-get install -y python3 wget python3-distutils python3-apt ssh rsync g++
RUN python3 --version
RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py
RUN pip install poetry

RUN poetry config virtualenvs.create false


#build c++ program
# todo perhaps move this to separate docker-compose service or something??
WORKDIR /mseed-app
ADD /mseed_converter /mseed-app
RUN g++ -g -o main main.cpp

WORKDIR /app/
COPY pyproject.toml poetry.lock ./
RUN poetry install

ADD app /app/
RUN chown -R 1000:1000 /app
USER 1000:1000

CMD /app/init.sh start
