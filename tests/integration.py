"""Isolated end-to-end PHP + SQLite tests. No production data or credentials used."""
import hashlib, http.cookiejar, json, os, re, secrets, shutil, socket, sqlite3, subprocess, sys, time
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, build_opener, HTTPCookieProcessor, HTTPRedirectHandler
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
PHP=Path(sys.argv[1] if len(sys.argv)>1 else ROOT/'.runtime/php/php.exe').resolve()
INI=ROOT/'.runtime/php/php.ini'
run=ROOT/'var'/('test-'+secrets.token_hex(5)); run.mkdir(parents=True)
for directory in ['app','public','scripts','content']:
    shutil.copytree(ROOT/directory,run/directory)
(run/'config').mkdir(); (run/'var').mkdir()
token=secrets.token_hex(32); password=secrets.token_hex(20)
basecmd=[str(PHP),'-c',str(INI)]
adminhash=subprocess.check_output(basecmd+[str(ROOT/'scripts/credentials.php'),'admin'],input=password.encode()).decode().strip()
config="<?php return ['environment'=>'production','admin_password_hash'=>%s,'api_token_hash'=>%s];" % (repr(adminhash),repr(hashlib.sha256(token.encode()).hexdigest()))
(run/'config/local.php').write_text(config,encoding='utf-8')
subprocess.run(basecmd+[str(run/'scripts/init.php')],check=True,capture_output=True)
# HTTPS is set only inside this disposable test router, never in shipped code.
(run/'test-router.php').write_text("<?php $_SERVER['HTTPS']='on'; require __DIR__.'/public/index.php';",encoding='utf-8')
with socket.socket() as sock:
    sock.bind(('127.0.0.1',0)); port=sock.getsockname()[1]
base=f'http://127.0.0.1:{port}'
log=(run/'server.log').open('w',encoding='utf-8')
server=subprocess.Popen(basecmd+['-S',f'127.0.0.1:{port}','-t',str(run/'public'),str(run/'test-router.php')],stdout=log,stderr=log,cwd=ROOT)
jar=http.cookiejar.CookieJar()
class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None
opener=build_opener(HTTPCookieProcessor(jar),NoRedirect())
checks=[]
def check(value,label):
    if not value: raise AssertionError(label)
    checks.append(label)
def req(path,body=None,auth=False,form=False,session=False):
    headers={}
    # Test transport is HTTP; manually forward the secure cookie only for these isolated tests.
    if session: headers['Cookie']='; '.join(c.name+'='+c.value for c in jar)
    if auth: headers['Authorization']='Bearer '+token
    if body is not None:
        headers['Content-Type']='application/x-www-form-urlencoded' if form else 'application/json'
        if not isinstance(body,bytes): body=json.dumps(body,ensure_ascii=False).encode()
    try:
        with opener.open(Request(base+path,data=body,headers=headers),timeout=8) as response:
            return response.status,response.read().decode(),dict(response.headers)
    except HTTPError as error: return error.code,error.read().decode(),dict(error.headers)
def database(): return sqlite3.connect(run/'var/site.sqlite')
def set_company(c):
    with database() as db: db.execute('UPDATE settings SET payload=? WHERE id=?',(json.dumps(c,ensure_ascii=False),'company'))
def set_page(p):
    with database() as db: db.execute('UPDATE pages SET status=?,payload=? WHERE slug=?',(p['status'],json.dumps(p,ensure_ascii=False),p['slug']))
def tokens(text): return re.findall(r"[\w]+(?:[’'-][\w]+)*",text)
try:
    for _ in range(80):
        try: req('/robots.txt'); break
        except (URLError,ConnectionError): time.sleep(.05)
    status,body,headers=req('/')
    check(status==503 and 'noindex' in headers.get('X-Robots-Tag',''),'Unconfigured production serves maintenance + noindex')
    check('Disallow: /' in req('/robots.txt')[1],'Unconfigured robots blocks indexing')
    check('<loc>' not in req('/sitemap.xml')[1],'Unverified sitemap is empty')
    check(req('/api/v1/articles')[0]==401,'API rejects anonymous requests')
    check(req('/api/v1/status',auth=True)[0]==200,'API token authentication works')
    check(req('/api/v1/articles',b'{bad',auth=True)[0]==400,'API rejects invalid JSON')
    check(req('/api/v1/articles',{'slug':[]},auth=True)[0]==422,'Malformed payload returns validation error')
    article=json.loads((ROOT/'content/article.example.json').read_text(encoding='utf-8'))
    article['status']='published'
    check(req('/api/v1/articles',article,auth=True)[0]==422,'Publication blocks unverified business and article')
    article['status']='draft'
    check(req('/api/v1/articles',article,auth=True)[0]==201,'API inserts a draft into database')
    article['title']='Titre révisé <script>alert(1)</script>'
    check(req('/api/v1/articles',article,auth=True)[0]==200,'API updates existing slug without duplicating article')
    check(len(json.loads(req('/api/v1/articles',auth=True)[1])['articles'])==1,'Article upsert is idempotent')
    c=json.loads((ROOT/'content/company.json').read_text(encoding='utf-8'))
    c.update(name='Entreprise fictive de test',phone='+33100000000',site_url='https://electricien.example',identity_verified=True,services_verified=True,hours_verified=True,hours_text='Horaires de test',pricing_verified=True,pricing_text='Conditions de test',legal_verified=True,legal_text='Mentions de test')
    set_company(c)
    check(req('/conseils/'+article['slug']+'/')[0]==404,'Draft article is private after company validation')
    data=json.loads((ROOT/'content/cities.json').read_text(encoding='utf-8'))
    check(len(data)==15,'Exactly 15 city pages are seeded')
    check(req('/electricien/'+data[0]['slug']+'/')[0]==404,'Unpublished city is private')
    p=data[0].copy(); p['status']='published'; set_page(p)
    check(req('/electricien/'+p['slug']+'/')[0]==404,'Status alone cannot bypass coverage gate')
    titles=set(); descriptions=set(); counts=[]
    for p in data:
        count=len(tokens(p['intro']+' '+' '.join(s['title']+' '+' '.join(s['paragraphs']) for s in p['sections'])+' '+' '.join(q['question']+' '+q['answer'] for q in p['faq'])))
        counts.append(count)
        check(600<=count<=1000,'Word count '+p['slug'])
        check(all(any(n['slug']==slug for n in data) for slug in p['neighbors']),'Neighbor links '+p['slug'])
        p.update(status='published',editorial_verified=True,coverage_verified=True,verified_districts=p['districts'],coverage_evidence='Fixture de test uniquement')
        set_page(p)
    for p in data:
        path='/electricien/'+p['slug']+'/'
        status,html,h=req(path)
        check(status==200,'Published route '+p['slug'])
        check(len(re.findall(r'<h1[ >]',html))==1,'Unique H1 '+p['slug'])
        title=re.search(r'<title>(.*?)</title>',html).group(1); check(title not in titles,'Unique title '+p['slug']); titles.add(title)
        desc=re.search(r'name="description" content="([^"]+)"',html).group(1); check(desc not in descriptions,'Unique description '+p['slug']); descriptions.add(desc)
        check('https://electricien.example'+path in html,'Canonical '+p['slug'])
        check('href="tel:+33100000000"' in html,'Verified click-to-call '+p['slug'])
        schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html).group(1))
        check(schema['@graph'][1]['areaServed']['name']==p['city'],'Service schema '+p['slug'])
        check('aggregateRating' not in html,'No fabricated rating '+p['slug'])
        check('index,follow' in html and 'noindex' not in h.get('X-Robots-Tag',''),'Indexable published page '+p['slug'])
    sitemap=ET.fromstring(req('/sitemap.xml')[1]); urls=[x.text for x in sitemap.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    check(sum('/electricien/' in u and u!='https://electricien.example/electricien/' for u in urls)==15,'Sitemap contains all 15 verified local URLs')
    check('Disallow: /\n' not in req('/robots.txt')[1],'Robots permits published site')
    article.update(status='published',editorial_verified='false')
    check(req('/api/v1/articles',article,auth=True)[0]==422,'String boolean cannot bypass editorial approval')
    article['editorial_verified']=True
    check(req('/api/v1/articles',article,auth=True)[0]==200,'Verified article publishes via API')
    status,html,h=req('/conseils/'+article['slug']+'/')
    check(status==200 and '&lt;script&gt;alert(1)&lt;/script&gt;' in html and '<script>alert(1)</script>' not in html,'Article renders safely with escaped markup')
    check('/conseils/'+article['slug']+'/' in req('/sitemap.xml')[1],'Published article automatically joins sitemap')
    conflict=article.copy(); conflict['slug']=data[0]['slug']
    check(req('/api/v1/articles',conflict,auth=True)[0]==409,'API cannot overwrite local pages')
    check(req('/admin/',b'action=login&password=anything',form=True)[0]==403,'Admin blocks POST without CSRF token')
    status,body,h=req('/admin/')
    csrf=re.search(r'name="csrf" value="([^"]+)"',body).group(1)
    old_session=';'.join(c.value for c in jar)
    req('/admin/',urlencode({'action':'login','csrf':csrf,'password':password}).encode(),form=True,session=True)
    check(old_session!=';'.join(c.value for c in jar),'Admin rotates session identifier at login')
    status,body,h=req('/admin/',session=True)
    check('Votre présence locale.' in body,'Authenticated admin dashboard is accessible')
    csrf=re.search(r'name="csrf" value="([^"]+)"',body).group(1)
    draft=article.copy(); draft['slug']='brouillon-admin'; draft['status']='draft'
    req('/admin/?new=article',urlencode({'action':'save_page','csrf':csrf,'payload':json.dumps(draft),'status':'draft','original_slug':''}).encode(),form=True,session=True)
    check(json.loads(req('/api/v1/articles?slug=brouillon-admin',auth=True)[1])['article']['status']=='draft','Admin editor persists an article in database')
    check(req('/admin/',b'action=logout&csrf=invalid',form=True,session=True)[0]==403,'Authenticated mutation rejects invalid CSRF')
    req('/admin/',urlencode({'action':'logout','csrf':csrf}).encode(),form=True,session=True)
    check('Votre présence locale.' not in req('/admin/',session=True)[1],'Logout removes authenticated access')
    p=data[0]; p['coverage_verified']=False; set_page(p)
    check(req('/electricien/'+p['slug']+'/')[0]==404,'Revoked coverage hides previously published page')
    check('/electricien/'+p['slug']+'/' not in req('/sitemap.xml')[1],'Revoked page removed from sitemap')
    check(req('/does-not-exist/')[0]==404,'Unknown route returns real 404')
    report={'checks_passed':len(checks),'city_pages':len(data),'min_words':min(counts),'max_words':max(counts),'database':'SQLite (MySQL requires Hostinger acceptance test)','checks':checks}
    (ROOT/'docs/test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False,indent=2))
finally:
    server.terminate(); server.wait(timeout=10); log.close()
    # Temporary fixture remains under var/ for inspection; never packaged or published.
