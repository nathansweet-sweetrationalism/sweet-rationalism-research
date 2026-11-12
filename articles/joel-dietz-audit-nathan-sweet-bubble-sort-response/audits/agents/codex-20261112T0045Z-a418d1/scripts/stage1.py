"""Private manuscript inventory, public-source retrieval and real command capture.
Run with the pinned requirements in README. No manuscript bytes are published.
"""
import argparse, concurrent.futures, hashlib, io, json, os, re, subprocess, sys, time, urllib.request, zipfile
from pathlib import Path
from bs4 import BeautifulSoup

RUN = Path(__file__).resolve().parent.parent
ARTICLE = RUN.parents[2]
REPO = ARTICLE.parents[1]
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
def command(label, args, cwd, private=False, timeout=180):
    start=time.time()
    try:
        p=subprocess.run(args,cwd=cwd,capture_output=True,timeout=timeout)
        out,err,code=p.stdout,p.stderr,p.returncode
    except subprocess.TimeoutExpired as e:
        out,err,code=e.stdout or b'',e.stderr or b'',124
    folder=(PRIV/'logs' if private else RUN/'logs'); folder.mkdir(exist_ok=True)
    (folder/(label+'.stdout.txt')).write_bytes(out); (folder/(label+'.stderr.txt')).write_bytes(err)
    rec={'label':label,'command':args,'cwd':str(cwd),'exit_code':code,'seconds':round(time.time()-start,3),'stdout_sha256':sha(out),'stderr_sha256':sha(err),'private':private}
    with (PRIV/'commands-private.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(rec)+'\n')
    # Absolute private locations are redacted from the public command receipt.
    safe=json.loads(json.dumps(rec).replace(str(PRIV),'PRIVATE').replace(str(REPO),'REPO'))
    with (RUN/'commands.txt').open('a',encoding='utf-8') as f: f.write(json.dumps(safe)+'\n')
    return rec

def fetch(url):
    dest=PRIV/'cache'/sha(url.encode())
    try:
        if dest.exists(): raw=dest.read_bytes(); status='CACHED'
        else:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'IndependentAudit/1.0'}),timeout=50) as r:
                raw=r.read(); status=r.status
            dest.write_bytes(raw)
        return {'url':url,'status':status,'sha256':sha(raw),'bytes':len(raw),'cache_key':dest.name}
    except Exception as e: return {'url':url,'status':'ERROR','error':str(e)}

def inventory():
    wp=json.loads((PRIV/'wordpress-response.json').read_text(encoding='utf-8'))
    raw=wp['content']; soup=BeautifulSoup(raw,'html.parser')
    panels=[]
    for det in soup.select('details.rcf-computational-test'):
        ta=det.find('textarea'); prompt=ta.get_text() if ta else ''
        urls=re.findall(r'https://[^\s<>"\']+',prompt)
        panels.append({'panel_id':det.get('id'),'source_prompt_sha256':sha(prompt.encode()),'prompt_characters':len(prompt),
            'primary_zip_url':next((u for u in urls if 'raw.githubusercontent.com' in u and '.zip' in u),''),
            'backup_zip_url':next((u for u in urls if '/wp-content/uploads/' in u and '.zip' in u),''),
            'commands':sorted(set(re.findall(r'python\s+audit\.py(?:\s+--[a-z]+(?:\s+test-data/[a-z]+\.json)?) *',prompt))),
            'selftest_only_literal':'SELFTEST_ONLY' in prompt,'fixture_check_only_literal':'FIXTURE_CHECK_ONLY' in prompt,
            'button_count':len(det.find_all('button')),'textarea_count':len(det.find_all('textarea')),
            'human_zip_urls':[a.get('href') for a in det.find_all('a',href=True) if '.zip' in a['href']]})
        (PRIV/'panels'/f"{det.get('id')}.txt").write_text(prompt,encoding='utf-8')
    ids=[x.get('id') for x in soup.find_all(id=True)]
    links=[dict(href=a['href'],text=a.get_text(' ',strip=True),target=a.get('target'),rel=a.get('rel')) for a in soup.find_all('a',href=True)]
    dump(PRIV/'links.json',links)
    alltext=soup.get_text(' ',strip=True)
    for x in soup.select('details.rcf-computational-test'): x.decompose()
    blocks=[]; section='opening'
    for n,x in enumerate(soup.find_all(['h1','h2','h3','h4','p','li','pre','blockquote'])):
        if x.find_parent(['blockquote','li','pre']): continue
        if x.name.startswith('h'): section=x.get('id') or f'heading-{n}'
        txt=x.get_text(' ',strip=True)
        blocks.append({'id':f'b{n:04d}','tag':x.name,'section':section,'text':txt})
    dump(PRIV/'blocks.json',blocks)
    (PRIV/'article-readable.txt').write_text('\n\n'.join(f"[{x['id']} {x['section']}] {x['text']}" for x in blocks),encoding='utf-8')
    candidates=[x for x in blocks if re.search(r'\d|[=<>≈]|Bayes|probabil|likelihood|counterfactual|necessary|sufficient',x['text'],re.I)]
    dump(PRIV/'math-candidates.json',candidates)
    result={'snapshot':{'wordpress_post_id':wp['id'],'wordpress_status':wp['status'],'wordpress_modified':wp['modified'],'wordpress_content_sha256':sha(raw.encode()),'github_base_commit':'2ee1a4233d37339e27580e59e83af3284f0027d1','upstream_commit':'4bed72c17f09bf336e36e7472e64d457db3b0195'},
        'panels':panels,'pair_equality':{k:len({p['source_prompt_sha256'] for p in panels if '-'+k+'-' in p['panel_id']})==1 for k in ['validator','xenobot','tadpole','score','ports','authorship','doi']},
        'block_count':len(blocks),'math_candidate_blocks':len(candidates),'duplicate_ids':sorted({x for x in ids if ids.count(x)>1}),
        'missing_internal_targets':[a['href'] for a in links if a['href'].startswith('#') and a['href'][1:] not in ids],
        'external_link_policy_failures':sum(1 for a in links if a['href'].startswith('http') and 'sweetrationalism.com' not in a['href'] and (a['target']!='_blank' or not {'noopener','noreferrer'}.issubset(a['rel'] or []))),
        'internal_new_tab_count':sum(1 for a in links if 'sweetrationalism.com' in a['href'] and a['target']=='_blank'),
        'script_tags':len(soup.find_all('script')),'images_without_alt':len(soup.select('img:not([alt])'))}
    dump(RUN/'inventory.json',result)
    print(json.dumps({k:result[k] for k in ['block_count','math_candidate_blocks','duplicate_ids','missing_internal_targets','external_link_policy_failures','internal_new_tab_count']}))

def packages():
    specs=json.loads((ARTICLE/'sources.json').read_text())['tests']
    urls=[v[k] for v in specs.values() for k in ['github_zip_url','wp_zip_url']]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: receipts=list(pool.map(fetch,urls))
    dump(RUN/'retrieval-packages.json',receipts); byurl={x['url']:x for x in receipts}; results=[]
    for kind,spec in specs.items():
        a,b=(byurl[spec[k]] for k in ['github_zip_url','wp_zip_url']); rec={'id':kind,'mirrors_equal':a.get('sha256')==b.get('sha256') if 'sha256' in a and 'sha256' in b else None,'retrievals':[a,b]}
        good=next((x for x in [a,b] if 'sha256' in x),None)
        if not good: results.append(rec); continue
        z=zipfile.ZipFile(PRIV/'cache'/good['cache_key']); rec['crc_failure']=z.testzip(); rec['members']=z.namelist()
        target=PRIV/'packages'/kind; target.mkdir(parents=True,exist_ok=True)
        for name in z.namelist():
            dest=(target/name).resolve()
            assert dest.is_relative_to(target.resolve()),'Unsafe ZIP member'
        z.extractall(target)
        rec['file_hashes']={n:sha(z.read(n)) for n in z.namelist() if not n.endswith('/')}
        code=next(target.rglob('audit.py')); cfg=code.parent/'test.json'
        rec['harness_identical']=code.read_bytes().replace(b'\r\n',b'\n')==(ARTICLE/'audit.py').read_bytes().replace(b'\r\n',b'\n')
        rec['config_semantic_equal']=json.loads(cfg.read_text())==json.loads((ARTICLE/'test-data'/f'{kind}.json').read_text())
        results.append(rec)
    dump(RUN/'packages.json',results)
    print(json.dumps({'packages':len(results),'mirror_matches':sum(x['mirrors_equal'] is True for x in results),'errors':[r for r in receipts if r['status']=='ERROR']}))

def execute():
    # The sole harness was read in full before execution; package equality is checked first.
    items=json.loads((RUN/'packages.json').read_text())
    for x in items:
        if not x.get('harness_identical'): raise RuntimeError('Unreviewed differing package')
    def one(kind):
        for mode in ['--live','--selftest']:
            command(kind+mode,[sys.executable,'audit.py',mode,'--config',f'test-data/{kind}.json'],ARTICLE)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: list(pool.map(one,[x['id'] for x in items]))
    for label,args in [('missing-mode',[]),('conflict-mode',['--live','--selftest']),('missing-config',['--live','--config','not-present.json'])]: command(label,[sys.executable,'audit.py']+args,ARTICLE)
    for script,args in [('bottom_line_gate.py',['--format','html']),('core_framework_links_gate.py',['--strict']),('prose_audit.py',['--format','html','--json'])]:
        command(script,[sys.executable,str(REPO/'scripts'/script),str(PRIV/'article-original.html')]+args,REPO,private=True)
    command('environment',[sys.executable,'-m','pip','freeze'],PRIV)
    command('repository-tests',[sys.executable,'-m','pytest','tests',str(ARTICLE/'agents/test_validate_submission.py'),'-q'],REPO)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--private',type=Path,required=True);ap.add_argument('stage',choices=['inventory','packages','execute']);a=ap.parse_args();PRIV=a.private.resolve()
    for f in ['panels','cache','logs']: (PRIV/f).mkdir(parents=True,exist_ok=True)
    globals()[a.stage]()
