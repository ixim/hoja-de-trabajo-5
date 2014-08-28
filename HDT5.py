# -*- coding: cp1252 -*-
"""
Hoja de trabajo No. 5
Ixim Cojti Lopez    12697
Luis Tello          12

Esta es una simulación de un procesador al llevar a cabo varios procesos
"""

import simpy
import random

INTERVALO_PROCESOS = 1#tiempo creacion de procesos de forma exponencial
RAMDOM_SEED = 3
PROCESOS = 150#PROBAR CON PROCESOS DE 25,50,100,150 Y 200 

def inicio(env,RAMtotal,procesador,intervalo,PROCESOS,waiting):
    for i in range(PROCESOS):
        arrive = env.now
        instrucciones = random.randint(1,10)#se asigna la cant de instrucciones q tiene el proceso
        c = new(env,RAMtotal,procesador,instrucciones,'Proceso%02d' % i,arrive,waiting)
        env.process(c)
        t = random.expovariate(1.0/intervalo)#tiempo en q aparece otro proceso
        yield env.timeout(t)#se espera hasta tiempo t para otro proceso
    
def new (env,RAMtotal,procesador,instrucciones,name,arrive,waiting):
    global RAMnuevo,wait,totalwait
    RAMnuevo = random.randint(1,10)#numero aleatorio del ram requerido por proceso

    with RAMtotal.get(RAMnuevo) as req:
        yield req
        
    print('%s RAM libre: %7.4f RAM asignado:%7.4f Instrucciones:%7.4f' % (name,RAMtotal.level,RAMnuevo,instrucciones))
    d=ready(env,procesador,instrucciones,name,RAMnuevo,arrive,waiting)
    env.process(d)
        
def ready(env,procesador,instrucciones,name,RAMnuevo,arrive,waiting):
        global totalwait

        while instrucciones > 3:
            with procesador.request() as reqProcesador:  #pedimos conectarnos al
                yield reqProcesador
                yield env.timeout(1)

                print ('%s Instrucciones restantes:%s'%(name,instrucciones))
                instrucciones = instrucciones - 3#se resta la cant de instrucciones q hace la CPU por unidad de tiempo
                siguiente = random.choice(["ready","waiting"])

                if siguiente == "waiting":
                    print 
                    with waiting.request() as reqWaiting:
                        yield reqWaiting
                        yield env.timeout(5)
                    
        print 'Salta instruccinoes menor o igual a 3'
        with RAMtotal.put(RAMnuevo) as req:
            yield req
        
        wait = env.now - arrive
        totalwait = totalwait + wait
        print name,' Termina ','Tiempo actual: ',wait
        
#comienza la simulacion
random.seed(RAMDOM_SEED)
env = simpy.Environment()
instrucciones = 0
totalwait = 0.0

#comienza el proceso
procesador = simpy.Resource(env, capacity=1)
RAMtotal = simpy.Container(env, init=100, capacity=100)
waiting = simpy.Resource(env, capacity=1)
env.process(inicio(env,RAMtotal,procesador, INTERVALO_PROCESOS,PROCESOS,waiting))
env.run()

print 'Tiempo total',totalwait,'Promedio de tiempo total: ',totalwait / PROCESOS
