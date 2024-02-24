import sys
import time
from simple_ai import *
from MQTTClient import *

class Task:
  def __init__(self, delay, period, duration, func):
    self.delay = delay
    self.duration = duration
    self.func = func
    self.period = period
    self.run_me = 0

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
        task.func()
        #decrease duration of task by 1 if duration > 0
        if(task.duration > 0):
          task.duration -= 1
        #remove task 
        if(task.duration == 0):
          self.remove_task(task)




tasks = Tasks()

def ai_detect():
  #reset: counter_mask, counter_no_mask, counter_no_people 
  #for function image_detector_many_times()
  reset_detect_many_times()
  #set duratio of detect_image_task is 5 for this task will run 5 times
  detect_image_task.duration = 5
  #ADd task detect many times
  tasks.add_task(detect_image_task)

ai_detect_task = Task(delay = 20, period = 50, duration = -1, func = ai_detect)


client = mqtt_client()
def image_detect_task():
  result = image_detector_many_times()
  if(result == -1):
    client.publish("ai", "Camera error")
    print("Camera error")
    detect_image_task.duration = 0
  elif(result == None):
    if(detect_image_task.duration == 1):
      client.publish("ai", "Không xác định được")
      print("Không xác định được")
  else:
    class_name = class_names[result]
    client.publish("ai", class_name)
    print(class_name)

    detect_image_task.duration = 0
  

detect_image_task = Task(delay = 0, period = 1, duration = 5, func = image_detect_task )

if __name__ == "__main__":

  tasks.add_task(ai_detect_task)  
  while 1:
    tasks.update()
    tasks.dispatch()

    time.sleep(0.1) #time unit is 100ms
    