# #!/usr/bin/python3
# encoding=utf8
# -*- coding: utf-8 -*-
"""
@author: Noname400
"""

from funcP import *
from consts import *

def createParser ():
    parser = argparse.ArgumentParser(description='WIF Hunt')
    parser.add_argument ('-db', '--database', action='store', type=str, help='File BF', default='')
    parser.add_argument ('-th', '--threading', action='store', type=int, help='threading', default='1')
    parser.add_argument ('-wif', '--wif', action='store', type=str, help='WIF', default='')
    parser.add_argument ('-sl', '--sleep', action='store', type=int, help='pause start (sec)', default='5')
    parser.add_argument ('-bal', '--balance', action='store_true', help='check balance')
    parser.add_argument ('-telegram', '--telegram', action='store_true', help='send telegram')
    return parser.parse_args().database, parser.parse_args().threading, parser.parse_args().wif, parser.parse_args().sleep, parser.parse_args().balance, parser.parse_args().telegram

def run(*args):
    inf.db = args[0]
    inf.th = args[1]
    inf.wif = args[2]
    inf.delay = args[3]
    inf.balance = args[4]
    inf.telegram = args[5]
    total_counter = args[6]
    process_counter = args[7]
    found_counter = args[8]

    tc = 0
    ind:int = 1

    inf.bf = load_BF(inf.db)
    process_counter.increment(1)
    cc1 = 0
    try:
        while True:
            pp = multiprocessing.current_process()
            if pp.is_alive():
                pass
            else:
                process_counter.decrement(1)
            start_time = time.time()
            it = bwif(inf.wif, found_counter)
            if it == None: continue
            total_counter.increment(it)
            st = time.time() - start_time
            ftc = tc
            tc = total_counter.value()
            tc_float, tc_hash = convert_int(tc)
            btc = tc - ftc
            try:
                speed = int((btc/st))
            except ZeroDivisionError:
                speed = 1234
            speed_float, speed_hash = convert_int(speed)
            fc = found_counter.value()
            pc = process_counter.value()
            if multiprocessing.current_process().name == '0':
                if cc1 == 100:
                    print(f'{yellow}> Cores:{pc} | Hash: {tc_float:.2f} {tc_hash} | {speed_float:.2f} {speed_hash} | Found: {fc}',end='\r')
                    cc1 = 0
            inf.count = 0
            cc1+=1
            ind += 1
    except(KeyboardInterrupt, SystemExit):
        print('\n[EXIT] Interrupted by the user.')
        logger_info.info('[EXIT] Interrupted by the user.')
        sys.exit()

if __name__ == "__main__":
    inf.db, inf.th, inf.wif, inf.delay, inf.balance, inf.telegram = createParser()
    if inf.wif == '':
        print(f'{red}[E] пустой WIF')
        logger_err.error(('[E] пустой WIF'))
        sys.exit()

    if inf.th < 1:
        print(f'{red}[E] The number of processes must be greater than 0')
        logger_err.error(('[E] The number of processes must be greater than 0'))
        sys.exit()

    if inf.th > multiprocessing.cpu_count():
        print(f'{red}[I] The specified number of processes exceeds the allowed')
        print(f'{green}[I] FIXED for the allowed number of processes')
        inf.th = multiprocessing.cpu_count()

    print('-'*70,end='\n')
    print(f'[I] Version: {inf.version}')
    logger_info.info(f'Start {inf.version}')
    print(f'[I] Total kernel of CPU: {multiprocessing.cpu_count()}')
    print(f'[I] Used kernel: {inf.th}')
    print(f'[I] WIF: {inf.wif}')
    print(f'[I] Bloom Filter : {inf.db}')
    print(f'[I] Smooth start {inf.delay} sec')

    if inf.balance: print('[I] Check balance BTC: On')
    else: print('[I] Check balance: Off')
    if inf.telegram: print('[I] Telegram: On')
    else: print('[I] Telegram: Off')
    print(f'START: {date_str()}')
    print('-'*70,end='\n')
    
    total_counter = Counter(0)
    process_counter = Counter(0)
    brain_counter = Counter(0)
    found_counter = Counter(0)
    mnem_counter = Counter(0)

    procs = []
    try:
        for r in range(inf.th): 
            p = Process(target=run, name= str(r), args=(inf.db, inf.th, inf.wif, inf.delay, inf.balance, inf.telegram, total_counter, process_counter, brain_counter, found_counter, mnem_counter,))
            procs.append(p)
            p.start()
        for proc in procs: proc.join()
    except(KeyboardInterrupt, SystemExit):
        print('\n[EXIT] Interrupted by the user.')
        logger_info.info('[EXIT] Interrupted by the user.')
        sys.exit()