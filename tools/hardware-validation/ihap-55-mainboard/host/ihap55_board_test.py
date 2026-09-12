#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,time
from pathlib import Path
RAILS={'VBUS_IN':(4.75,5.25),'SYS_5V':(4.75,5.25),'SYS_3V3':(3.0,3.6),'BATT':(2.5,4.25)}
REQUIRED_CHECKS=('usb_console','health_adc','oled','radar','door_level_valid','spare_adc','spare_digital','service_tx_disabled')
def evaluate(r,profile):
 bad=[]
 if r.get('record_type')!='board_self_test':bad.append('wrong record_type')
 if r.get('profile')!=profile:bad.append('profile mismatch')
 checks=r.get('checks',{})
 for k in REQUIRED_CHECKS:
  if checks.get(k) is not True:bad.append(f'check failed: {k}')
 if profile=='standard' and checks.get('dht11') is not True:bad.append('STANDARD requires DHT11')
 if profile=='precision':
  if checks.get('bme280') is not True:bad.append('PRECISION requires BME280')
  if checks.get('bme280_chip_id') not in (0x60,96):bad.append('BME280 chip id != 0x60')
 for n,v in r.get('rails',{}).items():
  if n in RAILS and v is not None:
   lo,hi=RAILS[n]
   if not lo<=float(v)<=hi:bad.append(f'{n}={v} outside {lo}..{hi} V')
 return bad
def transact(port,profile,timeout):
 try:import serial
 except ImportError:raise SystemExit('pyserial missing: pip install -r requirements.txt')
 with serial.Serial(port,115200,timeout=.25) as s:
  time.sleep(.5);s.reset_input_buffer();s.write((json.dumps({'cmd':'self_test','profile':profile,'schema':'ihap55.board.v1'})+'\n').encode());s.flush();deadline=time.monotonic()+timeout;records=[]
  while time.monotonic()<deadline:
   line=s.readline()
   if not line:continue
   try:r=json.loads(line.decode(errors='replace'))
   except json.JSONDecodeError:continue
   records.append(r)
   if r.get('record_type')=='board_self_test':return r,records
 raise SystemExit('No board_self_test record before timeout')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--port',required=True);ap.add_argument('--profile',choices=['standard','precision'],default='standard');ap.add_argument('--timeout',type=float,default=12);ap.add_argument('--out',type=Path);a=ap.parse_args();r,records=transact(a.port,a.profile,a.timeout);bad=evaluate(r,a.profile);out={'schema':'ihap55.host.v1','pass':not bad,'failures':bad,'self_test':r,'records':records};print(json.dumps(out,indent=2));
 if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n')
 raise SystemExit(0 if not bad else 2)
if __name__=='__main__':main()
