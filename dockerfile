FROM python:3.8.2-alpine3.11

RUN pip3.8 install flask -i https://pypi.douban.com/simple

workdir /data/readApp

CMD python main.py
