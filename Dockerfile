FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt .
COPY requirements_extras.txt .
RUN pip install -U pip wheel setuptools \
 && pip install -r requirements.txt \
 && pip install -r requirements_extras.txt
COPY . .
ENTRYPOINT ["python", "example.py"]
