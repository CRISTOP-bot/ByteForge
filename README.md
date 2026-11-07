# ByteForge

**ByteForge** es un modelo diminuto para aprender programación de sistemas y desarrollo de sistemas operativos: kernels, memoria, procesos, drivers, ABI, toolchains, pruebas y depuración.

Es un modelo de lenguaje n-grama de tokens entrenado desde cero. No es un transformer, no comprende ni verifica código, y puede inventar respuestas o producir fragmentos incorrectos. Revisa, compila y prueba cualquier salida; no lo uses para producción ni decisiones de seguridad.

## Entrenar y probar

Requiere Python 3.10+ y no instala paquetes:

```sh
python train.py
python chat.py --prompt "kernel memory" --length 24
python -m unittest discover -s tests -v
```

El corpus educativo está en `data/corpus.txt` (CC0). Inspecciona calidad/licencias antes de ampliarlo. El entrenamiento produce `model.bfng`, un archivo de texto en formato compartido documentado en `docs/model-format.md`.

## Runtimes

Los lectores C11, C++17, Rust, Go, Java 17+ y JavaScript (Node 20+) consumen el mismo modelo y generan con una regla determinista. Python es el entrenador canónico y runtime de referencia. NASM aporta una rutina x86-64 real para seleccionar una frecuencia; no se presenta como un runtime ni como el modelo completo. No son siete modelos distintos.

Ejemplos desde la raíz del repo tras entrenar:

```sh
cc -std=c11 -O2 src/c/byteforge.c -o byteforge-c && ./byteforge-c model.bfng 12
c++ -std=c++17 -O2 src/cpp/byteforge.cpp -o byteforge-cpp && ./byteforge-cpp model.bfng 12
(cd src/rust && cargo run --release -- ../../model.bfng 12)
(cd src/go && go run . ../../model.bfng 12)
(cd src/java && javac ByteForge.java && java ByteForge ../../model.bfng 12)
node src/js/byteforge.mjs model.bfng 12
```

## CI y límites de verificación

GitHub Actions entrena el modelo, corre pruebas, instala/compila los toolchains y compara la salida de los runtimes. El estado del workflow es la evidencia para las implementaciones remotas; que un archivo fuente exista no significa que ya esté compilado. En el entorno local de creación no hay compiladores ni runtimes de C, ASM, Rust, Go, Java o Node disponibles; solo pude ejecutar y probar Python aquí.

Licencia del código: MIT (`LICENSE`). Licencia del corpus de ejemplo: CC0-1.0 (`data/LICENSE`).