from django.shortcuts import reverse
from .models import Lead, LeadStatus
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .forms import LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadStatusUpdateForm
from django.views.generic import (
    TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView, FormView)
from django.core.mail import send_mail
from agents.utils import OrganizerRoleCheckerAndLoginRequiredMixin, RedirectIfAlreadyLoggedInMixin


# ============================PROTECTED ROUTES=====================================#
class SignupView(RedirectIfAlreadyLoggedInMixin, CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class CustomLoginView(RedirectIfAlreadyLoggedInMixin, LoginView):
    template_name = "registration/login.html"


# view for site's landing page
class HomePageView(TemplateView):
    template_name = "homepage.html"


class GetStartedView(TemplateView):
    template_name = "learn_to_use.html"


# ================LEAD RELATED==================================#
# list of all leads view
class AllLeadsView(LoginRequiredMixin, ListView):
    template_name = "leads/all_leads.html"
    context_object_name = "leads"

    # if you are an organizer, you can see all leads you made in your oganization

    # if you are an agent, you can only see leads from the org you belong to,
    # and that they are leads that were assigned to you

    def get_queryset(self):
        if self.request.user.is_organizer:
            queryset = Lead.objects.filter(organisation=self.request.user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation=self.request.user.agent.organisation, agent__isnull=False)
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllLeadsView, self).get_context_data(**kwargs)

        if self.request.user.is_organizer:
            # look for leads within the current org that are not yet linked to any agents
            queryset = Lead.objects.filter(organisation=self.request.user.userprofile, agent__isnull=True)

            context.update({

                "unassigned_leads": queryset

            })

        return context


# lead details view
class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead_detail"

    def get_queryset(self):
        if self.request.user.is_organizer:
            # if you are an organizer, you can see all leads you made in your oganization
            queryset = Lead.objects.filter(organisation=self.request.user.userprofile)
        else:
            # if you are an agent, you can only see leads from the org you belong to,
            # and that they are leads that were assigned to you
            queryset = Lead.objects.filter(organisation=self.request.user.agent.organisation)
            queryset.filter(agent__user=self.request.user)
        return queryset


# create new lead view
class LeadCreateView(OrganizerRoleCheckerAndLoginRequiredMixin, CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:all_leads")

    def form_valid(self, form):
        newLead = form.save(commit=False)
        newLead.organisation = self.request.user.userprofile
        newLead.save()

        # send an email before returning back to whatever form_valid is doing
        send_mail(

            subject="A lead has been created",
            message="Visit site to see new lead",
            from_email="test@test.com",
            recipient_list=["sometest@test.com"]

        )
        return super(LeadCreateView, self).form_valid(form)


# update a lead view
class LeadUpdateView(OrganizerRoleCheckerAndLoginRequiredMixin, UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        if self.request.user.is_organizer:
            # if you are an organizer, you can see all leads you made in your oganization
            queryset = Lead.objects.filter(organisation=self.request.user.userprofile)
        else:
            # if you are an agent, you can only see leads from the org you belong to,
            # and that they are leads that were assigned to you
            queryset = Lead.objects.filter(organisation=self.request.user.agent.organisation)
            queryset.filter(agent__user=self.request.user)
        return queryset

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse("leads:lead_detail", kwargs={'pk': pk})


# delete a lead view
class LeadDeleteView(OrganizerRoleCheckerAndLoginRequiredMixin, DeleteView):
    template_name = "leads/lead_delete.html"

    def get_success_url(self):
        return reverse("leads:all_leads")

    def get_queryset(self):
        if self.request.user.is_organizer:
            # if you are an organizer, you can see all leads you made in your oganization
            queryset = Lead.objects.filter(organisation=self.request.user.userprofile)
        else:
            # if you are an agent, you can only see leads from the org you belong to,
            # and that they are leads that were assigned to you
            queryset = Lead.objects.filter(organisation=self.request.user.agent.organisation)
            queryset.filter(agent__user=self.request.user)
        return queryset


class AssignAgentView(OrganizerRoleCheckerAndLoginRequiredMixin, FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:all_leads")

    def form_valid(self, form):
        agent_to_assign = form.cleaned_data['agent']
        lead_to_assign_an_agent_to = Lead.objects.get(id=self.kwargs['pk'])
        lead_to_assign_an_agent_to.agent = agent_to_assign
        lead_to_assign_an_agent_to.save()
        return super(AssignAgentView, self).form_valid(form)


# ================LEAD RELATED==================================#

# ================LEAD STATUSES RELATED==================================#
class AllLeadStatusesView(ListView):
    template_name = "leads/all_lead_statuses.html"
    context_object_name = "lead_statuses"

    def get_queryset(self):
        if self.request.user.is_organizer:
            queryset = LeadStatus.objects.filter(organisation=self.request.user.userprofile)
        else:
            queryset = LeadStatus.objects.filter(organisation=self.request.user.agent.organisation)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllLeadStatusesView, self).get_context_data(**kwargs)

        if self.request.user.is_organizer:
            queryset = Lead.objects.filter(organisation=self.request.user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=self.request.user.agent.organisation)

        context.update({
            "unassigned_leads_count": queryset.filter(lead_status__isnull=True).count()
        })
        return context


class LeadsDetailsByLeadStatusView(LoginRequiredMixin, DetailView):
    template_name = "leads/leads_details_by_status.html"
    context_object_name = "lead_status"

    def get_context_data(self, **kwargs):
        context = super(LeadsDetailsByLeadStatusView, self).get_context_data(**kwargs)

        # Lead.objects.filter(lead_status=self.get_object())

        # reverse look up through related_names
        leads_under_this_status_type = self.get_object().leads.all()

        context.update({
            "leads_under_this_status_type": leads_under_this_status_type
        })
        return context

    def get_queryset(self):
        if self.request.user.is_organizer:
            queryset = LeadStatus.objects.filter(organisation=self.request.user.userprofile)
        else:
            queryset = LeadStatus.objects.filter(organisation=self.request.user.agent.organisation)

        return queryset


class LeadStatusUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "leads/lead_status_update.html"
    form_class = LeadStatusUpdateForm

    def get_queryset(self):
        if self.request.user.is_organizer:
            # if you are an organizer, you can see all leads you made in your oganization
            queryset = Lead.objects.filter(organisation=self.request.user.userprofile)
        else:
            # if you are an agent, you can only see leads from the org you belong to,
            # and that they are leads that were assigned to you
            queryset = Lead.objects.filter(organisation=self.request.user.agent.organisation)
            queryset.filter(agent__user=self.request.user)
        return queryset

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse("leads:lead_detail", kwargs={'pk': pk})

# ================LEAD STATUSES RELATED==================================#


# ============================PROTECTED ROUTES=====================================#
