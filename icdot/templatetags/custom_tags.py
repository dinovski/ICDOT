from django import template
from django.template import TemplateDoesNotExist

register = template.Library()


@register.simple_tag(takes_context=True)
def read_file(context, template_name):
    """
    Load a text file using the template loader

    Example: {% read_file 'admin_doc/pages/about.md' as source %}
    """

    for loader in context.template.engine.template_loaders:
        try:
            return loader.get_template(template_name).source
        except TemplateDoesNotExist:
            pass
    else:
        raise TemplateDoesNotExist(template_name)
