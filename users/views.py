from users.forms import UserLoginForm, RegistrationForm, UserProfileForm
from django.urls import reverse_lazy, reverse
from products.models import Basket
from django.views.generic.edit import CreateView, UpdateView
from users.models import User, EmailVerification
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from common.views import TitleMixin
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')

class UserRegistrationView(CreateView, SuccessMessageMixin, TitleMixin):
    model = User
    form_class = RegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно прошли регистрацию'
    title = 'Store'

class UserProfileView(UpdateView, TitleMixin):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

class EmailVerificationView(TitleMixin, UpdateView):
    title = 'Store'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired:
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))