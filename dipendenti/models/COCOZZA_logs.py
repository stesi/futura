import os
import datetime

def PRINT(text):
    print(str(text))
    with open('LOGS.txt', 'a') as f:
        f.write(str(text))


# Inizio log
def START_LOGS():
    PRINT("\n\n****************************************\n****************************************\n\nDATA E ORA ATTUALE: " + str(datetime.datetime.now()) + " - FILE IN ESECUZIONE: " + str(os.path.basename(__file__)) + "\n\n\n")

