FROM python:3.9-slim
WORKDIR /app
COPY . /app
# RUN apt-get update && apt-get install -y libenchant1c2a
RUN pip install
CMD ["python", "runner.py", "run"]
