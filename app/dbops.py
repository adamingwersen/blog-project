from app import app, db
from app.models import User, Post, PostRegister
from datetime import datetime

def count_downvotes(post_id):
    downvotes = PostRegister.query.filter_by(post_id = post_id).sum(downvote)
    return(downvotes)


def count_upvotes(post_id):
    upvotes = PostRegister.query.filter_by(post_id = post_id).sum(upvote)
    return(upvotess)
