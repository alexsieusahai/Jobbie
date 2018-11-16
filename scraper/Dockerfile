FROM python:3
EXPOSE 5000
ADD . /code
WORKDIR /code
CMD ["ls"]
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]
