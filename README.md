# Cache com TTL em um decorador

`functools.lru_cache` nunca expira. Este decorador guarda o resultado de uma
função por N segundos e depois recalcula.

```
python main.py
```

O que o exemplo ensina:

- **Decorador com argumento** é uma função que devolve um decorador. Por isso
  são três níveis: `cache_ttl(segundos)` → `decorador(func)` → `envolve(*args)`.
- O dicionário `guardado` vive na closure: cada função decorada tem o seu.
- `functools.wraps` preserva `__name__` e `__doc__` da função original.
- A chave inclui os kwargs ordenados, então `f(a=1, b=2)` e `f(b=2, a=1)`
  caem na mesma entrada.

Publicado pelo [@python_brasil](https://instagram.com/python_brasil).
