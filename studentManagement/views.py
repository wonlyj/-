import sqlite3
from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import StudentModel, StudentInformationModel, CourseModel
from django.forms.models  import model_to_dict
# Create your views here.
import json

# def some_view(request):
#     if request.user.is_authenticated:
#         user_profile = StudentModel.objects.get(username=request.user.username)

# 主界面
def index(request):
    context = {
        'status': '未登录状态'
    }

    if 'user' in request.session:
        if 'yourname' in request.session['user']:
            username = request.session['user']['username']
            yourname = request.session['user']['yourname']
            context['status'] = yourname if yourname else username

    return render(request, 'studentManage/index.html', context)

# 登录界面
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not all([username,password]):
            context = {
                'status': '错误！用户名和密码不能为空！',
                'length': 0
            }
            return render(request, 'studentManage/login.html', context)
        else:
            student = StudentModel.objects.filter(username=username,password=password)
            if len(student):
                # 将用户的信息存放到session中，session在中间件中是默认启用的
                request.session['user'] = {
                    'user_id':student[0].user_id,
                    'username': username,
                    'password': password
                }
                context = {
                    'status': student[0].yourname,
                    'msg': '已登录',
                    'lenght': 1
                }
                return render(request, 'studentManage/index.html', context)
            else:
                context = {
                    'status': '用户名或密码错误！请重新输入！如未注册，请先注册！'
                }
                return render(request, 'studentManage/login.html', context)
    else:
        context = {
            'status': '请输入用户名和密码',
            'length': 0
        }
        return render(request, 'studentManage/login.html', context)

#注册界面
def regist(request):
    if request.method == "POST":
        username = request.POST.get("username")
        yourname = request.POST.get("yourname")
        password = request.POST.get("password")
        verif_password = request.POST.get("verif_password")
        student = StudentModel.objects.filter(username=username)
        # 注册验证错误信息汇总
        error_message = ""
        if not all([username,yourname,password,verif_password]):
            error_message+="注册信息不能为空;\n"
        if student:
            error_message+="该用户名已存在;\n"
        if password!=verif_password:
            error_message+="两次密码输入不一致;\n"
        # 如果存在注册信息则重定向到注册页面
        if error_message:
            context = {
                "error": error_message
            }
            return render(request, 'studentManage/regist.html', context)

        # 注册信息有效，注册成功
        stu_data = StudentModel()
        stu_data.username = username
        stu_data.yourname = yourname
        stu_data.password = password
        stu_data.save()
        context = {
            'status': yourname+'  注册成功，请输入用户名密码登录！',
        }

        request.session['user'] = {
            'user_id': stu_data.user_id,
            'username': username,
            'yourname': yourname,
            'password': password
        }

        return render(request, 'studentManage/login.html', context)

    else:
        return render(request, 'studentManage/regist.html')


# 退出界面
def logout(request):
    # 注销掉用户，从删除session中保存的信息
    del request.session['user']
    return render(request, 'studentManage/index.html')


# 增加数据 增加只能root用户或者管理员才能操作
def add(request):
    if request.method == "POST":
        root_information = request.session['user']
        user_id = root_information['user_id']
        root_id = StudentModel.objects.get(pk=user_id).user_id
        if user_id == root_id:
            stu_id = request.POST.get('stu_id')
            stu_name = request.POST.get('stu_name')
            if not all([stu_id, stu_name]):
                context = {
                    'msg': '学号或名字有遗漏',
                }
                return render(request, 'studentManage/add.html', context)
            stu_data = StudentInformationModel()
            stu_data.user_id = root_id
            stu_data.stu_id = stu_id
            stu_data.stu_name = stu_name
            stu_data.stu_phone = request.POST.get('stu_phone')
            stu_data.stu_address = request.POST.get('stu_address')
            stu_data.stu_faculty = request.POST.get('stu_faculty')
            stu_data.stu_major = request.POST.get('stu_major')
            stu_data.save()
            context = {
                'success': '增加成功',
            }
            return render(request, 'studentManage/add.html', context)
        else:
            context = {
                'error': '只用root用户和管理员才能操作'
            }
            return render(request, 'studentManage/add.html', context)
    else:
        return render(request, 'studentManage/add.html')


# 查询
def select(request):
    if request.method == "POST":
        stu_id = request.POST.get('stu_id')
        # if id=='':
        #     id=request.session['user']['id']
        try:
            stu_data = StudentInformationModel.objects.get(stu_id=stu_id)
            # print(stu_data.stu_id, stu_data.stu_name, stu_data.stu_phone, stu_data.stu_address, stu_data.stu_faculty,
            #       stu_data.stu_major)
        except:
            context = {
                'error': "not found studnet id: "+str(stu_id),
            }
            return render(request, 'studentManage/select.html', context)

        stu_course = CourseModel.objects.filter(stu_id=stu_id)
        dct = {}
        for stu in stu_course:
            dct[stu.course] = stu.grade
        context = {
            'stu_id': stu_data.stu_id,
            'stu_name': stu_data.stu_name,
            'stu_phone': stu_data.stu_phone,
            'stu_address': stu_data.stu_address,
            'stu_faculty':  stu_data.stu_faculty,
            'stu_major':  stu_data.stu_major,
            'course_data': dct,
            'msg': True
        }
        return render(request, 'studentManage/select.html', context)
    else:
        root_information = request.session.get('user')
        if root_information is None:
            context = {
                'error': '请先登录'
            }
            return render(request, 'studentManage/select.html', context)

        user_id = root_information['user_id']
        stu_data = StudentInformationModel.objects.filter(user_id=user_id).first()
        if stu_data is None:
            context = {
                'error': '请先登录'
            }
            return render(request, 'studentManage/select.html', context)

        context = {
            'msg': False,
            'stu_id': '例如：123'
        }
        return render(request, 'studentManage/select.html', context)


# 删除
def delete(request):
    if request.method == "POST":
        try:
            id = int(request.POST.get('stu_id'))
            # StudentInformationModel.objects.filter(stu_id=id).delete()
            stu_data = StudentInformationModel.objects.filter(stu_id=id)
            if len(stu_data):
                stu_data.delete()
                context = {
                    'msg': '成功删除'
                }
                return render(request, 'studentManage/delete.html', context)
            else:
                context = {
                    'msg': '学生学号输入错误，请确认后重新输入!'
                }
                return render(request, 'studentManage/delete.html', context)
        except:
            context = {
                'msg': '学生学号输入错误，请确认后重新输入!'
            }
            return render(request, 'studentManage/delete.html', context)
    else:
        root_information = request.session['user']
        user_id = root_information['user_id']
        stu_data = StudentInformationModel.objects.filter(user_id=user_id).first()
        context = {
            'stu_id': stu_data.stu_id
        }
        return render(request, 'studentManage/delete.html', context)


# 修改
def update(request):
    user_information = request.session['user']
    user_id = user_information['user_id']
    stu_data = StudentInformationModel.objects.filter(user_id=user_id).first()
    context = {
            'stu_id': stu_data.stu_id,
            'stu_name': stu_data.stu_name,
            'stu_phone': stu_data.stu_phone,
            'stu_address': stu_data.stu_address,
            'stu_faculty':  stu_data.stu_faculty,
            'stu_major':  stu_data.stu_major,
    }
    if request.method == "POST":
        stu_id = request.POST.get('stu_id')
        stu_name = request.POST.get('stu_name')
        stu_phone = request.POST.get('stu_phone')
        stu_address = request.POST.get('stu_address')
        stu_faculty = request.POST.get('stu_faculty')
        stu_major = request.POST.get('stu_major')
        #StudentInformationModel.objects.filter(stu_id=id).update(stu_id=stu_id, stu_name=stu_name, stu_phone=stu_phone, stu_address=stu_address, stu_faculty=stu_faculty, stu_major=stu_major)
        stu_data = StudentInformationModel.objects.get(stu_id=stu_id)
        stu_data.stu_id = stu_id
        stu_data.stu_name = stu_name
        stu_data.stu_phone = stu_phone
        stu_data.stu_address = stu_address
        stu_data.stu_faculty = stu_faculty
        stu_data.stu_major = stu_major
        stu_data.save()
        context = {
            'stu_id': stu_id,
            'stu_name': stu_name,
            'stu_phone': stu_phone,
            'stu_address': stu_address,
            'stu_faculty': stu_faculty,
            'stu_major': stu_major,
            'msg': '修改成功',
        }
        return render(request, 'studentManage/update.html', context)
    else:
        return render(request, 'studentManage/update.html', context)

def new_studentinformation(request):
    conn = sqlite3.connect('db.sqlite3')
    faculty = request.GET.get('faculty')  # 获取通过下拉表单选中的院系值
    if faculty:
        c = conn.execute('SELECT stu_id, stu_name, stu_phone, stu_faculty, stu_major, stu_address FROM new_studentinformation WHERE stu_faculty=? ORDER BY stu_id', (faculty,))
    else:
        c = conn.execute('SELECT stu_id, stu_name, stu_phone, stu_faculty, stu_major, stu_address FROM new_studentinformation ORDER BY stu_id')
    slists = c.fetchall()
    return render(request, 'studentManage/information.html', {'new_studentinformation': slists})
