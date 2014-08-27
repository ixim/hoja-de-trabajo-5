# -*- coding: cp1252 -*-
"""
Hoja de trabajo No. 5
Ixim Cojti Lopez    12697
Luis Tello          12

Esta es una simulación de un procesador al llevar a cabo varios procesos
"""

import simpy
import random

INTERVALO_PROCESOS = 10#tiempo creacion de procesos de forma exponencial
RAMDOM_SEED = 3

def inicio(env,procesador,intervalo):
    
    for i in range(15):
        instrucciones = random.randint(1,10)#se asigna la cant de instrucciones q tiene el proceso
        c = new(env,procesador,instrucciones,'Proceso%02d' % i)
        env.process(c)
        t = random.expovariate(1.0/intervalo)#tiempo en q aparece otro proceso
        yield env.timeout(t)#se espera hasta tiempo t para otro proceso
    
def new (env,procesador,instrucciones,name):
    global RAMtotal,RAMnuevo
    RAMnuevo = random.randint(1,10)#numero aleatorio del ram requerido por proceso
    RAMtotal = RAMtotal - RAMnuevo#ram restante de total
    print('RAM libre: %7.4f %s RAM asignado:%7.4f Instrucciones:%7.4f' % (RAMtotal, name,RAMnuevo,instrucciones))
    
    if RAMtotal > RAMnuevo:#si el ram nuevo asignado es menor al ram restante, se puede realizar 
        env.process(ready(env,procesador,instrucciones,name))
    else:#VERIFICAR ESTA PARTE DE CUANDO HACE FALTA ESPERAR PARA OBTENER RAM
        with RAMnuevo.request() as req:  #pedimos conectarnos al
            RAMnuevo = random.uniform(1, 10)#ram
            yield req

            tib = random.expovariate(1.0 / 10)
            yield env.timeout(tib)#se espera el tiempo asignado a tib
            print('%7.4f %s: Finished' % (env.now, name))

def ready(env,procesador,instrucciones,name):
    global wait,totalwait,RAMtotal,RAMnuevo

    arrive = env.now
    print('Tiempo %7.4f' % (arrive))

    while instrucciones > 3:
        instrucciones = instrucciones - 3#se resta la cant de instrucciones q hace la CPU por unidad de tiempo
        print('instrucciones: %7.4f' % (instrucciones))
        yield env.timeout(1)

    RAMtotal = RAMtotal + RAMnuevo
    print('RAM reasignado: %7.4f' % (RAMnuevo))
    wait = env.now - arrive
    totalwait = totalwait + wait

#comienza la simulacion
random.seed(RAMDOM_SEED)
env = simpy.Environment()
instrucciones = 0
totalwait = 0

#comienza el proceso
procesador = simpy.Resource(env, capacity=1)
RAMtotal = 50#simpy.Container(env, capacity=100, init=3)

env.process(inicio(env, procesador, INTERVALO_PROCESOS))
env.run()

print 'tiempo total de espera', totalwait, 'promedio: ',totalwait / 20.0
