

def log_parametros_y_retorno(func):
    def wrapper(*args, **kwargs):
        print(f"Llamando a: {func.__name__}")
        print(f"Parámetros posicionales (args): {args}")
        print(f"Parámetros nombrados (kwargs): {kwargs}")
        resultado = func(*args, **kwargs)
        print(f"Retorno: {resultado}")
        return resultado
    return wrapper

@log_parametros_y_retorno
def sumar(a, b):
    return a + b

sumar(5, 3)
