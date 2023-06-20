import MeCab
import jaconv
import sqlite3
dbname = 'datasets.db'
conn = sqlite3.connect(dbname, check_same_thread=False)
cur = conn.cursor()

from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from typing import Literal
import uvicorn

import re
import os
import sys

with open('Description.md','r') as f:
  description = f.read()

app = FastAPI(
  title='発音 API',
  description=description,
  version='0.0.1',
  terms_of_service='https://api.topi.cf/terms/',
  contact={
    'name': 'とぴ。',
    'url': 'https://twitter.com/topi_banana',
    'email': 'support@topi.cf',
  }
)

p = re.compile(r'([a-zA-Z]+)')

mecab = MeCab.Tagger('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd -r ./mecabrc -Oyomi')

class Token:
  alphabet: str
  kana: str

class Result:
  original: str
  yomi: str = ''
  yomi_kana: str = ''
  result: str = ''
  alphabet_tokens: list[Token] = []
  def __init__(self, txt:str):
    self.original = txt
    self.yomi = mecab.parse(self.original).split()[0]
    self.yomi_kana = jaconv.kata2hira(self.yomi)
    self.result = self.yomi_kana
    self.alphabet_tokens = []
    for i in set(p.findall(self.result)):
      token = Token()
      token.alphabet = i
      if i == i.upper():# 全て大文字
        r = []
        for j in list(i.lower()):
          cur.execute(f'SELECT kana FROM big WHERE alphabet="{j}"')
          r.append(cur.fetchall()[0][0])
        token.kana = ''.join(r)
      else:
        cur.execute(f'SELECT kana FROM cmu WHERE alphabet="{i.lower()}"')
        r = cur.fetchall()
        if r:# 単語が見つかった場合
          token.kana = r[0][0]
        else:# ローマ字に変換
          token.kana = jaconv.alphabet2kana(i)
      self.alphabet_tokens.append(token)
      self.result = self.result.replace(i, token.kana)
  def dump(self):
    return {**vars(self), 'alphabet_tokens': [vars(x) for x in self.alphabet_tokens]}

@app.get('/request')
def info(txt:str):
  result = Result(txt)
  return result.dump()

@app.get('/{txt}')
def v1(txt:str):
  result = Result(txt)
  return {'text':result.result}

if __name__ == '__main__':
  uvicorn.run(app, host=os.getenv('HASTUONAPI_HOST', '0.0.0.0'), port=int(os.getenv('HASTUONAPI_PORT', '10487')))