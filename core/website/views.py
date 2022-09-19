from django.views.generic import TemplateView


class IndexView(TemplateView):
    """
    Class that rendering the index page
    """
    template_name = 'website/index.html'
    
class AboutView(TemplateView):
    """
    Class that rendering the about page
    """
    template_name = 'website/about.html'
    
class contactView(TemplateView):
    """
    Class that rendering the contact page
    """
    template_name = 'website/contact.html'