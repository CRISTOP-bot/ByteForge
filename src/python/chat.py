#!/usr/bin/env python3
"""Deterministic reference generator for ByteForge .bfng v1."""
import argparse
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def load(path):
 with open(path,encoding='ascii') as f:
  h=f.readline().rstrip('\n').split('\t')
  if len(h)!=4 or h[0]!='BYTEFORGE_NGRAM_V1': raise ValueError('bad model header')
  order,vn,bos=map(int,h[1:]);v={};edges=defaultdict(list)
  for line in f:
   p=line.rstrip('\n').split('\t')
   if len(p)==3 and p[0]=='v': v[int(p[1])]=bytes.fromhex(p[2]).decode('utf8')
   elif len(p)==order+3 and p[0]=='n':
    a=list(map(int,p[1:]));ctx=tuple(a[:order]);n,count=a[order:]
    if count<=0: raise ValueError('bad frequency')
    edges[ctx].append((n,count))
   else: raise ValueError('bad model record')
  if order<1 or len(v)!=vn or bos!=vn or any(i not in v for i in range(vn)): raise ValueError('invalid header/vocabulary')
  return order,bos,v,edges
def generate(model,length=30,prompt=''):
 order,bos,v,edges=model;ctx=(bos,)*order;out=[]
 prompt_tokens=prompt.split()
 ids={token:i for i,token in v.items()}
 # Seed from the longest known suffix of the prompt; unknown words do not crash generation.
 for width in range(min(order,len(prompt_tokens)),0,-1):
  suffix=prompt_tokens[-width:]
  if all(token in ids for token in suffix):
   candidate=(bos,)*(order-width)+tuple(ids[token] for token in suffix)
   if candidate in edges:
    ctx=candidate
    break
 for _ in range(length):
  opts=edges.get(ctx,[])
  if not opts:break
  nxt,_=min(opts,key=lambda x:(-x[1],x[0]));out.append(v[nxt]);ctx=ctx[1:]+(nxt,)
 return ' '.join(prompt_tokens+out)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--model',type=Path,default=ROOT/'model.bfng');p.add_argument('--length',type=int,default=30);p.add_argument('--prompt',default='');a=p.parse_args()
 if not 0<=a.length<=10000:p.error('length must be 0..10000')
 print(generate(load(a.model),a.length,a.prompt))
if __name__=='__main__':main()
