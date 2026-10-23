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
 # Normalize directory frames for both existing and updated source archives.
 (destination/'case-document.css').write_text('/* The PDF provides the visual hierarchy; the website supplies a quiet reader. */\n.case-reader-head{padding-top:150px;padding-bottom:48px}.reader-back{font-size:13px;color:#d5dceb;display:inline-block;margin-bottom:40px}.reader-heading{display:flex;align-items:baseline;justify-content:space-between;gap:32px}.reader-heading h1{font-size:clamp(36px,4.2vw,64px);line-height:1.2;font-weight:500;letter-spacing:-.04em;margin:0}.reader-heading>.mono{font-size:12px;line-height:1.6;color:#c0c7d6;white-space:nowrap}.reader-scope{font-size:14px;line-height:1.8;color:#c4ccdc;margin:24px 0 0;max-width:44em}\n.case-reader{width:min(1280px,calc(100% - 80px));margin:0 auto;background:#fff;line-height:0;isolation:isolate;overflow:hidden}.reader-sheet,.reader-sheet .art-open{display:block;width:100%;padding:0;margin:0;border:0;border-radius:0;background:#fff;line-height:0;box-shadow:none}.reader-sheet .art-open{cursor:zoom-in}.reader-sheet img{display:block;width:100%;height:auto;max-height:none;object-fit:fill;transform:none;transition:none;opacity:1}.reader-sheet .art-open:hover img{transform:none}.reader-sheet .art-open:focus-visible{outline:3px solid #5068ed;outline-offset:-3px;position:relative;z-index:1}.case-reader-next{padding-top:56px;padding-bottom:72px}.case-reader-next>span{font-size:12px;color:#c4ccdc}.case-reader-next>a{display:flex;align-items:center;justify-content:space-between;font-size:clamp(28px,3vw,46px);line-height:1.3;margin-top:20px;gap:20px}.document-case .prototype-link{display:none}\n/* Equal column widths, with each source artwork shown at its original ratio. */\n.motion-project[data-motion-project] .motion-project-pin{height:auto;min-height:100svh;padding-block:80px}\n.motion-project[data-motion-project] .motion-project-image{width:100%;height:auto;aspect-ratio:auto;max-height:none;justify-self:stretch;align-self:center;background:transparent}\n.motion-project[data-motion-project] .motion-project-image img{display:block;width:100%;height:auto;max-height:none;object-fit:contain;object-position:center;transform:none}\n@media(max-width:760px){.case-reader-head{padding-top:112px;padding-bottom:32px}.reader-back{margin-bottom:28px;font-size:12px}.reader-heading{display:block}.reader-heading h1{font-size:34px;line-height:1.25}.reader-heading>.mono{font-size:11px;margin-top:16px}.reader-scope{font-size:13px;margin-top:16px;max-width:25em}.case-reader{width:100%;margin:0}.case-reader-next{padding-top:40px;padding-bottom:48px}.case-reader-next>a{font-size:28px}}\n@media print{.case-reader-head{padding-top:20px}.case-reader{width:100%;overflow:visible}.reader-sheet{break-inside:auto}.reader-back,.case-reader-next{display:none}}\n',encoding='utf-8')
 for page in destination.rglob('*.html'):
  content=page.read_text(encoding='utf-8')
  page.write_text(re.sub(r'case-document\.css\?v=\d+', 'case-document.css?v=3', content),encoding='utf-8')
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
