from mslemon.views.base import BaseViewer

from mslemon.managers.consultant.tickets import TicketManager
from mslemon.managers.consultant.phone import PhoneCallManager



class JSONViewer(BaseViewer):
    def __init__(self, request):
        super(JSONViewer, self).__init__(request)
        self.tm = TicketManager(self.request.db)
        self.pcm = PhoneCallManager(self.request.db)
        self.context = None
        if 'context' in self.request.matchdict:
            self.context = self.request.matchdict['context']

        # make dispatch table
        self._cntxt_meth = dict(
            ticketcal=self.get_ticket_calendar_status,
            phonecal=self.get_phone_calls,)

        # dispatch context request
        if self.context in self._cntxt_meth:
            self._cntxt_meth[self.context]()
        else:
            msg = 'Undefined Context: %s' % self.context
            self.layout.content = '<b>%s</b>' % msg


    def serialize_ticket_current_status_for_calendar(self, cstatus):
        viewticket = self.request.route_url('consult_tickets',
                                            context='viewticket',
                                            id=cstatus.ticket_id)
        data = dict(id=cstatus.ticket_id,
                    start=cstatus.last_change.isoformat(),
                    end=cstatus.last_change.isoformat(),
                    title=cstatus.ticket.title,
                    url=viewticket)
        return data

    def serialize_phone_call_for_calendar(self, pcall):
        viewcall = self.request.route_url('consult_phone',
                                          context='viewcall',
                                          id=pcall.id)
        data = dict(id=pcall.id,
                    start=pcall.received.isoformat(),
                    end=pcall.received.isoformat(),
                    title=pcall.caller,
                    url=viewcall)
        return data
    

    def get_phone_calls(self):
        start_ts = self.request.GET['start']
        end_ts = self.request.GET['end']
        calls = self.pcm.get_calls_range_ts(start_ts, end_ts)
        clist = []
        for pcall in calls:
            pcdata = self.serialize_phone_call_for_calendar(pcall)
            clist.append(pcdata)
        self.response = clist
        
        
    def get_ticket_calendar_status(self):
        start_ts = self.request.GET['start']
        end_ts = self.request.GET['end']
        slist = []
        for cstatus in self.tm.get_current_status_range_ts(start_ts, end_ts):
            caldata = self.serialize_ticket_current_status_for_calendar(cstatus)
            slist.append(caldata)
        #self.response = dict(updates=slist)
        #self.response = 'sdfsdfsdf'
        self.response = slist
    
        
