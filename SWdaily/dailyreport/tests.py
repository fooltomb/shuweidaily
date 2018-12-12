from django.test import TestCase
from django.urls import reverse
from .models import Users

# Create your tests here.
def create_user():
    a=Users.objects.create()
    a.name='aaa'
    a.save()
    return a

class LoginViewTests(TestCase):
    def test_get(self):
        response=self.client.get(reverse('dailyreport:login'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'dailyreport/login.html')
    def test_no_username(self):
        response=self.client.post(reverse('dailyreport:login'),{'username':'kpajiofjaenojgfpo','pwd':'iodijaohefe'})
        self.assertEqual(response.status_code,200)
        #self.assertQuerysetEqual(response.context['error_message'],'没有此用户,请检查用户名')
        self.assertContains(response,"没有此用户，请检查用户名")
        self.assertTemplateUsed(response,'dailyreport/login.html')
    def test_wrong_password(self):
        create_user()
        response=self.client.post(reverse('dailyreport:login'),{'username':'aaa','pwd':'111111'})

        self.assertEqual(response.status_code,200)
        #self.assertQuerysetEqual(response.context['error_message'],[])
        self.assertContains(response,"密码错误")

