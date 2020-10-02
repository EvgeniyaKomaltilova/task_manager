FROM python:3.8
ENV PYTHONUNBUFFERED=1
RUN mkdir /task_manager
WORKDIR /task_manager
COPY requirements.txt /task_manager/
RUN pip install -r requirements.txt
COPY . /task_manager/
