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
    cursor.execute("SELECT * FROM category")
    categorylist = dictfetchall(cursor)

    context = {
        "categorylist": categorylist
    }

    # Message according medicines Role #
    context['heading'] = "Category Details";
    return render(request, 'category-details.html', context)

def lists(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM category")
    categorylist = dictfetchall(cursor)

    context = {
        "categorylist": categorylist
    }

    # Message according medicines Role #
    context['heading'] = "Category Details";
    return render(request, 'category-list.html', context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM category WHERE category_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, categoryId):
    context = {
        "fn": "update",
        "categoryDetails": getData(categoryId),
        "heading": 'Update Category',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        category_logo = None
        if(request.FILES and request.FILES['category_logo']):
            categoryImage = request.FILES['category_logo']
            fs = FileSystemStorage()
            filename = fs.save(categoryImage.name, categoryImage)
            category_logo = "/uploads/"+str(categoryImage)
        cursor.execute("""
                   UPDATE category
                   SET category_title=%s, category_url=%s, category_logo=%s, category_description=%s WHERE category_id = %s
                """, (
            request.POST['category_title'],
            request.POST['category_url'],
            category_logo,
            request.POST['category_description'],
            categoryId
        ))
        context["categoryDetails"] =  getData(categoryId)
        messages.add_message(request, messages.INFO, "Category updated succesfully !!!")
        return redirect('category-listing')
    else:
        return render(request, 'category.html', context)


def add(request):
    context = {
        "fn": "add",
        "heading": 'Add Category'
    }
    if (request.method == "POST"):
        category_logo = None
        if(request.FILES and request.FILES['category_logo']):
            categoryImage = request.FILES['category_logo']
            fs = FileSystemStorage()
            filename = fs.save(categoryImage.name, categoryImage)
            category_logo = "/uploads/"+str(categoryImage)
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO category
		   SET category_title=%s, category_url=%s, category_logo=%s, category_description=%s
		""", (
            request.POST['category_title'],
            request.POST['category_url'],
            category_logo,
            request.POST['category_description']))
        return redirect('category-listing')
    return render(request, 'category.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM category WHERE category_id=' + id
    cursor.execute(sql)
    messages.add_message(request, messages.INFO, "Category Deleted succesfully !!!")
    return redirect('category-listing')
