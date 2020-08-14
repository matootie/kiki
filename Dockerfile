FROM python:3.7-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install
CMD ["python", "-m", "pipenv", "run", "kiki"]
