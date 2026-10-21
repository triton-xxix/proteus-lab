# Bey's stated rules, coded as literally as they allow:
# 15m bar close breaks the last confirmed swing (structure break), wait for a retest of the broken
# level (limit at the level, up to 8 bars), stop one point beyond the opposite swing, target 2R,
# exits checked on 5m bars (stop first if both in one bar), close after 1 day if neither hit.
# MNQ: $2 per point, $2 round trip for commission and slippage. One position at a time.
import pandas as pd, numpy as np, sys
def load(f):
    d=pd.read_csv(f,header=[0,1],index_col=0); d.columns=[c[0] for c in d.columns]
    d.index=pd.to_datetime(d.index,utc=True).tz_convert('America/New_York'); return d[['Open','High','Low','Close']].dropna()
b=load('nq15.csv'); f=load('nq5.csv')
K=2; RR=float(sys.argv[1]) if len(sys.argv)>1 else 2.0; WAIT=8; MINR,MAXR=5,60
H,L,C=b.High.values,b.Low.values,b.Close.values; t=b.index; n=len(b)
trades=[]; last_sh=last_sl=None; i=K*2; busy_until=None
sh=[None]*n; sl=[None]*n
for j in range(K,n-K):
    if H[j]==max(H[j-K:j+K+1]): sh[j+K]=(j,H[j])   # confirmed K bars later
    if L[j]==min(L[j-K:j+K+1]): sl[j+K]=(j,L[j])
i=0
while i<n:
    if sh[i]: last_sh=sh[i]
    if sl[i]: last_sl=sl[i]
    if busy_until is not None and t[i]<=busy_until: i+=1; continue
    sig=None
    if last_sh and C[i]>last_sh[1] and (i==0 or C[i-1]<=last_sh[1]) and last_sl: sig=('long',last_sh[1],last_sl[1]-1)
    elif last_sl and C[i]<last_sl[1] and (i==0 or C[i-1]>=last_sl[1]) and last_sh: sig=('short',last_sl[1],last_sh[1]+1)
    if not sig: i+=1; continue
    side,lvl,stop=sig; risk=abs(lvl-stop)
    if not (MINR<=risk<=MAXR): i+=1; continue
    fill=None
    for k in range(i+1,min(i+1+WAIT,n)):
        if side=='long':
            if L[k]<=stop: break
            if L[k]<=lvl: fill=k; break
        else:
            if H[k]>=stop: break
            if H[k]>=lvl: fill=k; break
    if fill is None: i+=1; continue
    tgt=lvl+RR*risk if side=='long' else lvl-RR*risk
    start=t[fill]; end=start+pd.Timedelta(days=1)
    w=f[(f.index>=start)&(f.index<end)]
    # start at the 5m bar where the limit actually filled; in that bar only the stop counts
    touch=(w.Low<=lvl) if side=='long' else (w.High>=lvl)
    if not touch.any(): i+=1; continue
    w=w.loc[touch.idxmax():]
    res=None; first=True
    for ts,r in w.iterrows():
        if first:
            first=False
            if (side=='long' and r.Low<=stop) or (side=='short' and r.High>=stop): res=(ts,stop,'stop'); break
            continue
        if side=='long':
            if r.Low<=stop: res=(ts,stop,'stop'); break
            if r.High>=tgt: res=(ts,tgt,'target'); break
        else:
            if r.High>=stop: res=(ts,stop,'stop'); break
            if r.Low<=tgt: res=(ts,tgt,'target'); break
    if res is None:
        if len(w)==0: i+=1; continue
        res=(w.index[-1],w.Close.iloc[-1],'time')
    pts=(res[1]-lvl) if side=='long' else (lvl-res[1])
    trades.append(dict(entry=start,side=side,level=round(lvl,2),risk=round(risk,2),exit=res[0],how=res[2],pts=round(pts,2),usd=round(pts*2-2,2)))
    busy_until=res[0]; i=fill+1
T=pd.DataFrame(trades)
def summ(x,name):
    w=(x.usd>0).sum(); print(f"{name}: {len(x)} trades, {w} wins {len(x)-w} losses, win {w/len(x):.0%}, net ${x.usd.sum():.0f} on 1 MNQ, avg ${x.usd.mean():.1f}, worst run {worst(x)}")
def worst(x):
    m=c=0
    for u in x.usd: c=c+1 if u<=0 else 0; m=max(m,c)
    return m
print(f"RR {RR}, bars {b.index[0].date()} to {b.index[-1].date()}")
summ(T,'all'); summ(T.tail(15),'last 15')
print('by side:',T.groupby('side').usd.agg(['count','sum']).to_dict());T.to_csv(f'bey_trades_rr{RR}.csv',index=False)
print(T.tail(15).assign(entry=lambda d:d.entry.dt.strftime('%d %b %H:%M'))[['entry','side','risk','how','pts','usd']].to_string(index=False))
