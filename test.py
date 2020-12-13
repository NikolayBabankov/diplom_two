import unittest
import main
import app.db

class TestMultiplication(unittest.TestCase):

    def setUp(self):
        print('Начало тестов')
    

    def tearDown(self):
        print('Конец тестов')
    
    
    def test_number1(self):
        print('тест №1 Получение данных о пользователи')
        self.assertEqual(main.dating_user(107565058), [107565058, '-', 'Карина', 'Хрустовская', [494, 'https://sun9-32.userapi.com/impf/c836722/v836722058/2e6d9/amFYcco4riE.jpg?size=1080x1080&quality=96&proxy=1&sign=d5ef509ff9b753645e8cd323b2341aca&c_uniq_tag=Mf-pzXC-Sr4IktlcTKU4PAvTRXu4-f7OXqnBff8SyWA&type=album'], [343, 'https://sun9-36.userapi.com/impf/c836220/v836220058/a4e9/3X5_im-2m6g.jpg?size=1200x1200&quality=96&proxy=1&sign=508fdd0ff36dcdc34e0b3f50a9bce61e&c_uniq_tag=wWBBUN4SC23zzRjzpviUcoxjQhQ0b5I_tbfcKLKlFP8&type=album'], [306, 'https://sun9-73.userapi.com/impf/c844418/v844418211/1c2358/nCQq4CUrD2M.jpg?size=960x1280&quality=96&proxy=1&sign=50b18ba3ef204b79368eb31890f35bf5&c_uniq_tag=dOULjAJYJ_15LLFAj7Hec_FRUB9fXXRe7oJlC-a3pSU&type=album']])
    
    def test_number2(self):
        print('тест №2 Запись данных понравившегося человека')
        self.assertEqual(app.db.dating_user_record([96454656, 22, 'Алёна', 'Мазурова', 
        [975, 'https://sun9-69.userapi.com/impf/c637824/v637824656/282/Esl7m5-h_so.jpg?size=673x1019&quality=96&proxy=1&sign=f15a3e3686e9facccf77753b948cea08&c_uniq_tag=3ahHMJe4DJAGy4GdM01iHrqIM_SEpEyLzXo0qPb8bHE&type=album'], 
        [821, 'https://sun9-44.userapi.com/impf/gTE4u5-b0jqJvL7pR4vmFBo-Y5Ku5HS44BMJFw/jKaihddQ-Ik.jpg?size=1200x1500&quality=96&proxy=1&sign=1e06322a352bafc244aa158489255f85&c_uniq_tag=YoDNeSnmd3_IeYjz3mC_Oky_iqO3Z1PqLjmr4C9ptHo&type=album'], 
        [806, 'https://sun9-4.userapi.com/impf/v9VHUaHrgvoGyktpYp3j2D4Jh0KnLRFALlfwIg/_gMLz9o2T2Q.jpg?size=720x540&quality=96&proxy=1&sign=b81b2a9154e02ab6b17069b2a33eb122&c_uniq_tag=iC1MpbYqt-LI08Oau99hZNZbsIUUv_qcIM8uO4IokUw&type=album']]
        , 582841708), True)

if __name__ == '__main__':
    unittest.main()
