FROM python

RUN git clone https://github.com/neologd/mecab-ipadic-neologd.git

RUN apt update
RUN apt install -y \
  sudo \
  mecab libmecab-dev mecab-ipadic-utf8

RUN ./mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -a -n -y

RUN pip install jaconv mecab-python3 fastapi uvicorn[standard]

WORKDIR /app

COPY ./* ./