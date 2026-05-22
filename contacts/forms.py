# 导入 Django 表单模块
from django import forms
# 导入对应的模型 Contact
from .models import Contact

# Contact 表单，基于 ModelForm 自动生成
class ContactForm(forms.ModelForm):
    # 表单核心配置（Meta 类）
    class Meta:
        # 指定这个表单对应哪个数据库模型
        model = Contact
        # 指定表单需要显示的字段（这里只需要 message）
        fields = ['message']  
        
        # 配置字段的前端样式、输入框类型（widgets）
        widgets = {  
            "message": forms.Textarea(
                attrs={
                    # Bootstrap 样式
                    'class': 'form-control',
                    # 提示文字
                    'placeholder': 'Enter Your message here',
                    # 文本框高度 5 行
                    'rows': 5
                }
            )
        }