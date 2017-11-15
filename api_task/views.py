from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Task
from .task import producer, Track


def api_task(request):
    task = Task.objects.create() # создаем запись в базе 
    producer.execute(task.id) # передаем id задачи в очередь
    return HttpResponse('number task - %i' % task.id)

    
def api_status_task(request, id):
    t = Task.objects.get(id=int(id))
    status = Track.status_task(int(id)) # узнаем текущий статус задачи
    context = {'status': status['status'], 'create_time': t.create_time, 'start_time': t.start_time, 'time_to_execute': t.exec_time}
    return JsonResponse(context, safe=False)
    