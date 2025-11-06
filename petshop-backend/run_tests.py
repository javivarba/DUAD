import pytest
import sys

def run_tests():
    """
    Script para ejecutar todos los tests automáticamente
    Genera un reporte de cobertura
    """
    args = [
        'tests/',                    # Directorio de tests
        '-v',                        # Verbose
        '--cov=app',                 # Cobertura del código en app/
        '--cov-report=html',         # Reporte HTML
        '--cov-report=term-missing', # Reporte en terminal
    ]
    
    exit_code = pytest.main(args)
    
    if exit_code == 0:
        print("\n✅ Todos los tests pasaron exitosamente!")
    else:
        print("\n❌ Algunos tests fallaron. Revisa el reporte arriba.")
    
    return exit_code

if __name__ == '__main__':
    sys.exit(run_tests())