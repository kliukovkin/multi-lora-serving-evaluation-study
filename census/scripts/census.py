#!/usr/bin/env python3
"""HF LoRA adapter census: list adapters per base model, fetch adapter_config.json + file sizes. Resumable."""
import json, sys, time, os, re, concurrent.futures as cf, urllib.request, urllib.error, urllib.parse
BASES = ["meta-llama/Llama-3.1-8B-Instruct","Qwen/Qwen3-8B","meta-llama/Llama-3.3-70B-Instruct",
         "Qwen/Qwen3-32B","Qwen/Qwen3-30B-A3B","mistralai/Mistral-7B-Instruct-v0.3","meta-llama/Llama-3.2-3B-Instruct"]
OUT = sys.argv[1]; DEADLINE = time.time() + float(sys.argv[2])
UA = {"User-Agent": "adapter-census/0.1 (research; contact via github kliukovkin)"}
def get(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.status, r.read(), r.headers
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(min(60, 5 * 2 ** i)); continue
            return e.code, b"", e.headers
        except Exception as e:
            time.sleep(2 * (i + 1))
    return 0, b"", {}
def list_adapters(base):
    path = f"{OUT}/list_{base.replace('/','__')}.json"
    if os.path.exists(path): return json.load(open(path))
    ids, url = [], "https://huggingface.co/api/models?limit=1000&filter=" + urllib.parse.quote(f"base_model:adapter:{base}", safe=":")
    while url:
        st, body, h = get(url)
        if st != 200: print("list fail", base, st, file=sys.stderr); break
        page = json.loads(body)
        ids += [{"id": m["id"], "downloads": m.get("downloads", 0), "likes": m.get("likes", 0), "createdAt": m.get("createdAt")} for m in page]
        m = re.search(r'<([^>]+)>;\s*rel="next"', h.get("Link", "") or "")
        url = m.group(1) if m else None
    json.dump(ids, open(path, "w")); return ids
def one(base, m):
    rid = m["id"]; rec = {"base": base, **m}
    st, body, _ = get(f"https://huggingface.co/{rid}/resolve/main/adapter_config.json")
    rec["cfg_status"] = st
    if st == 200:
        try:
            c = json.loads(body)
            rec.update({k: c.get(k) for k in ("peft_type","r","lora_alpha","target_modules","use_dora","use_rslora","modules_to_save","rank_pattern","base_model_name_or_path","task_type","bias")})
            if isinstance(rec.get("rank_pattern"), dict): rec["rank_pattern"] = len(rec["rank_pattern"])
        except Exception as e: rec["cfg_error"] = str(e)[:100]
    st2, body2, _ = get(f"https://huggingface.co/api/models/{rid}?blobs=true")
    if st2 == 200:
        try:
            sib = json.loads(body2).get("siblings", [])
            w = [s for s in sib if re.search(r"adapter_model\.(safetensors|bin)$", s.get("rfilename",""))]
            rec["adapter_bytes"] = max([s.get("size") or 0 for s in w], default=None)
            rec["n_files"] = len(sib)
        except Exception as e: rec["meta_error"] = str(e)[:100]
    return rec
done = set()
res_path = f"{OUT}/census.jsonl"
if os.path.exists(res_path):
    for l in open(res_path): done.add(json.loads(l)["id"] + "|" + json.loads(l)["base"])
todo = []
for b in BASES:
    L = list_adapters(b); print(b, len(L), flush=True)
    todo += [(b, m) for m in L if m["id"] + "|" + b not in done]
print("todo", len(todo), "done", len(done), flush=True)
with open(res_path, "a") as f, cf.ThreadPoolExecutor(6) as ex:
    futs = []
    for b, m in todo:
        if time.time() > DEADLINE: break
        futs.append(ex.submit(one, b, m))
        if len(futs) >= 60:
            for fu in futs: f.write(json.dumps(fu.result()) + "\n")
            f.flush(); futs = []
    for fu in futs: f.write(json.dumps(fu.result()) + "\n")
print("written total", sum(1 for _ in open(res_path)))
