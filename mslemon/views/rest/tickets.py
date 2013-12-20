from pyramid.security import Everyone, Authenticated

from cornice.resource import resource, view

from mslemon.models.misslemon import Description
from mslemon.models.misslemon import Ticket, TicketCurrentStatus
from mslemon.models.misslemon import TicketStatusChange
from mslemon.models.misslemon import TicketDocument

from mslemon.managers.tickets import TicketManager

from mslemon.views.rest.base import BaseResource


# FIXME: this needs to be in manager
import transaction



@resource(collection_path='/rest/msl/tickets/main',
          path='/rest/msl/tickets/main/{id}',
          permission='user')
class TicketResource(BaseResource):
    dbmodel = Ticket

    def __init__(self, request):
        super(TicketResource, self).__init__(request)
        self.mgr = TicketManager(self.db)

    def collection_get(self):
        q = self.db.query(self.dbmodel)
        return dict(data=[o.serialize() for o in q])


@resource(collection_path='/rest/msl/tickets/filtered/{filter}/',
          path='/rest/msl/tickets/filtered/{filter}/{id}',
          permission='user')
class FilteredTicketResource(BaseResource):
    dbmodel = Ticket
    
    
    
