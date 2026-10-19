"""Escreva seu proprio cache com um decorador.

O `functools.lru_cache` e otimo, mas nao expira: um dado que mudou no banco
continua sendo servido para sempre. Este decorador guarda o resultado por N
segundos e depois recalcula. Em 20 linhas voce entende como decorador com
argumento funciona por dentro.

    python main.py
"""
import functools
import time


def cache_ttl(segundos):
    """Decorador COM argumento = funcao que devolve um decorador."""
    def decorador(func):
        guardado = {}                    # chave: (args, kwargs) -> (valor, quando)

        @functools.wraps(func)           # preserva nome e docstring de func
        def envolve(*args, **kwargs):
            chave = (args, tuple(sorted(kwargs.items())))
            agora = time.time()
            if chave in guardado:
                valor, quando = guardado[chave]
                if agora - quando < segundos:
                    return valor         # ainda vale: nem chama func
            valor = func(*args, **kwargs)
            guardado[chave] = (valor, agora)
            return valor

        envolve.limpar = guardado.clear  # bonus: cache.limpar() na mao
        return envolve
    return decorador


@cache_ttl(segundos=2)
def cotacao(moeda):
    print(f"  (buscando {moeda} na API...)")
    time.sleep(1)                        # finge a latencia da rede
    return 5.55 if moeda == "USD" else 6.10


if __name__ == "__main__":
    inicio = time.time()
    for _ in range(3):
        print(cotacao("USD"), f"{time.time() - inicio:.1f}s")
    print("esperando o cache expirar...")
    time.sleep(2)
    print(cotacao("USD"), f"{time.time() - inicio:.1f}s")
