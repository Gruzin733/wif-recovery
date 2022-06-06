#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Noname400
"""

from consts import *

def send_telegram(text: str):
    try:
        requests.get('https://api.telegram.org/bot{}/sendMessage'.format(telegram.token), params=dict(
        chat_id=telegram.channel_id,
        text=text))
        sleep(20)
    except:
        print(f'{red}[E] Error send telegram.')
        logger_err.error(f'[E] Error send telegram.')
        if inf.telegram_err > 3 : 
            inf.telegram == False
            return
        else: 
            inf.telegram_err += 1
            sleep(10)
            return send_telegram(text)

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
    
def reverse_string(s):
    return s[::-1]

def get_balance(address,cyr):
    time.sleep(11) 
    if cyr == 'ETH':
        try:
            response = requests.get(inf.ETH_bal_server[1] + '0x' + address)
            return int(response.json()['result'])
        except:
            print('[E][ETH] NOT connect balance server')
            logger_err.error('[E][ETH] NOT connect balance server')
            return -1
    else:
        try:
            if inf.bal_srv_count == 0:
                response = requests.get(inf.bal_server[inf.bal_srv_count] + str(address))
                return int(response.json()['n_tx']), float(response.json()['balance'])
            elif inf.bal_srv_count == 1:
                response = requests.get(inf.bal_server[inf.bal_srv_count] + str(address))
                return int(response.json()['txApperances']), float(response.json()['balance'])
            elif inf.bal_srv_count == 2:
                response = requests.get(inf.bal_server[inf.bal_srv_count] + str(address))
                return int(response.json()['data']['total_txs']), float(response.json()['data']['balance'])
            elif inf.bal_srv_count == 3:
                response = requests.get(inf.bal_server[inf.bal_srv_count] + str(address))
                return int(response.json()['n_tx']), float(response.json()['final_balance'])
        except:
            logger_err.error('[E][BTC, 44, 32] NOT connect balance server')
            print('[E][BTC, 44, 32] NOT connect balance server')
            if inf.bal_err < 10:
                inf.bal_err += 1
            else:
                if inf.bal_srv_count < 3:
                    inf.bal_srv_count += 1
                else:
                    inf.bal_srv_count = 0
            inf.bal_all_err += 1
            if inf.bal_all_err == 40:
                inf.balance = False
            return -1

def load_BF(load):
    try:
        fp = open(load, 'rb')
    except FileNotFoundError:
        print(f'{red}[E] File: {load} not found.')
        logger_err.error(f'[E] File: {load} not found.')
        sys.exit()
    else:
        n_int = int(multiprocessing.current_process().name)
        time.sleep(inf.delay*n_int)
        return BloomFilter.load(fp)    
    
def gen(rep):
    if rep == '{A}':
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        return random.choice(alphabet)
    elif rep == '{1}':
        alphabet = 'KL'
        return random.choice(alphabet)
    elif rep == '{2}':
        alphabet = 'wxyz12345'
        return random.choice(alphabet)
    elif rep == '{3}':
        alphabet = 'xn'
        return random.choice(alphabet)
    elif rep == '{4}':
        alphabet = 'eoaq'
        return random.choice(alphabet)
    elif rep == '{5}':
        alphabet = '17'
        return random.choice(alphabet)
    elif rep == '{6}':
        alphabet = 'rnhm'
        return random.choice(alphabet)
    elif rep == '{7}':
        alphabet = 'rnx'
        return random.choice(alphabet)
    elif rep == '{8}':
        alphabet = ''
        return random.choice(alphabet)
    elif rep == '{9}':
        alphabet = ''
        return random.choice(alphabet)
    elif rep == '{10}':
        alphabet = ''
        return random.choice(alphabet)
    elif rep == '{11}':
        alphabet = ''
        return random.choice(alphabet)
    
def date_str():
    now = datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")

def bwif(wif,fc):
    er = 0
    co = 0
    compr = False
    group_size = 1
   
    for pars in range(20):
        if wif.find('{') > -1: 
            pos = wif.find('{')
            cu = wif[pos:pos+3]
            #print(cu)
            if wif.find(cu) > -1:
                wif = wif.replace(cu, gen(cu),1)
                #print(cu,wif)
            if wif.find('{A}') > -1:
                wif = wif.replace('{A}',gen('{A}'),1)
            #print(wif)
            
    private_key_WIF = (wif)

    if (private_key_WIF[:1] == '5') and (len(private_key_WIF) != 51):
        print(f'\n {private_key_WIF} {len(private_key_WIF)}: ОШИБКА ДЛИНЫ WIF 5')
    if (private_key_WIF[:1] == 'K') and (len(private_key_WIF) != 52):
        print('ОШИБКА ДЛИНЫ WIF K')
    if (private_key_WIF[:1] == 'L') and (len(private_key_WIF) != 52):
        print('ОШИБКА ДЛИНЫ WIF L')
    
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
        #print(f'\n {first_encode.hex()}: ОШИБКА 80')
        return None
    private_key = first_encode.hex()[2:cut]
    pvk_int = int(private_key,16)
    P = secp256k1_lib.scalar_multiplication(pvk_int)
    current_pvk = pvk_int + 1
    Pv = secp256k1_lib.point_sequential_increment(group_size, P)
    for tmp in range(group_size):
        #print(f'{hex(current_pvk + tmp)}')
        h1601 = secp256k1_lib.pubkey_to_h160(0, compr, Pv[tmp*65:tmp*65+65])
        if (h1601.hex() == 'f894ae393519664b55749b372f53d61f42253e13') or (h1601.hex() in inf.bf):
            fc.increment(1)
            print(f'\n FOUND: {date_str()} PrivateKey={hex(current_pvk + tmp)} Hash = {h1601.hex()}')
            logger_found.info(f'\n FOUND: {date_str()} PrivateKey={hex(current_pvk + tmp)} Hash = {h1601.hex()}')
        co += 1
    return co