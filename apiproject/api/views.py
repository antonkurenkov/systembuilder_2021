from django.shortcuts import render
import sys

sys.path.append('/usr/src/app')
from chore.hooks import make_stable_connection


def hello_world(request):
    session = make_stable_connection()
    info = session.get_last_current_assembly()
    session.close_session()
    context = {
        'author': info.author,
        'commit_message': info.commit_message,
        'commit_id': info.commit_id,
        'commit_created_at': info.created_at,
        'assembly': info.assembly,
        'date': info.date,
    }
    return render(request, 'apiproject/base.html', context)
