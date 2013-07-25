from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey


from sqlalchemy.orm import relationship

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


