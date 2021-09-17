from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import connection


# Create your views here.

def listing(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM specialization")
    specializationlist = dictfetchall(cursor)

    context = {
        "specializationlist": specializationlist
    }

    # Message according medicines Role #
    context['heading'] = "Specialization Details";
    return render(request, 'specialization-details.html', context)

def lists(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM specialization")
    specializationlist = dictfetchall(cursor)

    context = {
        "specializationlist": specializationlist
    }

    # Message according medicines Role #
    context['heading'] = "Specialization Details";
    return render(request, 'specialization-list.html', context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM specialization WHERE specialization_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, specializationId):
    context = {
        "fn": "update",
        "specializationDetails": getData(specializationId),
        "heading": 'Update Specialization',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        specialization_logo = None
        if(request.FILES and request.FILES['specialization_logo']):
            specializationImage = request.FILES['specialization_logo']
            fs = FileSystemStorage()
            filename = fs.save(specializationImage.name, specializationImage)
            specialization_logo = "/uploads/"+str(specializationImage)
        cursor.execute("""
                   UPDATE specialization
                   SET specialization_title=%s, specialization_logo=%s, specialization_description=%s WHERE specialization_id = %s
                """, (
            request.POST['specialization_title'],
            specialization_logo,
            request.POST['specialization_description'],
            specializationId
        ))
        context["specializationDetails"] =  getData(specializationId)
        messages.add_message(request, messages.INFO, "Specialization updated succesfully !!!")
        return redirect('specialization-listing')
    else:
        return render(request, 'specialization.html', context)


def add(request):
    context = {
        "fn": "add",
        "heading": 'Add Specialization'
    }
    if (request.method == "POST"):
        specialization_logo = None
        if(request.FILES and request.FILES['specialization_logo']):
            print("All Images")
            specializationImage = request.FILES['specialization_logo']
            print(specializationImage)
            fs = FileSystemStorage()
            filename = fs.save(specializationImage.name, specializationImage)
            specialization_logo = "/uploads/"+str(specializationImage)
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO specialization
		   SET specialization_title=%s, specialization_logo=%s, specialization_description=%s
		""", (
            request.POST['specialization_title'],
            specialization_logo,
            request.POST['specialization_description']))
        return redirect('specialization-listing')
    return render(request, 'specialization.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM specialization WHERE specialization_id=' + id
    cursor.execute(sql)
    messages.add_message(request, messages.INFO, "Specialization Deleted succesfully !!!")
    return redirect('specialization-listing')
