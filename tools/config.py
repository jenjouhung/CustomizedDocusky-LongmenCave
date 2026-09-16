"""Data_SPEC field contract. Importers and public UI share this configuration."""
HEADERS = ['序號 (filename)','題名 (title)','題記編號(metatags/Epigraph_No)','朝代(time_dynasty)','年號(time_norm_year)','題記時序(metatags/Epigraph_sequence)','中曆月份(metatags/month)','中曆日(metatags/day)','西曆年(year_for_grouping)','訖工中曆年月日','石窟群名稱(geo_level1)','窟龕名(geo_level2)','窟內位置(geo_level3)','著錄書名(compilation_name)','原書頁碼(book_code)','供養人姓名(metagas_authors)','供養人性別(doctype)','供養人身份(doc_topic_1)','供養人官職(metatags/donor_title)','造像緣起(doc_topic_2)','主要迴向對象(metatags/main_recipients)','次要迴向對象(metatags/secondary_recipient)','受迴向者官職(metatags/recipient_title)','造像內容(metatags/statues)','造像數量','量詞(metatags/quantifier)','主訴願望(metatags/wishes)','題記錄文']
CONFIG = dict(title='龍門石窟北魏紀年題記', headers=HEADERS, key=0, titleField=1, text=27, sort=8, display=[1,2,0,4,6,8,11,12,27], facets=[4,8,11,12,13,15,16,17,19,20,21,22,23,24,26], multi=[15,20,21,23,26], required=[0,1,2,27], numeric=[8,24], separator=';', pageSize=10, schema=1)
CONFIG.update(schema=2, tagFacets=[
    {'name': 'PersonName', 'label': '標記人名'},
    {'name': 'LocName', 'label': '標記地名'},
    {'name': 'Office', 'label': '標記職官名'},
    {'name': 'Udef_Buddhist_Term', 'label': '佛教詞彙'},
    {'name': 'Udef_Cultural_Term', 'label': '文化詞彙'},
])
