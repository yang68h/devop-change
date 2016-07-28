#!/usr/bin/python
# coding = utf-8

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from opman.models import HostList
from devop.views.permission import PermissionVerify, SelfPaginator
from opman.forms import HostListForm
from opman.forms import XlsxUpload
from opman.models import Xlsx,KaoQin,HostXlsx
from openpyxl import load_workbook
from datetime import datetime,timedelta
from .analystor import getworktime,getalldate,gethours
from opman.models import MyUser as User
import random
@login_required
@PermissionVerify()
def ListHost(request):
    mList = HostList.objects.all()
    lst = SelfPaginator(request, mList, 20)
    kwvars = {
        'lpage': lst,
        'request': request,
    }
    return render_to_response('HostManage/host.list.html', kwvars)


@login_required
@PermissionVerify()
def AddHost(request):
    form = HostListForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('listhosturl'))
    else:
        form = HostListForm()

    kwvars = {
        'form': form,
        'request': request,
    }

    return render_to_response('HostManage/host.add.html', kwvars, RequestContext(request))


@login_required
@PermissionVerify()
def EditHost(request, ID):
    host = HostList.objects.get(id=ID)

    if request.method == 'POST':
        form = HostListForm(request.POST, instance=host)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listhosturl'))
    else:
        form = HostListForm(instance=host)

    kwvars = {
        'ID': ID,
        'form': form,
        'request': request,
    }

    return render_to_response('HostManage/host.edit.html', kwvars, RequestContext(request))


@login_required
@PermissionVerify()
def DeleHost(request, ID):
    HostList.objects.filter(id=ID).delete()
    return HttpResponseRedirect(reverse('listhosturl'))


@login_required
@PermissionVerify()
def UploadHost(request):
    if request.method == "POST":
        hf = XlsxUpload(request.POST,request.FILES)
        if hf.is_valid():
            date = hf.cleaned_data['date']
            filename = hf.cleaned_data['filename']
            xlsx = HostXlsx()
            xlsx.date = date
            xlsx.filename = filename
            xlsx.save()
            return HttpResponse('upload ok!')
    else:
        hf = XlsxUpload()
    xlist = HostXlsx.objects.all()
    lst = SelfPaginator(request,xlist,20)
    kwvars = {
        'hf': hf,
        'hpage': lst,
        'request': request,
    }
    return render_to_response('HostManage/host.upload.html',kwvars,RequestContext(request))


@login_required
@PermissionVerify()
def WriteHost(request,ID):
    xlsx = HostXlsx.objects.get(id=ID)
    filename = xlsx.filename
    date = xlsx.date
    wb = load_workbook(filename=filename)
    ps = wb.get_sheet_by_name('Sheet3')
    rows = ps.rows
    alldata = []
    for row in rows:
        line = [col.value for col in row]
        alldata.append(line)
    # for h in alldata[1:]:
    #     if h == '':
    #         pass
    #     else:
    for x in range(1,len(alldata[1:]) + 1):
        hdata = HostList()
        print(x)
        hdata.idcinfo = alldata[x][0]
        hdata.ipinfo = alldata[x][1]
        hdata.repairinfo = alldata[x][2]
        hdata.username = alldata[x][3]
        hdata.buytime = alldata[x][4]
        hdata.hostname = alldata[x][5]
        hdata.osinfo = alldata[x][6]
        hdata.password = alldata[x][7]
        hdata.memoryinfo = alldata[x][8]
        hdata.diskinfo = alldata[x][9]
        hdata.cpuinfo = alldata[x][10]
        hdata.snnum = alldata[x][11]
        hdata.usefor = alldata[x][12]
        hdata.status = alldata[x][13]
        hdata.save()


    # year = int(date.strftime('%Y'))
    # month = int(date.strftime('%m'))
    # datelist = getalldate(year, month)
    # user = User.objects.all()
    # userlist = []
    # for i in user:
    #     userlist.append(i.fullname)
    # for u in userlist:
    #     if u == '':
    #         pass
    #     else:
    #         for day in datelist:
    #             nextday = datetime.strptime(
    #                 day, '%Y-%m-%d').date() + timedelta(days=1)
    #             jilu = getworktime(u, day, alldata)
    #             jilu1 = getworktime(u, nextday, alldata)
    #             a = gethours(u, day, jilu1, jilu)
    #             if a == None:
    #                 pass
    #             else:
    #                 fullname = a['username']
    #                 uid = user.get(fullname=fullname).id
    #                 kq = KaoQin()
    #                 kq.date = a['date']
    #                 kq.on = a['on']
    #                 kq.off = a['off']
    #                 kq.plus = a['plus']
    #                 kq.late = a['late']
    #                 kq.leave = a['leave']
    #                 kq.content = a['content']
    #                 kq.fullname_id = uid
    #                 kq.save()
    return HttpResponseRedirect(reverse('uploadhost'))


