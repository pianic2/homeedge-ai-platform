#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]; c=json.loads((ROOT/'hardware/edge-mainboard/schematic-contract.json').read_text()); bad=[]
expected={0:'RADAR_RX_FROM_LD2410C_TX',1:'RADAR_TX_TO_LD2410C_RX_SERVICE_ONLY',3:'DOOR_SENSE',4:'ENV_DHT_DATA',5:'SPARE_ADC_CAPABLE',6:'I2C_SDA',7:'I2C_SCL',10:'SPARE_DIGITAL'}
for p,n in expected.items():
 if c['gpio'].get(str(p))!=n:bad.append(f'GPIO{p}')
for x in ('audio_gpio','audio_adc','audio_connector'):
 if x not in c['prohibited']:bad.append(f'missing prohibition {x}')
if c['door_network']!={'pullup_ohm':10000,'series_ohm':1000,'filter_cap_nf':100,'filter_population':'DNP'}:bad.append('door network')
if (c['usb']['d_minus_gpio'],c['usb']['d_plus_gpio'])!=(18,19):bad.append('USB native pins')
if c['health_monitor']['address']!='0x48':bad.append('health ADC address')
print(json.dumps({'schema':'ihap55.contract-check.v1','pass':not bad,'failures':bad},indent=2)); raise SystemExit(0 if not bad else 2)
