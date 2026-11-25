import json,re,sys
sys.path.insert(0,'.')
from curated import ROWS
meta=json.load(open('../meta.json')); meta.update(json.load(open('meta_a3.json')))
k=json.load(open('keys.json')); key={int(a):b for a,b in k['key'].items()}; O=k['O']
bib=open('refs.bib').read()
def esc(s): return s.replace('\\','').replace('&','\\&').replace('%','\\%').replace('_','\\_').replace('#','\\#').replace('$','\\$')
def addarx(i,hp=None):
    global bib
    kk='ax'+i.replace('.','')
    if '@misc{'+kk+',' in bib: return kk
    m=meta[i]; au=' and '.join(a.strip() for a in m['authors'][:8])+(' and others' if len(m['authors'])>8 else '')
    bib+='\n\n@misc{%s,\n author={%s},\n title={{%s}},\n howpublished={%s},\n year={%s}\n}'%(kk,esc(au),esc(m['title']),(hp+'. ' if hp else 'arXiv preprint ')+'arXiv:'+i,m['published'][:4])
    return kk
key[1015]=O['bitdelta']; key[1005]=O['layerloom']
key[1017]=addarx('2406.08903','NeurIPS 2024'); key[1018]=addarx('2406.09041'); key[1020]=addarx('2603.15965')
for kk,a,t,v,y in [('rock','Wu and others','Serving Multimodal Models in Cloud with Heterogeneous-Aware Resource Orchestration for Thousands of LoRA Adapters','IEEE CLUSTER','2025'),('dop','Zhou and others','Dynamic Operator Optimization for Efficient Multi-Tenant LoRA Model Serving','AAAI','2025'),('cannikin','Zhu and others','Cannikin: No Lagger of SLO in Concurrent Multiple LoRA LLM Serving','IEEE Transactions on Parallel and Distributed Systems','2025')]:
    if '@misc{'+kk+',' not in bib: bib+='\n\n@misc{%s,\n author={%s},\n title={{%s}},\n howpublished={%s},\n year={%s}\n}'%(kk,a,t,v,y)
key[1002]='rock'; key[1003]='dop'
# records added 24 Nov 2026 (no arXiv versions); titles not recorded for MixLoRA and DyMerge-LoRA, so the system name is used
for kk,a,t,v,y in [('mixlora','Chen and Yu and Fu and Hu and Yang','{MixLoRA}: An Efficient Multi-Tenant Framework for Concurrently Serving Diverse {LoRA} Models in Large Language Models','ICPP 2025, pp. 11--21. doi:10.1145/3754598.3754605','2025'),('dymergelora','Xu and Chen and Lao and Zhang and Zhu','{DyMerge-LoRA}: On-{GPU} Post-Merge Fusion for High-Throughput Multi-Tenant Composite {LoRA} Serving','KDD 2026, pp. 1728--1738. doi:10.1145/3770854.3780270. Artifact: doi:10.5281/zenodo.18058116','2026'),('climb','Zhang and Liang and Zuo and Wang','{CLIMB}: Taming the {LoRA} Residency Cliff in Multi-{LoRA} Serving','ICML 2026. OpenReview id 4bN7wxsIcL. Artifact: \\url{https://github.com/maxsignalll/CLIMB_artifact}','2026')]:
    if '@misc{'+kk+',' not in bib: bib+='\n\n@misc{%s,\n author={%s},\n title={{%s}},\n howpublished={%s},\n year={%s}\n}'%(kk,a,t,v,y)
key[2004]='mixlora'; key[2008]='dymergelora'; key[2007]='climb'
O['peraxis']=addarx('2512.19720','NeurIPS 2025 CCFM Workshop')
# venue fixes in bib howpublished
def fixhp(kk,new):
    global bib
    bib=re.sub(r'(@misc\{'+kk+r',.*?howpublished=\{)[^}]*(\})',lambda m:m.group(1)+new+m.group(2),bib,flags=re.S)
fixhp(key[41],'ACM SoCC 2025. arXiv:2507.03220'); fixhp(key[71],'CVPR 2026 Mobile AI Workshop. arXiv:2603.29535')
fixhp(key[57],'NeurIPS 2025. arXiv:2504.12397'); fixhp(key[55],'AAAI 2026. arXiv:2603.11873'); fixhp(key[58],'ICLR 2026. arXiv:2603.13281')
fixhp(key[54],'NeurIPS 2025. arXiv:2510.23346'); fixhp(key[1020],'ICML 2026. arXiv:2603.15965'); fixhp(key[61],'Transactions on Machine Learning Research, 2026. arXiv:2512.17910')
fixhp(key[43],'Future Generation Computer Systems 186:108735, 2026. doi:10.1016/j.future.2026.108735. arXiv:2602.24044'); fixhp(key[67],'Proc. ICCSMT 2025, ACM. arXiv:2512.20210')
def setentry(kk,au,ti,hp,y):
    global bib
    e='@misc{%s,\n author={%s},\n title={{%s}},\n howpublished={%s},\n year={%s}\n}'%(kk,au,ti,hp,y)
    if '@misc{'+kk+',' in bib: bib=re.sub(r'@misc\{'+kk+r',.*?\n\}',lambda m:e,bib,count=1,flags=re.S)
    else: bib+='\n\n'+e
for a in [('dlora','Bingyang Wu and Ruidong Zhu and Zili Zhang and Peng Sun and Xuanzhe Liu and Xin Jin','{dLoRA}: Dynamically Orchestrating Requests and Adapters for {LoRA} {LLM} Serving','18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24), pp. 911--927','2024'),
  ('pets','Zhe Zhou and Xuechao Wei and Jiejing Zhang and Guangyu Sun','{PetS}: A Unified Framework for Parameter-Efficient Transformers Serving','2022 USENIX Annual Technical Conference (USENIX ATC 22), pp. 489--504','2022'),
  ('mlora26','Shaolong Li and Xiang Yang and Qi Qi and Haifeng Sun and Zirui Zhuang and Bo He and Wanyi Ning and Jingyu Wang','{M-LoRA}: Efficient Serving for Concurrent {LoRA} Adapters with Memory-Aware Speculative Scheduler on Single {GPU}','Proc. IJCAI 2026, pp. 4509--4517. doi:10.24963/ijcai.2026/502','2026'),
  ('rock','Shuaipeng Wu and Yanying Lin and Shijie Peng and Wenyan Chen and Chong Ma and Min Shen and Le Chen and Chengzhong Xu and Kejiang Ye','{Rock}: Serving Multimodal Models in Cloud with Heterogeneous-Aware Resource Orchestration for Thousands of {LoRA} Adapters','2025 IEEE International Conference on Cluster Computing (CLUSTER), pp. 1--13. doi:10.1109/CLUSTER59342.2025.11186463','2025'),
  ('dop','Changhai Zhou and Yuhua Zhou and Shiyang Zhang and Yibin Wang and Zekai Liu','Dynamic Operator Optimization for Efficient Multi-Tenant {LoRA} Model Serving','Proc. AAAI Conference on Artificial Intelligence 39(21), pp. 22910--22918. doi:10.1609/aaai.v39i21.34453','2025'),
  ('cannikin','Ruidong Zhu and Ziyue Jiang and Zhi Zhang and Xin Liu and Xuanzhe Liu and Xin Jin','{Cannikin}: No Lagger of {SLO} in Concurrent Multiple {LoRA} {LLM} Serving','IEEE Transactions on Parallel and Distributed Systems 36(9), pp. 1972--1984. doi:10.1109/TPDS.2025.3590014','2025'),
  ('agrawal25','Amey Agrawal and Nitin Kedia and Anmol Agarwal and Jayashree Mohan and Nipun Kwatra and Souvik Kundu and Ramachandran Ramjee and Alexey Tumanov','On Evaluating Performance of {LLM} Inference Serving Systems','arXiv preprint arXiv:2507.09019','2025'),
  ('anwar26','Muhammad Faizan Anwar and Sina Keshvadi','A Controlled Experimental Evaluation of Configuration and Cache Architecture in {LLM} Serving Engines','arXiv preprint arXiv:2611.05991','2026'),
  ('pape26','David Pape and Jonathan Evertz and Lea Sch{\\"o}nherr','The Silent Hyperparameter: Quantifying the Impact of Inference Backends on {LLM} Reproducibility','arXiv preprint arXiv:2605.19537','2026')]:
    setentry(*a)
O['agrawal']='agrawal25'; O['anwar']='anwar26'; O['pape']='pape26'; O['loraswitch']='ax240517741'
fixhp(key[42],'NeurIPS 2025 ML for Systems Workshop. arXiv:2508.08343'); fixhp(key[27],'ATC 2026. arXiv:2604.07173'); fixhp(key[75],'NSDI 2026. arXiv:2402.18789')
open('refs.bib','w').write(bib)
json.dump({'key':{str(a):b for a,b in key.items()},'O':O},open('keys.json','w'))
order='FSRXNCKL'
codesym={'repo':'\\checkmark','artifact':'\\checkmark','link':'($\\circ$)','fork':'($\\circ$)','PR':'($\\circ$)','':''}
R=sorted(ROWS,key=lambda r:(r['year'],r['name'].lower()))
t2=[]
for r in R:
    if r['num'] not in key: print('NOKEY',r['name'])
    marks=' & '.join('$\\bullet$' if c in r['stages'] else '' for c in order)
    cd=codesym[r['code']]+('$^{a}$' if r['arch'] else '')
    ck=key[r['num']]+(',ax240517741' if r['name']=='AdaFuse' else '')
    t2.append(f"{r['name']}~\\cite{{{ck}}} & {str(r['year'])[2:]} & {r['venue'].replace('preprint','--')} & {marks} & {r['compat'].replace('-','--')} & {r['exact'].replace('~','$\\approx$').replace('-','--')} & {r['base']} & {cd} \\\\")
open('t2.tex','w').write('\n'.join(t2))
wsn={'syn':'syn.','lmsys':'LMSYS','azfn':'AzFn','llm':'LLM tr.','prod':'prod.$^\\dagger$','prodre':'prod.$^\\ddagger$','prodna':'prod.$^\\S$'}
cfg={'native':'n','merged':'m','backbone':'b','swap':'s','split':'p','merged+native':'m,n','swap+native':'s,n','merged+backbone':'m,b'}
t3=[]
for r in R:
    if not r['bl'] and not r['ws']: continue
    bl=', '.join((b+'$^{'+cfg[c]+'}$' if b=='vLLM' else b) for b,c in r['bl'].items()) or '--'
    t3.append(f"{r['name']} & {r['built']} & {bl} & {'\\checkmark' if r['ver'] else ''} & {r['main'] or 'n/s'} & {r['mx'] or 'n/s'} & {r['real']} & {', '.join(wsn[w] for w in r['ws']) or '--'} \\\\")
open('t3.tex','w').write('\n'.join(t3))
print(len(t2),len(t3))
