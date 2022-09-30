from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import NewsletterForm, ContactForm


class IndexView(generic.TemplateView):
    """
    Class that rendering the index page
    """

    template_name = "website/index.html"


class AboutView(generic.TemplateView):
    """
    Class that rendering the about page
    """

    template_name = "website/about.html"


class contactView(generic.CreateView):
    """
    Class that rendering the contact page
    """

    form_class = ContactForm
    success_url = reverse_lazy("website:contact")
    template_name = "website/contact.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        messages.success(self.request, "Your ticket submit successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, "Something went wrong.")
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class NewsletterView(generic.CreateView):
    """only  accept POST"""

    form_class = NewsletterForm
    http_method_names = ["post"]
    success_url = reverse_lazy("website:index")
    template_name = "blank.html"

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        messages.success(
            self.request,
            "Your email is submit successfully,\
                         be sure we are not sending you spams.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, "Something went wrong.")
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
