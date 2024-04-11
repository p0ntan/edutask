import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController

@pytest.fixture
def user_controller(dao_response: list):
    mockedDao = mock.MagicMock()
    mockedDao.find.return_value = dao_response
    controller = UserController(mockedDao)
    return controller

@pytest.mark.assignment_2
class TestGetUserByEmail:
    @pytest.mark.parametrize('dao_response, expected', [
        ([], None),
        ([{'name': 'First Dave', 'email': 'valid_user@test.com'}],{'name': 'First Dave', 'email': 'valid_user@test.com'}),
        ([{'name': 'First Dave', 'email': 'valid_user@test.com'}, {'name': 'Second Dave', 'email': 'valid_user@test.com'}], {'name': 'First Dave', 'email': 'valid_user@test.com'}),
        ([{'name': 'First Dave', 'email': 'valid_user@test.com'}, {'name': 'Second Dave', 'email': 'valid_user@test.com'}, {'name': 'Third Dave', 'email': 'valid_user@test.com'}], {'name': 'First Dave', 'email': 'valid_user@test.com'})
    ])
    def test_get_user_valid_email(self, user_controller, expected):
        validation_result = user_controller.get_user_by_email(email='valid_user@test.com')
        assert validation_result == expected

    @pytest.mark.parametrize('dao_response, expected', [
        ([{'name': 'First Dave', 'email': 'valid_user@test.com'}, {'name': 'Second Dave', 'email': 'valid_user@test.com'}], 'Error: more than one user found with mail valid_user@test.com\n'),
        ([{'name': 'First Dave', 'email': 'valid_user@test.com'}, {'name': 'Second Dave', 'email': 'valid_user@test.com'}, {'name': 'Third Dave', 'email': 'valid_user@test.com'}], 'Error: more than one user found with mail valid_user@test.com\n')
    ])
    @pytest.mark.testlest
    def test_multiple_users(self, user_controller, expected, capsys):
        user_controller.get_user_by_email(email='valid_user@test.com')
        captured = capsys.readouterr()

        assert captured.out == expected

    @pytest.mark.parametrize('email', [
        ('mail@missingdot'),
        (None)
    ])
    def test_invalid_email(self, email):
        mockedDao = mock.MagicMock(); 
        controller = UserController(dao=mockedDao)
        invalid_email = email
        with pytest.raises(ValueError):
            controller.get_user_by_email(invalid_email)
