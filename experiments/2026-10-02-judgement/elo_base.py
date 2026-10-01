"""Blind baseline for the 2-4 Oct 2026 window: Elo (eloratings.net via pitch/brief.py, 1 Oct) to 1X2 and over 2.5
by independent Poisson, fitted so P(H)+P(D)/2 equals the Elo win expectancy. No market prices used."""
import math, json
ELO = {"Cyprus":1310,"Armenia":1367,"Bosnia & Herzegovina":1655,"Sweden":1759,"Faroe Islands":1382,"Slovakia":1675,
"France":2103,"Italy":1882,"Hungary":1691,"Georgia":1630,"Poland":1681,"Romania":1590,"Ukraine":1798,"Northern Ireland":1630,
"Finland":1532,"Albania":1632,"Belarus":1514,"San Marino":821,"Croatia":1891,"England":2114,"Estonia":1383,"Luxembourg":1439,
"Iceland":1591,"Bulgaria":1423,"North Macedonia":1490,"Scotland":1721,"Spain":2281,"Czech Republic":1659,"Switzerland":1968,
"Slovenia":1694,"Netherlands":1970,"Serbia":1687,"Portugal":2047,"Norway":1908,"Republic of Ireland":1717,"Israel":1613}
FIX = [("2026-10-02T16:00:00Z","Cyprus","Armenia",100),("2026-10-02T18:45:00Z","Bosnia & Herzegovina","Sweden",100),
("2026-10-02T18:45:00Z","Faroe Islands","Slovakia",100),("2026-10-02T18:45:00Z","France","Italy",100),
("2026-10-02T18:45:00Z","Hungary","Georgia",100),("2026-10-02T18:45:00Z","Poland","Romania",100),
("2026-10-02T18:45:00Z","Ukraine","Northern Ireland",0),("2026-10-03T13:00:00Z","Finland","Albania",100),
("2026-10-03T16:00:00Z","Belarus","San Marino",0),("2026-10-03T16:00:00Z","Croatia","England",100),
("2026-10-03T16:00:00Z","Estonia","Luxembourg",100),("2026-10-03T16:00:00Z","Iceland","Bulgaria",100),
("2026-10-03T18:45:00Z","North Macedonia","Scotland",100),("2026-10-03T18:45:00Z","Spain","Czech Republic",100),
("2026-10-03T18:45:00Z","Switzerland","Slovenia",100),("2026-10-04T18:45:00Z","Netherlands","Serbia",100),
("2026-10-04T18:45:00Z","Portugal","Norway",100),("2026-10-04T18:45:00Z","Republic of Ireland","Israel",100)]
def pois(k, m): return math.exp(-m) * m**k / math.factorial(k)
def probs(mh, ma):
    h=d=a=o=0.0
    for i in range(11):
        for j in range(11):
            p=pois(i,mh)*pois(j,ma)
            if i>j: h+=p
            elif i==j: d+=p
            else: a+=p
            if i+j>2: o+=p
    return h,d,a,o
out=[]
for ko,h,a,ha in FIX:
    dr=ELO[h]+ha-ELO[a]; we=1/(10**(-dr/400)+1)
    T=2.35+1.6*abs(we-0.5)**1.5*2   # mismatches score more
    lo,hi=-3.0,3.0
    for _ in range(60):
        s=(lo+hi)/2; ph,pd,pa,po=probs((T+s)/2,(T-s)/2)
        if ph+pd/2<we: lo=s
        else: hi=s
    out.append({"kickoff_utc":ko,"home":h,"away":a,"elo_diff_with_home":dr,"we":round(we,3),"total":round(T,2),
                "p":[round(ph,3),round(pd,3),round(pa,3)],"over25":round(po,3)})
    print("%-22s v %-20s dr %+5d We %.2f  H %.2f D %.2f A %.2f  O2.5 %.2f" % (h,a,dr,we,ph,pd,pa,po))
json.dump(out,open("/Users/triton/PROTEUS/experiments/2026-10-02-judgement/elo_base.json","w"),indent=1)
