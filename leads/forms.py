from django import forms
from .models import Lead, Agent
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

CustomUser = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        # override default User to CustomUser
        model = CustomUser
        fields = (
            "username",
        )

        field_classes = {'username': UsernameField}


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone',
            'email',

        )


# class LeadForm(forms.Form):
#     first_name = forms.CharField()
#     last_name = forms.CharField()
#     age = forms.IntegerField(min_value=0)


class AssignAgentForm(forms.Form):
    # create select menu to select from available agents
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents_from_this_org = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)

        self.fields['agent'].queryset = agents_from_this_org


class LeadStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            "lead_status",
        )
