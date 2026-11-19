from PIL import Image
import numpy as np, os
def load(f):
    im=Image.open(f)
    if im.mode in('RGBA','LA','P'):
        im=im.convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); im=bg
    return im.convert('RGB')
def bands(mask,axis,mingap):
    p=mask.any(axis=axis); out=[];s=None;gap=0
    for i,v in enumerate(p):
        if v:
            if s is None: s=i
            e=i;gap=0
        elif s is not None:
            gap+=1
            if gap>=mingap: out.append((s,e));s=None
    if s is not None: out.append((s,e))
    return out
def info(f,mingap=8):
    im=load(f);a=np.asarray(im).astype(int);m=(a.min(axis=2)<235)
    print(f,im.size,'rows',bands(m,1,mingap),'cols',bands(m,0,mingap))
import sys
if __name__=="__main__":
    for f in sys.argv[1:]: info(f)
