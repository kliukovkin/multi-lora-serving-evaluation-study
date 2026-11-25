# Papers per vLLM-baseline configuration, from curated.py. Writes fig1.pdf.
import collections, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from curated import ROWS
lab={'native':'Native multi-adapter path','merged':'Merged weights','backbone':'Backbone only',
     'split':'Split with fine-tuning framework','swap':'Own swap baseline'}
c=collections.Counter()
for r in ROWS:
    if 'vLLM' in r['bl']:
        for x in r['bl']['vLLM'].split('+'): c[x]+=1
order=['native','merged','backbone','split','swap']
vals=[c[k] for k in order]
plt.rcParams.update({'font.family':'serif','font.size':8})
fig,ax=plt.subplots(figsize=(3.3,1.55))
y=range(len(order))[::-1]
ax.barh(list(y),vals,color='#4a6f8a',height=0.6)
for yi,v in zip(y,vals): ax.text(v+0.25,yi,str(v),va='center',fontsize=8)
ax.set_yticks(list(y)); ax.set_yticklabels([lab[k] for k in order])
ax.set_xlabel('Papers'); ax.set_xlim(0,max(vals)+2.5)
for s in ('top','right'): ax.spines[s].set_visible(False)
fig.tight_layout(pad=0.2); fig.savefig('fig1.pdf')
print(dict(zip(order,vals)))
