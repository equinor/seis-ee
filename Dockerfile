FROM registry.git.equinor.com/sentry/decimate:latest
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN useradd  --uid 1000 --user-group seis

# Install python/pip
RUN apt-get update -y && apt-get install -y python3 wget python3-distutils python3-apt ssh rsync
RUN python3 --version
RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py
RUN pip install poetry

RUN poetry config virtualenvs.create false
WORKDIR /app/
COPY pyproject.toml poetry.lock ./
RUN poetry install

ADD app /app/
RUN chown -R seis:seis /app
USER seis
# TODO: create init.sh
#ENTRYPOINT ["python3", "/app/app.py"]