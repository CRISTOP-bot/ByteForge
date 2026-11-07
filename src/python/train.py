#!/usr/bin/env python3
"""Train ByteForge's portable token n-gram model from scratch."""
import argparse
import re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
TOKEN_RE=re.compile(r"[\w]+|[^\w\s]",re.UNICODE)
EOS="__BYTEFORGE_EOS__"
def train(text,order=2):
 if order<1 or order>8: raise ValueError('order must be between 1 and 8')
 sentences=[]
 for line in text.splitlines():
  if not line.strip() or line.lstrip().startswith('#'): continue
  tokens=TOKEN_RE.findall(line)
  if tokens:
   if EOS in tokens: raise ValueError('corpus contains reserved EOS token')
   sentences.append(tokens+[EOS])
 if not sentences: raise ValueError('training corpus is empty')
 vocab=sorted({token for sentence in sentences for token in sentence}); ids={t:i for i,t in enumerate(vocab)}; bos=len(vocab); transitions=Counter()
 for sentence in sentences:
  history=[bos]*order
  for token in sentence:
   nxt=ids[token]; transitions[tuple(history)+(nxt,)]+=1; history=history[1:]+[nxt]
 lines=[f'BYTEFORGE_NGRAM_V1\t{order}\t{len(vocab)}\t{bos}']
 lines += [f'v\t{i}\t{t.encode("utf-8").hex()}' for i,t in enumerate(vocab)]
 lines += ['n\t'+'\t'.join(map(str,key))+f'\t{count}' for key,count in sorted(transitions.items())]
 return '\n'.join(lines)+'\n'
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--corpus',type=Path,default=ROOT/'data/corpus.txt');p.add_argument('--output',type=Path,default=ROOT/'model.bfng');p.add_argument('--order',type=int,default=2);a=p.parse_args();m=train(a.corpus.read_text(encoding='utf-8'),a.order);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(m,encoding='ascii');print(f"ByteForge entrenado: {sum(x.split(chr(9),1)[0]=='n' for x in m.splitlines())} transiciones -> {a.output}")
if __name__=='__main__':main()
