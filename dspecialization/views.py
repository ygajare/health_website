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
    SQL = "SELECT * FROM dspecialization, specialization, users_user WHERE user_id = dspecialization_doctor_id AND specialization_id = dspecialization_specialization_id"
    if(request.session['user_level_id'] == 3):
        user_id = request.session['user_id']
        SQL = "SELECT * FROM dspecialization, specialization, users_user WHERE user_id = dspecialization_doctor_id AND specialization_id = dspecialization_specialization_id AND user_id = "+str(user_id)
    cursor.execute(SQL)
    dspecializationlist = dictfetchall(cursor)

    context = {
        "dspecializationlist": dspecializationlist
    }

    # Message according medicines Role #
    context['heading'] = "DspecializationConfig Details";
    return render(request, 'dspecialization-details.html', context)

def doctor_specialization(request, userId):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dspecialization, specialization, users_user WHERE user_id = dspecialization_doctor_id AND specialization_id = dspecialization_specialization_id AND user_id = "+userId)        
    dspecializationlist = dictfetchall(cursor)

    context = {
        "dspecializationlist": dspecializationlist
    }

    # Message according medicines Role #
    context['heading'] = "DspecializationConfig Details";
    return render(request, 'dspecialization-details.html', context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dspecialization WHERE dspecialization_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, dspecializationId):
    context = {
        "fn": "update",
        "dspecializationDetails": getData(dspecializationId),
        "doctorlist": getDropDown('users_user', 'user_level_id = 3'),
        "specializationlist":  getDropDown('specialization', 'specialization_id'),
        "heading": 'Update DspecializationConfig',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE dspecialization
                   SET dspecialization_doctor_id=%s, dspecialization_specialization_id=%s, dspecialization_description=%s WHERE dspecialization_id = %s
                """, (
            request.POST['dspecialization_doctor_id'],
            request.POST['dspecialization_specialization_id'],
            request.POST['dspecialization_description'],
            dspecializationId
        ))
        context["dspecializationDetails"] =  getData(dspecializationId)
        messages.add_message(request, messages.INFO, "DspecializationConfig updated succesfully !!!")
        return redirect('dspecialization-listing')
    else:
        return render(request, 'dspecialization.html', context)


def add(request):
    context = {
        "fn": "add",
        "heading": 'Add DspecializationConfig',
        "doctorlist": getDropDown('users_user', 'user_level_id = 3'),
        "specializationlist":  getDropDown('specialization', 'specialization_id')
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO dspecialization
		   SET dspecialization_doctor_id=%s, dspecialization_specialization_id=%s, dspecialization_description=%s
		""", (
            request.POST['dspecialization_doctor_id'],
            request.POST['dspecialization_specialization_id'],
            request.POST['dspecialization_description']))
        return redirect('dspecialization-listing')
    return render(request, 'dspecialization.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM dspecialization WHERE dspecialization_id=' + id
    cursor.execute(sql)
    messages.add_message(request, messages.INFO, "DspecializationConfig Deleted succesfully !!!")
    return redirect('dspecialization-listing')

def getDropDown(table, condtion):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table + " WHERE " + condtion)
    dropdownList = dictfetchall(cursor)
    return dropdownList