from django.shortcuts import render, redirect
from django.shortcuts import HttpResponseRedirect,Http404,render_to_response
from django.http    import HttpResponse
from django.views.decorators import csrf
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session

from .models import Book, System_Person, Booksys_Person, Read_Person, Lend_Stream

import MySQLdb.cursors    #

# Create your views here.


#user = None
SqlName = "bms"
user_name = "test"
user_type = 0

# 连接数据库
def cn_connectDatabase():
    try:
        connect = MySQLdb.connect("localhost", "curry", "heqinyang", SqlName, charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
        cursor = connect.cursor()
        return connect, cursor
    
    except MySQLdb.Error as e:
        print("connect ", SqlName, " failed: ", e.args[0])
        pass

# 根目录视图函数
def root(request):
    return render(request, "system/home_page.html")



# 登陆页面视图函数
def sign_in(request):
    #错误类型初始置0
    context = {
        "error_type": 0,
    }
    if request.POST:
        context['error_type'] = 0
        #提取表单中的输入数据
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        #查找system_person表
        username_search_system_person_result = System_Person.objects.filter(System_User=username)
        password_search_system_person_result = System_Person.objects.filter(System_User=username, System_Password=password)
        #查找booksys_person表
        username_search_book_person_result = Booksys_Person.objects.filter(BookSys_User=username)
        password_search_book_person_result = Booksys_Person.objects.filter(BookSys_User=username, BookSys_Password=password)
        #查找reader_person表
        username_search_reader_person_result = Read_Person.objects.filter(Person_User=username)
        password_search_reader_person_result = Read_Person.objects.filter(Person_User=username, Person_Password=password)
        #如果密码不存在， 登陆失败，返回用户名不存在,错误类型 -1
        if len(username_search_system_person_result) <= 0 and len(username_search_book_person_result) <= 0 and len(username_search_reader_person_result) <= 0:
            #将错误类型置 -1 弹出相应的错误信息
            context['error_type'] = -1
            return render(request, "system/sign_in.html", context)
        #系统管理员
        elif len(username_search_system_person_result) > 0 :
            #密码错误1
            if len(password_search_system_person_result) <= 0:
                context['error_type'] = 1
                return render(request, "system/sign_in.html", context)
            else:
                global user_name
                user_name = username
                request.session['user_type'] = 1
                request.session['user_name'] = username
                return redirect("/system-admin/")

        #图书管理员
        elif len(username_search_book_person_result) > 0:
            #密码错误2
            if len(password_search_book_person_result) <= 0:
                context['error_type'] = 1
                return render(request, "system/sign_in.html", context)
            else:
                #request.session['login_status'] = "YES"
                # if user is not None:
                #     login(request, user)
                global user_name
                user_name = username
                request.session['user_type'] = 2
                request.session['user_name'] = username
                return redirect("/books-admin/")

        #读者
        elif len(username_search_reader_person_result) > 0:
            #密码错误3
            if len(password_search_reader_person_result) <= 0:
                context['error_type'] = 1
                return render(request, "system/sign_in.html", context)
            else:
                global user_name
                user_name = username
                request.session['user_type'] = 3
                request.session['user_name'] = username
                return redirect("/reader/")

    return render(request, "system/sign_in.html")


def system_admin(request):
    return render(request,"system/system_admin.html")



# 图书管理员登陆后的首页的视图函数
@login_required(login_url="/404/")
def books_admin(request):
    return render(request, "system/books_admin.html")




def reader(request):
    # 将登陆时保存的读者信息提取出来传入模板
    context = {
        "reader_user" : request.session['user_name'],
    }
    return render(request,"system/reader.html", context)


# 404页面
def page_404(request):
    return render(request, "system/page_404.html")



# 系统管理员查看所有图书管理员
def books_admin_all_members(request):
    # 返回所有图书管理员数据集
    All_books_admin = Booksys_Person.objects.all()
    # 查询所有books_admind管理员的信息，构造如context传入模板
    context = {
        "All_books_admind" : All_books_admin,
    }
    # 如果不存在至少一个图书管理员的账号，返回404页面
    if len(All_books_admin) <= 0:
        return redirect('/404/')
    else:
        return render(request, "system/books_admin_all_members.html", context)



# 系统管理员修改图书管理员的信息
def change_books_admin_all_members(request):
    # 获取所有图书管理员的数据集
    All_books_admin = Booksys_Person.objects.all()
    # 查询所有books_admind管理员的信息，构造如context传入模板
    context = {
        "All_books_admin": All_books_admin,
    }
    # 如果不存在至少一个图书管理员的账号，返回404页面
    if len(All_books_admin) <= 0:
        return redirect('/404/')
    else:
        return render(request, "system/change_books_admin_all_members.html", context)



# 系统管理员修改某个图书管理员的信息
def edit_books_admin(request, books_admin_name):
    # 获取该图书管理员数据
    books_admin_set = Booksys_Person.objects.filter(BookSys_User=books_admin_name)
    # 如果是提交表单
    if request.POST:
        # 根据路由获取相应的图书管理员的数据
        origin_books_admin = Booksys_Person.objects.filter(BookSys_User=books_admin_name)
        origin_books_admin.update(BookSys_User=request.POST['books_admin_user'])
        origin_books_admin.update(BookSys_Password=request.POST['books_admin_pwd'])
        origin_books_admin.update(BookSys_Name=request.POST['books_admin_name'])
        origin_books_admin.update(BookSys_Phone=request.POST['books_admin_phone'])

        return redirect("/system-admin/change_books_admin_all_members/")

    if len(books_admin_set) <= 0:
        return redirect('/404/')
    else:
        books_admin = books_admin_set[0]
        context = {
            "books_admin": books_admin,
        }
        return render(request, "system/edit_books_admin.html", context)



# 系统管理员添加一个图书管理员的信息
def add_one_books_admin(request):
    if request.POST:
        if request.POST['books_admin_phone'] == None:
            return redirect("/404/")
        books_admin_phone = request.POST['books_admin_phone']
        p = Booksys_Person.objects.create(BookSys_User=request.POST['books_admin_user'], BookSys_Password=request.POST['books_admin_pwd'], BookSys_Name=request.POST['books_admin_name'], BookSys_Phone=books_admin_phone)
        return redirect("/system-admin/change_books_admin_all_members/")
    return render(request, "system/add_one_books_admin.html")


# 系统管理员查看所有读者
def reader_all_members(request):
    # 返回所有读者数据集
    All_reader = Read_Person.objects.all()
    context = {
        "All_reader" : All_reader,
    }
    # 如果不存在至少一个图书管理员的账号，返回404页面
    if len(All_reader) <= 0:
        return redirect('/404/')
    else:
        return render(request, "system/reader_all_members.html", context)



# 系统管理员修改读者的信息
def change_reader_all_members(request):
    # 获取所有读者的数据集
    All_reader = Read_Person.objects.all()
    # 查询所有读者的信息，构造context传入模板
    context = {
        "All_reader": All_reader,
    }
    # 如果不存在至少一个图书管理员的账号，返回404页面
    if len(All_reader) <= 0:
        return redirect('/404/')
    else:
        return render(request, "system/change_reader_all_members.html", context)



# 系统管理员修改某个读者的信息
def edit_reader(request, reader_name):
    # 获取该读者数据
    reader_set = Read_Person.objects.filter(Person_User=reader_name)
    # 如果是提交表单
    if request.POST:
        # 根据路由获取相应的图书管理员的数据
        origin_books_admin = Read_Person.objects.filter(Person_User=reader_name)
        origin_books_admin.update(Person_User=request.POST['reader_user'])
        origin_books_admin.update(Person_Password=request.POST['reader_pwd'])
        origin_books_admin.update(Person_Name=request.POST['reader_name'])
        origin_books_admin.update(Person_Phone=request.POST['reader_phone'])
        origin_books_admin.update(Person_CanBorrow=request.POST['reader_canborrow'])

        return redirect("/system-admin/change_reader_all_members/")

    if len(reader_set) <= 0:
        return redirect('/404/')
    else:
        reader = reader_set[0]
        context = {
            "reader": reader,
        }
        return render(request, "system/edit_reader.html", context)



# 系统管理员添加某个读者的信息
def add_one_reader(request):
    if request.POST:
        if request.POST['reader_phone'] == None:
            return redirect("/404/")
        books_admin_phone = request.POST['reader_phone']
        p = Read_Person.objects.create(Person_User=request.POST['reader_user'], Person_Password=request.POST['reader_pwd'], Person_Name=request.POST['reader_name'], Person_Phone=request.POST['reader_phone'], Person_CanBorrow=request.POST['reader_canborrow'])
        return redirect("/system-admin/change_reader_all_members/")
    return render(request, "system/add_one_reader.html")


# 系统管理员查看自己的信息
def system_admin_check_self_info(request):
    #user = Booksys_Person.objects.filter(BookSys_User=request.session['user_name'])[0]
    user = System_Person.objects.filter(System_User=request.session['user_name'])[0]
    print(user)
    context = {
        "user": user,
    }
    return render(request,"system/system_admin_check_self_info.html", context)



# 系统管理员修改自己的信息
def system_admin_change_pwd(request):
    global user_name
    user_type = request.session['user_type']

    if request.POST:
        origin_user = System_Person.objects.filter(System_User=request.POST['system_admin_user'])
        origin_user.update(System_User=request.POST['system_admin_user'],
                           System_Password=request.POST['system_admin_pwd'],
                           System_Name=request.POST['system_admin_name'],
                           System_Phone=request.POST['system_admin_phone'])
        origin_user = System_Person.objects.filter(System_User=request.POST['system_admin_user'])[0]
        request.session['user_type'] = 1
        context = {
            "user_type": int(1),
            "user_data": origin_user,
        }
        # return render(request, "system/books_admin_change_pwd.html", context)
        return redirect("/system-admin/change_pwd_succeed/")

    if user_type == 1:
        current = System_Person.objects.filter(System_User=user_name)
        # print(current)
        if len(current) <= 0:
            return redirect("/404/")
        else:
            current_user_data = current[0]
            # print(current_user_data.BookSys_Name)
            context = {
                "user_type": user_type,
                "user_data": current_user_data,
            }
            return render(request, "system/system_admin_change_pwd.html", context)
    # return render(request, "system/books_admin_change_pwd.html")
    return redirect("/404/")



# 系统管理员 修改个人信息成功
def system_admin_change_pwd_succeed(request):
    return render(request, "system/system_admin_change_pwd_succeed.html")



# 读者 查询全部图书信息
# 读者 可以从全部图书里的Borrow按钮借阅图书
def reader_all_books(request):
    context = {}
    # 获取所有图书对象，返回一个列表
    obj_list = Book.objects.all()
    context['obj_list'] = obj_list
    context['reader_user'] = request.session['user_name']
    return render(request,"system/reader_all_books.html", context)



# 读者 查看单本图书详情信息
def reader_book_detail(request, book_name):
    result_set = Book.objects.filter(book_name=book_name)
    # 如果该书名在数据库中不存在，返回404页面
    if len(result_set) <= 0:
        return redirect('/404/')
    else:
        # 由于书名唯一，所以结果是set里的下标为[0]的这个对象
        book_information = result_set[0]
        # 构造一个要传入模板的字典
        context = {
            "book_info": book_information,
        }
        return render(request, "system/reader_book_detail.html", context)



# 读者 借阅某本图书
#def reader_borrow(request, book_name):
    #return render(request,"system/reader_borrow.html")



# 读者 确定借阅某本图书
def reader_confirm_borrow(request, book_name):
    context = {
        "book_name" : book_name,
    }
    return render(request, "system/reader_confirm_borrow.html", context)



# 读者 借阅某本图书成功
def reader_borrow_succeed(request, book_name):

    # 提取读者账号
    reader_username = request.session['user_name']
    # 获取该条数据
    reader = Read_Person.objects.filter(Person_User=user_name)
    # 获取可借余量的同时将其减1
    reader_canborrow = reader[0].Person_CanBorrow - 1
    # 更新可借余量
    reader.update(Person_CanBorrow=reader_canborrow)
    # 更新书的状态 从未借出 0 更新至 已借出 1
    book = Book.objects.filter(book_name=book_name)
    book.update(book_status = 1)
    # 构建 lend 数据
    # 添加如数据库
    one_len_stream = Lend_Stream.objects.create(lend_stream_reader_name=reader_username, lend_stream_book_name=book_name, lend_stream_type=1)
    context = {
        "book_name" : book_name,
        "reader_user" : reader_username,
    }
    return render(request, "system/reader_borrow_succeed.html", context)



# 读者 查看自身的借阅信息
def reader_self_lend_stream(request, reader_user):
    # 提取读者账号
    reader_username = request.session['user_name']
    # 根据传入的reader_user 查 lend_stream 表中的数据
    lend_information = Lend_Stream.objects.filter(lend_stream_reader_name=reader_user)
    # 根据传入的reader_user 查该读者的可借余量
    reader_canborrow = Read_Person.objects.filter(Person_User=reader_user)[0].Person_CanBorrow
    context = {
        "lend_stream" : lend_information,
        "reader_canborrow" : reader_canborrow,
        "reader_user" : reader_username,
    }
    return render(request, "system/reader_self_lend_stream.html", context)



# 读者 确认归还某本图书
def reader_confirm_return(request, book_name):
    context = {
        "book_name": book_name,
    }
    return render(request, "system/reader_confirm_return.html", context)



# 读者归还某本图书成功
def reader_return_succeed(request, book_name):
    # 提取读者账号
    reader_username = request.session['user_name']
    # 获取该条数据
    reader = Read_Person.objects.filter(Person_User=user_name)
    # 获取可借余量的同时将其加1
    reader_canborrow = reader[0].Person_CanBorrow + 1
    # 更新可借余量
    reader.update(Person_CanBorrow=reader_canborrow)
    # 更新书的状态 从已借出 1 更新至 未借出 0
    book = Book.objects.filter(book_name=book_name)
    book.update(book_status=0)
    # 构建 lend 数据
    # 添加如数据库
    one_len_stream = Lend_Stream.objects.create(lend_stream_reader_name=reader_username,
                                                lend_stream_book_name=book_name, lend_stream_type=2)
    context = {
        "book_name": book_name,
        "reader_user": reader_username,
    }
    return render(request, "system/reader_return_succeed.html", context)



# 读者 查看个人信息
def reader_check_self_info(request):
    # 提取读者账号
    reader_username = request.session['user_name']
    user = Read_Person.objects.filter(Person_User=request.session['user_name'])[0]
    #print(user)
    context = {
        "user": user,
        "reader_user": reader_username,
    }
    return render(request, "system/reader_check_self_info.html", context)



# 读者 修改个人信息
def reader_change_pwd(request):
    user_name = request.session['user_name']
    user_type = request.session['user_type']

    if request.POST:
        origin_user = Read_Person.objects.filter(Person_User=request.POST['reader_user'])
        origin_user.update(Person_User=request.POST['reader_user'],
                           Person_Password=request.POST['reader_pwd'],
                           Person_Name=request.POST['reader_name'],
                           Person_Phone=request.POST['reader_phone'])
        origin_user = Read_Person.objects.filter(Person_User=request.POST['reader_user'])[0]
        request.session['user_type'] = 3
        context = {
            "user_type": int(3),
            "user_data": origin_user,
        }
        # return render(request, "system/books_admin_change_pwd.html", context)
        return redirect("/reader/change_pwd_succeed/")

    if user_type == 3:
        current = Read_Person.objects.filter(Person_User=user_name)
        # print(current)
        if len(current) <= 0:
            return redirect("/404/")
        else:
            current_user_data = current[0]
            # print(current_user_data.BookSys_Name)
            context = {
                "user_type": user_type,
                "user_data": current_user_data,
                "reader_user" : user_name,
            }
            return render(request, "system/reader_change_pwd.html", context)
    



# 读者 修改个人信息成功
def reader_change_pwd_succeed(request):
    return render(request, "system/reader_change_pwd_succeed.html")




# 图书管理员 查看全部图书
def books_admin_all_books(request):
    context = { }
    # 获取所有图书对象，返回一个列表
    obj_list = Book.objects.all()
    context['obj_list'] = obj_list

    return render(request, "system/all_books.html", context)



# 图书管理员 查看单本图书详情
def books_admin_book_detail(request, book_name):
    # 使用通过路由传入的参数 book_name 来查找图书对象
    # 为了更好理解filter返回的是一个集合，所以采用下面的写法
    result_set = Book.objects.filter(book_name=book_name)
    # 如果该书名在数据库中不存在，返回404页面
    if len(result_set) <= 0:
        return redirect('/404/')
    else:
        # 由于书名唯一，所以结果是set里的下标为[0]的这个对象
        book_information = result_set[0]
        # 构造一个要传入模板的字典
        context = {
            "book_info" : book_information,
        }
        return render(request, "system/books_admin_book_detail.html", context)



# 图书管理员 对单本图书进行编辑
def books_admin_edit_book(request, book_name):
    result_set = Book.objects.filter(book_name=book_name)
    # 如果是提交表单
    if request.POST:
        origin_book = Book.objects.filter(book_name=book_name)
        # 覆盖修改信息
        origin_book.update(book_name=request.POST['book_name'])
        origin_book.update(book_author=request.POST['book_author'])
        origin_book.update(book_publish=request.POST['book_publish'])
        origin_book.update(book_language=request.POST['book_language'])
        origin_book.update(book_price=request.POST['book_price'])
        origin_book.update(book_publish_date=request.POST['book_publish_date'])
        origin_book.update(book_ISBN=request.POST['book_ISBN'])
        origin_book.update(book_introduction=request.POST['book_introduction'])
        context = {}
        # 重新构造传入信息
        #context['book_info'] = Book.objects.filter(book_name=request.POST['book_name'])[0]
        #return render(request, "system/edit_book_succeed.html")
        return redirect("/books-admin/all_books/" + str(request.POST['book_name']) + "/")

    if len(result_set) <= 0:
        return redirect("/404")
    else:
        book_information = result_set[0]
        context = {
            "book_info" : book_information,
        }
        return render(request, "system/edit_book.html", context)



# 图书管理员 对图书编辑成功
def books_admin_edit_book_succeed(request):
    return render(request, "system/edit_book_succeed.html")



# 图书管理员 填写新增图书的信息的页面
def add_one_book(request):
    return render(request, "system/add_one_book.html")



# 借阅总览
def books_admin_all_lend_list(request):
    # 获取所有借阅与归还数据
    All_lend_stream = Lend_Stream.objects.all()
    # 构造context传入模板
    context = {
        "All_lend_stream" : All_lend_stream,
    }
    return render(request, "system/all_lend_list.html", context)



# 借阅流水
def books_admin_borrow_list(request):
    # 获取所有借阅数据 type = 1 为借阅
    All_borrow_stream = Lend_Stream.objects.filter(lend_stream_type=1)
    context = {
        "All_borrow_stream": All_borrow_stream,
    }
    return render(request, "system/borrow_list.html", context)



# 归还流水
def books_admin_return_list(request):
    # 获取所有借阅数据 type = 2 为归还
    All_return_stream = Lend_Stream.objects.filter(lend_stream_type=2)
    context = {
        "All_return_stream" : All_return_stream,
    }
    return render(request, "system/return_list.html", context)



# 图书管理员查看个人信息
def books_admin_check_self_info(request):
    user = Booksys_Person.objects.filter(BookSys_User=request.session['user_name'])[0]
    print(user)
    context = {
        "user" : user,
    }
    return render(request, "system/books_admin_check_self_info.html", context)

# 图书管理员修改密码
def books_admin_change_pwd(request):
    user_name = request.session['user_name']
    user_type = request.session['user_type']

    if request.POST:
        origin_user = Booksys_Person.objects.filter(BookSys_User=request.POST['books_admin_user'])
        origin_user.update(BookSys_User=request.POST['books_admin_user'], BookSys_Password=request.POST['books_admin_pwd'], BookSys_Name=request.POST['books_admin_name'], BookSys_Phone=request.POST['books_admin_phone'])
        origin_user = Booksys_Person.objects.filter(BookSys_User=request.POST['books_admin_user'])[0]
        request.session['user_type'] = 2
        context = {
            "user_type": int(2),
            "user_data": origin_user,
        }
        #return render(request, "system/books_admin_change_pwd.html", context)
        return redirect("/book-admin/change_pwd_succeed/")


    if user_type == 2:
        current = Booksys_Person.objects.filter(BookSys_User=user_name)
        #print(current)
        if len(current) <= 0:
            return redirect("/404/")
        else:
            current_user_data = current[0]
            #print(current_user_data.BookSys_Name)
            context = {
                "user_type" : user_type,
                "user_data" : current_user_data,
            }
            print(user_name)
            return render(request, "system/books_admin_change_pwd.html", context)
    return redirect("/404/")



# 图书管理员修改个人信息成功
def books_admin_change_pwd_succeed(request):
    return render(request, "system/books_admin_change_pwd_succeed.html")

# 图书管理员删除某本图书
# 返回提示删除成功
def books_admin_delete_book(request, book_name):
    # 查找这本书的数据
    book = Book.objects.filter(book_name=book_name)
    book.delete()
    return render(request, "system/delete_book_succeed.html")
