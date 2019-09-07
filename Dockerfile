FROM python:3.7-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install
CMD ["pipenv", "run", "python", "runner.py", "run"]
