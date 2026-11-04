"""Publish an article through the site's authenticated API. Credentials stay out of CLI arguments."""
import argparse
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

parser = argparse.ArgumentParser(description='Envoyer un article vers le site Hostinger.')
parser.add_argument('file', type=Path)
parser.add_argument('--publish', action='store_true', help='Publier après validation éditoriale ; sinon enregistrer un brouillon.')
args = parser.parse_args()
base = os.environ.get('ELECTRICIEN_SITE_URL', '').rstrip('/')
token = os.environ.get('ELECTRICIEN_API_TOKEN', '')
parsed = urllib.parse.urlparse(base)
if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.path not in ('','/') or parsed.query or parsed.fragment:
    parser.error('ELECTRICIEN_SITE_URL doit être le domaine HTTPS définitif.')
if len(token) < 24:
    parser.error('Définissez ELECTRICIEN_API_TOKEN dans l’environnement sécurisé de la session.')
payload = json.loads(args.file.read_text(encoding='utf-8'))
payload['kind'] = 'article'
payload['status'] = 'published' if args.publish else 'draft'
if args.publish and payload.get('editorial_verified') is not True:
    parser.error('Le contenu doit être relu et editorial_verified doit valoir true.')
request = urllib.request.Request(base+'/api/v1/articles', data=json.dumps(payload,ensure_ascii=False).encode(), headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'},method='POST')
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None
try:
    with urllib.request.build_opener(NoRedirect()).open(request,timeout=30) as response:
        result = json.load(response)
    print(json.dumps(result,ensure_ascii=False,indent=2))
except urllib.error.HTTPError as error:
    print('Publication refusée :', error.code)
    print(error.read().decode('utf-8',errors='replace'))
    raise SystemExit(1)
except urllib.error.URLError:
    raise SystemExit('Connexion impossible. Vérifiez le domaine, le certificat et l’accès réseau. Aucun secret n’a été affiché.')
