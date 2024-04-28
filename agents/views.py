from django.shortcuts import reverse
from django.views.generic import (
    TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView)
from .forms import AgentModelForm
from leads.models import Agent
from .utils import OrganizerRoleCheckerAndLoginRequiredMixin, CustomRawPasswordGenerator
from django.core.mail import send_mail
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


class AllAgentsView(OrganizerRoleCheckerAndLoginRequiredMixin, ListView):
    template_name = "agents/all_agents.html"

    def get_queryset(self):
        individual_org = self.request.user.userprofile
        return Agent.objects.filter(organisation=individual_org)

    context_object_name = "agents"


class AgentDetailView(OrganizerRoleCheckerAndLoginRequiredMixin, DetailView):
    template_name = "agents/agent_detail.html"

    def get_queryset(self):
        individual_org = self.request.user.userprofile
        return Agent.objects.filter(organisation=individual_org)

    context_object_name = "agent_detail"


class AgentCreateView(OrganizerRoleCheckerAndLoginRequiredMixin, CreateView):
    template_name = "agents/agents_create.html"

    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:all_agents")

    def form_valid(self, form):
        user_account_for_agent_user = form.save(commit=False)
        user_account_for_agent_user.is_agent = True
        user_account_for_agent_user.is_organizer = False

        custom_raw_pass_generator = CustomRawPasswordGenerator()
        raw_random_pass = custom_raw_pass_generator.generateRawPassword()

        user_account_for_agent_user.set_password(raw_random_pass)
        user_account_for_agent_user.save()
        Agent.objects.create(
            user=user_account_for_agent_user,
            organisation=self.request.user.userprofile,
        )

        send_mail(
            subject="You are invited to be an agent",
            message=("Hello staff, you were added as an agent on the system. Please log in to start"
                     "working"),
            from_email=env("DEFAULT_FROM_EMAIL"),
            recipient_list=[user_account_for_agent_user.email]
        )

        # get user obj and assign as org profile
        # ORM reverses relationship and gives userprofile field
        # user_account_for_agent_user.organisation = self.request.user.userprofile
        # user_account_for_agent_user.save()
        return super(AgentCreateView, self).form_valid(form)


class AgentUpdateView(OrganizerRoleCheckerAndLoginRequiredMixin, UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_success_url(self):
        pk = self.kwargs['pk']

        return reverse("agents:agent_detail", kwargs={'pk': pk})

    def get_queryset(self):
        individual_org = self.request.user.userprofile
        return Agent.objects.filter(organisation=individual_org)

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs['instance'] = kwargs['instance'].user
        return kwargs

    def form_valid(self, form):
        # Save the form data
        form.save()
        return super(AgentUpdateView, self).form_valid(form)


class AgentDeleteView(OrganizerRoleCheckerAndLoginRequiredMixin, DeleteView):
    template_name = "agents/agent_delete.html"

    def get_queryset(self):
        individual_org = self.request.user.userprofile
        return Agent.objects.filter(organisation=individual_org)

    def get_success_url(self):
        return reverse("agents:all_agents")
