.. -*- mode: rst -*-

=============================
mslemon
=============================
.. image:: https://travis-ci.org/umeboshi2/trumpet.png?branch=master
   :target: https://travis-ci.org/umeboshi2/trumpet


This is a simple web application for managing contacts, clients,
events, trouble tickets, and phone calls.




http://pieceofpy.com/blog/2011/08/01/pyramid-and-traversal-with-a-restful-interface/

UPDATE (2011-08-05)
Please use caution when reading this post. A lot of the approach and implementation here is flawed. I am keeping the post up for historical purposes, but I am currently working on a follow up post that has a much better and proper implementation of traversal for SQLalchemy models. The practice of not returning real instances as traversal expects and tightly coupling the models to the traversal method is something that is less than desirable and will lead to more pain than gain long term. That being said, some of the approaches here are a good way to learn about traversal and how one might want to use it with their data model.

Original Post
When Pyramid was first being developed I was intrigued by the idea that I could create context aware views and use a host of methods to check permissions on those contexts, generate URLs based off those contexts, and auto-magically call the view required based on the context and the requested resource path.

So one of my first experiments with Pyramid was to implement proper resource urls for contexts in a RESTful fashion. Eventually I plan to do this for the entire collection as well, but for now all I need is the context level RESTful interface. The goal of which is to have URLs that go something like this.

/resource/id (GET) - default view of the resource
/resource/id/edit (GET) - the form that allows you to edit the resource
/resource/id/create (GET) - the form that allows you to edit the resource
/resource/id (PUT) - updates
/resource/id (POST) - create
/resource/id (DELETE) - delete
This ends up being pretty damn simple with Pyramid and Traversal and for those of you new to traversal or even those who aren't, I highly recommend reading the Much Ado About Traversal chapter in the Pyramid documentation. Also on a side note all of the snippets from this post are part of a real project called Stockpot and the code is freely available via SourceForge.

My Root
So first step for me was to design my Root object. This is the really the foundation for traversal and determines what resources it will be able to find and how to interact with them once it finds them. My Root object is simple and looks like this.

?
1
2
3
4
5
6
7
8
9
10
11
12
13
def _owned(obj, name, parent):
    obj.__name__ = name
    obj.__parent__ = parent
    return obj
 
class Root(dict):
    __name__ = None
    __parent__ = None
    #
    def __init__(self, request):
        dict.__init__(self)
        self.request = request
        self['user'] = _owned(User, 'user', self)
This is pretty straightforward. We create a user entry point for the first call to getitem and return the User model with a name of user and the Root object as the parent.

My Model
For my Root object to really do anything useful our model class needs to do some work so that when the traversal algorithm calls getitem on our User model it actually gets something useful back. I've done this using a base class for my declarative_base call.

?
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
class StockpotBase(object):
    @classmethod
    def __getitem__(cls, k):
        try:
            result =  DBSession().query(cls).filter_by(id=k).one()
            result.__parent__ = result
            result.__name__ = str(k)
            return result
        except NoResultFound, e:
            raise KeyError
    @classmethod
    def __len__(cls):
        return DBSession().query(cls).count()    
    @classmethod
    def __iter__(cls):
        return (x for x in DBSession().query(cls))
 
Base = declarative_base(cls=StockpotBase)
 
class User(Base):
    __tablename__ = 'users'
    __name__ = 'user'
    #
    def __init__(self, email, password=None, display_name=None):
        self.email = email
        self.password = password
        self.display_name = display_name
    #
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True)
    display_name = Column(String, nullable=True)
    user_groups = relation(Group, backref='user', secondary=groups)
    groups = association_proxy('user_groups', 'name', creator=Group.group_creator)
    recipes = relation(Recipe, backref='user')
    #
    def __str__(self):
        return 'User(id={0}, email={1}, groups={2})'.format(self.id, self.email, self.groups)
 
def __repr__(self):
        return self.__str__()
So that is a pretty big chunk of code so let me go through what is happening, it is rather simple. I've created StockpotBase which has the methods our traversal algorithm is going to want. I've used that as the cls for my declarative_base call so that any class that I create that inherits from Base will have all of the proper methods needed.

The getitem itself ensures that the parent is set to the generic user class and the name of the class is set to the primary key. This is important later when we start using resource_url() to generate links for us in our templates, if you consider that the urls will be generated with the pattern of /parent.name/context.name

My Views
With the Root object setup and our model "traversal enabled", we can look at how the views for this will be setup. I personally like to use the config.scan('stockpot.views') helper and use the @view_config decorator for my views. I find it cleaner and easier to to have the view_config right with the actually def.

?
1
2
3
4
5
6
7
8
9
# RESOURCE_URL = /user/id
@view_config(context=User, renderer='user/view.mako')
def get(request):
    return dict(user=request.context)
 
# RESOURCE_URL = /user/id/edit
@view_config(name='edit', context=User, renderer='user/edit.mako')
def edit(request):
    return dict(user=request.context)
So here is the default GET view. It allows anyone to use this view, but I will have a blog post about permissions with ACL and traversal later, and it uses the renderer of my user/view.mako template. Then we have the edit view which requires User:edit permissions and uses the edit.mako template. Pretty simple. Next we have the first of the JSON views (they don't have to be JSON).

?
1
2
3
4
@view_config(context=User, request_method='PUT', xhr=True, renderer='json')
def put(request):
    user = request.context
    return dict(method='PUT', user_id=user.id, email=user.email)
And the mako template jQuery for this might look something like this

$$code(lang=javascript, linenums=True) $(document).ready(function() { $('#put').click(function() { $.ajax({ url: '${request.resource_url(user)}', type: 'PUT', context: document.body, dataType: 'json', success: function(data) { console.log(data); alert('done'); } }); }); });

And that is it. You would repeat the same view pattern for request_method POST and request_method DELETE and you would have RESTful API in to your resources/models in a very clean fashion.

What Happens
When a user visits the resource url a simple series of calls to getitem happens. The Root (/) object is called with 'user'. A User object with the name of 'user' and the parent of Root is returned. The User class has it's getitem called and uses the DBSession to lookup a user based on the key given. For example /user/1 (Root / User / k) would result in '1' being passed to the user objects getitem as the key. If it locates the user, it returns the instance and sets the name and parent. If you don't set the name when you call resource_url with the context, the generated URL would look read /user instead of /user/1.

There is nothing after the 1 so it looks for a generic unnamed view that handles the User context. In our case, our get method. When you add on edit, /user/1/edit it works in the same fashion, but when it tries to call getitem a second time on the User instance it will throw a key error which tells Pyramid that I am looking for a view named edit with the context of User. This traversal works the same way for the JSON calls as well.

Feedback
I don't like the fact that there are extra DB calls here, but it is a trade off. Even the /user/1/edit has to make two database calls to get the KeyError and review the proper view, but as a side-effect I can do something like /user/1/collection/1 and get the specific item of the collection owned by the user. That extends to edits as well ... /user/1/collection/1/edit. Overall I like how this pattern has evolved in my application, but would appreciate any feedback or suggested improvements to what I've done so far.

