from trumpet.config.base import basetemplate
from trumpet.config.base import add_view

viewers = dict(contacts='ContactViewer',
               clients='ClientViewer',
               calendar='CalendarViewer',)


def configure_wiki(config, rootpath):
    wiki_view = 'mslemon.views.wiki.WikiViewer'
    config.add_route('view_wiki', rootpath)
    add_view(config, wiki_view, 'view_wiki')

    config.add_route('list_pages', '%s/listpages' % rootpath)
    add_view(config, wiki_view, 'list_pages')

    config.add_route('view_page', '%s/{pagename}' % rootpath)
    add_view(config, wiki_view, 'view_page')

    config.add_route('add_page', '%s/add_page/{pagename}' % rootpath)
    add_view(config, wiki_view, 'add_page', permission='wiki_add')

    config.add_route('edit_page', '%s/{pagename}/edit_page' % rootpath)
    add_view(config, wiki_view, 'edit_page', permission='wiki_edit')

def configure_mslemon_cases(config, rootpath='mslcases',
                            permission='consultant'):
    route_name = 'msl_cases'
    config.add_route(route_name,
                     '/%s/cases/{context}/{id}' % rootpath)
    #FIXME: better module name
    config.add_view('mslemon.views.cases.MainCaseViewer',
                    route_name=route_name,
                    renderer=basetemplate,
                    layout='base',
                    permission=permission)
    route_name = 'msl_casesjson'
    config.add_route(route_name,
                     '/%s/casesjson/{context}/{id}' % rootpath)
    config.add_view('mslemon.views.cases.CaseJSONViewer',
                    route_name=route_name,
                    renderer='json',
                    layout='base',
                    permission=permission)
    route_name = 'msl_casesfrag'
    config.add_route(route_name,
                     '/msl/casesfrag/{context}/{id}')
    config.add_view('mslemon.views.cases.CaseFrag',
                    route_name=route_name,
                    renderer='string',
                    layout='base',
                    permission=permission)


def configure_mslemon_docs(config, rootpath='msldocs',
                            permission='consultant'):
    route_name = 'msl_docs'
    config.add_route(route_name,
                     '/%s/docs/{context}/{id}' % rootpath)
    #FIXME: better module name
    config.add_view('mslemon.views.documents.MainDocumentViewer',
                    route_name=route_name,
                    renderer=basetemplate,
                    layout='base',
                    permission=permission)

def configure_consultant(config, rootpath='/consult', permission='consultant'):
    config.add_route('consult', rootpath)
    config.add_view('mslemon.views.consultant.main.MainViewer',
                    route_name='consult',
                    renderer=basetemplate,
                    layout='base',
                    permission=permission)
    for route in ['contacts', 'clients', 'calendar']:
        route_name = 'consult_%s' % route
        config.add_route(route_name,
                         '%s/%s/{context}/{id}' % (rootpath, route))
        view = 'mslemon.views.consultant.%s.%s' % (route, viewers[route])
        config.add_view(view, route_name=route_name,
                        renderer=basetemplate,
                        layout='base',
                        permission=permission)
    route_name = 'consult_frag'
    config.add_route(route_name,
                     '%s/frag/{context}/{id}' % rootpath)
    config.add_view('mslemon.views.consultant.frag.FragViewer',
                    route_name=route_name,
                    renderer='string',
                    layout='base',
                    permission=permission)

    route_name = 'consult_caljson'
    config.add_route(route_name,
                     '%s/caljson/{context}/{id}' % rootpath)
    config.add_view('mslemon.views.consultant.calendar.CalendarJSONViewer',
                    route_name=route_name,
                    renderer='json',
                    layout='base',
                    permission=permission)
    
    ###################################
    route_name = 'msl_tickets'
    config.add_route(route_name,
                     '/msl/tickets/{context}/{id}')
    #FIXME: better module name
    config.add_view('mslemon.views.tickets.MSLViewer',
                    route_name=route_name,
                    renderer=basetemplate,
                    layout='base',
                    permission=permission)
    route_name = 'msl_tktjson'
    config.add_route(route_name,
                     '/msl/tktjson/{context}/{id}')
    config.add_view('mslemon.views.tickets.TicketJSONViewer',
                    route_name=route_name,
                    renderer='json',
                    layout='base',
                    permission=permission)
    route_name = 'msl_tktfrag'
    config.add_route(route_name,
                     '/msl/tktfrag/{context}/{id}')
    config.add_view('mslemon.views.tickets.TicketFrag',
                    route_name=route_name,
                    renderer='string',
                    layout='base',
                    permission=permission)
    route_name = 'msl_phonecalls'
    config.add_route(route_name,
                     '/msl/phonecalls/{context}/{id}')
    config.add_view('mslemon.views.phonecalls.MSLPhoneViewer',
                    route_name=route_name,
                    renderer=basetemplate,
                    layout='base',
                    permission=permission)
    route_name = 'msl_pcallfrag'
    config.add_route(route_name,
                     '/msl/pcallfrag/{context}/{id}')
    config.add_view('mslemon.views.phonecalls.PhoneCallFrag',
                    route_name=route_name,
                    renderer='string',
                    layout='base',
                    permission=permission)
    route_name = 'msl_pcalljson'
    config.add_route(route_name,
                     '/msl/pcalljson/{context}/{id}')
    config.add_view('mslemon.views.phonecalls.PhoneCallJSONViewer',
                    route_name=route_name,
                    renderer='json',
                    layout='base',
                    permission=permission)
    
    
    route_name = 'msl_scandocs'
    config.add_route(route_name,
                     '/msl/scandocs/{context}/{id}')
    config.add_view('mslemon.views.consultant.pdfscans.ScannedDocumentsViewer',
                    route_name=route_name,
                    renderer=basetemplate,
                    layout='base',
                    permission=permission)

    route_name = 'msl_scandoc_json'
    config.add_route(route_name,
                     '/msl/scandocsjson/{context}/{id}')
    view = 'mslemon.views.consultant.pdfscans.ScannedDocumentsJSONViewer'
    config.add_view(view,
                    route_name=route_name,
                    renderer='json',
                    layout='base',
                    permission=permission)
    
