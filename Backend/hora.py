import time
from datetime import datetime
print ("Iniciando el script...")
while True:
    ahora = datetime.now().strftime("%H:%M:%S")
    print(f"Hora actual: {ahora}")
    time.sleep(60)