import numpy as np, json
rng=np.random.default_rng(7)
def logit(p): return np.log(p/(1-p))
def sig(x): return 1/(1+np.exp(-x))
def U(S,req,red,sigma):
    # req: two complementary ids; red: optional redundant copy of req[1]
    has=lambda i:i in S
    both=has(req[0]) and (has(req[1]) or (red is not None and has(red)))
    single=has(req[0]) or has(req[1]) or (red is not None and has(red))
    p=.9 if both else (.27 if single else .2)
    return sig(logit(p)+rng.normal(0,sigma))
def d(p,eps=.1): return -np.log(p)+eps
def trace(us,K,g=.8):
    ds=[d(u) for u in us]; dl=[np.log(ds[i]/ds[i+1]) for i in range(len(us)-1)]; T=len(dl); out=[]
    for k in range(T):
        h=min(k+K-1,T-1); w=[g**(u-k) for u in range(k,h+1)]
        out.append(sum(w[u-k]*dl[u] for u in range(k,h+1))/sum(w))
    return out
def auc(pos,neg):
    pos=np.array(pos);neg=np.array(neg)
    if len(pos)==0 or len(neg)==0:return float('nan')
    return float(((pos[:,None]>neg[None,:]).mean()+.5*(pos[:,None]==neg[None,:]).mean()))
def run(sigma,N=6000,red_rate=0.,K_null=3):
    R={k:([],[]) for k in ['TRACE-K1','TRACE-K3','per-call','LOO','group']}
    grp_ok=[];cost=[]
    for _ in range(N):
        n=rng.integers(3,6); ids=list(range(n)); rng.shuffle(ids)
        req=ids[:2]; red=ids[2] if rng.random()<red_rate and n>3 else None
        order=list(rng.permutation(n))
        # prefix scores share the same noisy evaluator
        us=[U(set(),req,red,sigma)]; cur=[]
        for o in order:
            cur.append(int(o)); us.append(U(set(cur),req,red,sigma))
        t1=trace(us,1); t3=trace(us,3)
        per=[us[i+1]-us[i] for i in range(n)]
        full=np.mean([U(set(order),req,red,sigma) for _ in range(K_null)])
        loo={}
        for o in order:
            loo[o]=full-np.mean([U(set(order)-{o},req,red,sigma) for _ in range(K_null)])
        # backward elimination
        G=set(int(o) for o in order); base=full; evals=K_null+n*K_null
        for o in sorted(order,key=lambda x:loo[x]):
            cand=G-{int(o)}
            val=np.mean([U(cand,req,red,sigma) for _ in range(K_null)]); evals+=K_null
            if val>=base-.08: G=cand
        need={req[0]}
        truth=lambda o:(o==req[0] or o==req[1] or o==red)
        for i,o in enumerate(order):
            pos=int(o) in req
            irrelevant=(int(o)!=red) and not pos
            if int(o)==red and red is not None: continue
            for name,val in [('TRACE-K1',t1[i]),('TRACE-K3',t3[i]),('per-call',per[i]),('LOO',loo[o]),('group',float(int(o) in G))]:
                (R[name][0] if pos else R[name][1]).append(val)
        grp_ok.append(req[0] in G and ((req[1] in G) or (red in G if red is not None else False)) and len(G)==2)
        cost.append(evals)
    return {k:round(auc(*v),3) for k,v in R.items()}|{'group_exact':round(float(np.mean(grp_ok)),3),'evals':round(float(np.mean(cost)),1)}
rows=[]
for s in [0,.2,.5,1.0,1.5]:
    rows.append(('sigma',s,run(s)))
for rr in [.5]:
    rows.append(('sigma_red',.2,run(.2,red_rate=rr)))
# fixed example
us=[.2,.25,.25,.9]
print('fixed',[round(x,3) for x in trace(us,3)])
for r in rows: print(r)
json.dump(rows,open('/tmp/sim/res.json','w'),ensure_ascii=False)
