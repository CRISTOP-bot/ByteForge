import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'/'python'))
from train import train
from chat import load,generate,tokenize,detokenize

class ByteForgeTests(unittest.TestCase):
 def test_portable_format_and_repeatable_generation(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'model.bfng';p.write_text(train('kernel memory kernel process kernel memory',2),encoding='ascii')
   model=load(p);self.assertEqual(model[0],2);self.assertEqual(generate(model,8),generate(model,8));self.assertTrue(generate(model,5))
 def test_prompt_guides_generation(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'model.bfng';p.write_text(train('kernel memory kernel memory driver interrupt driver interrupt',1),encoding='ascii')
   model=load(p);self.assertTrue(generate(model,3,'kernel').startswith('kernel'))
 def test_unknown_prompt_is_safe(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'model.bfng';p.write_text(train('kernel memory kernel memory',1),encoding='ascii')
   self.assertTrue(generate(load(p),2,'unknown-topic').startswith('unknown - topic'))
 def test_training_is_reproducible_and_comments_are_ignored(self):
  self.assertEqual(train('# note\nkernel memory kernel'),train('kernel memory kernel'))
  self.assertEqual(train('kernel memory kernel',2),train('kernel memory kernel',2))
 def test_order_changes_model_header(self):
  self.assertIn('BYTEFORGE_NGRAM_V1\t3\t',train('kernel memory process',3))
 def test_generation_stops_at_example_boundary(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'model.bfng';p.write_text(train('kernel memory\ndriver interrupt',1),encoding='ascii')
   self.assertEqual(generate(load(p),10,'kernel'),'kernel memory')
 def test_eos_token_is_reserved(self):
  with self.assertRaises(ValueError):train('kernel __BYTEFORGE_EOS__ memory',1)
 def test_prompt_tokenization_matches_training_punctuation(self):
  self.assertEqual(tokenize('¿Cómo va el kernel?'),['¿','Cómo','va','el','kernel','?'])
  self.assertEqual(detokenize(['¿','Cómo','va','el','kernel','?']),'¿Cómo va el kernel?')
 def test_prompt_with_punctuation_is_safe(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'model.bfng';p.write_text(train('¿Cómo funciona el kernel?',1),encoding='ascii')
   self.assertTrue(generate(load(p),4,'¿Cómo funciona').startswith('¿Cómo funciona'))
 def test_reject_empty_corpus_and_bad_order(self):
  with self.assertRaises(ValueError):train('  ')
  with self.assertRaises(ValueError):train('kernel',0)
  with self.assertRaises(ValueError):train('kernel',9)
 def test_unicode_round_trip(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'unicode.bfng';p.write_text(train('núcleo x86_64 núcleo memoria',1),encoding='ascii');self.assertTrue(generate(load(p),3))
if __name__=='__main__':unittest.main()
