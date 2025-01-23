# from unittest.mock import AsyncMock, MagicMock
#
#
# from core.models import User
# from tests.fixtures import test_client
# import faker
# from core.database.session_manager import get_async_session
#
# fake = faker.Faker(locale="en_US")
# # Test: Fetch all users
# # def test_read_users(mock_db_session):
# #     # Mock the database response
# #     mock_db_session.return_value.query.return_value.all.return_value = [
# #         {"username": "user1", "email": "user1@example.com"}]
# #
# #     response = test_client.get("api/v1/users?skip=0&limit=10")
# #     print("Im here",response.url, response)
# #
# #     assert response.status_code == 200
# #     assert len(response.json()) == 1
# #     assert response.json()[0]["username"] == "user1"
# #     assert response.json()[0]["email"] == "user1@example.com"
#
#
# # Test: Check if a username is available
#
#
# def test_check_username_availability():
#     # Simulate a non-existing username
#     mock_result = MagicMock()
#     mock_result.scalars.return_value.first.return_value = None
#     session_mock = AsyncMock()
#     session_mock.execute.return_value = mock_result
#     test_client.app.dependency_overrides[get_async_session] = lambda: session_mock
#     response = test_client.get("/users/check-username/availableusername")
#
#     assert response.status_code == 200
#     assert response.json() == {"message": "Username is available"}
#
#     del mock_result
#     del session_mock
#     del test_client.app.dependency_overrides[get_async_session]
#
#     # Simulate an existing username
#     mock_result = MagicMock()
#     mock_result.scalars.return_value.first.return_value = User(
#         username=fake.user_name(), email=fake.email(), name=fake.name()
#     )
#     session_mock = AsyncMock()
#     session_mock.execute.return_value = mock_result
#     test_client.app.dependency_overrides[get_async_session] = lambda: session_mock
#     response = test_client.get("/users/check-username/takenusername")
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Username already taken"}
#
#     del mock_result
#     del session_mock
#     del test_client.app.dependency_overrides[get_async_session]
#
#
# #
# # # Test: Delete a users account
# # def test_delete_account(mock_db_session):
# #     # Mock the database response
# #     mock_db_session.return_value.query.return_value.filter.return_value.first.return_value = {"username": "user1",
# #                                                                                               "email": "user1@example.com"}
# #     mock_db_session.return_value.delete.return_value = None  # Simulate successful deletion
# #
# #     response = test_client.delete("/users/delete/user1")
# #
# #     assert response.status_code == 200
# #     assert response.json()["username"] == "user1"
# #
# #     # Test users not found case
# #     mock_db_session.return_value.query.return_value.filter.return_value.first.return_value = None
# #
# #     response = test_client.delete("/users/delete/nonexistentuser")
# #
# #     assert response.status_code == 404
# #     assert response.json() == {"detail": "User not found"}
# #
# #
# # # Test: Create a new users
# # def test_create_new_user(mock_db_session):
# #     user_data = UserCreate(username="newuser", email="newuser@example.com", password="password")
# #
# #     # Mock the database responses for existing users checks
# #     mock_db_session.return_value.query.return_value.filter.return_value.first.return_value = None  # No existing users
# #
# #     # Mock users creation
# #     mock_db_session.return_value.add.return_value = None
# #
# #     response = test_client.post("/users", json=user_data.dict())
# #
# #     assert response.status_code == 200
# #     assert response.json()["username"] == "newuser"
# #     assert response.json()["email"] == "newuser@example.com"
# #
# #     # Test email already registered
# #     mock_db_session.return_value.query.return_value.filter.return_value.first.return_value = {
# #         "email": "existinguser@example.com"}
# #
# #     response = test_client.post("/users", json=user_data.dict())
# #
# #     assert response.status_code == 400
# #     assert response.json() == {"detail": "Email already registered"}
# #
# #     # Test username already taken
# #     mock_db_session.return_value.query.return_value.filter.return_value.first.return_value = {
# #         "username": "existinguser"}
# #
# #     response = test_client.post("/users", json=user_data.dict())
# #
# #     assert response.status_code == 400
# #     assert response.json() == {"detail": "Username already taken"}
# #
# #
# # # Test: Fetch a specific users by username
# # def test_read_user(mock_db_session):
# #     # Mock the database response
# #     mock_db_session.return_value.query.return_value.filter.return_value.first.return_value = {"username": "user1",
# #                                                                                               "email": "user1@example.com"}
# #
# #     response = test_client.get("/users/user1")
# #
# #     assert response.status_code == 200
# #     assert response.json()["username"] == "user1"
# #     assert response.json()["email"] == "user1@example.com"
# #
# #     # Test users not found case
# #     mock_db_session.return_value.query.return_value.filter.return_value.first.return_value = None
# #
# #     response = test_client.get("/users/nonexistentuser")
# #
# #     assert response.status_code == 404
# #     assert response.json() == {"detail": "User not found"}
# #
# #
# # # Test: Update an existing users
# # def test_update_existing_user(mock_db_session):
# #     user_data = UserUpdate(username="newusername", email="newuser@example.com")
# #
# #     # Mock the database response
# #     mock_db_session.return_value.query.return_value.filter.return_value.first.return_value = {"username": "user1",
# #                                                                                               "email": "user1@example.com"}
# #
# #     response = test_client.put("/users/user1", json=user_data.dict())
# #
# #     assert response.status_code == 200
# #     assert response.json()["username"] == "newusername"
# #     assert response.json()["email"] == "newuser@example.com"
# #
# #     # Test users not found case
# #     mock_db_session.return_value.query.return_value.filter.return_value.first.return_value = None
# #
# #     response = test_client.put("/users/nonexistentuser", json=user_data.dict())
# #
# #     assert response.status_code == 404
# #     assert response.json() == {"detail": "User not found"}
# #
# #
# # # Test: Delete a users by username
# # def test_delete_existing_user(mock_db_session):
# #     # Mock the database response
# #     mock_db_session.return_value.query.return_value.filter.return_value.first.return_value = {"username": "user1",
# #                                                                                               "email": "user1@example.com"}
# #
# #     response = test_client.delete("/users/user1")
# #
# #     assert response.status_code == 200
# #     assert response.json()["username"] == "user1"
# #
# #     # Test users not found case
# #     mock_db_session.return_value.query.return_value.filter.return_value.first.return_value = None
# #
# #     response = test_client.delete("/users/nonexistentuser")
# #
# #     assert response.status_code == 404
# #     assert response.json() == {"detail": "User not found"}
