"""Cache complete article-linked sources privately; expose no protected link inventory."""
import argparse,concurrent.futures,json,re,urllib.parse
from pathlib import Path
import stage1
from bs4 import BeautifulSoup
ap=argparse.ArgumentParser();ap.add_argument('--private',type=Path,required=True);a=ap.parse_args();stage1.PRIV=a.private.resolve();P=stage1.PRIV
links=json.loads((P/'links.json').read_text(encoding='utf-8'))
urls=sorted({x['href'].split('#')[0] for x in links if x['href'].startswith('https://')})
urls=[re.sub(r'https://github.com/([^/]+/[^/]+)/blob/',r'https://raw.githubusercontent.com/\1/',u) for u in urls]
dois=sorted({urllib.parse.unquote(u.split('doi.org/',1)[1]) for u in urls if 'doi.org/' in u})
urls += ['https://api.crossref.org/works/'+urllib.parse.quote(d,safe='') for d in dois]
urls += ['https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285','https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510','https://www.tandfonline.com/doi/full/10.1080/00031305.2016.1154108','https://arriveguidelines.org/arrive-guidelines','https://plato.stanford.edu/entries/logic-classical/','https://iep.utm.edu/val-snd/','https://arxiv.org/html/2510.22954v2','https://arxiv.org/html/2405.07987v3','https://europepmc.org/articles/PMC2907210?pdf=render','https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0112732','https://api.crossref.org/works/10.1016%2FS0376-0421(02)00005-2','https://microsoft.github.io/z3guide/docs/logic/intro/']
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(stage1.fetch,dict.fromkeys(urls)))
stage1.dump(P/'source-retrievals.json',results)
for r in results:
    if 'cache_key' not in r:continue
    raw=(P/'cache'/r['cache_key']).read_bytes()
    if b'<html' in raw[:10000].lower() or b'<!doctype' in raw[:500].lower():
        s=BeautifulSoup(raw,'html.parser')
        for n in s.select('script,style,nav,header,footer'): n.decompose()
        (P/'cache'/(r['cache_key']+'.txt')).write_text(s.get_text(' ',strip=True),encoding='utf-8')
stage1.dump(stage1.RUN/'source-retrieval-summary.json',{'total':len(results),'succeeded':sum('sha256' in x for x in results),'errors_count':sum(x['status']=='ERROR' for x in results),'private_inventory_sha256':stage1.sha((P/'source-retrievals.json').read_bytes()),'scope':'Complete URL inventory retained privately; successful HTTP response does not certify source content or claims.'})
print(json.dumps({'total':len(results),'errors':[x for x in results if x['status']=='ERROR']},indent=2))
