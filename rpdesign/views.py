from django.http import Http404
from django.contrib import auth
from django.contrib.auth.models import User
import json
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from rpdesign import models
try:
    import StringIO
    StringIO = StringIO.StringIO
except Exception:
    from io import StringIO
import cgi, os
from django import http
from django.conf import settings
from easy_pdf.rendering import render_to_pdf_response
# Create your views here.

def index_view(request):
    if not request.user.is_authenticated():
        return render(request, 'unlogin_index.html')
    else:
        name = request.user.first_name
        return HttpResponseRedirect('/visitList/')

def login_post(request):
    if not request.POST:
        raise Http404
    rtnJSON = dict()
    stunum = request.POST.get('stunum', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=stunum, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        rtnJSON['result'] = 'success'
        if user.check_password(user.username):

            rtnJSON['next'] = '/visitList/'
    else:
        rtnJSON['result'] = 'failed'
        if User.objects.filter(username=stunum, is_active=True):
            rtnJSON['error'] = 'wrong password'
        else:
            rtnJSON['error'] = 'not exist'
    return HttpResponse(json.dumps(rtnJSON), content_type="application/json")

def newStaff(request):
    if not request.user.is_superuser:
        return render(request, 'unlogin_index.html')
    departments = models.Department.objects.all()
    departmentList = []
    for department in departments:
        departmentList.append({'id':department.id, 'dname':department.dname})
    return render(request, 'newstaff.html', {'departmentList': departmentList})

def addStaff(request):
    if not request.user.is_superuser:
        return render(request, 'unlogin_index.html')
    try:
        idnum = request.POST['idnum']
        sname = request.POST['sname']
        department = request.POST['department']
        Phonenum = request.POST['Phonenum']
        newUser = User.objects.create_user(username=idnum, password=idnum, first_name=sname)
        newUser.save()
        dDepartment = models.Department.objects.get(id=department)
        new_staff = models.Staff(user=newUser, idnum=idnum, sname=sname, phonenum=Phonenum, department=dDepartment)
        new_staff.save()
        return HttpResponseRedirect('/visitList/')
    except:
        return HttpResponseRedirect('/visitList/')


def addVisit(request):
    if not request.user.is_authenticated():
        return render(request, 'unlogin_index.html')
    try:
        IDnum = request.POST['IDnum']
        Pname = request.POST['Pname']
        PIDnum = request.POST['PIDnum']
        Sexual = int(request.POST['Sexual'])
        Age = int(request.POST['Age'])
        Phonenum = request.POST['Phonenum']
        RType = request.POST['RepairType']
        patient = models.Patient.objects.filter(pname = Pname, idnum = PIDnum)
        if len(patient) == 0:
            patient = models.Patient(pname = Pname, idnum = PIDnum, P_sexual = Sexual, P_page = Age, phonenum = Phonenum)
            patient.save()
        else:
            patient = patient[0]
        staff = models.Staff.objects.get(user_id=request.user.id)
        department = staff.department
        new_v = models.RPDVisit(idnum=IDnum, pid = patient, sid = staff, department = department, quadraticTops = '', innerPathList='', conntype_hollow = False, tongue_cover = False, maxilla_cover = False, type=RType)
        new_v.save()
        new_v = models.RPDVisit.objects.get(idnum = IDnum)

        for i in xrange(32):
            if i % 16 == 0 or i % 16 == 15:
                newTooth = models.Tooth(vid = new_v, pos = i, tooth_lost = 2, tooth_base = 0, tooth_clasp = 0, tooth_support = 0)
            else:
                newTooth = models.Tooth(vid = new_v, pos = i, tooth_lost = 0, tooth_base = 0, tooth_clasp = 0, tooth_support = 0)
            newTooth.save()

        url = '/showVisit/?IDnum=' + IDnum + '&method=show'
        return HttpResponseRedirect(url)

    except:
         return HttpResponseRedirect('/visitList/')

def showPatient(request):
    if not request.user.is_authenticated() :
        return render(request, 'unlogin_index.html')
    pid = request.GET['IDnum']
    patient = models.Patient.objects.filter(id = pid)
    if len(patient) > 0:
        patient = patient[0]
        visitList = models.RPDVisit.objects.filter(pid=patient)
        vlist = []
        for visit in visitList:
            vlist.append({'vid': visit.idnum, 'pname':visit.pid.pname, 'pidnum':visit.pid.idnum, 'pidID':visit.pid.id})

        return render(request, 'patient.html',{'patient': patient,'user':request.user,'visitList':vlist})
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

def logout_get(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def showVisitList(request):
    if not request.user.is_authenticated():
        return render(request, 'unlogin_index.html')

    visitList = models.RPDVisit.objects.all()
    vlist = []
    for visit in visitList:
        vlist.append({'vid': visit.idnum, 'pname':visit.pid.pname, 'pidnum':visit.pid.idnum, 'pidID':visit.pid.id})

    if request.user.is_superuser:
        staffList = models.Staff.objects.all()
        slist = []
        for staff in staffList:
            slist.append({'sid':staff.idnum, 'sname':staff.sname, 'department':staff.department.dname})

        return render(request, 'managelist.html', {'vlist': vlist,'user':request.user,'slist':slist})
    else:
        return render(request, 'visitlist.html', {'vlist': vlist,'user':request.user})


def newVisit(request):
    if not request.user.is_authenticated():
        return render(request, 'unlogin_index.html')
    try:
        pid = request.GET['pid']
        patient = models.Patient.objects.filter(id=pid)
        if len(patient) > 0:
            patient = patient[0]
            return render(request, 'newvisit.html', {'patient':patient})
        else:
            return render(request, 'newvisit.html')
    except:
        return render(request, 'newvisit.html')

def editTeeth(request):
    if not request.user.is_authenticated():
        return render(request, 'unlogin_index.html')
    teethList = request.POST.getlist('teethList[]')
    quadraticTops = request.POST.getlist('quadraticTops[]')
    remarkList = request.POST.getlist('remarkList[]')
    Pname =  request.POST.get('Pname')
    PIDnum =  request.POST.get('PIDnum')
    Age =  request.POST.get('Age')
    Phonenum =  request.POST.get('Phonenum')
    Sexual =  request.POST.get('Sexual')
    RepairType =  request.POST.get('RepairType')
    IDnum =  request.POST.get('IDnum')
    innerPathList = request.POST.getlist('innerPathList[]')
    conntype_hollow = request.POST.get('conntype_hollow')
    maxilla_cover = request.POST.get('maxilla_cover')
    tongue_cover = request.POST.get('tongue_cover')
    projects = request.POST.getlist('projects[]')
    materials = request.POST.getlist('materials[]')
    model_edge = request.POST.get('model_edge')
    occlusion_state = request.POST.get('occlusion_state')
    occlusion_record = request.POST.get('occlusion_record')
    teeth_pre = request.POST.get('teeth_pre')
    problem = request.POST.get('problem')
    solution = request.POST.get('solution')
    precheck = request.POST.get('precheck')
    finalcheck = request.POST.get('finalcheck')
    design_explain = request.POST.get('design_explain')
    color = request.POST.get('color')
    model_maker = request.POST.get('model_maker')
    model_checker = request.POST.get('model_checker')
    paraffin_maker = request.POST.get('paraffin_maker')
    burnish_maker = request.POST.get('burnish_maker')
    china_arrange_makeer = request.POST.get('china_arrange_makeer')
    paraffin_checker = request.POST.get('paraffin_checker')
    burnish_checker = request.POST.get('burnish_checker')
    china_arrange_checker = request.POST.get('china_arrange_checker')
    fee = request.POST.get('fee')

    visit = models.RPDVisit.objects.get(idnum=IDnum)
    patient = models.Patient.objects.get(id = visit.pid.id)
    patient.pname = Pname
    patient.idnum = PIDnum
    patient.P_page = Age
    patient.phonenum = Phonenum
    patient.P_sexual = Sexual
    patient.save()

    visit.project.clear()
    for project in projects:
        treatment = models.Treatproject.objects.get(id=project)
        visit.project.add(treatment)

    visit.material.clear()
    for material in materials:
        treatment_material = models.Material.objects.get(id=material)
        visit.material.add(treatment_material)

    visit.model_edge = int(model_edge)
    visit.occlusion_state = int(occlusion_state)
    visit.occlusion_record = int(occlusion_record)
    visit.teeth_pre = int(teeth_pre)
    visit.problem = problem
    visit.solution = solution
    visit.precheck = precheck
    visit.finalcheck = finalcheck
    visit.design_explain = design_explain
    visit.color = color
    visit.model_maker = model_maker
    visit.model_checker = model_checker
    visit.paraffin_maker = paraffin_maker
    visit.burnish_maker = burnish_maker
    visit.china_arrange_makeer = china_arrange_makeer
    visit.paraffin_checker = paraffin_checker
    visit.burnish_checker = burnish_checker
    visit.china_arrange_checker = china_arrange_checker
    if fee and (type(eval(fee))==int or type(eval(fee))==float):
        visit.fee = float(fee)
    else:
        visit.fee = 0
    visit.type = RepairType

    teethobjs = models.Tooth.objects.filter(vid=visit)
    for i in xrange(32):
        toothprop = teethList[i].split(',')
        for toothobj in teethobjs:
            if toothobj.pos == i:
                toothobj.tooth_lost = int(toothprop[0])
                toothobj.tooth_base = int(toothprop[1])
                toothobj.tooth_clasp = int(toothprop[2])
                toothobj.tooth_support = int(toothprop[3])
                toothobj.tongue_blank = int(toothprop[3])
                toothobj.save()

    quadraticTopString = ''
    for top in quadraticTops:
        top = top.split(',')
        quadraticTopString += top[0] + ';'
        for i in xrange(1,len(top),2):
            quadraticTopString += top[i] +  ',' + top[i+1] + ';'
        quadraticTopString += '\n'
    visit.quadraticTops = quadraticTopString

    innerPathListString = ''
    for point in innerPathList:
        point = point.split(',')
        innerPathListString += point[0] + ',' + point[1] + ';'
    visit.innerPathList = innerPathListString

    if request.POST.get('make_model_date') != '':
        visit.make_model_date = request.POST.get('make_model_date')
    if request.POST.get('get_model_date') != '':
        visit.get_model_date = request.POST.get('get_model_date')
    if request.POST.get('try_paraffin') != '':
        visit.try_paraffin = request.POST.get('try_paraffin')
    if request.POST.get('try_stake') != '':
        visit.try_stake = request.POST.get('try_stake')
    if request.POST.get('try_crown') != '':
        visit.try_crown = request.POST.get('try_crown')
    if request.POST.get('try_base') != '':
        visit.try_base = request.POST.get('try_base')
    if request.POST.get('finish_date') != '':
        visit.finish_date = request.POST.get('finish_date')
    if request.POST.get('try_cradled') != '':
        visit.try_cradled = request.POST.get('try_cradled')
    if request.POST.get('try_teeth_arrange') != '':
        visit.try_teeth_arrange = request.POST.get('try_teeth_arrange')
    if request.POST.get('precheck_date') != '':
        visit.precheck_date = request.POST.get('precheck_date')
    if request.POST.get('finalcheck_date') != '':
        visit.finalcheck_date = request.POST.get('finalcheck_date')

    if(conntype_hollow == 'true'):
        visit.conntype_hollow = True
    if(maxilla_cover == 'true'):
        visit.maxilla_cover = True
    if(tongue_cover == 'true'):
        visit.tongue_cover = True

    visit.save()
    return HttpResponse('Success')

def showVisit(request):
    if not request.user.is_authenticated():
        return render(request, 'unlogin_index.html')
    IDnum = request.GET['IDnum']
    method = request.GET['method']

    staff = models.Staff.objects.get(user_id=request.user.id)
    visit = models.RPDVisit.objects.get(idnum=IDnum)
    teeth = models.Tooth.objects.filter(vid=visit)
    quadraticTopString = visit.quadraticTops
    innerPathListString = visit.innerPathList

    if visit.tongue_cover:
        tongue_cover = 'true'
    else:
        tongue_cover = 'false'
    if visit.maxilla_cover:
        maxilla_cover = 'true'
    else:
        maxilla_cover = 'false'
    if visit.conntype_hollow:
        conntype_hollow = 'true'
    else:
        conntype_hollow = 'false'

    quadraticTopString = quadraticTopString.split('\n')
    quadraticTopString.pop()
    quadraticTops = []
    for top in quadraticTopString:
        top = top.split(';')
        top.pop()
        for i in xrange(1,len(top)):
            top[i] = top[i].split(',')
            top[i][0] = float(top[i][0])
            top[i][1] = float(top[i][1])
        quadraticTops.append(top)

    innerPathListString = innerPathListString.split(';')
    innerPathListString.pop()
    for i in xrange(len(innerPathListString)):
        innerPathListString[i] = innerPathListString[i].split(',')
        innerPathListString[i][0] = float(innerPathListString[i][0])
        innerPathListString[i][1] = float(innerPathListString[i][1])

    teethList = []
    for i in xrange(32):
        teethList.append([[],[],[],[],[]])
    for tooth in teeth:
        teethList[tooth.pos][0] = tooth.tooth_lost
        teethList[tooth.pos][1] = tooth.tooth_base
        teethList[tooth.pos][2] = tooth.tooth_clasp
        teethList[tooth.pos][3] = tooth.tooth_support
        teethList[tooth.pos][4] = tooth.tongue_blank

    make_model_date = ''
    if visit.make_model_date:
        make_model_date = visit.make_model_date.strftime('%Y-%m-%d')
    get_model_date = ''
    if visit.get_model_date:
        get_model_date = visit.get_model_date.strftime('%Y-%m-%d')
    try_paraffin = ''
    if visit.try_paraffin:
        try_paraffin = visit.try_paraffin.strftime('%Y-%m-%d')
    try_stake = ''
    if visit.try_stake:
        try_stake = visit.try_stake.strftime('%Y-%m-%d')
    try_crown = ''
    if visit.try_crown:
        try_crown = visit.try_crown.strftime('%Y-%m-%d')
    try_base = ''
    if visit.try_base:
        try_base = visit.try_base.strftime('%Y-%m-%d')
    finish_date = ''
    if visit.finish_date:
        finish_date = visit.finish_date.strftime('%Y-%m-%d')
    try_cradled = ''
    if visit.try_cradled:
        try_cradled = visit.try_cradled.strftime('%Y-%m-%d')
    try_teeth_arrange = ''
    if visit.try_teeth_arrange:
        try_teeth_arrange = visit.try_teeth_arrange.strftime('%Y-%m-%d')
    precheck_date = ''
    if visit.precheck_date:
        precheck_date = visit.precheck_date.strftime('%Y-%m-%d')
    finalcheck_date = ''
    if visit.finalcheck_date:
        finalcheck_date = visit.finalcheck_date.strftime('%Y-%m-%d')

    projectList = models.Treatproject.objects.filter(type=visit.type)
    projects = []
    for project in visit.project.all():
        projects.append(project.id)

    materialList = models.Material.objects.filter(type=visit.type)
    materials = []
    for material in visit.material.all():
        materials.append(material.id)
    patient = visit.pid

    if visit.fee:
        fee = visit.fee
    else:
        fee = ""
    if visit.problem:
        problem = visit.problem
    else:
        problem = ""
    if visit.solution:
        solution = visit.solution
    else:
        solution = ""
    if visit.precheck:
        precheck = visit.precheck
    else:
        precheck = ""
    if visit.finalcheck:
        finalcheck = visit.finalcheck
    else:
        finalcheck = ""
    if visit.design_explain:
        design_explain = visit.design_explain
    else:
        design_explain = ""
    if visit.color:
        color = visit.color
    else:
        color = ""
    if visit.model_maker:
        model_maker = visit.model_maker
    else:
        model_maker = ""
    if visit.model_checker:
        model_checker = visit.model_checker
    else:
        model_checker = ""
    if visit.paraffin_maker:
        paraffin_maker = visit.paraffin_maker
    else:
        paraffin_maker = ""
    if visit.burnish_maker:
        burnish_maker = visit.burnish_maker
    else:
        burnish_maker = ""
    if visit.china_arrange_makeer:
        china_arrange_makeer = visit.china_arrange_makeer
    else:
        china_arrange_makeer = ""
    if visit.paraffin_checker:
        paraffin_checker = visit.paraffin_checker
    else:
        paraffin_checker = ""
    if visit.burnish_checker:
        burnish_checker = visit.burnish_checker
    else:
        burnish_checker = ""
    if visit.china_arrange_checker:
        china_arrange_checker = visit.china_arrange_checker
    else:
        china_arrange_checker = ""

    visitDic = {
        'staff': staff,
        'IDnum': visit.idnum,
        'patient': patient,
        'RType': visit.type,
        'teethList':json.dumps(teethList),
        'quadraticTops':json.dumps(quadraticTops),
        'innerPathList': json.dumps(innerPathListString),
        'conntype_hollow':conntype_hollow,
        'tongue_cover':tongue_cover,
        'maxilla_cover':maxilla_cover,
        'IDnum':IDnum,
        'make_model_date': make_model_date,
        'get_model_date': get_model_date,
        'try_paraffin': try_paraffin,
        'try_stake': try_stake,
        'try_crown': try_crown,
        'try_base': try_base,
        'finish_date': finish_date,
        'try_cradled': try_cradled,
        'try_teeth_arrange': try_teeth_arrange,
        'precheck_date': precheck_date,
        'finalcheck_date': finalcheck_date,
        'projectList': projectList,
        'projects': json.dumps(projects),
        'materialList': materialList,
        'materials': json.dumps(materials),
        'fee': fee,
        'model_edge': visit.model_edge,
        'occlusion_state': visit.occlusion_state,
        'occlusion_record': visit.occlusion_record,
        'teeth_pre': visit.teeth_pre,
        'problem': problem,
        'solution': solution,
        'precheck': precheck,
        'finalcheck': finalcheck,
        'design_explain': design_explain,
        'color': color,
        'model_maker': model_maker,
        'model_checker': model_checker,
        'paraffin_maker': paraffin_maker,
        'burnish_maker': burnish_maker,
        'china_arrange_makeer': china_arrange_makeer,
        'paraffin_checker': paraffin_checker,
        'burnish_checker': burnish_checker,
        'china_arrange_checker': china_arrange_checker
    }

    if method == "show":
        tpl = "teeth.html"
        return render(request, tpl, visitDic)
    else:
        tpl = "print.html"
        return render(request, tpl, visitDic)
        #return render_to_pdf_response(request, tpl,visitDic)




def editPatient(request):
    if not request.user.is_authenticated():
        return render(request, 'unlogin_index.html')
    pid = request.GET['pid']
    try:
        patient = models.Patient.objects.get(id=int(pid))
        Pname = request.POST['Pname']
        PIDnum = request.POST['PIDnum']
        Sexual = int(request.POST['Sexual'])
        Age = int(request.POST['Age'])
        Phonenum = request.POST['Phonenum']
        patient.pname = Pname
        patient.idnum = PIDnum
        patient.P_sexual = Sexual
        patient.P_page = Age
        patient.phonenum = Phonenum
        patient.save()
        return HttpResponseRedirect('/showPatient?IDnum='+pid)
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

def deleteVisits(request):
    if not request.user.is_authenticated():
        return render(request, 'unlogin_index.html')
    visitsToDelete = request.POST.getlist('visitsToDelete[]')
    for visit in visitsToDelete:
        deleteVisit(visit)
    return HttpResponse('Success')

def deleteVisit(visit):
    vid = models.RPDVisit.objects.get(idnum=visit)
    models.Tooth.objects.filter(vid=vid.id).delete()
    vid.delete()
    return