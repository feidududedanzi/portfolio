from pathlib import Path
import re,sys,shutil

def build(source,destination,repository,owner):
 source=Path(source); destination=Path(destination)
 prefix='' if repository.lower()==(owner+'.github.io').lower() else '/'+repository
 origin=f'https://{owner}.github.io{prefix}'
 for f in source.rglob('*'):
  if not f.is_file() or '.openai' in f.relative_to(source).parts:continue
  target=destination/f.relative_to(source);target.parent.mkdir(parents=True,exist_ok=True)
  if f.suffix.lower() in ['.html','.css','.js','.json','.svg'] and 'vendor' not in f.parts:
   text=f.read_text(encoding='utf-8')
   text=re.sub(r'https://(?:purpose-design-chen-portfolio|chen-luyang-portfolio)\.bouncy-olm-1976\.chatgpt\.site',origin,text)
   if prefix:
    text=re.sub(r'''(["'`])/(?!/)(?=[a-zA-Z0-9#?]|["'`])''',lambda m:m[1]+prefix+'/',text)
    text=re.sub(r'url\(/(?!/)',lambda m:'url('+prefix+'/',text)
    # Language title lookup uses site-relative paths.
    if f.name=='app.js':text=text.replace('location.pathname.replace(',f'location.pathname.slice({len(prefix)}).replace(')
   target.write_text(text,encoding='utf-8')
  else:shutil.copy2(f,target)
 (destination/'.nojekyll').write_text('',encoding='utf-8')
 missing=[]
 for f in destination.rglob('*.html'):
  for u in re.findall(r'(?:href|src)="(/[^"#?]*)',f.read_text(encoding='utf-8')):
   local=u[len(prefix):] if prefix and u.startswith(prefix+'/') else u
   if not (destination/local.lstrip('/')).exists():missing.append((str(f),u))
 assert not missing,missing
 print('GitHub Pages base path and HTML resource references verified:',prefix or '/')

if __name__=='__main__':
 if len(sys.argv)!=5:raise SystemExit('build-github-pages.py SOURCE DESTINATION REPOSITORY OWNER')
 build(*sys.argv[1:])
