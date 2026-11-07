#!/usr/bin/env python3
"""Train a tiny character n-gram language model from scratch."""
import argparse
from collections import defaultdict
import json
from pathlib import Path

ORDER = 4
ROOT = Path(__file__).resolve().parent


def train(text: str, order: int = ORDER) -> dict:
    text = text.strip()
    if not text:
        raise ValueError("Training corpus is empty")
    counts = defaultdict(lambda: defaultdict(int))
    padded = " " * order + text + " "
    for i in range(order, len(padded)):
        context, next_char = padded[i - order:i], padded[i]
        counts[context][next_char] += 1
    return {
        "format": "papuu-char-ngram-v1",
        "order": order,
        "characters_seen": len(text),
        "contexts": {ctx: dict(freqs) for ctx, freqs in counts.items()},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=ROOT / "data/corpus.txt")
    parser.add_argument("--output", type=Path, default=ROOT / "model.json")
    args = parser.parse_args()
    model = train(args.corpus.read_text(encoding="utf-8"))
    args.output.write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Entrenado: {model['characters_seen']} caracteres, {len(model['contexts'])} contextos -> {args.output}")


if __name__ == "__main__":
    main()
