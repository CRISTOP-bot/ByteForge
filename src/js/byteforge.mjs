#!/usr/bin/env node
// ByteForge .bfng v1 runtime; Node.js 18+ standard library only.
import fs from 'node:fs';
function fail(s){console.error(`byteforge: ${s}`);process.exit(1)}
const [file, rawSteps='20', ...extra]=process.argv.slice(2);
if(!file||extra.length) fail('usage: node byteforge.mjs model.bfng [token-count]');
const lines=fs.readFileSync(file,'ascii').split(/\r?\n/).filter(Boolean);
const h=lines.shift().split('\t');
if(h.length!==4||h[0]!=='BYTEFORGE_NGRAM_V1') fail('bad model header');
const order=Number(h[1]), vn=Number(h[2]), bos=Number(h[3]);
if(!Number.isInteger(order)||order<1||order>8||!Number.isInteger(vn)||vn<1||vn>20000||bos!==vn) fail('invalid model header');
const vocab=Array(vn), edges=[];
for(const line of lines){const p=line.split('\t');
 if(p[0]==='v'&&p.length===3){const id=Number(p[1]);if(!Number.isInteger(id)||id<0||id>=vn||!/^(?:[0-9a-fA-F]{2})*$/.test(p[2]))fail('bad vocabulary');vocab[id]=Buffer.from(p[2],'hex').toString('utf8');}
 else if(p[0]==='n'&&p.length===order+3){const ctx=p.slice(1,order+1).map(Number),next=Number(p[order+1]),count=Number(p[order+2]);if(ctx.some(x=>!Number.isInteger(x)||x<0||x>bos)||!Number.isInteger(next)||next<0||next>=vn||!Number.isSafeInteger(count)||count<=0)fail('bad transition');edges.push({ctx,next,count});}
 else fail('unknown model record');}
if(vocab.some(x=>x===undefined)) fail('missing vocabulary token');
const steps=Number(rawSteps);if(!Number.isInteger(steps)||steps<0||steps>10000)fail('bad token count');
let ctx=Array(order).fill(bos), out=[];
for(let k=0;k<steps;k++){let best=null;for(const e of edges)if(e.ctx.every((x,i)=>x===ctx[i])&&(!best||e.count>best.count||(e.count===best.count&&e.next<best.next)))best=e;if(!best)break;if(vocab[best.next]==='__BYTEFORGE_EOS__')break;out.push(vocab[best.next]);ctx=[...ctx.slice(1),best.next];}
console.log(out.join(' '));
