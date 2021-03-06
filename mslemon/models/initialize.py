from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import engine_from_config

import transaction

from mslemon.models.base import DBSession, Base
from mslemon.models.main import make_test_data

from trumpet.models.sitecontent import SitePath
from trumpet.models.sitecontent import populate_sitetext

from mslemon.models.usergroup import populate_groups
from mslemon.models.usergroup import populate

def initialize_database(settings):
    admin_username = settings.get('mslemon.admin.admin_username', 'admin')
    engine = engine_from_config(settings, 'sqlalchemy.')
    Base.metadata.create_all(engine)
    populate_groups()
    populate(admin_username)
    try:
        populate_sitetext()
    except IntegrityError:
        transaction.abort()
