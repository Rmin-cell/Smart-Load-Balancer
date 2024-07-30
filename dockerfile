
FROM registry.gitlab.com/qio/standard/python:3.9-alpine


WORKDIR /solution

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python", "Flask.py"]