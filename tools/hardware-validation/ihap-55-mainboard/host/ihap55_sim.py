#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from dataclasses import dataclass,asdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
CONTRACT=ROOT/'hardware/edge-mainboard/schematic-contract.json'
def divider(vref,rt,rb): return vref*(1+rt/rb)
def divider_bounds(vmin,vmax,rt,rb,tol_pct):
 t=tol_pct/100; return divider(vmin,rt*(1-t),rb*(1+t)),divider(vmax,rt*(1+t),rb*(1-t))
def efficiency_5v(vin,load):
 if load<=.15:return .88
 if load<=.50:return .91 if vin>=4 else .89
 return .88 if vin>=4 else .85
@dataclass
class Case:
 source:str; source_v:float; load_5v_a:float; load_3v3_a:float; intermediate_v:float; intermediate_input_a:float; sys5v_min_v:float; sys5v_max_v:float; sys3v3_min_v:float; sys3v3_max_v:float; pass_accepted:bool; notes:list[str]
def simulate_case(c,source,source_v,load5,load3):
 equiv5=load5+(3.3*load3/.90)/5
 if source=='usb': intermediate=max(0,source_v-.12)
 else:
  f=c['power']['charger']['boost_feedback']; intermediate=divider(f['vref_v'],f['r_top_kohm'],f['r_bottom_kohm'])*.98
 eff=efficiency_5v(intermediate,equiv5); iin=5*equiv5/(max(intermediate,.1)*eff)
 f=c['power']['post_5v']['feedback']; v5lo,v5hi=divider_bounds(f['vref_nom_v']*(1-f['vref_tol_pct']/100),f['vref_nom_v']*(1+f['vref_tol_pct']/100),f['r_top_kohm'],f['r_bottom_kohm'],f['tolerance_pct']); v5lo-=.035 if equiv5<=.5 else .075; v5hi+=.035
 f=c['power']['reg_3v3']['feedback']; v3lo,v3hi=divider_bounds(f['vref_range_v'][0],f['vref_range_v'][1],f['r_top_kohm'],f['r_bottom_kohm'],f['tolerance_pct']); v3lo-=.025 if load3<=.5 else .05; v3hi+=.025
 notes=[]
 if equiv5>1:notes.append('combined equivalent SYS5V load exceeds 1.0 A headroom')
 if not 1.3<=intermediate<=5.5:notes.append('TPS63802 input outside range')
 ok=v5lo>=4.75 and v5hi<=5.25 and v3lo>=3 and v3hi<=3.6 and 1.3<=intermediate<=5.5 and equiv5<=1
 return Case(source,source_v,load5,load3,intermediate,iin,v5lo,v5hi,v3lo,v3hi,ok,notes)
def sweep(c):
 out=[]
 for v in (4.75,5,5.25):
  for l5 in (.1,.5):
   for l3 in (.05,.25):out.append(simulate_case(c,'usb',v,l5,l3))
 for v in (2.7,3.3,3.6,4.2):
  for l5 in (.1,.5):
   for l3 in (.05,.25):out.append(simulate_case(c,'battery',v,l5,l3))
 return out
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--contract',type=Path,default=CONTRACT); ap.add_argument('--json',action='store_true'); a=ap.parse_args(); c=json.loads(a.contract.read_text()); cases=sweep(c); out={'schema':'ihap55.sim.v1','case_count':len(cases),'passed':sum(x.pass_accepted for x in cases),'failed':sum(not x.pass_accepted for x in cases),'cases':[asdict(x) for x in cases],'boundary':'Behavioral corner screening only; vendor SPICE and fabricated-board evidence remain required.'}
 print(json.dumps(out,indent=2) if a.json else f"IHAP-55 envelope: {out['passed']}/{out['case_count']} PASS"); raise SystemExit(0 if not out['failed'] else 2)
if __name__=='__main__':main()
