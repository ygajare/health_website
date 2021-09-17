from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db import connection

# Create your views here.

def index(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM category")
    categorylist = dictfetchall(cursor)

    context = {
        "categorylist": categorylist
    }

    # Message according medicines Role #
    context['heading'] = "Category Details";
    return render(request, 'index.html', context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')	
	
def listing(request, employeeId):
    try:
        employeelist =  employee.objects.filter(Q(employee_level=employeeId))
    except Exception as e:
        return HttpResponse('Something went wrong. Error Message : '+ str(e))

    context = {
        "showmsg": True,
        "message": "User Updated Successfully",
        "employeelist": employeelist
    }	
	    # Message according Users Role #
    if(employeeId == "1"):
        context['heading'] = "User Report";
    return render(request,'employee-report.html',context)
	