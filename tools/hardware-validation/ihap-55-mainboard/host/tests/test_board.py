import importlib.util,sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve();spec=importlib.util.spec_from_file_location('ihap55_board_test',HERE.parents[1]/'ihap55_board_test.py');m=importlib.util.module_from_spec(spec);sys.modules['ihap55_board_test']=m;spec.loader.exec_module(m)
class TestBoard(unittest.TestCase):
 def rec(self,p='standard'):
  checks={k:True for k in m.REQUIRED_CHECKS};checks.update({'dht11':p=='standard','bme280':p=='precision','bme280_chip_id':0x60 if p=='precision' else None});return {'record_type':'board_self_test','profile':p,'checks':checks,'rails':{'VBUS_IN':5,'BATT':3.8,'SYS_5V':5,'SYS_3V3':3.3}}
 def test_standard(self):self.assertEqual(m.evaluate(self.rec(),'standard'),[])
 def test_precision(self):self.assertEqual(m.evaluate(self.rec('precision'),'precision'),[])
 def test_bad_rail(self):
  r=self.rec();r['rails']['SYS_5V']=4.5;self.assertTrue(m.evaluate(r,'standard'))
 def test_tx_disabled(self):
  r=self.rec();r['checks']['service_tx_disabled']=False;self.assertTrue(m.evaluate(r,'standard'))
if __name__=='__main__':unittest.main()
