"""Atomic file versions and checksum-verified backup packages."""
import json, hashlib, shutil, tempfile, zipfile, datetime
from pathlib import Path
from config import CONFIG
from importer import read_excel
from markup import parse_text, PARSER_VERSION
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'workspace-data'
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp'); tmp.write_text(json.dumps(value,ensure_ascii=False,separators=(',',':')),encoding='utf-8'); tmp.replace(path)
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def manifest(): return read(DATA/'manifest.json') if (DATA/'manifest.json').exists() else {'schema':1,'current':None,'versions':[],'events':[]}
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def import_file(path):
    records,warnings,sheet=read_excel(path); m=manifest()
    version='v'+str(max([int(v['id'][1:]) for v in m['versions']]+[0])+1).zfill(4)
    DATA.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=DATA) as tmp:
        stage=Path(tmp); index={}; facets={}
        for n,r in enumerate(records):
            parsed=parse_text(r[CONFIG['text']], {t['name'] for t in CONFIG['tagFacets']})
            for pos,ch in enumerate(parsed['text']):
                index.setdefault(ch,{}).setdefault(str(n),[]).append(pos)
            for f in CONFIG['facets']:
                v=r[f]; vals=set(str(v).strip().split(';')) if f in CONFIG['multi'] and v is not None else [v]
                vals={x.strip() if isinstance(x,str) and f in CONFIG['multi'] else x for x in vals}
                for x in vals:
                    if f in CONFIG['multi'] and x=='': continue
                    facets.setdefault(str(f),{}).setdefault(json.dumps(x,ensure_ascii=False),[]).append(n)
            for name,term in {(t['name'],t['term']) for t in parsed['tags']}:
                facets.setdefault('tag:'+name,{}).setdefault(json.dumps(term,ensure_ascii=False),[]).append(n)
            write(stage/'records'/f'{n}.json',r)
            write(stage/'texts'/f'{n}.json',parsed)
        write(stage/'index.json',index); write(stage/'facets.json',facets)
        write(stage/'rows.json',[{str(i):r[i] for i in set(CONFIG['facets']+[0,CONFIG['sort']])} for r in records])
        meta={'id':version,'count':len(records),'created':now(),'source':path.name,'sha256':digest(path),'sheet':sheet,'headers':CONFIG['headers'],'warnings':warnings}
        meta.update(schema=2, parserVersion=PARSER_VERSION, offsetUnit='unicode-code-point')
        write(stage/'version.json',meta); write(stage/'config.json',CONFIG)
        write(stage/'checksums.json',{str(p.relative_to(stage)):digest(p) for p in stage.rglob('*') if p.is_file()})
        stage.rename(DATA/version)
    original=DATA/'originals'/f'{version}.xlsx'
    try:
        original.parent.mkdir(exist_ok=True); shutil.copy2(path,original)
        m['versions'].append(meta); m['current']=version; m['events'].append({'action':'import','version':version,'at':now()}); write(DATA/'manifest.json',m)
    except Exception:
        shutil.rmtree(DATA/version)
        original.unlink(missing_ok=True)
        raise
    return meta
def verify(folder):
    for version in read(folder/'manifest.json')['versions']:
        base=folder/version['id']
        for name,sha in read(base/'checksums.json').items():
            p=(base/name).resolve()
            if not p.is_relative_to(base.resolve()) or digest(p)!=sha: raise ValueError('資料校驗失敗：'+name)
def set_current(version):
    m=manifest()
    if version not in [v['id'] for v in m['versions']]: raise ValueError('未知版本')
    verify(DATA); m['events'].append({'action':'restore','before':m['current'],'after':version,'at':now()}); m['current']=version; write(DATA/'manifest.json',m)
def backup(automatic=False):
    verify(DATA); dest=ROOT/'backups'; dest.mkdir(exist_ok=True)
    path=dest/(('auto-' if automatic else '')+datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'.zip')
    files={str(p.relative_to(DATA)):p.read_bytes() for p in DATA.rglob('*') if p.is_file()}
    checks={n:hashlib.sha256(b).hexdigest() for n,b in files.items()}
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for n,b in files.items(): z.writestr(n,b)
        z.writestr('backup-checksums.json',json.dumps(checks)); z.writestr('backup-format.json','{"schema":1,"platform":"1.0.0"}')
    if automatic:
        for old in sorted(dest.glob('auto-*.zip'),reverse=True)[5:]:old.unlink()
    return path
def restore(path):
    with tempfile.TemporaryDirectory(dir=ROOT) as tmp, zipfile.ZipFile(path) as z:
        base=Path(tmp); names=z.namelist()
        if len(names)!=len(set(names)) or sum(i.file_size for i in z.infolist())>2*1024**3: raise ValueError('無效備份')
        if json.loads(z.read('backup-format.json'))!={'schema':1,'platform':'1.0.0'}: raise ValueError('備份版本不相容')
        checks=json.loads(z.read('backup-checksums.json'))
        if set(names)!=set(checks)|{'backup-checksums.json','backup-format.json'}: raise ValueError('備份清單不一致')
        for name,sha in checks.items():
            p=(base/name).resolve()
            if not p.is_relative_to(base.resolve()): raise ValueError('備份路徑不合法')
            content=z.read(name)
            if hashlib.sha256(content).hexdigest()!=sha: raise ValueError('備份校驗失敗')
            p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(content)
        verify(base)
        if DATA.exists(): backup(automatic=True)
        old=ROOT/'workspace-data.previous'
        if old.exists(): shutil.rmtree(old)
        if DATA.exists(): DATA.rename(old)
        try: base.rename(DATA)
        except Exception:
            if old.exists(): old.rename(DATA)
            raise
def public_build():
    verify(DATA); dest=ROOT/'public-build'
    if dest.exists(): shutil.rmtree(dest)
    shutil.copytree(ROOT/'web',dest); shutil.copytree(DATA,dest/'data',ignore=shutil.ignore_patterns('originals'))
    m=manifest(); m.pop('events',None); write(dest/'data'/'manifest.json',m)
    return dest
