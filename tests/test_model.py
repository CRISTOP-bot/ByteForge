import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'/'python'))
from train import train
from chat import load,generate

class ByteForgeTests(unittest.TestCase):
 def test_portable_format_and_repeatable_generation(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'model.bfng';p.write_text(train('kernel memory kernel process kernel memory',2),encoding='ascii')
   model=load(p);self.assertEqual(model[0],2);self.assertEqual(generate(model,8),generate(model,8));self.assertTrue(generate(model,5))
 def test_reject_empty_corpus_and_bad_order(self):
  with self.assertRaises(ValueError):train('  ')
  with self.assertRaises(ValueError):train('kernel',0)
 def test_unicode_round_trip(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'unicode.bfng';p.write_text(train('núcleo x86_64 núcleo memoria',1),encoding='ascii');self.assertTrue(generate(load(p),3))
if __name__=='__main__':unittest.main()
