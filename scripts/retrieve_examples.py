import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'data' / 'remotion-categories.zip'
STOP = set('a an and are as at be create for from in is it me my of on or the this to with video make please use'.split())

def tokens(text):
    return {w for w in re.findall(r'[a-z0-9]+', text.lower()) if len(w) > 2 and w not in STOP}

def main():
    req=json.loads(sys.stdin.read() or '{}')
    query=str(req.get('query',''))
    family=str(req.get('family','')).lower().strip()
    q=tokens(query)
    if not q:
        print(json.dumps({'examples': [], 'message': 'Add a little more detail to the prompt.'})); return
    if not ARCHIVE.is_file():
        print(json.dumps({'examples': [], 'count': 0, 'message': 'Optional dataset archive is not installed.'}))
        return
    ranked=[]
    with zipfile.ZipFile(ARCHIVE) as z:
        for name in z.namelist():
            if not name.startswith('categories/') or not name.endswith('.jsonl'): continue
            for line in z.read(name).decode('utf8').splitlines():
                if not line.strip(): continue
                r=json.loads(line)
                prompt=r['messages'][1]['content']
                hay=tokens(prompt+' '+r.get('family','')+' '+r.get('source','')+' '+str(r.get('palette','')))
                overlap=len(q & hay)
                if family and family in str(r.get('family','')).lower(): overlap += 4
                if overlap:
                    ranked.append((overlap/(len(q)**0.65),r))
    ranked.sort(key=lambda x:x[0],reverse=True)
    results=[]
    seen=set()
    for score,r in ranked:
        if r.get('id') in seen: continue
        seen.add(r['id'])
        results.append({'id':r['id'],'family':r['family'],'source':r['source'],'prompt':r['messages'][1]['content'],'project':r['messages'][2]['content'][:9000],'match_score':round(score,3)})
        if len(results)==3: break
    print(json.dumps({'examples':results,'count':len(results)},ensure_ascii=False))

if __name__=='__main__': main()
