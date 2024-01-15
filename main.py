"""Gibt Systemparameter aus und speichert sie in Logdatei
"""
import subprocess
import platform
from datetime import datetime
import time
import os
import psutil
import pandas as pd

class Logging:
    """KLasse um Logs zu erstellen
    """
    # Erzeuge String mit aktuellem Datum
    current_date = datetime.now().strftime('%Y-%m-%d')
    # definiere Dateinamen mit Pfad
    dateipfad = './logs/' + current_date + '.csv'
    # Cecke ob die Date bereits existiert
    if not os.path.isfile(dateipfad):
        # Falls Datei nicht existiert, erstelle einen leeren DataFrame und speichere ihn als CSV 
        df = pd.DataFrame([['Zeit', 'CPU Auslastung', 'RAM Auslastung']])
        df.to_csv(dateipfad, index=False)
        print(f'Datei mit dem Pfad {dateipfad} erstellt.')
    else:
        print(f'Eine Datei mit dem Pfad {dateipfad} existiert bereits.')
    
    def update_logdatei(self):
        """liest aktuelle Werte aus und speichert sie in Logdatei
        """
        ram = RAM_Nutzung()
        datum = datetime.now()
        # Öffne CSV Datei 
        df = pd.read_csv(self.dateipfad)
        # Füge Monitorwerte der Logdatei hinzu
        zeit = datum.time().strftime("%H:%M:%S")
        cpu_nutzung = psutil.cpu_percent(interval=1, percpu=False)
        ram_nutzung = ram.ram_nutzung()
        df.loc[len(df.index)] = [zeit, cpu_nutzung, ram_nutzung]
        # Save the updated dataframe back to the CSV file
        df.to_csv(self.dateipfad, index=False)

class Prozesse:
    """im jetzigen Zustand nicht benutzt, da nur bedingt aussagekräftiger Wert
    """
    def check_prozesse(self):
        proc = 0
        if platform.system() == "Windows":
            proc = subprocess.check_output("tasklist.exe|find /i \" K\" /c", shell=True)

        elif platform.system() == "Darwin": #für mac benutzer
            proc = subprocess.check_output("ps -A | wc -l", shell=True)
            print(platform.system(), platform.release())

        elif platform.system() == "Linux":
            proc = subprocess.check_output("ps aux | wc -l", shell=True)
        print(platform.system(), platform.release())
        process_count = int(proc)
        return process_count

    def warnung_prozesse(self, anzahl):
        if anzahl > 200:
            ausgabe = "WARNUNG! Anzahl der Prozesse liegt über dem Schwellenwert! bei: " + str(anzahl)
            return ausgabe
        ausgabe = "Die Anzahl der Prozesse liegt unter dem Schwellenwert! bei: " + str(anzahl)
        return ausgabe


class RAM_Nutzung:
    """RAM Nutzungs Funktionen
    """
    def ram_nutzung(self):
        """Gibt verfügbaren und benutzten Ram aus.
        
        Returns:
            float: Nutzung in Prozent
        """
        vvm = psutil.virtual_memory()
        ram_total = round(vvm.total / 1024 / 1024 / 1024, 2)
        ram_verfugbar = round(vvm.available / 1024 / 1024 / 1024, 2)
        nutzung = vvm.percent
        print('Nutzbarer RAM insgesamt:', ram_total, 'GB')
        print('Verfügbarer RAM:', ram_verfugbar, 'GB')
        return nutzung

    def ram_warnung(self, ram_nutzung):
        """Gibt je nach Nutzung unterschiedliche Warnungen aus.

        Args:
            ram_nutzung (float): bekommt Wert normalerweise von self.ram_nutzung

        Returns:
            str: Ausgabetext
        """
        if ram_nutzung > 85.0:
            ausgabe = "WARNUNG! RAM Auslastung bei: " + str(ram_nutzung) + '%'
            print(ausgabe)
            return ausgabe
        ausgabe = "RAM Auslastung ist in Ordnung und liegt bei: " + str(ram_nutzung) + '%'
        print(ausgabe)
        return ausgabe


class CPU_Nutzung:
    """CPU Nutzungs Funktionen 
    """
    def cpu_nutzung(self):
        """Gibt Anzahl der logischen Prozessoren aus.

        Returns:
            float: Nutzung in Prozent 
        """
        anzahl = psutil.cpu_count()
        print('Anzahl logischer Prozessoren:', anzahl)
        nutzung = psutil.cpu_percent(interval=1, percpu=False)
        return nutzung

    def cpu_warnung(self,cpu_nutzung):
        """Gibt je nach Nutzung unterschiedliche Warnungen aus.

        Args:
            cpu_nutzung (float):  bekommt Wert normalerweise von self.cpu_nutzung

        Returns:
            str: Ausgabetext
        """
        if cpu_nutzung < 60.0:
            ausgabe = "CPU Auslastung in Ordnung und liegt bei: " + str(cpu_nutzung) + '%'
            print(ausgabe)
            return ausgabe
        if 60.0 < cpu_nutzung < 90.0:
            ausgabe = "WARNUNG! CPU Auslastung bei: " + str(cpu_nutzung) + '%'
            print(ausgabe)
            return ausgabe
        if cpu_nutzung >= 90.0:
            ausgabe = "KRITISCH! CPU Auslastung bei: " + str(cpu_nutzung) + '%'
            print(ausgabe)
            return ausgabe


class Date_Time:
    def date_and_time(self):
        date = datetime.now()
        print("Datum:", date.date().strftime("%d %B, %Y"))
        print("Uhrzeit:", date.time().strftime("%H:%M Uhr"))


if __name__ == '__main__':
    # proz = Prozesse()
    cpu = CPU_Nutzung()
    ram = RAM_Nutzung()
    dt = Date_Time()
    log = Logging()

    while True:
        cpu.cpu_warnung(cpu.cpu_nutzung())
        print('-')
        ram.ram_warnung(ram.ram_nutzung())
        print('-')
        dt.date_and_time()
        print("-------------------------------------------------------\n")
        log.update_logdatei()
        time.sleep(3)