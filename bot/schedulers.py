from datetime import datetime
import time
from sqlalchemy import * 
from models import Passphrase, User, Article
from sqlalchemy.orm import scoped_session
from models import Session

def cleanup():
    print('Cleaning old users...')
    session = scoped_session(Session)

    try:
        one_hour_ago = int(datetime.now().timestamp()) - 3600

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
    print('Sending articles...')
    session = scoped_session(Session)

    try:
        articles = session.query(Article).filter(Article.publishAt <= int(datetime.now().timestamp())).all()
        users = session.query(User).filter(User.telegramId != -1).all()

        for article in articles:
            for user in users:
                bot.send_message(user.telegramId, article.article)
                time.sleep(0.25) # костыль :(
        
        for article in articles:
            session.delete(article)
        
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