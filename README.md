# PapuuAI

Un modelo de lenguaje diminuto en español, entrenado desde cero con Python puro y un corpus de ejemplo incluido. No descarga ni reutiliza pesos de otros modelos.

## Qué es y qué no es

PapuuAI es un modelo educativo de caracteres basado en frecuencias de n-gramas (contextos de 4 caracteres). Durante el entrenamiento cuenta qué carácter aparece después de cada contexto; al generar, elige caracteres según esas frecuencias. No comprende preguntas, no razona y puede producir texto incoherente. No es comparable con un asistente moderno ni está destinado a decisiones importantes.

## Ejecutar

Necesita Python 3.10 o posterior; no requiere paquetes externos.

```sh
python train.py
python chat.py --prompt "Hola" --length 180 --seed 7
```

Cambia `data/corpus.txt` para experimentar y vuelve a ejecutar `python train.py`. El modelo generado se guarda en `model.json`.

## Pruebas

```sh
python -m unittest discover -s tests -v
```

GitHub Actions ejecuta las pruebas, entrena el modelo y comprueba una generación en cada push y pull request. El entrenamiento es pequeño y corre en CPU.

## Estructura

- `train.py`: cuenta los patrones del corpus y serializa el modelo.
- `chat.py`: genera texto usando el modelo entrenado.
- `data/corpus.txt`: corpus de demostración editable.
- `tests/`: pruebas automáticas básicas.

## Licencia

MIT. Consulta `LICENSE`.
