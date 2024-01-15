from main import Logging
from main import Prozesse
from main import RAM_Nutzung
from main import CPU_Nutzung
from main import Date_Time

# Unit Tests, Funktionen werden mit dem Modul pytest auf GitHub Actions ausgeführt. 
 
def test_testfunction():
    assert 5 == 5

def test_CPU_Nutzung():
    cpu = CPU_Nutzung()
    assert cpu.cpu_warnung(20) == "CPU Auslastung in Ordnung und liegt bei: 20%"
    assert cpu.cpu_warnung(70) == "WARNUNG! CPU Auslastung bei: 70%"
    assert cpu.cpu_warnung(95) == "KRITISCH! CPU Auslastung bei: 95%"

def test_RAM_Nutzung():
    ram = RAM_Nutzung()
    assert ram.ram_warnung(50) == "RAM Auslastung ist in Ordnung und liegt bei: 50%"
    assert ram.ram_warnung(90) == "WARNUNG! RAM Auslastung hoch: 90%"