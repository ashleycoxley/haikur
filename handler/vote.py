from handler_helper import HaikurHandler
import model
from google.appengine.ext import ndb


def change_vote(haiku, signedin_username, vote_type, increment_or_decrement):
    if vote_type == 'upvote':
        if increment_or_decrement == 'increment':
            haiku.upvotes += 1
            haiku.upvote_usernames.append(signedin_username)
        elif increment_or_decrement == 'decrement':
            haiku.upvotes -= 1
            haiku.upvote_usernames.remove(signedin_username)
    elif vote_type == 'downvote':
        if increment_or_decrement == 'increment':
            haiku.downvotes += 1
            haiku.downvote_usernames.append(signedin_username)
        elif increment_or_decrement == 'decrement':
            haiku.downvotes -= 1
            haiku.downvote_usernames.remove(signedin_username)
    haiku.put()


def switch_vote(haiku, signedin_username, vote_type, previous_vote_type):
    change_vote(haiku, signedin_username, previous_vote_type, 'decrement')
    change_vote(haiku, signedin_username, vote_type, 'increment')


class VoteHandler(HaikurHandler):
    def post(self, haiku_id):
        user_id = self.read_user_cookie()
        signedin_username = self.get_username_by_cookie()
        haiku_id = self.request.get('haikuID')
        vote_type = self.request.get('voteType')
        haiku_key = ndb.Key('Haiku', int(haiku_id))
        print "haiku_id:", haiku_id
        print "vote_type:", vote_type

        haiku = haiku_key.get()
        upvoters = haiku.upvote_usernames
        downvoters = haiku.downvote_usernames
        if signedin_username in upvoters:
            previous_vote_type = 'upvote'
        if signedin_username in downvoters:
            previous_vote_type = 'downvote'
        voters = upvoters + downvoters

        if signedin_username in voters:
            if previous_vote_type == vote_type:
                change_vote(haiku, signedin_username, vote_type, 'decrement')
                # self.write(json.dumps({'error': error}))
            else:
                switch_vote(haiku, signedin_username, vote_type, previous_vote_type)
                # self.write(json.dumps({'error': error}))
        else:
            change_vote(haiku, signedin_username, vote_type, 'increment')
            # self.write(json.dumps({'error': error}))


