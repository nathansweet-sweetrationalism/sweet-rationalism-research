"""Independent exact, AST, numerical and SMT checks of pinned public sources.
No full upstream modules are imported or executed. Only reviewed pure functions
or expressions are extracted. Deterministic output; no biological validation.
"""
import argparse, ast, csv, hashlib, importlib.util, io, itertools, json, math, subprocess, sys
from decimal import Decimal
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import scipy, scipy.integrate, scipy.linalg, scipy.optimize
import sympy as sp
import z3

RUN=Path(__file__).resolve().parent.parent
ARTICLE=RUN.parents[2]
PIN='4bed72c17f09bf336e36e7472e64d457db3b0195'
def digest(x): return hashlib.sha256(x).hexdigest()
def source(path):
    raw=subprocess.check_output(['git','show',PIN+':'+path],cwd=UP)
    receipts.append({'path':path,'commit':PIN,'sha256':digest(raw),'bytes':len(raw)})
    return raw.decode('utf-8')
def module(text): return ast.parse(text)
def assignments(text,name):
    return [n.value for n in ast.walk(module(text)) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)]
def pure_functions(text,names,env):
    tree=module(text); subset=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert len(subset)==len(names)
    for n in subset:
        assert not any(isinstance(k,(ast.Import,ast.ImportFrom,ast.Global)) for k in ast.walk(n))
    exec(compile(ast.Module(body=subset,type_ignores=[]),'<reviewed-functions>','exec'),env)
    return env

def run():
    out={'versions':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__,'z3':z3.get_version_string()},'source_receipts':receipts}
    # Independently parse literal data, never the supplied regular expression.
    gen=source('docs/media/make_claim_aggregation.py')
    rows=next(ast.literal_eval(n.value) for n in module(gen).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TILES' for t in n.targets))
    vals=[F(str(r[-1]).rstrip('%')) for r in rows]
    assert len(vals)==7
    exact=sum(vals)/len(vals); decimal=sum(Decimal(str(float(v))) for v in vals)/Decimal(7)
    struct=list(map(F,['100','40.5','100','96.1','95','95','90.1']))
    loo=[sum(vals[:i]+vals[i+1:])/6 for i in range(7)]
    raw_ratios=[F('7.4')/F('11.1'),F('1.5')/F('11.1'),F('9.6')/F('11.1'),F('32')/F('33.3'),F('10.55')/F('11.1'),F('10.55')/F('11.1'),F('10')/F('11.1')]
    assert abs(float(exact)-float(decimal))<1e-12
    out['scores']={'display_inputs':[str(x) for x in vals],'mean_exact':str(exact),'mean_decimal':str(decimal),'structural_mean_exact':str(sum(struct)/7),'leave_one_out':[str(x) for x in loo],'raw_ratio_mean_percent':str(sum(raw_ratios)*100/7),'claim2_weight_sensitivity':{str(w):float((sum(vals)-vals[1]+w*vals[1])/(6+w)) for w in [0,1,2,5,10]},'negative_control_wrong_denominator':str(sum(vals)/6)}

    renderer=source('sorting-morphogenesis/render_13yo_illustrations.py')
    matrix=ast.literal_eval(assignments(renderer,'ai_matrix')[0].args[0]); prose=[F(str(r[1])) for r in matrix]
    before=100-sum(prose)/len(prose); split=100-sum([prose[0]]+prose)/(len(prose)+1)
    out['authorship']={'rows':len(prose),'before_exact':str(before),'after_split_exact':str(split),'before_percent':float(before),'after_percent':float(split),'numpy_crosscheck':100-float(np.mean([float(x) for x in prose])),'equal_half_weight_split_invariant':before==100-(sum(prose[1:])+prose[0]/2+prose[0]/2)/len(prose)}

    validator=source('sorting-morphogenesis/validate_kymograph_and_paper.py')
    records=[]
    for n in ast.walk(module(validator)):
        if isinstance(n,ast.Dict):
            pairs={k.value:v for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and isinstance(k.value,str)}
            if 'relative_error_pct' in pairs and 'status' in pairs: records.append((n,pairs))
    assert len(records)==14
    ast_statuses=[ast.literal_eval(p['status']) for _,p in records]
    chosen=next(p for _,p in records if 'dg_by_f' in ast.unparse(p['relative_error_pct']) and '0.37' in ast.unparse(p['relative_error_pct']))
    # Exact expression inspected before execution: NumPy mean, float, abs, round only.
    expr=chosen['relative_error_pct']; allowed={'round','abs','float','np','dg_by_f'}
    assert {n.id for n in ast.walk(expr) if isinstance(n,ast.Name)}<=allowed
    tests=[]
    for measured in [0.37,3.7,0.0]:
        error=eval(compile(ast.Expression(expr),'<reviewed-error-expression>','eval'),{'round':round,'abs':abs,'float':float,'np':np,'dg_by_f':{'B':{3:[measured]}}})
        tests.append({'synthetic_measured':measured,'computed_error_pct':error,'status':ast.literal_eval(chosen['status'])})
    csv_rows=list(csv.DictReader(io.StringIO(source('sorting-morphogenesis/figures/zhang_2025_validation_benchmarks.csv'))))
    out['validator']={'record_count':len(records),'statuses':ast_statuses,'synthetic_controls':tests,'saved_rows':csv_rows}

    xenobot=source('models/2020-kriegman-xenobot-evolutionary-biobots.py')
    approved=['theta_deg','eta_sweep','spill_penalty','compacted_cells_curve']
    nodes=[n for n in ast.walk(module(xenobot)) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in approved for t in n.targets)]
    env={'np':np};exec(compile(ast.Module(body=nodes,type_ignores=[]),'<reviewed-xenobot-sweep>','exec'),env)
    def ref(t): return 12*(6+12.5*math.exp(-((t-65)/26)**2))*(math.exp(-((t-85)/38)**2) if t>85 else 1)
    dif=max(abs(ref(float(t))-float(v)) for t,v in zip(env['theta_deg'],env['compacted_cells_curve']))
    best=scipy.optimize.minimize_scalar(lambda t:-ref(t),bounds=(0,120),method='bounded')
    grids={str(step):float(np.arange(0,120+step/2,step)[np.argmax([ref(t) for t in np.arange(0,120+step/2,step)])]) for step in [5,1,.1,.01]}
    assert dif<1e-10 and abs(best.x-65)<1e-4
    out['xenobot']={'grid_maxima':grids,'continuous_optimum':best.x,'at_65':ref(65),'at_105':ref(105),'independent_max_discrepancy':dif,'programmed_maximum_derivation':'eta <=18.5 and penalty <=1; both attain bounds at theta=65 in [0,120], so product <=222 with unique equality at 65. Angle convention remains a separate source question.'}

    tad=source('models/2019-bischof-xenopus-craniofacial-remap.py'); data=json.loads(source('datasets/xenopus_craniofacial_remap/xenopus_craniofacial_remap_reference.json')); p=data['canonical_parameters']
    e=pure_functions(tad,['build_coupling_matrix','closed_loop_attractor_rhs','procrustes_lyapunov_energy'],{'np':np})
    K=np.array([p['K_eye']]*2+[p['K_naris']]*2+[p['K_jaw']]);C=e['build_coupling_matrix'](5,p['C_coupled']);A=np.diag(K+C.sum(axis=1))-C
    target=np.array(p['target_nf65_landmarks']); initial=np.array(p['wt_nf45_landmarks'])+np.array(next(r['perturbation_deltas'] for r in data['experimental_regimes'] if r['id']=='picasso_scrambled_craniofacial_closed_loop'))
    scenarios=[]
    for shift,eta in [(np.zeros_like(target),1),(np.ones_like(target)*2,1),(np.zeros_like(target),0)]:
        goal=target+shift; exact_y=goal+scipy.linalg.expm(-eta*A*20)@(initial-goal)
        f=lambda t,y:e['closed_loop_attractor_rhs'](y.reshape(5,2),goal,K,C,eta).ravel()
        sol=scipy.integrate.solve_ivp(f,[0,20],initial.ravel(),rtol=1e-11,atol=1e-13)
        errs=[]
        for dt in [.1,.05,.025]:
            y=initial.copy()
            for _ in range(round(20/dt)):
                rhs=lambda q:e['closed_loop_attractor_rhs'](q,goal,K,C,eta)
                k1=rhs(y);k2=rhs(y+dt*k1/2);k3=rhs(y+dt*k2/2);k4=rhs(y+dt*k3);y+=dt*(k1+2*k2+2*k3+k4)/6
            errs.append({'dt':dt,'error_vs_matrix_exp':float(np.max(abs(y-exact_y)))})
        scenarios.append({'target_shift':float(shift[0,0]),'eta':eta,'final_target_rms':float(np.sqrt(np.mean(np.sum((exact_y-goal)**2,axis=1)))),'solve_ivp_difference':float(np.max(abs(sol.y[:,-1].reshape(5,2)-exact_y))),'rk4_convergence':errs})
    assert max(s['solve_ivp_difference'] for s in scenarios)<1e-8
    H=sp.Matrix([[sp.Rational(str(float(x))) for x in row] for row in A]);eigen=np.linalg.eigvalsh(A)
    out['tadpole']={'scenarios':scenarios,'symmetric':bool(np.allclose(A,A.T)),'eigenvalues':eigen.tolist(),'positive_definite_exact_principal_minors':[str(H[:i,:i].det()) for i in range(1,6)],'derivation':'For symmetric nonnegative C and positive K, A=diag(K)+L(C) positive definite; V=1/2 sum_coordinates y.T A y; ydot=-eta A y; Vdot=-eta ||Ay||^2. eta=0 arrests motion; eta>0 converges asymptotically to supplied target. This is conditional model mathematics.'}

    port=source('sorting-morphogenesis/verify_multilang_ports.py');asserts=[n for n in ast.walk(module(port)) if isinstance(n,ast.Assert)]
    chosen=[n for n in asserts if any(isinstance(t,ast.Name) and t.id in ['cpp_data','js_data','py_kymo'] for t in ast.walk(n.test))]
    cp={'kymograph_n42':{f'{a}_final_values':[1,2,3] for a in ['selection','bubble','insertion']},'benchmarks':{'x':1},'frames':[[3,2,1],[1,2,3]]};js=json.loads(json.dumps(cp));py={a:{'final_values':[1,2,3]} for a in ['selection','bubble','insertion']};js['frames']=[[2,3,1],[1,2,3]]
    def check(c,j,p):
        try:exec(compile(ast.Module(body=chosen,type_ignores=[]),'<reviewed-port-assertions>','exec'),{'cpp_data':c,'js_data':j,'py_kymo':p});return True
        except AssertionError:return False
    frame_not_detected=check(cp,js,py);js['kymograph_n42']['selection_final_values']=[3,2,1]; final_detected=not check(cp,js,py)
    assert frame_not_detected and final_detected
    out['ports']={'assertions':len(chosen),'changed_intermediate_frames_accepted':frame_not_detected,'changed_final_array_rejected':final_detected,'scope':'Synthetic countermodel to sufficiency of these four assertions only, not a measured difference among real ports.'}

    # Two independent mechanisms for the finite logical inference.
    d,pv,z=z3.Bools('d p z');solver=z3.Solver();solver.add(d,z3.Not(pv));out['logic']={'D_success_with_P_false':str(solver.check())};solver=z3.Solver();solver.add(d,pv);out['logic']['D_success_with_P_true']=str(solver.check())
    q=z3.Real('q');solver=z3.Solver();solver.add(q>0,q<=1,q/q!=1);out['logic']['equal_positive_likelihood_ratio_countermodel']=str(solver.check())
    out['logic']['truth_table_D_does_not_entail_notP']=[dict(D=a,P=b) for a,b in itertools.product([False,True],repeat=2) if a and b]
    out['logic']['zero_likelihood_boundary']='0/0 undefined; both assigning zero probability requires a different model/density/support treatment.'
    inv=lambda v:sum(v[i]>v[j] for i in range(len(v)) for j in range(i+1,len(v)))
    adj=lambda v:sum(v[i]>v[i+1] for i in range(len(v)-1))
    count=0;counter=[]
    for n in range(2,8):
        for v in itertools.permutations(range(n)):
            for i in range(n-1):
                if v[i]>v[i+1]:
                    w=list(v);w[i],w[i+1]=w[i+1],w[i];assert inv(w)==inv(v)-1;count+=1
                    if adj(w)>adj(v) and len(counter)<1:counter.append({'before':v,'after':w,'I':[inv(v),inv(w)],'E':[adj(v),adj(w)]})
    out['sorting']={'adjacent_inverted_swaps_checked':count,'max_n':7,'two_metrics_counterexample':counter,'scope':'Distinct-key adjacent inverted swaps; not an unrestricted theorem about all selection swaps.'}
    spec=importlib.util.spec_from_file_location('supplied_harness',ARTICLE/'audit.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
    fake='# "status": "VERIFIED"\n# "relative_error_pct":\n'
    accepted=h.verify('validator',{'validator':fake},{},False)
    fixed_ast_counts=sum(isinstance(n,ast.Dict) for n in ast.walk(ast.parse(fake)))
    out['harness_adversary']={'comment_only_false_positive':accepted[0],'ast_repair_rejects_comment_only':fixed_ast_counts==0,'scope':'Supplied verifier reports a synthetic control without executing it; comments alone satisfy its string tests. Independent AST check above supplies the missing real execution.'}
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--upstream',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();UP=args.upstream;receipts=[]
    result=run();args.out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ['source_receipts','validator']},indent=2))
