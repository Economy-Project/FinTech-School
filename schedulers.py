from datetime import datetime
import time
from sqlalchemy import * 
from models import Passphrase, User, Article
from sqlalchemy.orm import scoped_session
from models import Session
import os
from dotenv import load_dotenv
load_dotenv()

CHANNEL = int(os.getenv("CHANNEL"))


def cleanup():
    print('Cleaning old users...')
    session = scoped_session(Session)

    try:
        one_hour_ago = int(datetime.utcnow().timestamp()) - 3600

        session.query(Passphrase).filter(
            Passphrase.user.in_(session.query(User.id).filter(
                and_(User.telegramId == -1, User.registeredAt < one_hour_ago)
            ))
        ).delete(synchronize_session = False)

        session.query(User).filter(
            and_(User.telegramId == -1, User.registeredAt < one_hour_ago)
        ).delete(synchronize_session = False)

        session.commit()
    
    except Exception as e:
        session.rollback()
        raise e
    
    finally:
        session.remove()

def send_articles(bot):
    session = scoped_session(Session)
    current_time = int(datetime.utcnow().timestamp())
    print(f"Sending articles, time = {current_time}")

    try:
        articles = session.query(Article).filter(Article.publishAt <= current_time).all()

        for article in articles:
            try:
                bot.send_message(CHANNEL, article.article)
                session.delete(article)
            except Exception as e:
                print(f"Could not send article {article.id}: {str(e)}")
        
        session.commit()

    except Exception as e:
        session.rollback()
        raise e
    
    finally:
        session.remove()
    

def cleanupScheduler(interval):
    while True:
        cleanup()
        time.sleep(interval)

def articleScheduler(interval, bot):
    while True:
        send_articles(bot)
        time.sleep(interval)