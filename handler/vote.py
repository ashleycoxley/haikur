from handler_helper import HaikurHandler
import model
from google.appengine.ext import ndb
import json


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
                vote_response = {'change': 'current_decrement'}
                self.response.write(json.dumps(vote_response))
            else:
                switch_vote(haiku, signedin_username, vote_type, previous_vote_type)
                vote_response = {'change': 'switch'}
                self.response.write(json.dumps(vote_response))
        else:
            change_vote(haiku, signedin_username, vote_type, 'increment')
            vote_response = {'change': 'current_increment'}
            self.response.write(json.dumps(vote_response))
