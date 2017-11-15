from .models import Task
import datetime
import time
import random
from queue import Queue, Empty, Full
from threading import Thread
              
                
class Producer(Thread):
    """
    отдаем задачи на выполнение
    """
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.daemon = True
        self.start()
        
    def execute(self, task):
        state = True
        while True:
            try:
                Track.status_in_queue(task)
                """вызываем исключение Full если в течение 1с не можем передать задачу в очередь"""
                self.queue.put(task, block=False, timeout=1)
                state = False
                time.sleep(1)
                break
            except Full:
                if state == False:
                    print('queue is full')
                state = True
                time.sleep(1)
                

class Consumer(Thread):
    """
    выполняем задачи
    """
    def __init__(self, queue):
        super().__init__()
        self.queue = queue       
        self.daemon = True # убиваем потоки вместе с приложением
        self.start()
    
    def run(self):
        state = True
        while True:
            try:
                """указываем что очередь пуста, вызываем исключение Empty, если не удалось получить задачу"""
                task = self.queue.get(block=False, timeout=1) 
                Track.status_run(task)
                state = False
                exec_time = random.randint(0,10)
                time.sleep(exec_time)
                Track.status_completed(task, exec_time)
            except Empty:
                if state == False:
                    print('%s empty' % self.getName())
                state = True
                time.sleep(0.1)

                
l = [] # храним состояние задач
class Track():
    """
    отслеживаем задачи, изменяем статусы в ходе выполнения
    """
    def status_in_queue(task):
        t = Task.objects.get(id=task)
        task = {task:{'status' : 'In queue'}}
        l.append(task)


    def status_run(task):
        if len(l) > 1:
            for i in l:
                if task in i.keys():
                   i[task]['status'] = 'Run'
        else:
            l[0].get(task).update({'status' : 'Run'})           

            
    def status_completed(task, exec_time):
        now = datetime.datetime.now()
        t = Task.objects.get(id=task)
        if len(l) > 1:
            for i in l:
                if task in i.keys():
                   i[task]['status'] = 'Completed'
                   t.start_time = now.strftime("%H:%M:%S.%f") # время завершения
                   t.exec_time = exec_time # время выполнения
                   t.save(update_fields=['start_time', 'exec_time']) # сохраняем в базу по завершению
        else:
            l[0].get(task).update({'status' : 'Completed'})
            t.start_time = now.strftime("%H:%M:%S.%f")
            t.exec_time = exec_time
            t.save(update_fields=['start_time', 'exec_time'])
           
           
    def status_task(id):
        if len(l) > 1:
            for i in l:
                if id in i.keys():
                    return i[id]
        else:
            return l[0].get(id)
            
            
queue = Queue(2) # максимальное количество задач в очереди
consumer = [Consumer(queue) for x in range(2)] # создаем 2 потока выполнения
producer = Producer(queue)