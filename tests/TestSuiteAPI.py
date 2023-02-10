# ----------12 тестов по Заданию 19.7.2----------
from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

# Тест 1 - создание нового питомца без фото (тест к реализованному самостоятельно АРI-методу)
def test_create_pet_simple_with_valid_data(name='Chaika', animal_type='bird', age='3'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


# Тест 2 - добавление фото своему питомцу (тест к реализованному самостоятельно АРI-методу)
def test_successful_set_photo_pet(pet_photo='images/BIRD.jpeg'):
    """Проверяем возможность добавления фотографии питомца"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.set_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert result['pet_photo'] is not None
    else:
        raise Exception("There is no my pets")


# Тест 3
def test_get_api_key_for_wrong_password(email=valid_email, password='77777'):
    """Проверка с негативным сценарием - запрос api ключа возвращает статус 403 (ошибка пользователя),
     если введен неверный пароль"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


# Тест 4
def test_get_api_key_for_wrong_email(email='777@mail.ru', password=valid_password):
    """Проверка с негативным сценарием - запрос api ключа возвращает статус 403 (ошибка пользователя),
     если введен неверный адрес электронной почты"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


# Тест 5
def test_negative_add_new_pet_without_photo(name='Lara', animal_type='krisa', age='15', pet_photo=''):
    """Проверка невозможности добавить нового питомца с пустым фото"""

    try:
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except Exception as error:
        assert error

# Тест 6
def test_successful_delete_not_mine_pet():
    """Проверка с негативным сценарием - возможность удаления чужого питомца по его id."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key)
    pet_id = pets['pets'][0]['id']

    status, _ = pf.delete_pet(auth_key, pet_id)
    _, pets = pf.get_list_of_pets(auth_key)

    assert status == 200
    assert pet_id not in pets.values()
# Баг, так как удаляется чужой питомец


#  Тест 7
def test_create_pet_simple_with_negative_age(name='Lara', animal_type='krisa', age=-2):
    """Проверяем возможность добавить питомца c отрицательным значением возраста."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert int(result['age']) < 0
# Баг - должна быть проверка на ввод отрицательных значений возраста


# Тест 8
def test_add_new_pet_photo_png(name='DEREZA', animal_type='koza', age='8', pet_photo='images/KOZA.png'):
    """Проверяем что можно добавить питомца с корректными данными c фото в формате png"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['pet_photo'] is not None


# Тест 9
def test_add_new_pet_with_word_age(name='Nusha', animal_type='cat', age='неизвестно', pet_photo='images/Nusha.jpeg'):
    '''Проверка с негативным сценарием - добавление питомца с текстом в переменной age.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['age'] == age
# Баг. Добавляются питомцы с текстом в поле "age"

# Тест 10
def test_update_info_not_mine_pet(name='Nusha', animal_type='CAT', age=99):
    """Проверка с негативным сценарием - возможность обновления информации чужого питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, '')

    if len(pets['pets']) != 0:
        status, result = pf.update_pet_info(auth_key, pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no pets")
# Баг - можно изменить информацию у чужого питомца


# тест 11
def test_create_pet_simple_with_empty_data(name='', animal_type='', age=''):
    """Проверяем возможность добавить питомца без фото с пустыми данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
# Баг - питомец без данных добавляется на сайт


# Тест 12
def test_neganive_set_photo_not_mine_pet(pet_photo='images/krisa.jpeg'):
    """Проверка с негативным сценарием возможность добавления фотографии к чужому питомцу"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, '')

    status, result = pf.set_photo_pet(auth_key, pets['pets'][0]['id'], pet_photo)
    assert status == 200
# Баг - можно изменить фото чужого питомца. Но тест не стабилен и зависит от загрузки системы.
