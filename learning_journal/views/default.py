from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from datetime import date

from sqlalchemy.exc import DBAPIError

from learning_journal.models import Entries
from learning_journal.security import check_credentials
from pyramid.security import remember, forget


@view_config(route_name='login', renderer='../templates/login.jinja2', permission="guest")
def login_view(request):
    """Handle the login view."""
    if request.method == 'POST':
        username = request.params.get('username', '')
        password = request.params.get('password', '')
        if check_credentials(username, password):
            headers = remember(request, username)
            return HTTPFound(location=request.route_url('home'), headers=headers)
    return {}


@view_config(route_name='logout')
def logout_view(request):
    """Handle logging the user out."""
    auth_head = forget(request)
    return HTTPFound(request.route_url("home"), headers=auth_head)


@view_config(route_name='home', renderer='../templates/list.jinja2', permission="guest")
def home_view(request):
    try:
        query = request.dbsession.query(Entries).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'entries': query}


@view_config(route_name='create', renderer='../templates/create_entry.jinja2', permission='author')
def create_view(request):
    if request.method == "POST":
        entry = request.POST
        row = Entries(title=entry["title"], creation_date=date.today(), body=entry["body"])
        request.dbsession.add(row)
        return HTTPFound(request.route_url("home"))
    return {}


@view_config(route_name="detail", renderer="../templates/entry.jinja2", permission='guest')
def detail_view(request):
    """Handle the detail view for a specific journal entry."""
    the_id = int(request.matchdict["id"])
    entry = request.dbsession.query(Entries).get(the_id)
    return {"entry": entry}


@view_config(route_name="update", renderer="../templates/edit_entry.jinja2", permission='author')
def update_view(request):
    """Handle the view for updating a new entry."""
    the_id = int(request.matchdict["id"])
    if request.method == "POST":
        entry = request.POST
        query = request.dbsession.query(Entries).get(the_id)
        query.title = entry["title"]
        query.body = entry["body"]
        request.dbsession.flush()
        return HTTPFound(request.route_url("home"))
    entry = request.dbsession.query(Entries).get(the_id)
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
