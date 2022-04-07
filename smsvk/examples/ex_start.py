from smsvk import GetBalance, GetNumber, \
SetStatusActivation, GetCodeActivation, \
GetAvaibleService, GetCountNumberService
from smsvk import Api


api_key = 'THIS_API_KEY'
count_phone_number = 3
timeout = 15
limit = 10
ua = "ua"
timeout_wait_code = 10 * 60

api = Api(api_key, count_phone_number, timeout, limit, ua)

balance = GetBalance(api)
print(balance.request())

services = GetAvaibleService(api)
print(services.request_json())

count_serv = GetCountNumberService(api)
print(count_serv.request_json('tg_0'))

tg_phones = GetNumber(api)

tg_phones =  [i for i in tg_phones.request('tg_0') if len(i) == 3]  
tg_phones = [(i[0], i[1], i[2], 1) for i in tg_phones] 
''' [(1, 211, '199782912112', 1 ), (2, 333, '199701014551', 1 ), (3, 3333, '199801014211'), 1] '''

active_status = SetStatusActivation(api)
active_status = active_status.request_(tg_phones) #send 

''' [(1, 211, '199782912112', 'ACCESS_RETRY_GET'), 
     (2, 333, '199701014551', 'ACCESS_READY'), 
     (3, 533, '199801014211', 'ACCESS_READY')] '''

active_status = [(i[0], i[1], i[2]) for i in active_status]

#waiting sms code 
e = GetCodeActivation(api)
print(e.request(timeout_wait_code,active_status))


