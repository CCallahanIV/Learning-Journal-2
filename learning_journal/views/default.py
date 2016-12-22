from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
    try:
        query = request.dbsession.query(MyModel)
        one = query.filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'learning_journal'}


@view_config(route_name='create', renderer='../templates/form.jinja2')
def create_view(request):
    if request.method == "POST":
        # Get the form stuff
    return {}


# @view_config(route_name="home", renderer="templates/list.jinja2")
# def home_page(request):
#     """View for the home page."""
#     return {"entries": ENTRIES}


@view_config(route_name="detail", renderer="templates/entry.jinja2")
def detail_view(request):
    """Handle the detail view for a specific journal entry."""
    the_id = int(request.matchdict["id"])
    entry = ENTRIES[the_id]
    return {"entry": entry}


@view_config(route_name="create", renderer="templates/create_entry.jinja2")
def create_view(request):
    """Handle the view for creating a new entry."""
    return {}


@view_config(route_name="update", renderer="templates/edit_entry.jinja2")
def update_view(request):
    """Handle the view for updating a new entry."""
    the_id = int(request.matchdict["id"])
    entry = ENTRIES[the_id]
    return {"entry": entry}



db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
