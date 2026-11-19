# 產生 data.js / imgs.js / big/：來源 WAAC FW26 現貨 Excel + 倉庫庫存（unmatched_stock_codes.csv 11/19）
import openpyxl, csv, json, hashlib, io, base64, os, sys
from PIL import Image
from crop import load
SRC=sys.argv[1]; STOCK=sys.argv[2]; OUT=sys.argv[3]
st={r['貨號']:int(r['庫存量']) for r in csv.DictReader(open(STOCK,encoding='utf-8-sig'))}
wb=openpyxl.load_workbook(SRC); ws=wb['FW26']
imgs={}
for im in ws._images:
    imgs[im.anchor._from.row+1]=im  # excel row
NAMES={'WGGJX26610':('WAACKY 造型桿頭套','桿頭套'),'WGGJX26710':('WAACKY 造型桿頭套','桿頭套'),
 'WQRCX26541':('男款網眼棒球帽','棒球帽'),'WGRCX26640':('男款棉質棒球帽','棒球帽'),'WGRCX26670':('中性款條紋漁夫帽','漁夫帽'),
 'WGRCX26710':('女款綁帶遮陽帽','遮陽帽'),'WGRCX26740':('男款羊毛混紡棒球帽','棒球帽'),'WGRCX26741':('男款印花護耳帽','護耳帽'),
 'WQRCX26511':('女款緞帶遮陽帽','遮陽帽'),'WQRCX26512':('女款雙面漁夫帽','漁夫帽'),'WQRCX26514':('女款尼龍漁夫帽','漁夫帽')}
COLOR={'BRD':'咖啡','GRX':'綠色','BKX':'黑色','WHX':'白色','GRD':'深綠','CMX':'駝色','IVX':'象牙白','REX':'紅色','GYX':'灰色','BUL':'藍色','RED':'紅色','KHL':'卡其','NYX':'深藍'}
GEN={'MEN':'男','WOMEN':'女','UNI':'中性'}
# 多色合圖 → 單色裁切框（像素 [l,t,r,b]）
CROP={'WGGJX26610-BRD':(0,0,262,448),'WGGJX26710-GRX':(262,0,531,448),
 'WGRCX26640-BKX':(0,0,507,262),'WGRCX26640-GRD':(0,262,507,555),
 'WGRCX26710-CMX':(0,232,486,468),'WGRCX26710-IVX':(0,468,486,705),
 'WGRCX26740-BKX':(0,0,682,245),'WGRCX26740-GYX':(0,245,682,535)}
items={}; order=[]
for r in range(3,ws.max_row+1):
    v=[ws.cell(r,c).value for c in range(1,22)]
    if not v[5]: continue
    pn=v[5]; pc=v[6]; style=v[11]; cc=v[8]; size=str(v[10]); q=st.get(pn)
    if pc not in items:
        zh,cat=NAMES[style]
        items[pc]=dict(id=pc,sheet='FW26 現貨',no=str(len(order)+1),mon='',series='WAAC FW26',cat=cat,cg='配件',gen=GEN[v[7]],style=style,zh=zh,en='',
            color=COLOR.get(cc,cc),cc=cc,sku=pc,fab=v[18] or '',origin=v[17] or '',price=v[19] or 0,sizes=[],stock={},pn={},upc={},srcRow=r)
        order.append(pc)
    it=items[pc]; it['sizes'].append(size); it['stock'][size]=q if q is not None else int(v[20] or 0); it['pn'][size]=pn; it['upc'][size]=v[4]
    if q is None: print('NO STOCK MATCH',pn,file=sys.stderr)
    if r in imgs and 'img' not in it: it['img']=r
    # 材質不同列取第一筆；若同款色不同尺寸材質不同則合併
    if v[18] and v[18] not in it['fab']: it['fab']+=' ／ '+v[18]
os.makedirs(OUT+'/big',exist_ok=True)
IMG={}
for pc in order:
    it=items[pc]; r=it.pop('img',None)
    if r is None: it['doll']=''; print('NO IMG',pc,file=sys.stderr); continue
    raw=imgs[r]._data(); im=load(io.BytesIO(raw))
    if pc in CROP: im=im.crop(CROP[pc])
    # 白邊修整＋留白
    import numpy as np
    a=np.asarray(im).astype(int); m=(a.min(axis=2)<240); ys,xs=m.any(1).nonzero()[0],m.any(0).nonzero()[0]
    im=im.crop((max(0,xs[0]-2),max(0,ys[0]-2),min(im.width,xs[-1]+3),min(im.height,ys[-1]+3)))
    pad=int(max(im.size)*0.06); c=Image.new('RGB',(im.width+2*pad,im.height+2*pad),'white'); c.paste(im,(pad,pad)); im=c
    h=hashlib.md5((pc+':'+hashlib.md5(raw).hexdigest()).encode()).hexdigest()[:12]
    it['doll']=h
    b=io.BytesIO(); im.save(b,'JPEG',quality=93,subsampling=0); open(f'{OUT}/big/{h}.jpg','wb').write(b.getvalue())
    t=im.copy(); t.thumbnail((480,480),Image.LANCZOS); b=io.BytesIO(); t.save(b,'JPEG',quality=88); IMG[h]='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
for pc in order:
    it=items[pc]; it['stockTotal']=sum(it['stock'].values()); it.pop('srcRow')
L=[items[p] for p in order]
open(OUT+'/data.js','w').write('// WAAC FW26 現貨：商品資料。stock＝各尺寸現有庫存（倉庫庫存 2026-11-19），訂購數量不可超過。\nwindow.SDR_ITEMS='+json.dumps(L,ensure_ascii=False)+';\nwindow.WAAC_STOCK_DATE="2026-11-19";\n')
open(OUT+'/imgs.js','w').write('window.SDR_IMG='+json.dumps(IMG)+';\n')
print(len(L),'款色',len(set(i['style'] for i in L)),'款',sum(len(i['sizes']) for i in L),'SKU',sum(i['stockTotal'] for i in L),'件')
