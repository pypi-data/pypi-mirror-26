import sys
import os
import paste.lint

from authkit.authenticate import middleware, sample_app
from paste.fixture import *

sys.path.insert(0, os.getcwd()+'/examples/docs')

from form import app as form_app
from basic import app as basic_app
from digest import app as digest_app
from forward import app as forward_app
#from open_id import app as openid_app
from redirect import app as redirect_app

# Add the paste validation middleware
form_app = paste.lint.middleware(form_app)
basic_app = paste.lint.middleware(basic_app)
digest_app = paste.lint.middleware(digest_app)
forward_app = paste.lint.middleware(forward_app)
#openid_app = paste.lint.middleware(openid_app)
redirect_app = paste.lint.middleware(redirect_app)

sys.path.insert(0, os.getcwd()+'/examples/config')
from digest import app as config_app

def assertEqual(a,b):
    if a != b:
        raise AssertionError('%s != %s'%(a,b))

def assertAllEqual(*args):
    if not len(args)>2:
        raise Exception("Need two arguments")
    a = args[0]
    for b in args[1:]:
        if a != b:
            raise AssertionError('%s != %s'%(a,b))

apps = [
    form_app, 
    basic_app, 
    digest_app, 
    forward_app,
    #openid_app, 
    redirect_app,
    config_app,
]

def test_users_api_database():
    try: 
        from authkit.users.sqlalchemy_04_driver import UsersFromDatabase, setup_model
    except ImportError:
        raise Exception("Could not run the SQLAlchemy tests, not installed")
    try: 
        from sqlalchemymanager import SQLAlchemyManager
    except ImportError:
        raise Exception("Could not run the SQLAlchemy tests, SQLAlchemyManager is not installed")
    
    
    #f = os.path.join(os.getcwd(), 'mydb.db')
    #if os.path.exists(f):
    #    os.remove("mydb.db")

    app = SQLAlchemyManager(
        None, 
        {'sqlalchemy.url':'sqlite://:memory/'}, 
        [setup_model]
    )
    app.create_all()
    connection = app.engine.connect()
    session = app.session_maker(bind=connection)
    try:
        environ = {}
        environ['sqlalchemy.session'] = session
        environ['sqlalchemy.model'] = app.model
        d = UsersFromDatabase(environ)
        d.role_create("wiki")
        d.role_create("adMin")
        d.role_create("editor")
        d.group_create("pyLOns")
        d.group_create("dJAngo")
        d.user_create("jaMEs", "passWOrd1", "pyLoNs")
        d.user_create("ben", "password2")
        d.user_create("Simon", "password3")
        d.user_create("ian", "paSsword4")
        assertEqual(d.list_roles(),["admin", "editor", "wiki"])
        assertEqual(d.list_groups(),["django", "pylons"])
        assertEqual(d.list_users(),['ben', 'ian', 'james', 'simon'])
        assertEqual(d.user_has_password("james", "passWOrd1"), True)
        assertEqual(d.user_has_password("james", "password1"), False)
        
        d.role_create("test_role")
        d.group_create("test_group")
        d.user_create("test_user", "password")
        assertEqual(d.list_roles(),["admin", "editor", "test_role", "wiki"])
        assertEqual(d.list_groups(),["django", "pylons", "test_group"])
        assertEqual(d.list_users(),['ben', 'ian', 'james', 'simon', "test_user"])
        d.role_delete("test_role")
        d.group_delete("test_group")
        d.user_delete("test_user")
        assertEqual(d.list_roles(),["admin", "editor", "wiki"])
        assertEqual(d.list_groups(),["django", "pylons"])
        assertEqual(d.list_users(),['ben', 'ian', 'james', 'simon'])
    
        assertEqual(d.user_has_role("james", "admin"), False)
        d.user_add_role("james", "admin")
        assertEqual(d.user_has_role("james", "admin"), True)
        d.user_remove_role("james", "admin")
        assertEqual(d.user_has_role("james", "admin"), False)
    
        d.user_add_role("james", "wiki")
        d.user_add_role("simon", "wiki")
        d.user_add_role("james", "admin")
        #d.user_add_role("james", "editor")
        d.user_add_role("ben", "editor")
        
        assertEqual(d.user_has_group("james", "pylons"), True)
        assertEqual(d.user_has_group("simon", None), True)
        assertEqual(d.user_has_group("simon", "django"), False)
        d.user_set_group("simon", "dJangO")
        assertEqual(d.user_has_group("simon", None), False)
        d.user_set_group("bEn", "PyLONS")
        assertEqual(d.user_has_group("simon", "django"), True)
        assertEqual(d.user_has_group("bEn", "pYlons"), True)
        d.user_remove_group("bEn")
        assertEqual(d.user_has_group("bEn", "pYlons"), False)
        d.user_set_group("bEn", "PyLONS")
        assertEqual(d.user_has_group("bEn", "pYlons"), True)
        
        assertEqual(d.list_users(),['ben', 'ian', 'james', 'simon'])
        d.user_set_username("james", "jim")
        assertEqual(d.list_users(),['ben', 'ian', 'jim', 'simon'])
        d.user_set_username("jim", "james")
        
        from authkit.users import UsersFromFile, UsersFromString, AuthKitNoSuchUserError, AuthKitNoSuchGroupError,AuthKitNoSuchRoleError
        string_data = """jaMEs:passWOrd1:pyLOns wiki adMin
        ben:password2:pylons admin editor
        simon:password3:dJAngo
        ian:paSsword4 wiki
        """
        filename = 'test/user_file_data.txt'
        
        s = UsersFromString(string_data)
        f = UsersFromFile(filename)
    
        # Test Parsing
        assertAllEqual(
            s.passwords,
            f.passwords,
            {
                'james':'passWOrd1',
                'ben':'password2',
                'simon':'password3',
                'ian':'paSsword4',
            },
        )
        assertAllEqual(
            s.roles, 
            f.roles,
            {
                'james':['admin', 'wiki'],
                'ben':['admin','editor'],
                'ian':['wiki'],
                'simon':[],
            },
        )
        assertAllEqual(
            s.groups, 
            f.groups,
            {
                'james':'pylons',
                'ben':'pylons',
                'ian': None,
                'simon':'django',
            },
        )
        assertAllEqual(
            s.usernames, 
            f.usernames,
            ['ben', 'ian', 'james', 'simon'],
        )
    
        # Test list functions
        assertAllEqual(
            s.list_users(),
            f.list_users(),
            d.list_users(),
            ['ben', 'ian', 'james', 'simon'],
        )
        assertAllEqual(
            s.list_roles(), 
            f.list_roles(),
            d.list_roles(),
            ['admin', 'editor', 'wiki'],
        )
        assertAllEqual(
            s.list_groups(), 
            f.list_groups(),
            d.list_groups(),
            ['django','pylons'],
        )
    
        # Test user has functions
        assertAllEqual(
            s.user_has_role('jAMes','WiKi'), 
            f.user_has_role('jAMes','WiKi'), 
            d.user_has_role('jAMes','WiKi'), 
            True
        )
        assertAllEqual(
            s.user_has_role('jAMes','editOr'), 
            f.user_has_role('jAMes','editOr'), 
            d.user_has_role('jAMes','editOr'), 
            False
        )
        
        assertAllEqual(
            s.user_has_group('jAMeS','PyLons'), 
            f.user_has_group('jAMes','pylOns'), 
            d.user_has_group('jAMes','pylOns'), 
            True
        )
        assertAllEqual(
            s.user_has_group('jameS','djaNgo'), 
            f.user_has_group('JAMes','djAngo'), 
            d.user_has_group('JAMes','djAngo'), 
            False
        )
    
        assertAllEqual(
            s.user_has_password('jAMeS','passWOrd1'), 
            f.user_has_password('jAMes','passWOrd1'), 
            d.user_has_password('jAMes','passWOrd1'), 
            True
        )
        assertAllEqual(
            s.user_has_password('jameS','PASSWORD1'), 
            f.user_has_password('JAMes','PASSWORD1'), 
            d.user_has_password('JAMes','PASSWORD1'), 
            False
        )
    
        # Existence Methods
        assertAllEqual(
            s.user_exists('jAMeS'), 
            f.user_exists('jAMes'), 
            d.user_exists('jAMes'), 
            True
        )
        assertAllEqual(
            s.user_exists('nobody'), 
            f.user_exists('nobody'), 
            d.user_exists('nobody'), 
            False
        )
        
        # Existence Methods
        assertAllEqual(
            s.role_exists('wiKi'), 
            f.role_exists('Wiki'), 
            d.role_exists('Wiki'), 
            True
        )
        assertAllEqual(
            s.role_exists('norole'), 
            f.role_exists('norole'), 
            d.role_exists('norole'), 
            False
        )
        
        assertAllEqual(
            s.group_exists('pyLons'), 
            f.group_exists('PYlons'), 
            d.group_exists('PYlons'), 
            True
        )
        assertAllEqual(
            s.group_exists('nogroup'), 
            f.group_exists('nogroup'), 
            d.group_exists('nogroup'), 
            False
        )
    
    
        # User Methods
        
        assertAllEqual(
            s.user('James'), 
            f.user('James'),
            d.user('James'),
            {
                'username': 'james',
                'group':    'pylons',
                'password': 'passWOrd1',
                'roles':    ['admin','wiki'],
            }
        )
        
        # Test all user methods raise:
        for plugin in [s,f,d]:
            for func in [
                'user',
                'user_roles',
                'user_group',
                'user_password',
            ]:
                try:
                    getattr(plugin, func)('nouser')
                except AuthKitNoSuchUserError, e:
                    pass
                else:
                    raise AssertionError("Failed to throw a no user error")
        for plugin in [s,f,d]:
            for func in [
                'user_has_password',
                'user_has_role',
                'user_has_group',
            ]:
                try:
                    getattr(plugin, func)('nouser','somevar')
                except AuthKitNoSuchUserError, e:
                    pass
                else:
                    raise AssertionError("Failed to throw a no user error")
    
        assertAllEqual(
            s.user_roles('James'), 
            f.user_roles('James'),
            d.user_roles('James'),
            ['admin','wiki']
        )
        assertAllEqual(
            s.user_group('James'), 
            f.user_group('James'),
            d.user_group('James'),
            'pylons'
        )
        assertAllEqual(
            s.user_password('James'), 
            f.user_password('James'),
            d.user_password('James'),
            'passWOrd1'
        )
        
        session.flush()
        session.commit()
    finally:
        session.close()
        connection.close()

        

def test_users_model_api_database():
    sys.path.insert(0, os.getcwd()+'/examples/user/database-model')
    try: 
        from authkit.users.sqlalchemy_driver import UsersFromDatabase
    except ImportError:
        raise Exception("Could not run the SQLAlchemy tests, not installed")
    if os.path.exists("test.db"):
        os.remove("test.db")
    import model as test_model

    # Setup SQLAlchemy database engine
    from sqlalchemy import engine_from_config
    engine = engine_from_config({'sqlalchemy.url':'sqlite:///test.db'}, 'sqlalchemy.')
    test_model.init_model(engine)
    test_model.engine = engine
 
    d = UsersFromDatabase(test_model)
    
    test_model.meta.metadata.create_all(test_model.engine)
    
    d.role_create("wiki")
    d.role_create("adMin")
    d.role_create("editor")
    d.group_create("pyLOns")
    d.group_create("dJAngo")
    d.user_create("jaMEs", "passWOrd1", "pyLoNs")
    d.user_create("ben", "password2")
    d.user_create("Simon", "password3")
    d.user_create("ian", "paSsword4")
    assertEqual(d.list_roles(),["admin", "editor", "wiki"])
    assertEqual(d.list_groups(),["django", "pylons"])
    assertEqual(d.list_users(),['ben', 'ian', 'james', 'simon'])
    assertEqual(d.user_has_password("james", "passWOrd1"), True)
    assertEqual(d.user_has_password("james", "password1"), False)
    
    d.role_create("test_role")
    d.group_create("test_group")
    d.user_create("test_user", "password")
    assertEqual(d.list_roles(),["admin", "editor", "test_role", "wiki"])
    assertEqual(d.list_groups(),["django", "pylons", "test_group"])
    assertEqual(d.list_users(),['ben', 'ian', 'james', 'simon', "test_user"])
    d.role_delete("test_role")
    d.group_delete("test_group")
    d.user_delete("test_user")
    assertEqual(d.list_roles(),["admin", "editor", "wiki"])
    assertEqual(d.list_groups(),["django", "pylons"])
    assertEqual(d.list_users(),['ben', 'ian', 'james', 'simon'])

    assertEqual(d.user_has_role("james", "admin"), False)
    d.user_add_role("james", "admin")
    assertEqual(d.user_has_role("james", "admin"), True)
    d.user_remove_role("james", "admin")
    assertEqual(d.user_has_role("james", "admin"), False)

    d.user_add_role("james", "wiki")
    d.user_add_role("simon", "wiki")
    d.user_add_role("james", "admin")
    #d.user_add_role("james", "editor")
    d.user_add_role("ben", "editor")
    
    assertEqual(d.user_has_group("james", "pylons"), True)
    assertEqual(d.user_has_group("simon", None), True)
    assertEqual(d.user_has_group("simon", "django"), False)
    d.user_set_group("simon", "dJangO")
    assertEqual(d.user_has_group("simon", None), False)
    d.user_set_group("bEn", "PyLONS")
    assertEqual(d.user_has_group("simon", "django"), True)
    assertEqual(d.user_has_group("bEn", "pYlons"), True)
    d.user_remove_group("bEn")
    assertEqual(d.user_has_group("bEn", "pYlons"), False)
    d.user_set_group("bEn", "PyLONS")
    assertEqual(d.user_has_group("bEn", "pYlons"), True)
    
    assertEqual(d.list_users(),['ben', 'ian', 'james', 'simon'])
    d.user_set_username("james", "jim")
    assertEqual(d.list_users(),['ben', 'ian', 'jim', 'simon'])
    d.user_set_username("jim", "james")
    
    from authkit.users import UsersFromFile, UsersFromString, AuthKitNoSuchUserError, AuthKitNoSuchGroupError,AuthKitNoSuchRoleError
    string_data = """jaMEs:passWOrd1:pyLOns wiki adMin
    ben:password2:pylons admin editor
    simon:password3:dJAngo
    ian:paSsword4 wiki
    """
    filename = 'test/user_file_data.txt'
    
    s = UsersFromString(string_data)
    f = UsersFromFile(filename)

    # Test Parsing
    assertAllEqual(
        s.passwords,
        f.passwords,
        {
            'james':'passWOrd1',
            'ben':'password2',
            'simon':'password3',
            'ian':'paSsword4',
        },
    )
    assertAllEqual(
        s.roles, 
        f.roles,
        {
            'james':['admin', 'wiki'],
            'ben':['admin','editor'],
            'ian':['wiki'],
            'simon':[],
        },
    )
    assertAllEqual(
        s.groups, 
        f.groups,
        {
            'james':'pylons',
            'ben':'pylons',
            'ian': None,
            'simon':'django',
        },
    )
    assertAllEqual(
        s.usernames, 
        f.usernames,
        ['ben', 'ian', 'james', 'simon'],
    )

    # Test list functions
    assertAllEqual(
        s.list_users(),
        f.list_users(),
        d.list_users(),
        ['ben', 'ian', 'james', 'simon'],
    )
    assertAllEqual(
        s.list_roles(), 
        f.list_roles(),
        d.list_roles(),
        ['admin', 'editor', 'wiki'],
    )
    assertAllEqual(
        s.list_groups(), 
        f.list_groups(),
        d.list_groups(),
        ['django','pylons'],
    )

    # Test user has functions
    assertAllEqual(
        s.user_has_role('jAMes','WiKi'), 
        f.user_has_role('jAMes','WiKi'), 
        d.user_has_role('jAMes','WiKi'), 
        True
    )
    assertAllEqual(
        s.user_has_role('jAMes','editOr'), 
        f.user_has_role('jAMes','editOr'), 
        d.user_has_role('jAMes','editOr'), 
        False
    )
    
    assertAllEqual(
        s.user_has_group('jAMeS','PyLons'), 
        f.user_has_group('jAMes','pylOns'), 
        d.user_has_group('jAMes','pylOns'), 
        True
    )
    assertAllEqual(
        s.user_has_group('jameS','djaNgo'), 
        f.user_has_group('JAMes','djAngo'), 
        d.user_has_group('JAMes','djAngo'), 
        False
    )

    assertAllEqual(
        s.user_has_password('jAMeS','passWOrd1'), 
        f.user_has_password('jAMes','passWOrd1'), 
        d.user_has_password('jAMes','passWOrd1'), 
        True
    )
    assertAllEqual(
        s.user_has_password('jameS','PASSWORD1'), 
        f.user_has_password('JAMes','PASSWORD1'), 
        d.user_has_password('JAMes','PASSWORD1'), 
        False
    )

    # Existence Methods
    assertAllEqual(
        s.user_exists('jAMeS'), 
        f.user_exists('jAMes'), 
        d.user_exists('jAMes'), 
        True
    )
    assertAllEqual(
        s.user_exists('nobody'), 
        f.user_exists('nobody'), 
        d.user_exists('nobody'), 
        False
    )
    
    # Existence Methods
    assertAllEqual(
        s.role_exists('wiKi'), 
        f.role_exists('Wiki'), 
        d.role_exists('Wiki'), 
        True
    )
    assertAllEqual(
        s.role_exists('norole'), 
        f.role_exists('norole'), 
        d.role_exists('norole'), 
        False
    )
    
    assertAllEqual(
        s.group_exists('pyLons'), 
        f.group_exists('PYlons'), 
        d.group_exists('PYlons'), 
        True
    )
    assertAllEqual(
        s.group_exists('nogroup'), 
        f.group_exists('nogroup'), 
        d.group_exists('nogroup'), 
        False
    )


    # User Methods
    
    assertAllEqual(
        s.user('James'), 
        f.user('James'),
        d.user('James'),
        {
            'username': 'james',
            'group':    'pylons',
            'password': 'passWOrd1',
            'roles':    ['admin','wiki'],
        }
    )
    
    # Test all user methods raise:
    for plugin in [s,f,d]:
        for func in [
            'user',
            'user_roles',
            'user_group',
            'user_password',
        ]:
            try:
                getattr(plugin, func)('nouser')
            except AuthKitNoSuchUserError, e:
                pass
            else:
                raise AssertionError("Failed to throw a no user error")
    for plugin in [s,f,d]:
        for func in [
            'user_has_password',
            'user_has_role',
            'user_has_group',
        ]:
            try:
                getattr(plugin, func)('nouser','somevar')
            except AuthKitNoSuchUserError, e:
                pass
            else:
                raise AssertionError("Failed to throw a no user error")

    assertAllEqual(
        s.user_roles('James'), 
        f.user_roles('James'),
        d.user_roles('James'),
        ['admin','wiki']
    )
    assertAllEqual(
        s.user_group('James'), 
        f.user_group('James'),
        d.user_group('James'),
        'pylons'
    )
    assertAllEqual(
        s.user_password('James'), 
        f.user_password('James'),
        d.user_password('James'),
        'passWOrd1'
    )
        
        
        
