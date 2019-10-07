FROM python:3.6
COPY . /web
WORKDIR /web/api
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]