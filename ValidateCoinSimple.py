'''
#############################################################################
#                                                                           #
#   ValidateCoinSimple.py                                                   #
#   Copyright (C) 2013 linuxknow                                            #
#   linuxknow   [at] gmail dot com                                          #
#   This program is free software: you can redistribute it and/or modify    #
#   it under the terms of the GNU General Public License as published by    #
#   the Free Software Foundation, either version 3 of the License, or       #
#   (at your option) any later version.                                     #
#                                                                           #
#   This program is distributed in the hope that it will be useful,         #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#   GNU General Public License for more details.                            #
#                                                                           #
#   You should have received a copy of the GNU General Public License       #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>    #
#                                                                           #
#############################################################################
'''


import json
import bottle
from bottle import route, run, request, abort
from collections import deque

class Calculus():

    def __init__(self,total):
        self.list_address=[]
        self.amount = 0
        self.total_address = total

    def set_list_address(self,list_address):
        self.list_address = list_address

    def get_validate_address(self,address):
        if address is not None and address[0] in (1,3) and len(address)==34:
	    return True
        else:
	    return False

    def get_validate_amount(self,valor):
       print valor
       if not str(valor).isdigit():
           return False
       if int(valor) <= 0:
           return False
       else:
           return True
       

    def validate_all_address(self):
        ok = False
        for address in self.list_address:
            if self.get_validate_address(address):
                ok = True
        return ok

    def validate_bitcoin(self,data):

        queue = deque(['address1','address2','address3','address4','address5'])
        
        address_general = []

        for inc in range(0,(self.total_address+1),1):
            address_general.append(queue.popleft())

        for key in address_general:
            self.list_address.append(data[key])
     
        ##Debug
        if self.get_validate_amount(data['amount']):
            print "valido el numero"
        else:
            print "invalido numero"
        if self.validate_all_address():
            print "valido los address"
        else:
            print "direcciones invalidas"

        if self.get_validate_amount(data['amount']) and self.validate_all_address():
            return True
        else:
            return False


@route('/', method='GET')
def homepage():
    return 'validate bitcoin!'

@route('/validateCoin', method='PUT')
def validate():
    ##Testing para todo las address
    #validar={'amount','address1','address2','address3','address4','address5'}
    bitcoin={}
    cant_address = 0
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    bitcoin_web = json.loads(data)
    for key, value in bitcoin_web.iteritems():
        #if key not in validar:
        #    abort(400, 'No data received')
        #else:
        if key in ['address']:
            cant_address+=1
        bitcoin[key] = value
    #return dict(valores = str(entity))
    calcular = Calculus(cant_address)
    if calcular.validate_bitcoin(bitcoin):
        ##Datos que no tengo 
        str = "'INSERT INTO tumble VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (idTumble,inputAddress,bitcoin['amount'],....,100,''))"
        return "Bitcon agendado"
    else:
        #abort(400, 'No data received')
        return "Su bitcoin no es valido"

    ##Guarda la info en la DB
    #try:
    #    db['bitcoin'].save(bitcoin_web)
    #except ValidationError as ve:
    #    abort(400, str(ve))
    
bottle.debug(True) 
run(host='localhost', port=8082)
