# -*- coding: utf-8 -*-

from .logwr import logging
import time 
from datetime import datetime
import asyncio


def balance_mode(func):

    def wrapper(*args, **kwargs):

        r = func(*args, **kwargs)
        new_resp = []
        for resp in r: 
            if "ACCESS_BALANCE" in resp[-1]:
                balance = resp[-1].split(":")[-1]
                if float(balance) > 0:
                    new_resp.append( (resp[0], float(balance)) )
                else:
                    new_resp.append( (resp[0],"NO MONEY") )
            else:
                new_resp.append(resp)

        if "NO MONEY" in [ i[1] for i in new_resp ]:
            return "Need to put money on the balance"
        else:
            return new_resp[-1][1]

    return wrapper


def get_avaible_service_mode(func):

    def wrapper(*args, **kwargs):

        r = func(*args, **kwargs)
        if type(r[-1][1]) == dict:
            return list(r[-1][1]) 
        else:
            return r[-1][1]
    return wrapper

def get_count_number_mode(func):

    def wrapper(*args, **kwargs):

        r = func(*args, **kwargs)
        if args[1] in r[-1][1]:
            return int(r[-1][1].get(args[1], "Service not found"))
        else:
            return r[-1]
    return wrapper


def get_number_mode(func):

    def wrapper(*args, **kwargs):

        r = func(*args, **kwargs)
        new_resp = []
        for resp in r:  
        
            if 'ACCESS_NUMBER' in resp[-1]:
                id_, number = resp[-1].split(':')[1:]
                new_resp.append((resp[0], int(id_), number,))
            else:
                new_resp.append(resp)
        
        logging.info(f"Results from get_number_mode {new_resp}")
        return new_resp

    return wrapper


def set_status_activation_mode(func):

    def wrapper(*args, **kwargs):
        r = func(*args, **kwargs)
        return r
    return wrapper


async def wait_code(func, args, kwargs, timeout):
    
    abort_after = timeout
    nexttime = time.time()
    start = time.time()
    count = 0
    
    while True:
        count += 1
        date_format = "%Y-%b-%d %H:%M:%S"
        logging.info(f"{count}. Start while loop time - {datetime.fromtimestamp(start).strftime(date_format)}")
        delta = time.time() - start
        r = func(*args, **kwargs)
        logging.info(f"Get data from request: {r}")
        resp_new = []

        for resp in r:

            if 'STATUS_OK' in resp[-1]: #STATUS_OK
                resp_new.append((resp[0], resp[2], int(resp[-1].split(':')[-1])))
                args = (args[0],args[1],[i for i in args[2] if i[0] != resp[0]])
            elif 'STATUS_WAIT_RESEND' in resp[-1]:
                resp_new.append((resp[0], resp[2], resp[-1]))
                args = (args[0],args[1],[i for i in args[2] if i[0] != resp[0]])
            else:
                resp_new.append(resp)

        if not args[2]:
            logging.info(f"Quit from while loop time - {datetime.fromtimestamp(time.time()).strftime(date_format)}")
            return resp_new
        
        nexttime += 30
        sleeptime = nexttime - time.time()
        if sleeptime > 0:
            await asyncio.sleep(sleeptime)
        if delta >= abort_after:
            logging.info(f"Quit from while loop time - {datetime.fromtimestamp(time.time()).strftime(date_format)}")
            return resp_new


def get_code_activation_mode(func):
    
    async def wrapper(*args, **kwargs):

        r = await wait_code(func, args, kwargs, args[1])
        logging.info(f"Results from waite_code received len(r) = {len(r)}, r = {r}")
        code_true = [(i[0], i[1], i[2], 6) for i in r if type(i[2]) == int] #set 6
        logging.info(f"Results sms: code_true = {code_true}")
        other = [(i[0], i[1], i[2], 8) for i in r if i[2] != 'STATUS_WAIT_RESEND' and type(i[2]) != int ] #and i[3] != 'STATUS_CANCEL' and i[3] != 'NO_ACTIVATION'
        logging.info(f"Results other: len(other) = {len(other)}")
       
        if other:
            logging.info(f"Send status 8 for other={other}")
            args[0].request_(other) #send 8 chancel activation

        return r

    return wrapper
