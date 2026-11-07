import unittest
from train import train
from chat import generate


class TinyModelTests(unittest.TestCase):
    def test_training_records_contexts(self):
        model = train("hola hola")
        self.assertEqual(model["format"], "papuu-char-ngram-v1")
        self.assertGreater(len(model["contexts"]), 0)

    def test_generation_is_repeatable_with_seed(self):
        model = train("hola mundo. hola papuu.")
        self.assertEqual(generate(model, "hola", 24, 7), generate(model, "hola", 24, 7))

    def test_empty_corpus_rejected(self):
        with self.assertRaises(ValueError):
            train("  ")


if __name__ == "__main__":
    unittest.main()
