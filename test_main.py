from main import Logging
from main import Prozesse
from main import RAM_Nutzung
from main import CPU_Nutzung
from main import Date_Time

# Unit Tests, Funktionen werden mit dem Modul pytest auf GitHub Actions ausgeführt. 
 
def test_testfunction():
    assert 5 == 5

def test_CPU_Nutzung():
    nutzung = CPU_Nutzung()
    assert nutzung.cpu_warnung(20) == "CPU Auslastung in Ordnung und liegt bei: 20%"
    assert nutzung.cpu_warnung(70) == "WARNUNG! CPU Auslastung bei: 70%"
    assert nutzung.cpu_warnung(95) == "KRITISCH! CPU Auslastung bei: 95%"
