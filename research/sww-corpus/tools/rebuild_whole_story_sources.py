"""Retrieve the 387 frozen canonical transcripts in episode_index.txt, with caching.

python3 -I rebuild_whole_story_sources.py RESULTS_DIR TRANSCRIPT_DIR

Uses the original fetcher's parsing, a single worker and the inherited network settings.
Later publications and alternate transcriptions do not enter the frozen episode set.
Transcripts remain outside the repository. HTTP 429 Retry-After is honored.
"""
import email.utils
import hashlib
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

results, destination=map(Path,sys.argv[1:3]);destination.mkdir(parents=True,exist_ok=True)
slugs=[line.split()[2] for line in (results/'episode_index.txt').read_text().splitlines() if len(line.split())==3]
assert len(slugs)==len(set(slugs))==387

def get(url):
    for attempt in range(8):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=60) as response:
                body=response.read().decode('utf-8','replace')
            time.sleep(1.5)
            return body
        except (urllib.error.URLError,TimeoutError) as error:
            if attempt==7:raise
            retry=getattr(error,'headers',{}).get('Retry-After')
            delay=min(300,15*2**attempt)
            if retry:
                try:delay=max(delay,float(retry))
                except ValueError:
                    try:delay=max(delay,email.utils.parsedate_to_datetime(retry).timestamp()-time.time())
                    except (TypeError,ValueError):pass
            print(type(error).__name__,url,'backoff',delay,flush=True)
            time.sleep(delay)

for slug in sorted(slugs):
    path=destination/(slug+'.json')
    if path.exists():
        d=json.loads(path.read_text())
        assert d['slug']==slug and d['text'],path
        continue
    h=get('https://podscripts.co/podcasts/something-was-wrong/'+slug)
    m=re.search(r'window\.__EPISODE__ = (\{.*?\});?\s*</script>',h,re.S);meta={}
    if m:
        try:meta=json.loads(m.group(1)).get('episode',{})
        except json.JSONDecodeError:pass
    segs=[(int(sec),html.unescape(re.sub(r'<[^>]+>','',text)).strip())
          for sec,text in re.findall(r'class="psb-ep__sentence"[^>]*data-seconds="(\d+)"[^>]*>(.*?)</span>',h,re.S)]
    title=meta.get('title') or html.unescape((re.search(r'<title>(.*?)</title>',h) or [None,slug])[1])
    d=dict(slug=slug,title=title,notes=meta.get('description',''),segments=segs,text=' '.join(t for _,t in segs))
    assert d['text'],slug
    path.write_text(json.dumps(d));print(slug,'retrieved',flush=True)
manifest={'retrieved_date_utc':datetime.now(timezone.utc).date().isoformat(),
          'selection':'Original episode_index.txt canonical slugs; no later publications or alternate transcriptions',
          'episodes':[{'slug':slug,'sha256':hashlib.sha256((destination/(slug+'.json')).read_bytes()).hexdigest()}
                      for slug in sorted(slugs)]}
(results/'transcript_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Complete:',len(slugs),'canonical transcripts; manifest written',flush=True)
