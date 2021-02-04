FROM registry.git.equinor.com/sentry/decimate:latest
ENV PYTHONUNBUFFERED=1

RUN useradd  --uid 1000 --user-group seis

# Install python/pip
RUN apt-get update -y && apt-get install -y python3 wget python3-distutils python3-apt ssh rsync
RUN python3 --version
RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py
RUN pip install poetry


RUN poetry config virtualenvs.create false
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install

ADD seis_ee /app

#change permission of decimate folder to be able to run the decimate command from the sentry project
RUN chown -R seis:seis /decimate
RUN chmod -R 700 /decimate

USER seis
WORKDIR /data
#ENTRYPOINT ["python3", "/app/seis_ee.py"]