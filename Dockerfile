FROM python:3.10.5-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . .

RUN pip install -r requirements.txt
RUN apt-get update -y
RUN apt-get install -y locales && \
sed -i -e 's/# pt_BR UTF-8/pt_BR UTF-8/' /etc/locale.gen && \
dpkg-reconfigure --frontend=noninteractive locales

ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8