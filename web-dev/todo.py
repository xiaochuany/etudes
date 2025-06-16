# app.py
from fasthtml.common import *
from hmac import compare_digest

db = database("raw/db.db") # has to be in a subdirectory.
todos,users = db.t.todos, db.t.users

if todos not in db.t: # create with schema
    users.create(name=str, pwd=str, pk='name')
    todos.create(id=int, title=str, done=bool, name=str, details=str, priority=int, pk='id')

Todo,User = todos.dataclass(),users.dataclass()

login_redir = RedirectResponse('/login', status_code=303) # starlette thing

def before(req, sess):
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth: return login_redir
    todos.xtra(name=auth) # filter

markdown_js = """
import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
proc_htmx('.markdown', e => e.innerHTML = marked.parse(e.textContent));
"""

def _not_found(req, exc): return Titled('Oh no!', Div('We could not find that page :(')) # just an html page

bware = Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', '/login'])

app  = FastHTML(before=bware, 
         exception_handlers={404: _not_found}, 
         hdrs=(picolink,
            Style(':root { --pico-font-size: 100%; }'),
            SortableJS('.sortable'),
            Script(markdown_js, type='module')))

rt = app.route

@rt("/login")
def get():
    frm = Form(
        Input(id='name', placeholder='Name'),
        Input(id='pwd', type='password', placeholder='Password'),
        Button('login'),
        action='/login', method='post')
    return Titled('Login', frm)

@dataclass
class Login: name:str; pwd:str

@rt("/login")
def post(login:Login, sess):
    if not login.name or not login.pwd: return login_redir
    try: 
        u = users[login.name]
    except NotFoundError: 
        u = users.insert(login)
    if not compare_digest(u.pwd.encode("utf-8"), login.pwd.encode("utf-8")): return login_redir
    sess['auth'] = u.name
    return RedirectResponse('/', status_code=303)

@rt("/logout")
def get(sess):
    del sess['auth']
    return login_redir

@rt('/{fname:path}.{ext:static}')
def get(fname: str, ext: str): return FileResponse(f'{fname}.{ext}')


@patch
def __ft__(self:Todo):
    dt = '✅ ' if self.done else ''
    show = AX(self.title, f'/todos/{self.id}', 'current-todo') # see root get()
    edit = AX('edit', f'/edit/{self.id}', 'current-todo')
    cts = (dt, show, ' | ', edit, Hidden(id="id", value=self.id), Hidden(id="priority", value="0")) # hidden INPUT
    return Li(*cts, id=f'todo-{self.id}')

@rt("/")
def get(auth):
    title = f"{auth}'s Todo list"
    # define top
    top = Grid(H1(title), Div(A("logout", href="/logout", style='text-align: right')))
    # define card made of a add form (header), a display form (content) and empty div (footer)
    new_inp = Input(id='new-title', name='title', placeholder='New todo')
    add = Form(Group(new_inp, Button("add")),
               hx_post='/', target_id='todo-list', hx_swap='afterbegin')
    frm =Form(*todos(order_by='priority'),
              id='todo-list', cls='sortable', hx_post='/reorder', hx_trigger='end') # js end event: when dragging is complete
    card = Card(Ul(frm), header=add, footer= Div(id="current-todo"))  ## HERE is the current-todo
    return Title(title), Container(top, card)

@rt('/reorder')
def post(id:list[int]):
    for i, id_ in enumerate(id):
        todos.update({'priority':i}, id_)
    return tuple(todos(order_by='priority'))


def clr_details(): return Div(hx_swap_oob='innerHTML', id='current-todo')

@rt('/todos/{id}')
def delete(id:int):
    todos.delete(id)
    return clr_details()

@rt('/edit/{id}')
def get(id:int):
    res = Form(Group(Input(id="title"), Button("save")),
               Hidden(id="id"), CheckboxX(id="done", label="Done"),
               Textarea(id="details", name="details",row=10),
               hx_put='/', target_id=f'todo-{id}', id="edit")
    return fill_form(res, todos[id])

@rt('/')
def put(todo: Todo):
    return todos.update(todo), clr_details()

@rt("/")
def post(todo:Todo):
    new_inp =  Input(id="new-title", name="title", placeholder="New Todo", hx_swap_oob='true')
    return todos.insert(todo), new_inp

@rt("/todos/{id}")
def get(id:int):
    todo=todos[id]
    btn = Button("delete", hx_delete=f'/todos/{todo.id}',
                  target_id=f'todo-{todo.id}', hx_swap="outerHTML")
    return Div(H2(todo.title), Div(todo.details, cls="markdown"),btn)

serve()