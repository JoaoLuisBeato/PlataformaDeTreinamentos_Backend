import unittest
import requests


class Test(unittest.TestCase):
    def test(self):
        response = requests.post('http://127.0.0.1:5000/teste_tdd', json={'email': 'beto', 'password': 'banana'})
        resultado = response.json().get('acesso')   

        self.assertEqual(resultado, 'true')

if __name__ == '__main__':
    unittest.main()