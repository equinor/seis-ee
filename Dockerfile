###RUN docker login registry.git.equinor.com/sentry/decimate -u ${{secrets.GITLAB_USERNAME}} -p ${{secrets.GITLAB_ACCESS_TOKEN}}
RUN echo ${{ secrets.GITLAB_ACCESS_TOKEN }} | docker login example.com -u "${{ secrets.GITLAB_USERNAME }}" --password-stdin
FROM registry.git.equinor.com/sentry/decimate:latest
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN useradd  --uid 1000 --user-group seis

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
RUN chown -R seis:seis /app
USER seis

CMD /app/init.sh start
