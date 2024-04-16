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
    @pytest.mark.parametrize('dao_response, expected', [([], None)])
    def test_no_user_valid_email(self, user_controller, expected):
        validation_result = user_controller.get_user_by_email(email='valid_user@test.com')

        assert validation_result == expected

    @pytest.mark.parametrize('dao_response, expected', [
        ([{'name': 'First User'}], {'name': 'First User'}),
        ([{'name': 'First User'}, {'name': 'Second User'}], {'name': 'First User'}),
        ([{'name': 'First User'}, {'name': 'Second User'}, {'name': 'Third User'}], {'name': 'First User'})
    ])
    def test_get_user_valid_email(self, user_controller, expected):
        validation_result = user_controller.get_user_by_email(email='valid_user@test.com')

        assert validation_result == expected

    @pytest.mark.parametrize('dao_response, email', [
        ([{'name': 'First User'}, {'name': 'Second User'}], 'valid_user@test.com'),
        ([{'name': 'First User'}, {'name': 'Second User'}, {'name': 'Third User'}], 'valid_user@test.com')
    ])
    def test_multiple_users_warning_message(self, user_controller, email, capsys):
        user_controller.get_user_by_email(email)
        captured = capsys.readouterr()

        assert email in captured.out

    @pytest.mark.parametrize('email', [
        ('mail@missingdot'),
        (None)
    ])
    def test_invalid_email(self, email):
        mockedDao = mock.MagicMock()
        controller = UserController(dao=mockedDao)
        invalid_email = email

        with pytest.raises(ValueError):
            controller.get_user_by_email(invalid_email)

    def test_database_operation_failure(self):
        mockedDao = mock.MagicMock()
        mockedDao.find.side_effect = Exception('Database failure')
        controller = UserController(dao=mockedDao)

        with pytest.raises(Exception):
            controller.get_user_by_email(email="valid_user@test.com")
