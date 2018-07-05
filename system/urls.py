from django.urls import path

#导入视图函数
from . import views

urlpatterns = [
    # 根目录
    path("", views.root, name="root"),
    # 登陆界面
    path("sign_in/", views.sign_in, name="sign_in"),
    # 系统管理员登陆后的路由
    path("system-admin/", views.system_admin, name="sys_admin"),
    # 图书管理员登陆后的路由
    path("books-admin/", views.books_admin, name="books_admin"),
    # 读者登陆后的路由
    path("reader/", views.reader, name="reader"),

    # 读者查看全部图书的路由
    path("reader/all_books/", views.reader_all_books, name="reader_all_books"),
    # 读者查看单本图书详情的路由
    path("reader/all_books/<str:book_name>/", views.reader_book_detail, name="reader_book_detail"),
    # 读者查看个人信息的路由
    path("reader/check_self_info/", views.reader_check_self_info, name="reader_check_self_info"),
    # 读者修改个人信息的路由
    path("reader/change_pwd/", views.reader_change_pwd, name="reader_change_pwd"),
    # 读者修改个人信息成功
    path("reader/change_pwd_succeed/", views.reader_change_pwd_succeed, name="reader_change_pwd_succeed"),
    # 读者借阅某本图书的路由
    #path("reader/borrow/<str:book_name>", views.reader_borrow, name="reader_borrow"),
    # 读者 确定是否借阅某本图书的路由
    path("reader/borrow/confirm_borrow/<str:book_name>", views.reader_confirm_borrow, name="reader_confirm_borrow"),
    # 读者借阅某本图书成功
    path("reader/borrow_succeed/<str:book_name>", views.reader_borrow_succeed, name="reader_borrow_succeed"),
    # 读者查看个人所有借阅信息
    path("reader/self_lend_stream/<str:reader_user>", views.reader_self_lend_stream, name="reader_self_lend_stream"),
    # 读者确认是否归还某本图书的路由
    path("reader/return/confirm_return/<str:book_name>", views.reader_confirm_return, name="reader_confirm_return"),
    # 读者归还某本图书成功
    path("reader/return_succeed/<str:book_name>", views.reader_return_succeed, name="reader_return_succeed"),

    # 404页面路由
    path("404/",views.page_404,name="page_404"),

    # 系统管理员查看所有图书管理员信息的路由
    path("system-admin/books_admin_all_members/", views.books_admin_all_members, name="books_admin_all_members"),
    # 系统管理员修改所有图书管理员信息的路由
    path("system-admin/change_books_admin_all_members/", views.change_books_admin_all_members, name="change_books_admin_all_members"),
    # 系统管理员修改某个图书管理员信息的路由
    path("system-admin/edit_books_admin/<str:books_admin_name>/", views.edit_books_admin, name="edit_books_admin"),
    # 系统管理员添加一个图书管理员信息的路由
    path("system-admin/add_one_books_admin/", views.add_one_books_admin, name="add_one_books_admin"),
    # 系统管理员查看个人信息
    path("system-admin/check_self_info/", views.system_admin_check_self_info, name="system_admin_check_self_info"),

    # 系统管理员查看所有读者信息的路由
    path("system-admin/reader_all_members/", views.reader_all_members, name="reader_all_members"),
    # 系统管理员修改所有读者信息的路由
    path("system-admin/change_reader_all_members/", views.change_reader_all_members, name="change_reader_all_members"),
    # 系统管理员修改某个读者信息的路由
    path("system-admin/edit_reader/<str:reader_name>/", views.edit_reader, name="edit_reader"),
    # 系统管理员添加一个读者信息的路由
    path("system-admin/add_one_reader/", views.add_one_reader, name="add_one_reader"),

    # 系统管理员修改个人信息
    path("system-admin/change_pwd/", views.system_admin_change_pwd, name="system_admin_change_pwd"),
    # 系统管理员修改个人信息成功
    path("system-admin/change_pwd_succeed/", views.system_admin_change_pwd_succeed, name="system_admin_change_pwd_succeed"),

    # 图书管理员查看所有图书信息
    path("books-admin/all_books/", views.books_admin_all_books, name="all_books"),
    # 图书管理员对单本图书进行编辑的路由
    path("books-admin/edit_book/<str:book_name>/", views.books_admin_edit_book, name="edit_book"),
    # 图书管理员对图书编辑成功的路由
    path("books-admin/edit_book_succeed/", views.books_admin_edit_book_succeed, name="edit_book_succeed"),
    # 图书管理员填写要新增的图书的信息的路由
    path("books-admin/add_one_book/", views.add_one_book, name="add_one_book"),

    # 图书管理员 查看所有借阅与归还信息
    path("books-admin/all_lend_list/", views.books_admin_all_lend_list, name="lend_list"),
    # 图书管理员 查看所有借阅信息
    path("books-admin/borrow_list/", views.books_admin_borrow_list, name="borrow_list"),
    # 图书管理员 查看所有归还信息
    path("books-admin/return_list/", views.books_admin_return_list, name="return_list"),

    # 图书管理员查看个人信息
    path("books-admin/check_self_info/", views.books_admin_check_self_info, name="books_admin_check_self_info"),
    # 图书管理员修改个人信息页面的路由
    path("books-admin/change_pwd/", views.books_admin_change_pwd, name="books_admin_change_pwd"),
    # 图书管理员个人信息修改成功
    path("book-admin/change_pwd_succeed/", views.books_admin_change_pwd_succeed, name="books_admin_change_pwd_succeed"),
    # 图书管理员查看单本图书信息
    path("books-admin/all_books/<str:book_name>/", views.books_admin_book_detail, name="book_detail"),
    # 图书管理员 删除某本图书的信息，同时提示删除成功
    path("books-admin/delete/<str:book_name>/", views.books_admin_delete_book, name="books_admin_delete_book"),
]