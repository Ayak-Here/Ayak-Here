import json, os, urllib.request
from pathlib import Path
from collections import Counter
USER = 'Ayak-Here'
TOKEN = os.environ.get('GITHUB_TOKEN','')
ROOT = Path(__file__).resolve().parents[1]
def get(url):
    req=urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','Authorization':f'Bearer {TOKEN}','X-GitHub-Api-Version':'2022-11-28','User-Agent':'Ayak-Here-profile'})
    with urllib.request.urlopen(req,timeout=20) as r: return json.load(r)
def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
user=get(f'https://api.github.com/users/{USER}')
repos=get(f'https://api.github.com/users/{USER}/repos?per_page=100&type=owner&sort=updated')
stars=sum(r.get('stargazers_count',0) for r in repos if not r.get('fork'))
langs=Counter()
for r in repos:
    if r.get('fork'): continue
    try: langs.update(get(r['languages_url']))
    except Exception: pass
total=sum(langs.values()) or 1
top=[(k,round(v/total*100,1)) for k,v in langs.most_common(5)]
def card(dark):
    bg,border,text,muted=('#07111f','#26364b','#f8fafc','#94a3b8') if dark else ('#ffffff','#cbd5e1','#0f172a','#475569')
    purple,cyan,blue,pink,yellow=('#a78bfa','#22d3ee','#60a5fa','#f472b6','#facc15')
    rows=[('Public Repos',user.get('public_repos',0),cyan),('Followers',user.get('followers',0),purple),('Following',user.get('following',0),blue),('Total Stars',stars,pink)]
    s=''; y=62
    for label,val,col in rows:
        s+=f'<text x="26" y="{y}" font-family="monospace" font-size="12" fill="{muted}">{esc(label)}</text><text x="260" y="{y}" text-anchor="end" font-family="monospace" font-size="13" font-weight="700" fill="{col}">{val}</text>'; y+=29
    b=''; y=62
    mx=max([p for _,p in top] or [1])
    for i,(name,pct) in enumerate(top):
        col=[blue,cyan,yellow,pink,purple][i%5]; w=145*pct/mx
        b+=f'<text x="315" y="{y}" font-family="monospace" font-size="11" fill="{muted}">{esc(name)}</text><rect x="410" y="{y-10}" width="145" height="9" rx="4" fill="{border}"/><rect x="410" y="{y-10}" width="{w:.1f}" height="9" rx="4" fill="{col}"/><text x="570" y="{y}" font-family="monospace" font-size="10" fill="{text}">{pct}%</text>'; y+=25
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="620" height="190" viewBox="0 0 620 190"><rect x="1" y="1" width="618" height="188" rx="16" fill="{bg}" stroke="{border}"/><text x="24" y="30" font-family="monospace" font-size="14" font-weight="700" fill="{purple}">GITHUB ACTIVITY</text><text x="315" y="30" font-family="monospace" font-size="14" font-weight="700" fill="{purple}">MOST USED LANGUAGES</text><line x1="302" y1="14" x2="302" y2="176" stroke="{border}"/>{s}{b}</svg>'
(ROOT/'activity-dark.svg').write_text(card(True),encoding='utf-8')
(ROOT/'activity-light.svg').write_text(card(False),encoding='utf-8')
