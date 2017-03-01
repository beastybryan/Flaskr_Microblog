'''Beginning of Flasker test-Unit test skeleton'''

import os
import tempfile
import unittest
from flaskr import flaskr

class FlaskrTestCase(unittest.TestCase):
    '''Docstring'''
    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        '''Makes sure login and log out work.'''
        rav = self.app.get('/')                             # Had to change "rv" to "rav"
        assert b'No entries here so far' in rav.data        # Had to change "rv" to "rav".

    def login(self, username, password):
        '''Tests admin credentials'''
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        '''Tests admin logout'''
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        '''Initiates login logout test'''
        rav = self.login('admin', 'default')
        assert b'You were logged in' in rav.data
        rav = self.logout()
        assert b'You were logged out' in rav.data           #For all of the "def test_login_logout"
        rav = self.login('adminx', 'default')               # changed the variable "rv to "rav"
        assert b'Invalid username' in rav.data
        rav = self.login('admin', 'defaultx')
        assert b'Invalid password' in rav.data

    def test_messages(self):
        '''This tests if messages work.'''
        self.login('admin', 'default')
        rav = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rav.data
        assert b'&lt;Hello&gt;' in rav.data
        assert b'<strong>HTML</strong> allowed here' in rav.data

if __name__ == '__main__':
    unittest.main()
