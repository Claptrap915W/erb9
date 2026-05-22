# 导入 Django 必要模块：渲染页面、重定向
from django.shortcuts import render, redirect, get_object_or_404
# 导入自己写的 Contact 模型（存咨询信息的表）
from .models import Contact
# 导入消息提示模块（成功/错误提示）
from django.contrib import messages
from django.core.mail import send_mail
import os
from .forms import ContactForm


# Create your views here.

# 处理咨询表单的视图函数
def contact(request):
    # ======================
    # 1. 只处理【表单提交】POST 请求
    # 如果是打开页面 GET 请求，直接跳过这段逻辑
    # ======================
    if request.method == "POST":

        # 从表单 POST 数据里取出所有字段
        listing = request.POST['listing']          # 诊所名称
        listing_id = request.POST['listing_id']    # 诊所ID（隐藏字段）
        name = request.POST['name']                # 用户姓名
        email = request.POST['email']              # 邮箱
        phone = request.POST['phone']              # 电话
        message = request.POST['message']          # 留言内容
        user_id = request.POST['user_id']          # 前端传过来的用户ID
        doctor_email = request.POST['doctor_email']

        # ======================
        # 2. 防重复咨询逻辑（核心）
        # ======================
        # 判断：用户是否【已登录】
        if request.user.is_authenticated:
            # 如果已登录，用当前登录用户的真实 ID
            user_id = request.user.id

            # 查询数据库：
            # 这个用户（user_id）是否已经咨询过这个诊所（listing_id）
            has_contacted = Contact.objects.all().filter(
                listing_id=listing_id,  # 匹配：当前诊所ID
                user_id=user_id         # 匹配：当前登录用户ID
            )

            # 如果查询到记录 → 已经咨询过 → 阻止提交
            if has_contacted:
                messages.error(request,"You have already made an inquiry for this clinic")
                return redirect("listings:listing", listing_id=listing_id)

        # ======================
        # 3. 验证通过 → 创建咨询记录并保存到数据库
        # ======================
        contact = Contact(
            listing=listing, 
            listing_id=listing_id, 
            name=name, 
            email=email,
            phone=phone, 
            message=message, 
            user_id=user_id
        )
        contact.save()  # 真正执行保存到数据库
        # ! send mail
        # send_mail(
        #     "Clinci Inquiry",
        #     "There has been an inquiry for " + listing + ". Sign into the admin panel for"
        #     "more info",
        #     os.getenv('EMAIL_HOST_USER'),
        #     [doctor_email],
        #     fail_silently=False
        # )
        # 提交成功 → 显示成功提示
        messages.success(request,"Your request has been submitted, a representative will get back to you soon")
        
        # 提交完成后跳回诊所详情页
        return redirect('listings:listing', listing_id=listing_id)

def delete_contact(request ,contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    contact.delete()
    return redirect('accounts:dashboard')

def edit_contact(request, contact_id):

    # 1. 根据ID从数据库获取要编辑的咨询记录
    # 如果找不到，直接返回404页面
    contact = get_object_or_404(Contact, pk=contact_id)

    # 2. 判断请求方式：如果是POST = 用户提交了编辑表单
    if request.method == "POST":
        # 用提交的数据 去 更新已有的记录（instance=contact）
        form = ContactForm(request.POST, instance=contact)
        
        # 3. 验证表单数据是否合法
        if form.is_valid():
            # 合法 → 保存到数据库（执行更新操作）
            form.save()
            # 保存成功 → 跳回用户仪表盘
            return redirect('accounts:dashboard')

    # 4. 如果是GET请求 = 用户刚进入编辑页面，显示表单
    else:
        # 把已有的数据填充到表单里（instance=contact）
        form = ContactForm(instance=contact)
        
    # 渲染编辑页面，把表单和数据传给前端
    return render(request, "contacts/edit_contact.html", {
        "form": form,       # 表单对象
        "contact": contact  # 当前编辑的记录
    })