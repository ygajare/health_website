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
    cursor.execute("SELECT * FROM quotation")
    quotationlist = dictfetchall(cursor)

    context = {
        "quotationlist": quotationlist
    }

    # Message according medicines Role #
    context['heading'] = "Quotation Details";
    return render(request, 'quotation-details.html', context)

def details(request, quotationId):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM quotation, users_user, specialization  WHERE quotation_patient_id = user_id AND quotation_specialization_id = specialization_id AND quotation_id = "+quotationId)
    quotationdetails = dictfetchall(cursor)

    context = {
        "quotationdetails": quotationdetails[0],
        "quotationlist": getAllReply(request, quotationId)
    }

    # Message according medicines Role #
    context['heading'] = "Quotation Details";
    return render(request, 'quotation-details.html', context)

def reply_details(request, replyId):
    cursor = connection.cursor()
    SQL = "SELECT * FROM quotation, users_user, specialization, reply  WHERE reply_quotation_id = quotation_id AND quotation_patient_id = user_id AND quotation_specialization_id = specialization_id AND reply_id = "+replyId
    cursor.execute(SQL)
    replydetails = dictfetchall(cursor)

    context = {
        "replydetails": replydetails[0],
    }

    # Message according medicines Role #
    context['heading'] = "Quotation"
    return render(request, 'reply-details.html', context)

def getAllReply(request, id):
    cursor = connection.cursor()
    SQL = "SELECT * FROM reply WHERE reply_quotation_id = " + id
    user_level_id = str(request.session.get('user_level_id', None))
    doctor_id = str(request.session.get('user_id', None))
    if(user_level_id == "3"):
       SQL = "SELECT * FROM reply WHERE reply_quotation_id = " + id +" AND reply_doctor_id = "+doctor_id
    print(SQL+" == >"+user_level_id)
    cursor.execute(SQL)
    dataList = dictfetchall(cursor)
    return dataList

def lists(request):
    cursor = connection.cursor()
    user_level_id = str(request.session.get('user_level_id', None))
    user_id = str(request.session.get('user_id', None))
    SQL = "SELECT * FROM quotation, users_user, specialization  WHERE quotation_patient_id = user_id AND quotation_specialization_id = specialization_id"
    if(user_level_id == 2):
         SQL = "SELECT * FROM quotation, users_user, specialization  WHERE quotation_patient_id = user_id AND quotation_specialization_id = specialization_id AND user_id = "+user_id
    cursor.execute(SQL)
    quotationlist = dictfetchall(cursor)

    context = {
        "quotationlist": quotationlist
    }

    # Message according medicines Role #
    context['heading'] = "Quotation Details";
    return render(request, 'quotation-list.html', context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM quotation WHERE quotation_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0]

def update(request, quotationId):
    context = {
        "fn": "update",
        "quotationDetails": getData(quotationId),
        "heading": 'Update Quotation',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        quotation_logo = None
        if(request.FILES and request.FILES['quotation_logo']):
            quotationImage = request.FILES['quotation_logo']
            fs = FileSystemStorage()
            filename = fs.save(quotationImage.name, quotationImage)
            quotation_logo = "/uploads/"+str(quotationImage)
            cursor.execute("""
                   UPDATE `quotation` SET `quotation_insurance` = %s, `quotation_budget` = %s, `quotation_schedule` = %s, `quotation_start_date` = %s, `quotation_end_date` = %s, `quotation_start_time` = %s, `quotation_end_time` = %s, `quotation_rating` = %s, `quotation_location` = %s, `quotation_qualification` = %s, `quotation_experience` = %s, `quotation_image` = %s, `quotation_description` = %s WHERE `quotation_id` = %s; 
                """, (
            request.POST['quotation_insurance'],
            request.POST['quotation_budget'],
            request.POST['quotation_schedule'],
            request.POST['quotation_start_date'],
            request.POST['quotation_end_date'],
            request.POST['quotation_start_time'],
            request.POST['quotation_end_time'],
            request.POST['quotation_rating'],
            request.POST['quotation_location'],
            request.POST['quotation_qualification'],
            request.POST['quotation_experience'],
            quotation_logo,
            request.POST['quotation_description'],
            quotationId
        ))
        context["quotationDetails"] =  getData(quotationId)
        messages.add_message(request, messages.INFO, "Quotation updated succesfully !!!")
        return redirect('quotation-listing')
    else:
        return render(request, 'quotation.html', context)


def finalize(request, replyId, quotationId):
    context = {
        "fn": "update",
        "quotationDetails": getData(quotationId),
        "heading": 'Update Quotation',
    }
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE `quotation` SET `quotation_reply_id` = %s WHERE `quotation_id` = %s; 
        """, (
        replyId,
        quotationId
    ))
    messages.add_message(request, messages.INFO, "Your quotation has been succesfully  finalized. We reported to doctors !!!")
    return redirect('/quotation/reply-details/'+replyId)

def add(request, specializationId):
    if(request.session.get('authenticated', False) != True):
        messages.add_message(request, messages.INFO, "Kindly login to fill your request for quotations")
        return redirect('/users')
    context = {
        "fn": "add",
        "heading": 'Add Quotation',
        "specialization": getSpecialiationDetails(specializationId)
    }
    if (request.method == "POST"):
        patient_id = str(request.session.get('user_id', None))
        quotation_logo = None
        if(request.FILES and request.FILES['quotation_logo']):
            quotationImage = request.FILES['quotation_logo']
            fs = FileSystemStorage()
            filename = fs.save(quotationImage.name, quotationImage)
            quotation_logo = "/uploads/"+str(quotationImage)
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO quotation
		   SET `quotation_patient_id` = %s, `quotation_specialization_id` = %s, `quotation_insurance` = %s, `quotation_budget` = %s, `quotation_schedule` = %s, `quotation_start_date` = %s, `quotation_end_date` = %s, `quotation_start_time` = %s, `quotation_end_time` = %s, `quotation_rating` = %s, `quotation_location` = %s, `quotation_qualification` = %s, `quotation_experience` = %s, `quotation_image` = %s, `quotation_description` = %s
		""", (
            patient_id,
            request.POST['quotation_specialization_id'],
            request.POST['quotation_insurance'],
            request.POST['quotation_budget'],
            request.POST['quotation_schedule'],
            request.POST['quotation_start_date'],
            request.POST['quotation_end_date'],
            request.POST['quotation_start_time'],
            request.POST['quotation_end_time'],
            request.POST['quotation_rating'],
            request.POST['quotation_location'],
            request.POST['quotation_qualification'],
            request.POST['quotation_experience'],
            quotation_logo,
            request.POST['quotation_description']))
        messages.add_message(request, messages.INFO, "Your request has been submitted. You will can track from your My Requests section.")
        return redirect('/specialization/list')
    return render(request, 'quotation.html', context)

def quotation_reply(request, quotationId):
    if(request.session.get('authenticated', False) != True):
        messages.add_message(request, messages.INFO, "Kindly login to fill your request for replys")
        return redirect('/users')
    context = {
        "fn": "add",
        "heading": 'Add Quotation',
    }
    if (request.method == "POST"):
        doctor_id = str(request.session.get('user_id', None))
        reply_file = None
        if(request.FILES and request.FILES['reply_file']):
            replyImage = request.FILES['reply_file']
            fs = FileSystemStorage()
            filename = fs.save(replyImage.name, replyImage)
            reply_file = "/uploads/"+str(replyImage)
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO reply
		   SET `reply_treatment` = %s, `reply_doctor_id` = %s,`reply_quotation_id`=%s, `reply_doctor` = %s, `reply_qualification` = %s, `reply_experience` = %s, `reply_hospital` = %s, `reply_session` = %s, `reply_start_date` = %s, `reply_end_date` = %s, `reply_cost` = %s, `reply_insurace` = %s, `reply_location` = %s, `reply_file` = %s, `reply_description` = %s; 
		""", (
            request.POST['reply_treatment'],
            doctor_id,
            quotationId,
            request.POST['reply_doctor'],
            request.POST['reply_qualification'],
            request.POST['reply_experience'],
            request.POST['reply_hospital'],
            request.POST['reply_session'],
            request.POST['reply_start_date'],
            request.POST['reply_end_date'],
            request.POST['reply_cost'],
            request.POST['reply_insurace'],
            request.POST['reply_location'],
            reply_file,
            request.POST['reply_description']))
        messages.add_message(request, messages.INFO, "Your request for the quotation has been submitted.")
        return redirect('/quotation/details/'+quotationId)
    return render(request, 'quotation-reply.html', context)


def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM quotation WHERE quotation_id=' + id
    cursor.execute(sql)
    messages.add_message(request, messages.INFO, "Quotation Deleted succesfully !!!")
    return redirect('quotation-listing')

def getSpecialiationDetails(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM specialization WHERE specialization_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0]