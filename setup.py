import json

import sqlite3
dbname = 'data.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

# CMU辞書
cur.execute('CREATE TABLE cmu(alphabet STRING, kana STRING)')

with open('./cmu.json', 'r') as f:
  data = json.load(f)
for i in data:
  cur.execute(f'INSERT INTO cmu(alphabet, kana) values("{i}", "{data[i]}")')

# 大文字アルファベット
cur.execute('CREATE TABLE big(alphabet STRING, kana STRING)')
with open('./bigalphabet.json', 'r') as f:
  data = json.load(f)
for i in data:
  cur.execute(f'INSERT INTO big(alphabet, kana) values("{i}", "{data[i]}")')

conn.commit()

cur.close()
conn.close()