FROM python:3
EXPOSE 5000
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]

# Won't run right now; need to think of some workaround for pyodbc
