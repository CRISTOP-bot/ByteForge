#include <assert.h>
#include <stddef.h>
#include <stdint.h>
extern size_t bf_choose(const uint32_t *,const uint64_t *,size_t);
int main(void){uint32_t ids[]={8,2,4};uint64_t c[]={5,9,9};assert(bf_choose(ids,c,3)==1);assert(bf_choose(ids,c,0)==(size_t)-1);uint64_t d[]={10,10,1};assert(bf_choose(ids,d,3)==1);return 0;}
