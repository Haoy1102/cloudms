from datetime import datetime
from django.http import HttpResponse,JsonResponse,FileResponse,StreamingHttpResponse
from django.shortcuts import render
import os
from django.views.decorators.http import require_http_methods
from django.template import  Template,Context

# Create your views here.

def msgproc(request):
    datalist = []
    if request.method == "POST":
        userA = request.POST.get("userA", None)
        userB = request.POST.get("userB", None)
        msg = request.POST.get("msg", None)
        time = datetime.now()
        with open('msgdata.txt', 'a+', encoding='utf-8') as f:
            f.write("{}--{}--{}--{}--\n".format(userA, userB, msg, \
                                                time.strftime("%Y-%m-%d %H:%M:%S")))
    if request.method == "GET":
        userC = request.GET.get("userC", None)
        if userC != None:
            #try:
                with open("msgdata.txt", "r", encoding='utf-8') as f:
                    cnt = 0
                    for line in f:
                        linedata = line.split('--')
                        if linedata[0] == userC:
                            cnt = cnt + 1
                            d = {"userA": linedata[1], "msg": linedata[2] \
                                , "time": linedata[3]}
                            datalist.append(d)
                        if cnt >= 10:
                            break;
            #except FileNotFoundError:
            #    msg="Sorry,the file msgdata.txt""does not exist."
            #    print(msg)
    return render(request, "MsgSingleWeb.html", {"data": datalist})

def homeproc(request):
    return HttpResponse("<h1>这是首页，具体功能请访问<a href='./msggate/'>这里</a><h1>")

def homeproc1(request):
    response=JsonResponse({'key':'value1'})
    return response

def homeproc2(request):
    cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    response=FileResponse(open(cwd+"/msgapp/templates/example4.jpeg","rb"))
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="example4.jpeg"'
    return response

def file_download(request):
    with open('msgdata.txt',encoding="utf-8") as f:
        c=f.read()
    return HttpResponse(c)

def big_file_download(request):
    def file_iterator(file_name,chunk_size=12):
        with open(file_name,encoding="utf-8") as f:
            while True:
                c=f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    fname="msgdata.txt"
    response=StreamingHttpResponse(file_iterator(fname))
    return response

def pgproc(request):
    template=Template("<h1>这个程序的名字是{{name}}</h1>")
    context=Context({"name":"实验平台"})
    return HttpResponse(template.render(context))
