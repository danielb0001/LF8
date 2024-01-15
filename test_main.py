import subprocess
import platform
from datetime import datetime
import time
import os
import psutil
import pandas as pd

class Logging:
    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    # Create the file name
    file_name = './logs/' + current_date + '.csv'
    # Check if the file exists
    if not os.path.isfile(file_name):
        # If the file doesn't exist, create an empty DataFrame and save it as a CSV file
        df = pd.DataFrame([['Zeit', 'CPU Auslastung', 'RAM Auslastung']])
        df.to_csv(file_name, index=False)
        print(f'Created a new CSV file with the name: {file_name}')
    else:
        print(f'A CSV file with the name {file_name} already exists.')
    
    def append_values_to_logfile(self):
        ram = RAM_Nutzung()
        date = datetime.now()
        # Open a CSV file 
        df = pd.read_csv(self.file_name)
        # Append these variables as new columns to the dataframe
        time = date.time().strftime("%H:%M:%S")
        cpu_usage = psutil.cpu_percent(interval=1, percpu=False)
        ram_usage = ram.ram_usage()
        new_row = [time, cpu_usage, ram_usage]
        df.loc[len(df.index)] = new_row
        # Save the updated dataframe back to the CSV file
        df.to_csv(self.file_name, index=False)

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
        process_count = int(proc)
        Logging.append_values_to_log(self,process_count,"Anzahl Prozesse")
        return process_count

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

    def ram_usage(self):
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
            print("WARNUNG! RAM Auslastung hoch:", ram_nutzung, '%')
            ausgabe = "WARNUNG! RAM Auslastung hoch: " + str(ram_nutzung) + ' %'
            return ausgabe
        else:
            print("RAM Auslastung ist in Ordnung und liegt bei:", ram_nutzung, '%')
            ausgabe = "RAM Auslastung ist in Ordnung und liegt bei: " + str(ram_nutzung) + ' %'
            return ausgabe


class CPU_Nutzung:

    def cpu_usage(self):
        anzahl = psutil.cpu_count()
        print('Anzahl logischer Prozessoren:', anzahl)
        usage = psutil.cpu_percent(interval=1, percpu=False)
        return usage

    def cpu_warning(self,cpu_nutzung):
        if cpu_nutzung < 50.0:
            print("CPU Auslastung in Ordnung und liegt bei:", cpu_nutzung, '%')
            ausgabe = "CPU Auslastung in Ordnung und liegt bei: " + str(cpu_nutzung) + ' %'
            return ausgabe
        if cpu_nutzung >= 50.0 and cpu_nutzung < 90.0:
            print("WARNUNG! CPU Auslastung bei:", cpu_nutzung, '%')
            ausgabe = "WARNUNG! CPU Auslastung bei: " + str(cpu_nutzung) + ' %'
            return ausgabe
        if cpu_nutzung >= 90.0:
            print("KRITISCHER BEREICH CPU Auslastung bei:", cpu_nutzung, '%')
            ausgabe = "KRITISCHER BEREICH CPU Auslastung bei:" + str(cpu_nutzung) + '%'
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
        cpu.cpu_warning(cpu.cpu_usage())
        print('-')
        ram.ram_warning(ram.ram_usage())
        print('-')
        dt.date_and_time()
        print("-------------------------------------------------------\n")
        log.append_values_to_logfile()
        time.sleep(3)
        
def test_function():
    assert 5 == 5

def test_CPU_Nutzung():
    nutzung = CPU_Nutzung()
    assert(nutzung.cpu_warning(50) == "WARNUNG! CPU Auslastung bei: 50 %")