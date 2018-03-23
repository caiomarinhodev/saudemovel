from app.models import Logger


def logger(user, what):
    try:
        log = Logger(user=user, what=str(what))
        log.save()
    except (Exception,):
        pass
