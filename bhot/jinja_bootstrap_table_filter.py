from jinja2 import Markup

"""
Usage:
    from .jinja_bootstrap_table_filter import register_jinja2_filters
    ...
    register_jinja2_filters(app)

And then inside templates:

    {{ "asdfasdfasdf" | render_bootstrap_query_table }}

"""

def render_bootstrap_query_table(query):
    x = """
<table>
<tr>
<td>
fdsafsdafasd
</td>
</tr>
</table>
"""
    return Markup(x)



def register_jinja2_filters(app):
    app.jinja_env.filters['render_bootstrap_query_table'] = render_bootstrap_query_table
