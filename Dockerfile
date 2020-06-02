FROM python:3.7-slim
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y libenchant1c2a
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install
CMD ["pipenv", "run", "python", "runner.py", "run"]
