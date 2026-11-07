/* ByteForge .bfng v1 deterministic runtime, C11, no dependencies. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAX_VOCAB 20000
#define MAX_EDGES 200000
#define MAX_ORDER 8
#define MAX_LINE 65536
typedef struct { char *s; } Tok;
typedef struct { int ctx[MAX_ORDER], next; unsigned count; } Edge;
static Tok vocab[MAX_VOCAB]; static Edge edge[MAX_EDGES]; static int order,vn,bos,en;
static void die(const char*s){fprintf(stderr,"byteforge: %s\n",s);exit(1);}
static char *field(char **p){char*s=*p,*t=strchr(s,'\t');if(t){*t=0;*p=t+1;}else *p=s+strlen(s);return s;}
static int number(char*s){char*e;long n=strtol(s,&e,10);if(!*s||*e||n<0||n>2147483647)die("bad integer");return (int)n;}
static char *unhex(char*s){size_t n=strlen(s);if(n%2)die("bad hex");char*r=calloc(n/2+1,1);if(!r)die("out of memory");for(size_t i=0;i<n;i+=2){unsigned x;if(sscanf(s+i,"%2x",&x)!=1)die("bad hex");r[i/2]=(char)x;}return r;}
static void load(const char*path){FILE*f=fopen(path,"r");if(!f)die("cannot open model");char line[MAX_LINE];if(!fgets(line,sizeof line,f))die("empty model");line[strcspn(line,"\r\n")]=0;char*p=line;if(strcmp(field(&p),"BYTEFORGE_NGRAM_V1"))die("bad header");order=number(field(&p));vn=number(field(&p));bos=number(field(&p));if(order<1||order>MAX_ORDER||vn<1||vn>MAX_VOCAB||bos!=vn)die("invalid header");while(fgets(line,sizeof line,f)){line[strcspn(line,"\r\n")]=0;p=line;char*k=field(&p);if(!strcmp(k,"v")){int id=number(field(&p));if(id>=vn||vocab[id].s)die("bad vocabulary id");vocab[id].s=unhex(field(&p));}else if(!strcmp(k,"n")){if(en>=MAX_EDGES)die("too many transitions");Edge*x=&edge[en++];for(int i=0;i<order;i++){x->ctx[i]=number(field(&p));if(x->ctx[i]>bos)die("bad context");}x->next=number(field(&p));x->count=(unsigned)number(field(&p));if(x->next>=vn||!x->count)die("bad transition");}else if(*k)die("unknown record");}fclose(f);for(int i=0;i<vn;i++)if(!vocab[i].s)die("missing token");}
int main(int argc,char**argv){if(argc<2||argc>3)die("usage: byteforge model.bfng [tokens]");load(argv[1]);int steps=argc==3?number(argv[2]):20;if(steps>10000)die("too many tokens");int ctx[MAX_ORDER];for(int i=0;i<order;i++)ctx[i]=bos;for(int k=0;k<steps;k++){int b=-1;for(int i=0;i<en;i++){int same=1;for(int j=0;j<order;j++)if(edge[i].ctx[j]!=ctx[j]){same=0;break;}if(same&&(b<0||edge[i].count>edge[b].count||(edge[i].count==edge[b].count&&edge[i].next<edge[b].next)))b=i;}if(b<0)break;if(k)putchar(' ');fputs(vocab[edge[b].next].s,stdout);memmove(ctx,ctx+1,(order-1)*sizeof(int));ctx[order-1]=edge[b].next;}putchar('\n');return 0;}
