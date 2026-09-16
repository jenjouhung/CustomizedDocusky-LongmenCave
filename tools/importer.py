"""Read first XLSX sheet, preserving raw values; no third party dependencies."""
import zipfile, xml.etree.ElementTree as ET, re, posixpath
from config import CONFIG
from markup import parse_text
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def read_excel(path):
    if path.stat().st_size > 50*1024*1024: raise ValueError('Excel 超過 50 MB')
    warnings=[]
    with zipfile.ZipFile(path) as z:
        if sum(i.file_size for i in z.infolist())>512*1024*1024: raise ValueError('Excel 解壓大小超過安全上限 512 MB')
        shared=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            shared=[''.join(t.text or '' for t in x.findall('.//m:t',NS)) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        sheets=ET.fromstring(z.read('xl/workbook.xml')).find('m:sheets',NS)
        if sheets is None or not len(sheets): raise ValueError('Excel 沒有工作表')
        first=sheets[0]; rid=first.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        rels=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        target=next(r.get('Target') for r in rels if r.get('Id')==rid)
        target=target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
        rows=[]
        for row in ET.fromstring(z.read(target)).findall('.//m:sheetData/m:row',NS):
            values={}
            for cell in row:
                ref=cell.get('r',''); col=0
                for ch in re.sub('[0-9]','',ref): col=col*26+ord(ch)-64
                if cell.find('m:f',NS) is not None: raise ValueError(f'{first.get("name")} 第{row.get("r")}列 {ref}：不支援公式，請提供確定值')
                v=cell.find('m:v',NS); value=v.text if v is not None else None
                typ=cell.get('t')
                if typ=='s': value=shared[int(value)]
                elif typ=='inlineStr': value=''.join(t.text or '' for t in cell.findall('.//m:t',NS))
                elif value is not None and typ not in ('str','e'):
                    value=float(value); value=int(value) if value.is_integer() else value
                if value is not None: values[col-1]=value
            rows.append((int(row.get('r')),values))
    if not rows or rows[0][0]!=1: raise ValueError('第1列必須是標題列')
    expected=CONFIG['headers']; hdr=rows[0][1]
    if [hdr.get(i) for i in range(max(hdr,default=-1)+1)]!=expected: raise ValueError('欄位數、名稱或順序與 Data_SPEC 不符；請回到規格修訂流程')
    records=[]; seen=set()
    last=max((n for n,v in rows[1:] if v),default=1)
    for n,values in rows[1:]:
        if not values:
            if n<last: warnings.append(f'第{n}列：空白列，不形成紀錄')
            continue
        if max(values)>=len(expected): raise ValueError(f'第{n}列有額外欄位')
        r=[values.get(i) for i in range(len(expected))]
        for i in CONFIG['required']:
            if r[i] is None or not str(r[i]).strip(): raise ValueError(f'第{n}列 {expected[i]} 不得空白')
        key=str(r[0])
        if key in seen: raise ValueError(f'第{n}列 唯一鍵重複：{key}')
        seen.add(key)
        if len(str(r[27]))>200000: raise ValueError(f'第{n}列 全文超過200000字元')
        try:
            parse_text(r[CONFIG['text']], {t['name'] for t in CONFIG['tagFacets']})
        except ValueError as exc:
            raise ValueError(f'{first.get("name")} 第{n}列 {expected[CONFIG["text"]]}：{exc}') from exc
        for i,v in enumerate(r):
            if v is None: warnings.append(f'第{n}列 {expected[i]}：空白值')
            if i in CONFIG['multi'] and v is not None:
                parts=[p.strip() for p in str(v).split(';')]
                if '' in parts or len(parts)!=len(set(parts)) or '；' in str(v): warnings.append(f'第{n}列 {expected[i]}：空項、重複項或疑似分隔符號')
        records.append(r)
    if len(records)>50000: raise ValueError('紀錄超過50000筆')
    return records, warnings, first.get('name')
