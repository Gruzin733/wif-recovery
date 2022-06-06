# #!/usr/bin/python3
# encoding=utf8
# -*- coding: utf-8 -*-
"""
@author: Noname400
"""

import argparse
import ctypes
import datetime
import random, base58
from time import sleep
import logging
import multiprocessing
import os
import platform
import secrets
import smtplib
import socket
import string
import sys
import time
from logging import Formatter
from multiprocessing import Lock, Process, Value
from random import choice, randint
import bitcoin
import requests
from bip32 import BIP32
from bloomfilter import BloomFilter
from colorama import Back, Fore, Style, init
from mnemonic import Mnemonic
from datetime import datetime

import secp256k1_lib

init(autoreset = True)

yellow = Fore.YELLOW+Style.BRIGHT
red = Fore.RED+Style.BRIGHT
#clear = Style.RESET_ALL
green = Fore.GREEN+Style.BRIGHT

current_path = os.path.dirname(os.path.realpath(__file__))
logger_found = logging.getLogger('FOUND')
logger_found.setLevel(logging.INFO)
handler_found = logging.FileHandler(os.path.join(current_path, 'found.log'), 'a' , encoding ='utf-8')
handler_found.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger_found.addHandler(handler_found)

logger_info = logging.getLogger('INFO')
logger_info.setLevel(logging.INFO)
handler_info = logging.FileHandler(os.path.join(current_path, 'info.log'), 'a' , encoding ='utf-8')
handler_info.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger_info.addHandler(handler_info)

logger_dbg = logging.getLogger('DEBUG')
logger_dbg.setLevel(logging.DEBUG)
handler_dbg = logging.FileHandler(os.path.join(current_path, 'debug.log'), 'w' , encoding ='utf-8')
logger_dbg.addHandler(handler_dbg)

logger_err = logging.getLogger('ERROR')
logger_err.setLevel(logging.DEBUG)
handler_err = logging.FileHandler(os.path.join(current_path, 'error.log'), 'w' , encoding ='utf-8')
handler_err.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger_err.addHandler(handler_err)

class Counter:
    def __init__(self, initval=0):
        self.val = Value(ctypes.c_longlong, initval)
        self.lock = Lock()
    def increment(self, nom):
        with self.lock:
            self.val.value += nom
    def decrement(self, nom):
        with self.lock:
            self.val.value -= nom
    def zero(self):
        with self.lock:
            self.val.value = 0
    def value(self):
        with self.lock:
            return self.val.value

class telegram:
    token = '5097432912:AAE6iDOa-q1Q2BWkHQF5o-qjMiM_Ra0ioIQ'
    channel_id = '@mnemonicHUNT'

class inf:
    version:str = '* WIF HUNT v2.1.0 *'
    #general
    th:int = 1 #number of processes
    bf:BloomFilter
    db:str = ''
    wif:str = ''
    balance:bool = False
    bal_err:int = 0
    bal_server:list = ['https://api.blockcypher.com/v1/btc/main/addrs/', 'https://rest.bitcoin.com/v2/address/details/', 'https://sochain.com/api/v2/address/BTC/', \
        'https://blockchain.info/rawaddr/']
    bal_srv_count:int = 0
    bal_all_err = 0
    #telegram
    telegram = False
    telegram_err = 0
    count:int = 1
    count_nem = 0
    dt_now:str = ''
    delay:int = 5
    work_time:float = 0.0
    mode:str = ''
    mode_text:str = ''






