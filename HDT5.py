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

def inicio(env,RAMtotal,procesador,intervalo):
    
    for i in range(10):
        instrucciones = random.randint(1,10)#se asigna la cant de instrucciones q tiene el proceso
        c = new(env,RAMtotal,procesador,instrucciones,'Proceso%02d' % i)
        env.process(c)
        t = random.expovariate(1.0/intervalo)#tiempo en q aparece otro proceso
        yield env.timeout(t)#se espera hasta tiempo t para otro proceso
    
def new (env,RAMtotal,procesador,instrucciones,name):
    global RAMnuevo,arrive
    RAMnuevo = random.randint(1,10)#numero aleatorio del ram requerido por proceso
    
    with RAMtotal.get(RAMnuevo) as req:
        #print('%7.4f %s: Termina tiempo de espera' % (env.now, name))
        yield req

    print('RAM libre: %7.4f %s RAM asignado:%7.4f Instrucciones:%7.4f' % (RAMtotal.level, name,RAMnuevo,instrucciones))
    arrive = env.now
    env.process(ready(env,procesador,instrucciones,name))

def ready(env,procesador,instrucciones,name):
    global wait,totalwait#,RAMnuevo

    with procesador.request() as reqProcesador:  #pedimos conectarnos al
        yield reqProcesador
        yield env.timeout(1)

        while instrucciones > 3:
            instrucciones = instrucciones - 3#se resta la cant de instrucciones q hace la CPU por unidad de tiempo
            print('instrucciones: %7.4f' % (instrucciones))

    wait = env.now - arrive
    totalwait = totalwait + wait

#comienza la simulacion
random.seed(RAMDOM_SEED)
env = simpy.Environment()
instrucciones = 0
totalwait = 0

#comienza el proceso
procesador = simpy.Resource(env, capacity=1)
RAMtotal = simpy.Container(env, init=100, capacity=100)
#waiting = simpy.Resource(env, capacity=1)
env.process(inicio(env,RAMtotal,procesador, INTERVALO_PROCESOS))
env.run()

print 'tiempo total de espera', totalwait, 'promedio: ',totalwait / 5.0
