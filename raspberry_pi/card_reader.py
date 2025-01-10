#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO
from config import *  # pylint: disable=unused-wildcard-import
from mfrc522 import MFRC522
from datetime import datetime
import requests

terminal_id = "T0"
host = "http://localhost:8080/"
endpoint_name='enterance'


flag = True

def rfidRead():
        global flag
        global card

        MIFAREReader = MFRC522()

        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK and flag:
                (status, uid) = MIFAREReader.MFRC522_Anticoll()
                if status == MIFAREReader.MI_OK:
                    flag = False

                    num = 0
                    for i in range(0, len(uid)):
                        num += uid[i] << (i*8)
                    #print(f"Card read UID: {uid} > {num}")

                    card = f"{num}"
                    call_worker(card)

        elif not status == MIFAREReader.MI_OK:
            flag=True
 


def main_loop():
    while True:
        rfidRead()



def call_worker(worker_id):
    print({'terminal_id':terminal_id,
                     'worker_id':worker_id
                     })
    
    requests.post(host+endpoint_name,json = {'terminal_id':terminal_id,
                     'worker_id':worker_id
                     })


if __name__ == '__main__':
    main_loop()