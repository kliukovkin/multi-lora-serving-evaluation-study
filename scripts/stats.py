import sys,importlib,collections,statistics as st
m=importlib.import_module(sys.argv[1]); R=m.ROWS; V='vLLM'
o={}
o['N']=len(R)
o['peer']=dict(collections.Counter(r['peer'] for r in R))
o['year']=dict(sorted(collections.Counter(r['year'] for r in R).items()))
for s in 'FSRXNCKL': o['stage_'+s]=sum(s in r['stages'] for r in R)
o['compat']=dict(collections.Counter(r['compat'] for r in R))
o['exact']=dict(collections.Counter(r['exact'] for r in R))
o['base']=dict(collections.Counter(r['base'] for r in R))
o['built']=dict(collections.Counter(r['built'] for r in R))
vs=lambda r: r['built'] in('vLLM','SGLang')
o['vs_by_year']={y:(sum(vs(r) for r in R if r['year']==y),sum(r['year']==y for r in R)) for y in (2024,2025,2026)}
B=[r for r in R if r['bl']]
o['with_bl']=len(B)
c=collections.Counter()
for r in B:
    for k in r['bl']: c[k]+=1
o['bl_counts']=c.most_common()
o['ver']=(sum(r['ver'] for r in B),len(B))
PR=lambda r: r['peer'] in ('conf','journal')
o['peer_reviewed']=sum(PR(r) for r in R); o['other']=sum(not PR(r) for r in R)
o['ver_conf']=(sum(r['ver'] for r in B if PR(r)),sum(PR(r) for r in B))
o['ver_other']=(sum(r['ver'] for r in B if not PR(r)),sum(not PR(r) for r in B))
vc=collections.Counter(); 
for r in R:
    if V in r['bl']:
        for x in r['bl'][V].split('+'): vc[x]+=1
o['vllm_papers']=sum(V in r['bl'] for r in R); o['vllm_cfg']=dict(vc); o['vllm_cfg_sum']=sum(vc.values())
o['vllm_two']=[r['name'] for r in R if V in r['bl'] and '+' in r['bl'][V]]
o['only_slora']=[r['name'] for r in R if list(r['bl'])==['S-LoRA']]
M=[r for r in R if r['main']]
o['main_n']=len(M); o['main_med']=st.median(r['main'] for r in M)
o['main_med_conf']=(st.median(r['main'] for r in M if PR(r)),sum(PR(r) for r in M))
o['main_med_other']=(st.median(r['main'] for r in M if not PR(r)),sum(not PR(r) for r in M))
BND=getattr(m,'BOUNDARY',[])
o['boundary']=(len(BND),[b for b in BND if b not in [r['name'] for r in R]])
MB=[r for r in M if r['name'] not in BND]
o['main_med_nobnd']=(st.median(r['main'] for r in MB),len(MB))
o['main_le32']=sum(r['main']<=32 for r in M); o['main_ge1000']=sum(r['main']>=1000 for r in M)
o['main_le8']=sum(r['main']<=8 for r in M); o['main_ge100']=sum(r['main']>=100 for r in M)
X=[r for r in R if r['mx']]
o['mx_n']=len(X); o['mx_ge1000']=[r['name'] for r in X if r['mx']>=1000]; o['mx_med']=st.median(r['mx'] for r in X)
o['real']=dict(collections.Counter(r['real'] for r in R))
w=collections.Counter()
for r in R:
    for x in r['ws']: w[x]+=1
o['ws']=dict(w); o['ws_none']=sum(not r['ws'] for r in R)
o['syn_any']=sum('syn' in r['ws'] for r in R); o['syn_only']=sum(r['ws']==['syn'] for r in R)
o['inspected']=sum(r['code'] in ('repo','artifact') for r in R); o['nocode']=sum(r['code']=='' for r in R)
o['code']=dict(collections.Counter(r['code'] for r in R))
o['arch']=[r['name'] for r in R if r['arch']]
o['push_known']=sum(1 for r in R if r['push']); 
o['push_recent']=[r['name'] for r in R if r['push'] and r['push']>='2025-11' and r['code'] in('repo','artifact')]
o['table3_rows']=sum(1 for r in R if r['bl'] or r['ws'])
o['peer_by_year']={y:sum(PR(r) for r in R if r['year']==y) for y in (2024,2025,2026)}
for k,v in o.items(): print(k,':',v)
