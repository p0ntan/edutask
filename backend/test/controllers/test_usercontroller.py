import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController

@pytest.fixture
def user_controller(dao_response: list=None):
    mockedDao = mock.MagicMock()
    mockedDao.find.return_value = dao_response
    controller = UserController(mockedDao)
    return controller

@pytest.mark.assignment_2
class TestGetUserByEmail:
    # @pytest.mark.parametrize('dao_response, expected', [
    #     ([], None),
    #     ([{'name': 'First Dave', 'email': 'valid_user@test.com'}], [{'name': 'First Dave', 'email': 'valid_user@test.com'}])
    # ])
    # def test_get_user_valid_email(self):
    #     """"""


    @pytest.mark.parametrize('email', [
        ('mail@missingdot'),
        ('missingat.com'),
        ('@missinglocal.com'),
        ('local@.missingdomain'),
        ('local@missinghost.'),
        (None)
    ])
    def test_invalid_email(self, email):
        mockedDao = mock.MagicMock(); 
        controller = UserController(dao=mockedDao)
        invalid_email = email
        with pytest.raises(ValueError):
            controller.get_user_by_email(invalid_email)

