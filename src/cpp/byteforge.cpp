// ByteForge .bfng v1 reader/generator, C++17 standard library only.
#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
struct Edge{std::vector<int> ctx;int next,count;};
[[noreturn]] static void die(const char*s){std::cerr<<"byteforge: "<<s<<'\n';std::exit(1);}
static std::vector<std::string> split(const std::string&s){std::vector<std::string>v;std::stringstream ss(s);std::string x;while(std::getline(ss,x,'\t'))v.push_back(x);return v;}
static int num(const std::string&s){try{size_t n;int x=std::stoi(s,&n);if(n!=s.size()||x<0)die("bad integer");return x;}catch(...){die("bad integer");}}
int main(int argc,char**argv){if(argc<2||argc>3)die("usage: byteforge model.bfng [token-count]");std::ifstream in(argv[1]);if(!in)die("cannot open model");std::string line;if(!std::getline(in,line))die("empty model");auto h=split(line);if(h.size()!=4||h[0]!="BYTEFORGE_NGRAM_V1")die("bad header");int order=num(h[1]),vn=num(h[2]),bos=num(h[3]);if(order<1||order>8||vn<1||vn>20000||bos!=vn)die("invalid header");std::vector<std::string>v(vn);std::vector<bool>seen(vn);std::vector<Edge>edges;while(std::getline(in,line)){auto p=split(line);if(p.size()==3&&p[0]=="v"){int id=num(p[1]);if(id>=vn||seen[id]||p[2].size()%2)die("bad vocabulary");std::string token;for(size_t i=0;i<p[2].size();i+=2){try{token.push_back(static_cast<char>(std::stoi(p[2].substr(i,2),nullptr,16)));}catch(...){die("bad hex");}}v[id]=token;seen[id]=true;}else if(p.size()==static_cast<size_t>(order+3)&&p[0]=="n"){Edge e;for(int i=0;i<order;i++){int x=num(p[i+1]);if(x>bos)die("bad context");e.ctx.push_back(x);}e.next=num(p[order+1]);e.count=num(p[order+2]);if(e.next>=vn||!e.count)die("bad transition");edges.push_back(e);}else die("unknown record");}if(std::find(seen.begin(),seen.end(),false)!=seen.end())die("missing vocabulary");int steps=argc==3?num(argv[2]):20;if(steps>10000)die("too many tokens");std::vector<int>ctx(order,bos);bool first=true;for(int k=0;k<steps;k++){const Edge*best=nullptr;for(const auto&e:edges)if(e.ctx==ctx&&(!best||e.count>best->count||(e.count==best->count&&e.next<best->next)))best=&e;if(!best)break;if(v[best->next]=="__BYTEFORGE_EOS__")break;if(!first)std::cout<<' ';first=false;std::cout<<v[best->next];std::rotate(ctx.begin(),ctx.begin()+1,ctx.end());ctx.back()=best->next;}std::cout<<'\n';}
