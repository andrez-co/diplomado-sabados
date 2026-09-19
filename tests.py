from src.calculadora import Calculadora, sumar


# Prueba Unitaria
def test_sumar():
    assert sumar(2, 3) == 5


# Prueba de Integración
def test_integracion_calculadora():
    calc = Calculadora()
    resultado = calc.operar(10, 5)
    assert resultado == 15
