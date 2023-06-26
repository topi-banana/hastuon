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

# https://lifewithpython.com/2021/05/python-docker-env-vars.html
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONUTF8=1 \
  PYTHONIOENCODING="UTF-8" \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on

CMD [ "python", "main.py" ]