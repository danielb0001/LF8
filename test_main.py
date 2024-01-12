import subprocess
import platform
from datetime import datetime
import logging
import time
import psutil


class Prozesse:

    def check_process(self):
        proc = 0
        if platform.system() == "Windows":
            proc = subprocess.check_output("tasklist.exe|find /i \" K\" /c", shell=True)

        elif platform.system() == "Darwin": #für mac benutzer
            proc = subprocess.check_output("ps -A | wc -l", shell=True)
            print(platform.system(), platform.release())

        elif platform.system() == "Linux":
            proc = subprocess.check_output("ps aux | wc -l", shell=True)
        print(platform.system(), platform.release())
        anzahlProc = int(proc)
        return anzahlProc

    def warning_process(self, anzahl):
        if anzahl > 200:
            print("WARNUNG! Anzahl der Prozesse liegt über dem Schwellenwert!", anzahl)
            ausgabe = "WARNUNG! Anzahl der Prozesse liegt über dem Schwellenwert! " + str(anzahl)
            return ausgabe
        else:
            print("Die Anzahl der Prozesse liegt unter dem Schwellenwert! bei:", anzahl)
            ausgabe = "Die Anzahl der Prozesse liegt unter dem Schwellenwert! bei: " + str(anzahl)
            return ausgabe


class RAM_Nutzung:

    def ram_total(self):
        vvm = psutil.virtual_memory()
        RAM_total = round(vvm.total / 1024 / 1024 / 1024, 2)
        RAM_available = round(vvm.available / 1024 / 1024 / 1024, 2)
        nutzung = vvm.percent
        print('Nutzbarer RAM insgesamt:', RAM_total, 'GB')
        print('Verfügbarer RAM:', RAM_available, 'GB')
        return nutzung

    def ram_warning(self, ram_nutzung):
        #ram_nutzung = 61.0
        if ram_nutzung > 60.0:
            print("WARNUNG! RAM Auslastung zu hoch:", ram_nutzung, '%')
            ausgabe = "WARNUNG! RAM Auslastung zu hoch: " + str(ram_nutzung) + ' %'
            return ausgabe
        else:
            print("RAM Auslastung ist in Ordnung und liegt bei:", ram_nutzung, '%')
            ausgabe = "RAM Auslastung ist in Ordnung und liegt bei: " + str(ram_nutzung) + ' %'
            return ausgabe


class CPU_Nutzung:

    def cpu_count(self):
        anzahl = psutil.cpu_count()
        print('Anzahl logischer Prozessoren:', anzahl)
        prozent = psutil.cpu_percent(interval=1, percpu=False)
        return prozent

    def cpu_prozent(cpu_nutzung):
        if cpu_nutzung < 40.0:
            print("CPU Auslastung in Ordnung und liegt bei:", cpu_nutzung, '%')
            ausgabe = "CPU Auslastung in Ordnung und liegt bei: " + str(cpu_nutzung) + ' %'
            return ausgabe
        if cpu_nutzung > 40.0 and cpu_nutzung < 60.0:
            print("WARNUNG! CPU Auslastung zu hoch:", cpu_nutzung, '%')
            ausgabe = "WARNUNG! CPU Auslastung zu hoch: " + str(cpu_nutzung) + ' %'
            return ausgabe
        if cpu_nutzung > 60.0:
            print("KRITISCHER BEREICH! Umgehend Rechner/Server ausschalten!:", cpu_nutzung, '%')
            ausgabe = "KRITISCHER BEREICH! Umgehend Rechner/Server ausschalten! : " + str(cpu_nutzung) + '%'
            return ausgabe


class Date_Time:

    def date_and_time(self):
        date = datetime.now()
        print("Datum:", date.date().strftime("%d %B, %Y"))
        print("Uhrzeit:", date.time().strftime("%H:%M Uhr"))


if __name__ == '__main__':
    prozesse = Prozesse()
    ram_nutzung = RAM_Nutzung()
    cpu_nutzung = CPU_Nutzung()
    date_time = Date_Time()

    while True:
        cpu_auslastung = cpu_nutzung.cpu_count()
        cpu_nutzung.cpu_prozent(cpu_auslastung)
        print('-')
        ram_nutzung.ram_warning(ram_nutzung.ram_total())
        print('-')
        date_time.date_and_time()
        print("-------------------------------------------------------\n")
        time.sleep(3)
        
def test_function():
    assert 5 == 5
    
def test_CPU_Nutzung():
    assert(CPU_Nutzung.cpu_prozent(50) == "WARNUNG! CPU Auslastung zu hoch: 50 %")

# test
    
