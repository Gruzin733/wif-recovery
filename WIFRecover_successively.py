import argparse
import ctypes
import datetime
import random, base58
from time import sleep
import logging
import os
import platform
import secrets
import socket
import string
import sys
import time
from logging import Formatter
from random import choice, randint
import bitcoin
from datetime import datetime
import secp256k1_lib

total_counter = 0
found_counter = 0

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

def createParser ():
    parser = argparse.ArgumentParser(description='WIF Hunt')
    parser.add_argument ('-wif', '--wif', action='store', type=str, help='WIF', default='')
    return parser.parse_args().wif

def convert_int(cou:int):
    if cou < 1000:
        res = cou
        return res,'hash'
    if cou >= 1000 and cou < 1000000:
        res = cou/1000
        return res, 'Khash'
    if cou >= 1000000 and cou < 1000000000:
        res = cou/1000000
        return res, 'Mhash'
    if cou >= 1000000000 and cou < 1000000000000:
        res = cou/1000000000
        return res, 'Ghash'
    if cou >= 1000000000000 and cou < 1000000000000000:
        res = cou/1000000000000
        return res, 'Thash'
    if cou >= 1000000000000000 and cou < 1000000000000000000:
        res = cou/1000000000000000
        return res, 'Phash'

def date_str():
    now = datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")

def bwif(wif):
    global total_counter
    global found_counter
    group_size = 3500
    compr = True
    private_key_WIF = wif

    if (private_key_WIF[:1] == '5') and (len(private_key_WIF) != 51):
        print(f'\n {private_key_WIF} {len(private_key_WIF)}: ОШИБКА ДЛИНЫ WIF 5')
        exit()
    if (private_key_WIF[:1] == 'K') and (len(private_key_WIF) != 52):
        print('ОШИБКА ДЛИНЫ WIF K')
        exit()
    if (private_key_WIF[:1] == 'L') and (len(private_key_WIF) != 52):
        print('ОШИБКА ДЛИНЫ WIF L')
        exit()
    
    if private_key_WIF[:1] != '5': #проверяем какой ключ
        cut = -10
        compr = True
    else:
        cut = -8
        compr = False
    try:
        first_encode = base58.b58decode(private_key_WIF)
    except:
        print(f'\n {first_encode}: ОШИБКА base58.b58decod')
    if first_encode.hex()[:2] != '80': # проверяем верные 2 байта или нет
        print(f'\n {first_encode.hex()}: ОШИБКА 80')
    private_key = first_encode.hex()[2:cut]
    pvk_int = int(private_key,16)
    P = secp256k1_lib.scalar_multiplication(pvk_int)
    current_pvk = pvk_int + 1
    Pv = secp256k1_lib.point_sequential_increment(group_size, P)
    for tmp in range(group_size):
        #print(f'{hex(current_pvk + tmp)}')
        h1601 = secp256k1_lib.pubkey_to_h160(0, compr, Pv[tmp*65:tmp*65+65])
        if (h1601.hex() == 'ef58afb697b094423ce90721fbb19a359ef7c50e'):
            found_counter +=1
            print(f'\n FOUND: {date_str()} PrivateKey={hex(current_pvk + tmp)} Hash = {h1601.hex()}')
            logger_found.info(f'\n FOUND: {date_str()} PrivateKey={hex(current_pvk + tmp)} Hash = {h1601.hex()}')
        total_counter += 1

if __name__ == "__main__":
    wif = createParser()
    if wif == '':
        print(f'[E] пустой WIF')
        exit()

    print('-'*70,end='\n')
    print(f'[I] WIF: {wif}')
    print(f'START: {date_str()}')
    print('-'*70,end='\n')
    

    
    gen1= '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    gen2= '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    gen3= '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    gen4= '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    gen5= '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    gen6= '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    gen7= '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    st = time.time()
    for i1 in gen1:
        tc_float, tc_hash = convert_int(total_counter)
        print(f'{date_str()} Hash: {tc_float:.2f} {tc_hash} | Found: {found_counter}',end='\r')
        st = time.time()
        for i2 in gen2:
            for i3 in gen3:
                for i4 in gen4:
                    for i5 in gen5:
                        for i6 in gen6:
                            for i7 in gen7:
                                src = wif
                                src = src.replace('{1}',i1,1)
                                src = src.replace('{2}',i2,1)
                                src = src.replace('{3}',i3,1)
                                src = src.replace('{4}',i4,1)
                                src = src.replace('{5}',i5,1)
                                src = src.replace('{6}',i6,1)
                                src = src.replace('{7}',i7,1)
                                print(src)
                                bwif(src)
