from django.http import Http404
from django.contrib import auth
from django.contrib.auth.models import User
import json
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from rpdesign import models
# Create your views here.
def addVisit(request):
    try:
        IDnum = request.POST['IDnum']
        new_v = models.RPDVisit(idnum=IDnum, quadraticTops = '', innerPathList='')
        new_v.save()
        new_v = models.RPDVisit.objects.get(idnum = IDnum)

        for i in xrange(32):
            if i % 16 == 0 or i % 16 == 15:
                newTooth = models.Tooth(vid = new_v, pos = i, tooth_lost = 2, tooth_base = 0, tooth_clasp = 0, tooth_support = 0)
            else:
                newTooth = models.Tooth(vid = new_v, pos = i, tooth_lost = 0, tooth_base = 0, tooth_clasp = 0, tooth_support = 0)
            newTooth.save()

        url = '/showVisit/?IDnum=' + IDnum
        return HttpResponseRedirect(url)

    except:
         return HttpResponseRedirect('/newpatient/')

def showVisit(request):
    IDnum = request.GET['IDnum']
    visit = models.RPDVisit.objects.get(idnum=IDnum)
    teeth = models.Tooth.objects.filter(vid=visit)
    teethList = []
    for i in xrange(32):
        teethList.append([[],[],[],[]])
    for tooth in teeth:
        teethList[tooth.pos][0] = tooth.tooth_lost
        teethList[tooth.pos][1] = tooth.tooth_base
        teethList[tooth.pos][2] = tooth.tooth_clasp
        teethList[tooth.pos][3] = tooth.tooth_support
    return render(request, 'teeth.html',{'teethList':json.dumps(teethList), 'IDnum':IDnum})

def index_view(request):
    visitList = models.RPDVisit.objects.all()
    vlist = []
    for visit in visitList:
        vlist.append(visit.idnum)
    t = get_template('visitlist.html')
    c = RequestContext(request, {'vlist': vlist})
    html = t.render(c)
    return HttpResponse(html)

def newVisit(request):
     t = get_template('newvisit.html')
     return render(request, 'newvisit.html')

def editTeeth(request):
    teethList = request.POST.getlist('teethList[]')
    IDnum =  request.POST.get('IDnum')
    visit = models.RPDVisit.objects.get(idnum=IDnum)
    teethobjs = models.Tooth.objects.filter(vid=visit)
    for i in xrange(32):
        toothprop = teethList[i].split(',')
        for toothobj in teethobjs:
            if toothobj.pos == i:
                toothobj.tooth_lost = int(toothprop[0])
                toothobj.tooth_base = int(toothprop[1])
                toothobj.tooth_clasp = int(toothprop[2])
                toothobj.tooth_support = int(toothprop[3])
                toothobj.save()
    return HttpResponse('Success')