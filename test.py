# -*- coding: utf-8 -*-                                                                                                                                                                                  
from app import app                                                                                                                                                                                      
import unittest                                                                                                                                                                                          

class Test(unittest.TestCase):                                                                                                                                                                           

    def setUp(self):                                                                                                                                                                                     
        # cria uma instância do unittest, precisa do nome "setUp"                                                                                                                                        
        self.app = app                                                                                                                                                                    

        # envia uma requisicao GET para a URL                                                                                                                                                            
        self.result = self.app.get('/')                                                                                                                                                                  

    def test_requisicao(self):                                                                                                                                                                           
        # compara o status da requisicao (precisa ser igual a 200)                                                                                                                                       
        self.assertEqual(None, None)                                                                                                                                                   