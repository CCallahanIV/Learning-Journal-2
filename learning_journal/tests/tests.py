"""A short testing suite for the expense tracker."""


import pytest
import transaction

from pyramid import testing

from learning_journal.models import Entries, get_tm_session
from learning_journal.models.meta import Base

from datetime import datetime


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.

    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.

    This configuration will persist for the entire duration of your PyTest run.
    """
    settings = {
        'sqlalchemy.url': 'sqlite:///:memory:'}  # points to an in-memory database.
    config = testing.setUp(settings=settings)
    config.include('learning_journal.models')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture()
def db_session(configuration, request):
    """Create a session for interacting with the test database.

    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Instantiate a fake HTTP Request, complete with a database session.

    This is a function-level fixture, so every new request will have a
    new database session.
    """
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_models(dummy_request):
    """Add a bunch of model instances to the database.

    """
    for entry in ENTRIES:
            row = Entries(title=entry["title"], creation_date=entry["creation_date"], body=entry["body"])
            dummy_request.dbsession.add(row)

ENTRIES = [
        {"title": "There's value in stepping back.", "creation_date": datetime.strptime("December 14, 2016", "%B %d, %Y"), "body": """Sometimes principles from our past help with our present. Before starting the double linked list today, I committed to two things: Starting with the tests.  Designing before coding. I actually wrote some tests first, just sort of stream of consciousness but things quickly got messy. After flailing for a bit, I stepped back and mapped out the function of each method and made a list of everything I would want test about it. From that, I was able to write a fairly comprehensive testing suite that should require little refactoring to really test all functions of the Double Linked List.  Joey and I had some frustrating issues to work out with the server assignment. For whatever reason, since yesterday, our message sending on both the client and server sides decided to start escaping all the \r and \n characters. It had us and the TA's stumped for... far too long. We ended up changing our search parameters in our receiving while loops so that things could work again. Now I'm worried that I'll wake up tomorrow and it won't work. Or it just won't work whomever grades our assignment.  SUCH IS LIFE."""},
        {"title": "Revenge is Best SERVERED Cold", "creation_date": datetime.strptime("December 15, 2016", "%B %d, %Y"), "body": """The second you feel like youre starting to climb youre way out of the avalanche of work and information theres always some weird and random server error to pull you right back in.  Im struggling a lot to find ways to refactor and clean up the server code. I feel like were working with a patchwork of try/except statements, teetering towers of if/else logic, and precarious while loops.  Id like to see an example of a server done RIGHT. But I want to earn that - I want to finish my own server the hard way.  Hey, urllib2, sup?"""},
        {"title": "Whiteboarding", "creation_date": datetime.strptime("December 16, 2016", "%B %d, %Y"), "body": "Its fun, its hard, it makes your brain bend in ways you never thought possible. Really lucky I was partnered with Joey. He had the essential, Aha! moment that led to the solution. Glad I was able to contribute though. I worry that in the future as I prep for interviews, I'll won't be able to rely on flexible thinking to solve new problems. I'll likely have to plan ahead and try to expose myself to as many problem scenarios as possible in order to succeed. So it goes, more studying ahead.  The server assignment really started as a hacky mess. Lots of patchwork try/except blocks and grabbing specific errors in desperation. I think today we really nailed it down into something I can be somewhat proud of. Looking forward to the opportunity to go back in time and refactor things this weekend.  Also looking forward to beer."},
        {"title": "Recent Awesome Things We've Learned", "creation_date": datetime.strptime("December 19, 2016", "%B %d, %Y"), "body": "<ul><li>Big(O) Notation</li><li>Linked-List based Data Structures</li><li>Web App Deployment Frameworks (Pyramid)</li></ul><p>It feels like we're moving beyond the introductory part of Python knowledge and are really starting to get into the meat n' potatoes of development and CS concepts. For the first time in a while, I'm starting to feel somewhat empowered as a dev-in-development.  Not to say I know everything there is, but I know enough to now to actually make something with it, and more importantly, I'm starting to have some idea of what I don't know.</p><p>Despite the time crunch and the fast pace, I've enjoyed the class to this point.  BUT, I am really excited for what is to come.</p><p>Of course, the second I begin to think this, the rug will be pulled out from underneath once again.</p><p>Looking forward to building stuff.</p>"},
        {"title": "Tunnels, Lights, Progress, etc.", "creation_date": datetime.strptime("December 20, 2016", "%B %d, %Y"), "body": """Two quick things, the binary heap was initially a pain in the ass.  However, I feel really proud of the implementation I have.  Hooray for max OR min. Finally, I'm really excited for the group project.  I feel a strong personal connection to the purpose of this app and I'm excited to put our newfound skills and knowledge to good use."""},
        {"title": "They Said It Would Happen", "creation_date": datetime.strptime("December 21, 2016", "%B %d, %Y"), "body": "Unfortunately, I think I'm enjoying too much tinkering around with data structures.  We have fallen far behind on the journal stuff.  If we didn't have next week off, I'm not sure how it would all get done.  Getting tough to balance home and school life.  But that's the fun part, right?  The challenge!  BRING IT ON, COWBOY UP."}
]


# ======== UNIT TESTS ==========

def test_new_entries_are_added(db_session):
    """New expenses get added to the database."""
    for entry in ENTRIES:
            row = Entries(title=entry["title"], creation_date=entry["creation_date"], body=entry["body"])
            db_session.add(row)
    query = db_session.query(Entries).all()
    assert len(query) == len(ENTRIES)


def test_home_view_returns_empty_when_empty(dummy_request):
    """Test that the home view returns no objects in the expenses iterable."""
    from learning_journal.views.default import home_view
    result = home_view(dummy_request)
    assert len(result["entries"]) == 0


def test_home_view_returns_objects_when_exist(dummy_request, add_models):
    """Test that the home view does return objects when the DB is populated."""
    from learning_journal.views.default import home_view
    result = home_view(dummy_request)
    assert len(result["entries"]) == 6

# ======== FUNCTIONAL TESTS ===========


@pytest.fixture
def testapp():
    """Create an instance of webtests TestApp for testing routes.

    With the alchemy scaffold we need to add to our test application the
    setting for a database to be used for the models.
    We have to then set up the database by starting a database session.
    Finally we have to create all of the necessary tables that our app
    normally uses to function.

    The scope of the fixture is function-level, so every test will get a new
    test application.
    """
    from webtest import TestApp
    from learning_journal import main

    app = main({}, **{"sqlalchemy.url": 'sqlite:///:memory:'})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    return testapp


@pytest.fixture
def fill_the_db(testapp):
    """Fill the database with some model instances.

    Start a database session with the transaction manager and add all of the
    expenses. This will be done anew for every test.
    """
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        for entry in ENTRIES:
            row = Entries(title=entry["title"], creation_date=entry["creation_date"], body=entry["body"])
            dbsession.add(row)


def test_home_route_has_list(testapp):
    """The home page has a table in the html."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("ul")) == 1


def test_home_route_with_data_has_filled_list(testapp, fill_the_db):
    """When there's data in the database, the home page has some rows."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("li")) == 6


def test_home_route_has_list2(testapp):
    """Without data the home page only has the header row in its table."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("ul")) == 1


def test_create_entry_route_has_form(testapp):
    """Test that the "create" route loads a page with a form."""
    response = testapp.get('/journal/new-entry', status=200)
    html = response.html
    assert len(html.find_all("form")) == 1


def test_update_route_has_populated_form(testapp, fill_the_db):
    """Test the upate has a populated form."""
    response = testapp.get('/journal/1/edit-entry', status=200)
    title = response.html.form.input["value"]
    body = response.html.form.textarea.contents[0]
    assert title == ENTRIES[0]["title"]
    assert body == ENTRIES[0]["body"]


def test_detail_route_loads_proper_entry(testapp, fill_the_db):
    """Test that the detail route loads the proper entry."""
    response = testapp.get('/journal/2', status=200)
    title = response.html.find_all(class_='articleTitle')[0].contents[0]
    assert title == ENTRIES[1]["title"]
