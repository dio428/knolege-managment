import unittest
from app import create_app, db
from app.models import User, Product

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False # Disable CSRF for testing forms
    SECRET_KEY = 'a-secret-key-for-testing'

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

class ProductModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_product(self):
        p = Product(name='Test Product', barcode='123456789')
        db.session.add(p)
        db.session.commit()
        self.assertEqual(Product.query.count(), 1)
        self.assertEqual(Product.query.first().name, 'Test Product')
        self.assertEqual(Product.query.first().barcode, '123456789')

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In', response.data)

    def test_create_product_route_not_logged_in(self):
        response = self.client.get('/create_product', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In', response.data)

if __name__ == '__main__':
    unittest.main(verbosity=2)
