import json, collections, statistics as st, sys
rows=[json.loads(l) for l in open(sys.argv[1])]
print("total rows", len(rows))
print("cfg_status:", collections.Counter(r["cfg_status"] for r in rows).most_common())
ok=[r for r in rows if r["cfg_status"]==200 and isinstance(r.get("r"),int)]
print("with parsed config:", len(ok))
print("peft_type:", collections.Counter(r.get("peft_type") for r in ok).most_common(6))
lora=[r for r in ok if (r.get("peft_type") or "").upper()=="LORA"]
ATT={"q_proj","k_proj","v_proj","o_proj"}; MLP={"gate_proj","up_proj","down_proj"}
def tclass(t):
    if isinstance(t,str): return "regex/str"
    if not t: return "none"
    s=set(t)
    if s==ATT|MLP: return "all 7 linear"
    if s=={"q_proj","v_proj"}: return "q,v"
    if s==ATT: return "attention (q,k,v,o)"
    if s<=ATT: return "attention subset"
    if s<=ATT|MLP: return "attn+mlp subset"
    return "other"
def pct(c,n): return ", ".join(f"{k}: {v} ({100*v/n:.1f}%)" for k,v in c)
for base in ["ALL"]+sorted(set(r["base"] for r in lora)):
    L=[r for r in lora if base=="ALL" or r["base"]==base]; n=len(L)
    if not n: continue
    print(f"\n== {base}: {n} LoRA adapters")
    rc=collections.Counter(r["r"] for r in L)
    print(" rank:", pct(rc.most_common(8),n))
    rs=sorted(r["r"] for r in L); print("  median %d, p90 %d, p99 %d, max %d; share r<=16: %.1f%%, r>=64: %.1f%%, r>128: %.1f%%"%(rs[n//2],rs[int(.9*n)],rs[int(.99*n)],rs[-1],100*sum(x<=16 for x in rs)/n,100*sum(x>=64 for x in rs)/n,100*sum(x>128 for x in rs)/n))
    print(" targets:", pct(collections.Counter(tclass(r.get("target_modules")) for r in L).most_common(7),n))
    print("  DoRA: %.1f%%, rsLoRA: %.1f%%, modules_to_save set: %.1f%%, rank_pattern set: %.1f%%"%tuple(100*sum(bool(r.get(k)) for r in L)/n for k in ("use_dora","use_rslora","modules_to_save","rank_pattern")))
    sz=sorted(r["adapter_bytes"] for r in L if r.get("adapter_bytes"))
    if sz: print("  adapter file MiB: n=%d median %.0f, p90 %.0f, p99 %.0f, max %.0f"%(len(sz),sz[len(sz)//2]/2**20,sz[int(.9*len(sz))]/2**20,sz[int(.99*len(sz))]/2**20,sz[-1]/2**20))
    dl=sorted((r.get("downloads") or 0 for r in L),reverse=True); tot=sum(dl) or 1
    print("  downloads: top1%% of adapters = %.1f%% of downloads, top10%% = %.1f%%; zero-download share %.1f%%"%(100*sum(dl[:max(1,n//100)])/tot,100*sum(dl[:max(1,n//10)])/tot,100*sum(d==0 for d in dl)/n))
