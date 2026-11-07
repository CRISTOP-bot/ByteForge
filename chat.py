#!/usr/bin/env python3
"""Generate text with the tiny model trained by train.py."""
import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def generate(model: dict, prompt: str = "", length: int = 180, seed: int | None = None) -> str:
    rng = random.Random(seed)
    order = model["order"]
    text = prompt or " " * order
    for _ in range(length):
        context = text[-order:]
        options = model["contexts"].get(context)
        if not options:
            shorter = context
            while shorter and not options:
                shorter = shorter[1:]
                options = model["contexts"].get(shorter)
        if not options:
            options = {" ": 1}
        chars, weights = zip(*options.items())
        text += rng.choices(chars, weights=weights, k=1)[0]
    return text[len(prompt):].strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, default=ROOT / "model.json")
    parser.add_argument("--prompt", default="")
    parser.add_argument("--length", type=int, default=180)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    model = json.loads(args.model.read_text(encoding="utf-8"))
    print(generate(model, args.prompt, args.length, args.seed))


if __name__ == "__main__":
    main()
