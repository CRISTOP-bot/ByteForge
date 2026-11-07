#!/usr/bin/env python3
"""Deterministic reference generator for ByteForge .bfng v1."""
import argparse
import re
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
EOS='__BYTEFORGE_EOS__'
TOKEN_RE=re.compile(r"[\w]+|[^\w\s]",re.UNICODE)
def tokenize(text):
 return TOKEN_RE.findall(text)
def detokenize(tokens):
 text=' '.join(tokens)
 text=re.sub(r'\s+([,.;:!?%)\]\}])',r'\1',text)
 text=re.sub(r'([(¿¡\[])\s+',r'\1',text)
 return text.strip()
def load(path):
 with open(path,encoding='ascii') as f:
  h=f.readline().rstrip('\n').split('\t')
  if len(h)!=4 or h[0]!='BYTEFORGE_NGRAM_V1': raise ValueError('bad model header')
  order,vn,bos=map(int,h[1:]);v={};edges=defaultdict(list)
  for line in f:
   p=line.rstrip('\n').split('\t')
   if len(p)==3 and p[0]=='v':
    i=int(p[1]); token=bytes.fromhex(p[2]).decode('utf8')
    if i<0 or i>=vn or i in v: raise ValueError('invalid vocabulary id')
    v[i]=token
   elif len(p)==order+3 and p[0]=='n':
    a=list(map(int,p[1:]));ctx=tuple(a[:order]);n,count=a[order:]
    if count<=0 or n<0 or n>=vn or any(x<0 or x>bos for x in ctx): raise ValueError('invalid transition')
    edges[ctx].append((n,count))
   else: raise ValueError('bad model record')
  if order<1 or len(v)!=vn or bos!=vn or any(i not in v for i in range(vn)): raise ValueError('invalid header/vocabulary')
  return order,bos,v,edges
def generate(model,length=30,prompt=''):
 order,bos,v,edges=model;ctx=(bos,)*order;out=[]
 prompt_tokens=tokenize(prompt);ids={token:i for i,token in v.items() if token!=EOS}
 for width in range(min(order,len(prompt_tokens)),0,-1):
  suffix=prompt_tokens[-width:]
  if all(token in ids for token in suffix):
   candidate=(bos,)*(order-width)+tuple(ids[token] for token in suffix)
   if candidate in edges: ctx=candidate;break
 for _ in range(length):
  opts=edges.get(ctx,[])
  if not opts:break
  nxt,_=min(opts,key=lambda x:(-x[1],x[0]));token=v[nxt]
  if token==EOS:break
  out.append(token);ctx=ctx[1:]+(nxt,)
 return detokenize(prompt_tokens+out)
def interactive(model,length):
 print('ByteForge (escribe /salir para terminar)')
 while True:
  try: prompt=input('Tú> ').strip()
  except EOFError: break
  if prompt.lower() in {'/salir','/exit','/quit'}: break
  if not prompt: continue
  print('ByteForge>',generate(model,length,prompt))
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--model',type=Path,default=ROOT/'model.bfng');p.add_argument('--length',type=int,default=30);p.add_argument('--prompt',default='');p.add_argument('--interactive',action='store_true',help='iniciar una sesión de terminal');a=p.parse_args()
 if not 0<=a.length<=10000:p.error('length must be 0..10000')
 model=load(a.model)
 if a.interactive: interactive(model,a.length)
 else: print(generate(model,a.length,a.prompt))
if __name__=='__main__':main()
