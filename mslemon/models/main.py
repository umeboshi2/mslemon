import transaction

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey


from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError

from mslemon.models.base import Base, DBSession

# these models depend on the Base object above

import mslemon.models.usergroup
import mslemon.models.sitecontent
import mslemon.models.consultant

class LoginHistory(Base):
    __tablename__ = 'login_history'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    when = Column(DateTime, primary_key=True)
    

populate = mslemon.models.usergroup.populate


def make_test_data(session):
    from trumpet.security import encrypt_password
    from mslemon.models.usergroup import User, Group, UserGroup
    from mslemon.models.usergroup import Password
    db = session
    users = ['thor', 'zeus', 'loki']
    id_count = 1 # admin is already 1
    manager_group_id = 4 # magic number
    # add users
    try:
        with transaction.manager:
            for uname in users:
                id_count += 1
                user = User(uname)
                password = encrypt_password('p22wd')
                db.add(user)
                pw = Password(id_count, password)
                db.add(pw)
                ug = UserGroup(manager_group_id, id_count)
                db.add(ug)
    except IntegrityError:
        transaction.abort()
    from mslemon.models.consultant import PhoneCall
    count = db.query(PhoneCall).count()
    if count < 20:
        callers = ['James T. Kirk', 'Alfred Hitchcock',
                   'Johnny Dupree', 'George DeCoux']
        numbers = ['(234)-234-2354',
                   '(234)-345-3556',
                   '(601)-555-1212',]
        msgs = ['This is a message', 'This is another message',
                'There has been a change in plans',
                'Something important happened',
                'Please call back soon',]
        from mslemon.managers.consultant.phone import PhoneCallManager
        from datetime import datetime, timedelta
        import random
        ten_minutes = timedelta(minutes=10)
        one_hour = timedelta(hours=1)
        tdiffs = [ one_hour, - one_hour,
                   2*one_hour, -2*one_hour,
                   3*one_hour, -3*one_hour,
                   ten_minutes, -ten_minutes,
                   2*ten_minutes, -2*ten_minutes,
                   3*ten_minutes, -3*ten_minutes]
        now = datetime.now()
        pcm = PhoneCallManager(db)
        try:
            with transaction.manager:
                for ignore in range(10):
                    ctime = now + random.choice(tdiffs) + random.choice(tdiffs)
                    caller = random.choice(callers)
                    number = random.choice(numbers)
                    msg = random.choice(msgs)
                    pcm.new_call(ctime, caller, number, msg, 2, 3)
                for ignore in range(10):
                    ctime = now + random.choice(tdiffs) + random.choice(tdiffs)
                    caller = random.choice(callers)
                    number = random.choice(numbers)
                    msg = random.choice(msgs)
                    pcm.new_call(ctime, caller, number, msg, 3, 2)
        except IntegrityError:
            transaction.abort()
        
            
