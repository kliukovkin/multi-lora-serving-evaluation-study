# Compare corpus-derived numbers in main.tex with values recomputed from curated.py.
import re,collections,statistics as st,subprocess,json
from curated import ROWS as R, BOUNDARY as BND
t=open('main.tex').read()
V='vLLM'; PR=lambda r:r['peer'] in('conf','journal')
N=len(R); B=[r for r in R if r['bl']]; M=[r for r in R if r['main']]; X=[r for r in R if r['mx']]
vc=collections.Counter(x for r in R if V in r['bl'] for x in r['bl'][V].split('+'))
blc=collections.Counter(k for r in B for k in r['bl'])
cnt=lambda f,v: sum(r[f]==v for r in R)
stage=lambda s: sum(s in r['stages'] for r in R)
W=lambda n:['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen'][n] if n<16 else None
def words(n):
    tens={2:'twenty',3:'thirty',4:'forty',5:'fifty',6:'sixty'}
    return W(n) or (tens[n//10]+('-'+W(n%10) if n%10 else ''))
checks=[
 ('N in title',f'Artifacts in {N} Multi-LoRA'),('N abstract',f'We code {N} systems'),('N intro',f'corpus holds {N} systems'),
 ('2026 count',f"{sum(r['year']==2026 for r in R)} of them with a 2026"),
 ('corpus',f"\\textbf{{{N} systems}}"),('peer',f"{sum(PR(r) for r in R)} peer-reviewed ({cnt('peer','conf')} at conferences and {cnt('peer','journal')} in journals), {cnt('peer','workshop')} at workshops and {cnt('peer','preprint')} available"),
 ('boundary',f"{words(len(BND)).capitalize()} systems are boundary cases"),
 ('code',f"For {sum(r['code'] in('repo','artifact') for r in R)} of the {N} systems"),('nocode',f"remaining {cnt('code','')} we found"),
 ('sens code',f"raises {sum(r['code'] in('repo','artifact') for r in R)} of {N} to {sum(r['code'] in('repo','artifact','link') for r in R)}"),
 ('sens vllm',f"from {sum(V in r['bl'] for r in R)} papers to {sum(V in r['bl'] for r in R)+2}"),
 ('sens med',f"is {st.median(r['main'] for r in M):g} over all {len(M)} systems"),
 ('sens nobnd',f"{st.median(r['main'] for r in M if r['name'] not in BND):g} over the {sum(r['name'] not in BND for r in M)} that remain"),
 ('sens pr',f"{st.median(r['main'] for r in M if PR(r)):g} among the {sum(PR(r) for r in M)} peer-reviewed"),
 ('sens oth',f"{st.median(r['main'] for r in M if not PR(r)):g} among the {sum(not PR(r) for r in M)} preprints"),
 ('vllm built',f"{words(cnt('built','vLLM')).capitalize()} of the {N} prototypes"),
 ('substrate',f"{cnt('built','SGLang')} on SGLang".replace('3','three')),
 ('custom',f"{cnt('built','custom')} on custom"),('ns',f"{words(cnt('built','n/s'))} do not state it and {words(cnt('built','other'))} uses another"),
]
for y,w in ((2024,'among systems dated 2024'),(2025,'for 2025'),(2026,'for 2026')):
    ry=[r for r in R if r['year']==y]; checks.append(('vs'+str(y),f"{sum(r['built'] in(V,'SGLang') for r in ry)} of {len(ry)} {w}"))
checks+=[
 ('with bl',f"{words(len(B)).capitalize()} systems compare against at least one serving system; {N-len(B)} do not"),
 ('vllm bl',f"vLLM is a baseline in {blc[V]} of the {len(B)} and S-LoRA in {blc['S-LoRA']}"),
 ('others',f"HF PEFT follows with {blc['HF PEFT']}, dLoRA with {blc['dLoRA']}, Punica with {blc['Punica']} and SGLang with {blc['SGLang']}"),
 ('ver',f"{words(sum(r['ver'] for r in B)).capitalize()} of the {len(B)} state a version"),
 ('ver split',f"{words(sum(r['ver'] for r in B if PR(r)))} of the {sum(PR(r) for r in B)} peer-reviewed papers and {words(sum(r['ver'] for r in B if not PR(r)))} of the {sum(not PR(r) for r in B)} preprints"),
 ('vllm cfg',f"Among the {blc[V]} papers that compare against vLLM"),('cfg sum',f"counts sum to {sum(vc.values())}"),
 ('native',f"In {vc['native']} papers it is the engine's native"),('merged',f"In {vc['merged']} the adapter weights"),('bb',f"In {vc['backbone']} it is the backbone"),('split',f"In {vc['split']} co-serving"),
 ('abs cfg',f"(17 papers), adapter weights merged into the model ({vc['merged']}), the bare backbone ({vc['backbone']}), an inference engine beside a separate fine-tuning framework ({vc['split']}), and the authors' own model-swapping baseline ({vc['swap']})".replace('17',str(vc['native']))),
 ('fig cap',f"bars sum to {sum(vc.values())}"),
 ('scale',f"{words(len(M)).capitalize()} systems state the first: the median is {st.median(r['main'] for r in M):g}, {sum(r['main']<=32 for r in M)} use 32 or fewer, and {words(sum(r['main']>=1000 for r in M))} use 1{{,}}000"),
 ('scale2',f"The median is {st.median(r['main'] for r in M if r['name'] not in BND):g} without the boundary cases of Section~\\ref{{sec:method}}, {st.median(r['main'] for r in M if PR(r)):g} among peer-reviewed papers and {st.median(r['main'] for r in M if not PR(r)):g} among"),
 ('mx',f"{words(len(X)).capitalize()} state the second: the median is {st.median(r['mx'] for r in X):g} and {words(sum(r['mx']>=1000 for r in X))} reach"),
 ('abs med',f"among the {len(M)} systems that state it, the median main experiment uses {st.median(r['main'] for r in M):g} adapters; {words(sum(r['mx']>=1000 for r in X))} report"),
 ('abs code',f"for {sum(r['code'] in('repo','artifact') for r in R)} of {N} systems"),
 ('adapters',f"{cnt('real','real')} systems use trained or downloaded adapters, {cnt('real','syn')} synthetic weights only, {words(cnt('real','mixed'))} both, and {cnt('real','n/s')} do not say"),
 ('ws syn',f"{words(sum('syn' in r['ws'] for r in R)).capitalize()} systems generate arrivals"),('ws synonly',f"{sum(r['ws']==['syn'] for r in R)} of them in all"),
 ('azfn',f"{words(sum('azfn' in r['ws'] for r in R)).capitalize()} map functions"),('lmsys',f"and {words(sum('lmsys' in r['ws'] for r in R))} map the models"),
 ('llm',f"{words(sum('llm' in r['ws'] for r in R)).capitalize()} take lengths"),('prod',f"{words(sum(any(w.startswith('prod') for w in r['ws']) for r in R)+sum('mixed'==r['real'] and 0 for r in R)).capitalize()} papers use production"),
 ('ws none',f"{words(sum(not r['ws'] for r in R)).capitalize()} systems have no request workload"),
 ('t2cap',f"The {N} coded systems"),
 ('st F',f"{words(stage('F')).capitalize()} systems act here"),('st S',f"{words(stage('S')).capitalize()} make the choice"),('st R',f"{words(stage('R')).capitalize()} systems decide where"),
 ('st X',f"stage ({stage('X')} systems)"),('st N',f"On a node ({stage('N')} systems)"),('st C',f"only {words(stage('C'))} systems act"),('st K',f"{words(stage('K')).capitalize()} systems, all dated"),('st L',f"{words(stage('L')).capitalize()} systems place inference"),
 ('compat',f"Of {N} systems, {cnt('compat','D')} are drop-in, {cnt('compat','T')} require adapters trained in a special form, {cnt('compat','A')} change the base architecture or hardware, and for {cnt('compat','-')} co-serving"),
 ('exact',f"{words(cnt('exact','E')).capitalize()} systems are exact and {cnt('exact','~')} approximate ({cnt('exact','-')} not applicable)"),
 ('base',f"{words(cnt('base','LLM')).capitalize()} systems evaluate dense decoder LLMs; {words(cnt('base','MoE'))} target mixture-of-experts models, {words(cnt('base','Diff'))} diffusion models, {words(cnt('base','VLM'))} a vision-language model and {words(cnt('base','Enc'))} encoders"),
 ('gaps iv',f"{words(cnt('base','MoE'))}, {words(cnt('base','Diff'))} and {words(cnt('base','VLM'))} system respectively, {words(cnt('base','MoE')+cnt('base','Diff')+cnt('base','VLM'))} in total"),
 ('gaps sel',f"{words(stage('S'))} systems, although"),('gaps C',f"\\emph{{Cluster-level systems}}: {words(stage('C'))}"),('eng C',f"none of the {words(stage('C'))} reports"),
 ('concl',f"code for {sum(r['code'] in('repo','artifact') for r in R)} of {N} systems and found none for {cnt('code','')}"),
 ('reread','52 of the 62 papers'),
]
bad=0
for n,s in checks:
    ok=s in t
    if not ok: bad+=1
    print('OK ' if ok else 'BAD',n,'|',s)
# boundary list
m=re.search(r'with training \(([^)]*)\)',t); lst=[x.strip() for x in re.sub(r'~\\cite\{[^}]*\}','',m.group(1)).split(',')]
print('boundary list', 'OK' if sorted(lst)==sorted(BND) else 'BAD', len(lst))
# all systems cited: in t2 every row has \cite
t2=open('t2.tex').read().split('\n'); print('t2 rows',len(t2),'all cited',all('\\cite{' in x for x in t2))
print('stale numbers:',[w for w in ['63 ','Sixty-three',' 157 ','Fifty-two state','Forty-eight','Forty systems'] if w in t])
print('BAD',bad)
