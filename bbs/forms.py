#_*_coding:utf-8_*_
__author__ = 'ZhouMing'

from django import forms
from django.forms import Form,ModelForm
from django.forms import fields
from django.forms import widgets
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from bbs import models
from django.contrib.auth.models import User


class ArticleModelForm(ModelForm):
    class Meta:
        model = models.Article
        exclude = ('author','pub_date','priority',)

    # 先继承,再重写(想重新定义某些字段的属性,必须先继承,在重写,就这样记着)
    def __init__(self,*args,**kwargs):
        super(ArticleModelForm,self).__init__(*args,**kwargs)
        # self.fields['qq'].widget.attrs["class"] = "form-control"

        # for循环每一个字段,修改字段的class属性
        for field_name in self.base_fields:      #self.base_fields说白了就是把所有字段取出来但是是字典的形势
            field = self.base_fields[field_name]
            #这里可以是上面的例子field.widget.attrs["class"] = "form-control",也可以用update,用update的好处就是可以同时修改多个属性了
            field.widget.attrs.update({'class':"form-control"})


class RegisterForm(Form):
    username = forms.CharField(
        label = 'Username',
        max_length = 50,
        required=True,
        strip=True,
        error_messages={
            'required':'用户名不能为空',
        }
    )
    # email = forms.EmailField(label='Email',)
    password1 = forms.CharField(
        label='Password',
        widget=widgets.PasswordInput(attrs={'class':'form-control','placeholder':'Input Password'},render_value = True),
        min_length=6,
        max_length=12,
        validators = [
            RegexValidator(r'((?=.*\d))^.{6,12}$', '必须包含数字'),
            RegexValidator(r'((?=.*[a-zA-Z]))^.{6,12}$', '必须包含字母'),
            ],  # 用于对密码的正则验证
        error_messages={
            'required':'密码不能为空',
            'min_length':'密码最少为6个字符',
            'max_length':'密码不能超过12个字符'
        }
        )
    password2 = fields.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password Confirmation'},render_value=True),
        required=True,
        strip=True,
        error_messages={
            'required':'请再次输入密码！',
        }
    )
    name = forms.CharField(
        label='nickname',
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'Input Nickname'}),
        min_length=1,
        max_length=12,
        strip=True,
        required=True,
        error_messages={
            'required':'昵称不能为空',
            'min_length':'昵称最少为1个字符',
            'max_length':'昵称最多不能超过20个字符'
        }



    )

    def clean_username(self):
        # 对username的扩展验证，查找用户是否已经存在
        username = self.cleaned_data.get('username')
        users = User.objects.filter(username=username).count()
        if users:
            raise ValidationError('用户已经存在！')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise ValidationError('Your password is too short')
        elif len(password1) > 12:
            raise ValidationError('Your password is too long')
        return password1

    def clean_password2(self):
        #查看两次密码是否一致
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('Password mismatch.Please enter again')
        return password2


# class LoginForm(Form):
#     username = forms.CharField(label ='Username',max_length = 50)
#     password = forms.CharField(label = 'Password',widget=forms.PasswordInput,min_length=6,max_length=12)
#
#     def clean(self):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')
#         user = User.objects.filter(username=username).first()
#         if username and password:
#             if not user:
#                 raise ValidationError('This Username does not exists.')
#             elif password != user.password:
#                 raise ValidationError('Wrong Password')
#         return username

