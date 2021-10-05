from django.http import HttpResponse

from django.shortcuts import render

from djangoProject import socket as ss


def index(request):
    return render(request, "control.html")


def as_views(request):
    left = request.GET.get("l", "0")
    right = request.GET.get("r", "0")
    cmd = '{{driveCmd: {{l:{l}, r:{r} }} }}\n'.format(l=left, r=right)
    try:
        if ss.s_server.last_data is None:
            ss.s_server.last_data = ""
            ss.s_server.receive_thread()
        ss.s_server.send(cmd)
    except:
        ss.s_server.last_data = None
        return HttpResponse("wait connect")
    return HttpResponse(ss.s_server.last_data)
