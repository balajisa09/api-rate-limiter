import unittest
from app import app

class TestAPIRateLimiter(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_rate_limit(self):
        # Test that the rate limit is enforced
        for i in range(2):
            response = self.client.get('/api')
            self.assertEqual(response.status_code, 200)

        response = self.client.get('/api')
        self.assertEqual(response.status_code, 429)

    def test_rate_limit_reset(self):
        # Test that the rate limit is reset after the window size expires
        for i in range(2):
            response = self.client.get('/api')
            self.assertEqual(response.status_code, 429)

        # Wait for the window size to expire
        import time
        time.sleep(60)

        response = self.client.get('/api')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
