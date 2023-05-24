# import subprocess
# import time

# def standby_mac():
#     # Comando per mettere in standby il Mac
#     command = "pmset sleepnow"
    
#     # Esecuzione del comando utilizzando subprocess
#     subprocess.call(command, shell=True)

# # Ritardo di 15 minuti
# time.sleep(900)  # 900 secondi = 15 minuti

# # Chiamata alla funzione per mettere in standby il Mac
# standby_mac()




import subprocess

# Resto del tuo codice...

# Alla fine dello script:
subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'])


