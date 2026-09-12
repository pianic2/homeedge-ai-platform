import importlib.util,json,sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve();spec=importlib.util.spec_from_file_location('ihap55_sim',HERE.parents[1]/'ihap55_sim.py');m=importlib.util.module_from_spec(spec);sys.modules['ihap55_sim']=m;spec.loader.exec_module(m);c=json.loads((HERE.parents[5]/'hardware/edge-mainboard/schematic-contract.json').read_text())
class TestSim(unittest.TestCase):
 def test_tps(self):
  f=c['power']['post_5v']['feedback'];self.assertAlmostEqual(m.divider(f['vref_nom_v'],f['r_top_kohm'],f['r_bottom_kohm']),5,6)
 def test_3v3(self):
  f=c['power']['reg_3v3']['feedback'];self.assertAlmostEqual(m.divider(.6,f['r_top_kohm'],f['r_bottom_kohm']),3.318,3)
 def test_mp(self):
  f=c['power']['charger']['boost_feedback'];self.assertAlmostEqual(m.divider(f['vref_v'],f['r_top_kohm'],f['r_bottom_kohm']),5.184,3)
 def test_sweep(self):self.assertEqual([x for x in m.sweep(c) if not x.pass_accepted],[])
if __name__=='__main__':unittest.main()
