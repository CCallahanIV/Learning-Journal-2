import os
import sys
import transaction
from datetime import datetime

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import Entries


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    ENTRIES = [
        {"title": "There's value in stepping back.", "creation_date": datetime.strptime("December 14, 2016", "%B %d, %Y"), "body": """Sometimes principles from our past help with our present. Before starting the double linked list today, I committed to two things: Starting with the tests.  Designing before coding. I actually wrote some tests first, just sort of stream of consciousness but things quickly got messy. After flailing for a bit, I stepped back and mapped out the function of each method and made a list of everything I would want test about it. From that, I was able to write a fairly comprehensive testing suite that should require little refactoring to really test all functions of the Double Linked List.  Joey and I had some frustrating issues to work out with the server assignment. For whatever reason, since yesterday, our message sending on both the client and server sides decided to start escaping all the \r and \n characters. It had us and the TA's stumped for... far too long. We ended up changing our search parameters in our receiving while loops so that things could work again. Now I'm worried that I'll wake up tomorrow and it won't work. Or it just won't work whomever grades our assignment.  SUCH IS LIFE."""},
        {"title": "Revenge is Best SERVERED Cold", "creation_date": datetime.strptime("December 15, 2016", "%B %d, %Y"), "body": """The second you feel like youre starting to climb youre way out of the avalanche of work and information theres always some weird and random server error to pull you right back in.  Im struggling a lot to find ways to refactor and clean up the server code. I feel like were working with a patchwork of try/except statements, teetering towers of if/else logic, and precarious while loops.  Id like to see an example of a server done RIGHT. But I want to earn that - I want to finish my own server the hard way.  Hey, urllib2, sup?"""},
        {"title": "Whiteboarding", "creation_date": datetime.strptime("December 16, 2016", "%B %d, %Y"), "body": "Its fun, its hard, it makes your brain bend in ways you never thought possible. Really lucky I was partnered with Joey. He had the essential, Aha! moment that led to the solution. Glad I was able to contribute though. I worry that in the future as I prep for interviews, I'll won't be able to rely on flexible thinking to solve new problems. I'll likely have to plan ahead and try to expose myself to as many problem scenarios as possible in order to succeed. So it goes, more studying ahead.  The server assignment really started as a hacky mess. Lots of patchwork try/except blocks and grabbing specific errors in desperation. I think today we really nailed it down into something I can be somewhat proud of. Looking forward to the opportunity to go back in time and refactor things this weekend.  Also looking forward to beer."},
        {"title": "Recent Awesome Things We've Learned", "creation_date": datetime.strptime("December 19, 2016", "%B %d, %Y"), "body": "<ul><li>Big(O) Notation</li><li>Linked-List based Data Structures</li><li>Web App Deployment Frameworks (Pyramid)</li></ul><p>It feels like we're moving beyond the introductory part of Python knowledge and are really starting to get into the meat n' potatoes of development and CS concepts. For the first time in a while, I'm starting to feel somewhat empowered as a dev-in-development.  Not to say I know everything there is, but I know enough to now to actually make something with it, and more importantly, I'm starting to have some idea of what I don't know.</p><p>Despite the time crunch and the fast pace, I've enjoyed the class to this point.  BUT, I am really excited for what is to come.</p><p>Of course, the second I begin to think this, the rug will be pulled out from underneath once again.</p><p>Looking forward to building stuff.</p>"},
        {"title": "Tunnels, Lights, Progress, etc.", "creation_date": datetime.strptime("December 20, 2016", "%B %d, %Y"), "body": """Two quick things, the binary heap was initially a pain in the ass.  However, I feel really proud of the implementation I have.  Hooray for max OR min. Finally, I'm really excited for the group project.  I feel a strong personal connection to the purpose of this app and I'm excited to put our newfound skills and knowledge to good use."""},
        {"title": "They Said It Would Happen", "creation_date": datetime.strptime("December 21, 2016", "%B %d, %Y"), "body": "Unfortunately, I think I'm enjoying too much tinkering around with data structures.  We have fallen far behind on the journal stuff.  If we didn't have next week off, I'm not sure how it would all get done.  Getting tough to balance home and school life.  But that's the fun part, right?  The challenge!  BRING IT ON, COWBOY UP."},
        {"title": "First Time Entering On the New Site", "creation_date": datetime.strptime("December 22, 2016", "%B %d, %Y"), "body": "This is pretty exciting. This is the first time I'll actually be writing my journal entry in the form I created! Of course it won't persist until I upgrade it to Postgres, BUT STILL. Pretty cool. Getting the chance to work from an emptier plate today really helped alleviate some pressure. I'm very much looking forward to next week for the opportunity to go back through past assignments with a fine tooth comb and improve things, first by learning from earlier mistakes, and second by getting some points back. Hopefully, time permitting, I'll be able to work a bit on the twitter app. Going back to Javascript after three intensive weeks of Python should be a trip."}
    ]

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        for entry in ENTRIES:
            row = Entries(title=entry["title"], creation_date=entry["creation_date"], body=entry["body"])
            dbsession.add(row)
