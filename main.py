from uart import *
from MQTTClient import *
import time



class Task:
  def __init__(self, delay, period, duration, func, args = None):
    self.delay = delay
    self.duration = duration
    self.func = func
    self.period = period
    self.run_me = 0
    self.args = args

class Tasks:
  def __init__(self):
    self.tasks = list()

  def add_task(self, task):
    self.tasks.append(task)

  def remove_task(self, task):
    self.tasks.remove(task)

  def update(self):
    for task in self.tasks:
      if(task.delay >= 0):
        task.delay -= 1
        if(task.delay <= 0):
          task.delay = task.period
          task.run_me = 1

  def dispatch(self):
    for task in self.tasks:
      if(task.run_me):
        #reset flag run_me
        task.run_me = 0
        #active function of task
        if(task.args != "None"):
          task.func(task.args)
        else:
          task.func()
        #decrease duration of task by 1 if duration > 0
        if(task.duration > 0):
          task.duration -= 1
        #remove task 
        if(task.duration == 0):
          self.remove_task(task)

client = mqtt_client()

tasks = Tasks()
read_uart_task = Task(delay = 2, period = 1, duration = -1, func = readSerial, args = client)

if __name__ == "__main__":
  tasks.add_task(read_uart_task)
  while 1:
    tasks.update()
    tasks.dispatch()

    time.sleep(0.1) #time unit is 100ms