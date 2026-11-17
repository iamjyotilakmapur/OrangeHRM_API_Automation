from settings import BASE_URL
import requests
import allure


#GET
@allure.title("Get Employee Directory")
def test_get_employee_directory(api_client):
    url = f"{BASE_URL}/api/v2/directory/employees"

    response = api_client.get(url)

    assert response.status_code == 200
    assert "data" in response.json()
    assert response.json()["meta"]["total"] > 0
    assert response.json()["data"][0]["empNumber"] is not None
    assert isinstance(response.json()["data"][0]["empNumber"], int)
    assert isinstance(response.json()["data"][0]["firstName"], str)


#The employee directory API should return a list in the data field.
@allure.title("Verify Employee Data Is a List")
def test_employee_data_is_list(api_client):
    url = f"{BASE_URL}/api/v2/directory/employees"

    response = api_client.get(url)

    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)

#dictonary for specific employee id
@allure.title("Get Employee by ID")
def test_get_employee_by_id(api_client):

    with allure.step("Get employee directory"):
        directory_url = f"{BASE_URL}/api/v2/directory/employees"
        directory_response = api_client.get(directory_url)

    with allure.step("Get a valid employee ID"):
        assert directory_response.status_code == 200
        emp_number = directory_response.json()["data"][0]["empNumber"]

    with allure.step("Get employee details by ID"):
        url = f"{BASE_URL}/api/v2/pim/employees/{emp_number}"
        response = api_client.get(url)

    with allure.step("Verify employee details"):
        assert response.status_code == 200
        assert response.json()["data"]["empNumber"] == emp_number

#test an employee id that doesnt exists
@allure.title("Get Employee by Invalid ID")
def test_get_employee_by_not_found(api_client):

    emp_number = 9999
    url = f"{BASE_URL}/api/v2/pim/employees/{emp_number}"

    response = api_client.get(url)

    assert response.status_code == 422
    assert response.json()["error"]["message"] == "Invalid Parameter"

#Test API with an invalid token
@allure.title("Verify Invalid Token Handling")
def test_invalid_token():
    url = f"{BASE_URL}/api/v2/pim/employees"

    token = "invalid token"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers, allow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"] == f"{BASE_URL}/auth/login"

@allure.title("Get Employee Directory with Limit")
def test_get_employee_directory_with_limit(api_client):

    url = f"{BASE_URL}/api/v2/directory/employees"

    params = {
        "limit": 5
    }

    response = api_client.get(url, params=params)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 5

    assert response.json()["meta"]["total"] >= 5


@allure.title("Get Employee Directory with Limit and Offset")
def test_get_employee_directory_with_limit_and_offset(api_client):
    url = f"{BASE_URL}/api/v2/directory/employees"

    params = {
        "limit": 5,
        "offset": 5
    }

    response = api_client.get(url, params=params)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 5

    first_page_params = {"limit": 5}
    first_page_response = api_client.get(url, params=first_page_params)

    second_page_params = {"limit": 5, "offset": 5}
    second_page_response = api_client.get(url, params=second_page_params)

    assert first_page_response.status_code == 200
    assert second_page_response.status_code == 200

    first_page_emp = first_page_response.json()["data"][0]["empNumber"]
    second_page_emp = second_page_response.json()["data"][0]["empNumber"]

    assert first_page_emp != second_page_emp

#POST - create employee
@allure.title("Create Employee")
def test_create_employee(api_client):
    url = f"{BASE_URL}/api/v2/pim/employees"

    payload = {
        "firstName": "API",
        "lastName": "TestEmployee"
    }

    response = api_client.post(url, json=payload)

    assert response.status_code == 200
    assert "data" in response.json()
    assert response.json()["data"]["empNumber"] is not None
    assert response.json()["data"]["firstName"] == payload["firstName"]
    assert response.json()["data"]["lastName"] == payload["lastName"]

    emp_number = response.json()["data"]["empNumber"]

    get_url = f"{BASE_URL}/api/v2/pim/employees/{emp_number}"

    get_response = api_client.get(get_url)

    assert get_response.status_code == 200
    assert get_response.json()["data"]["empNumber"] == emp_number
    assert get_response.json()["data"]["firstName"] == payload["firstName"]
    assert get_response.json()["data"]["lastName"] == payload["lastName"]

@allure.title("Create Employee Without Last Name")
def test_create_employee_without_last_name(api_client):
    url = f"{BASE_URL}/api/v2/pim/employees"

    payload = {
        "firstName": "API"
    }

    response = api_client.post(url, json=payload)

    assert response.status_code == 422
    assert response.json()["error"]["message"] == "Invalid Parameter"
    assert "lastName" in response.json()["error"]["data"]["invalidParamKeys"]

@allure.title("Create Employee Without First Name")
def test_create_employee_without_first_name(api_client):
    url = f"{BASE_URL}/api/v2/pim/employees"

    payload = {
        "lastName": "TestEmployee"
    }

    response = api_client.post(url, json=payload)

    assert response.status_code == 422
    assert response.json()["error"]["message"] == "Invalid Parameter"
    assert "firstName" in response.json()["error"]["data"]["invalidParamKeys"]

#test create candidate
@allure.title("Create Candidate")
def test_create_candidate(api_client):

    with allure.step("Send POST request to create candidate"):
        url = f"{BASE_URL}/api/v2/recruitment/candidates"

        payload = {
            "firstName": "API",
            "lastName": "Candidate",
            "email": "api.candidate.test@example.com"
        }

        response = api_client.post(url, json=payload)

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify candidate is created successfully"):
        assert "data" in response.json()
        assert response.json()["data"]["id"] is not None

    with allure.step("Verify candidate details"):
        assert response.json()["data"]["firstName"] == payload["firstName"]
        assert response.json()["data"]["lastName"] == payload["lastName"]
        assert response.json()["data"]["email"] == payload["email"]

#test get
@allure.title("Get Candidate")
def test_get_candidate(api_client, candidate_id):

    with allure.step("Send GET request for candidate"):
        url = f"{BASE_URL}/api/v2/recruitment/candidates/{candidate_id}"
        response = api_client.get(url)

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify candidate ID"):
        assert response.json()["data"]["id"] == candidate_id

    with allure.step("Verify candidate details"):
        assert response.json()["data"]["firstName"] == "API"
        assert response.json()["data"]["lastName"] == "TestCandidate"
        assert response.json()["data"]["email"] == "api.testcandidate@example.com"

@allure.title("Update Candidate")
def test_update_candidate(api_client, candidate_id):

    with allure.step("Send PUT request to update candidate"):
        url = f"{BASE_URL}/api/v2/recruitment/candidates/{candidate_id}"

        payload = {
            "firstName": "API",
            "lastName": "UpdatedCandidate",
            "email": "api.updatedcandidate@example.com"
        }

        response = api_client.put(url, json=payload)

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify candidate ID"):
        assert response.json()["data"]["id"] == candidate_id

    with allure.step("Verify updated candidate details"):
        assert response.json()["data"]["firstName"] == payload["firstName"]
        assert response.json()["data"]["lastName"] == payload["lastName"]
        assert response.json()["data"]["email"] == payload["email"]

@allure.title("Delete Candidate")
def test_delete_candidate(api_client, candidate_id):

    with allure.step("Send DELETE request to delete candidate"):
        url = f"{BASE_URL}/api/v2/recruitment/candidates"
        payload = {"ids": [candidate_id]}

        response = api_client.delete(url, json=payload)

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify candidate is deleted successfully"):
        assert str(candidate_id) in response.json()["data"]

# end-to-end CRUD test using one candidate ID
#Step1: Create a mew candidate id
@allure.title("Candidate CRUD End-to-End Flow")
def test_candidate_crud_flow(api_client):

    with allure.step("Create candidate"):
        url = f"{BASE_URL}/api/v2/recruitment/candidates"
        payload = {
            "firstName": "API",
            "lastName": "CRUDCandidate",
            "email": "api.crudcandidate@example.com"
        }

        response = api_client.post(url, json=payload)

        assert response.status_code == 200
        candidate_id = response.json()["data"]["id"]

    with allure.step("Get candidate"):
        get_url = f"{BASE_URL}/api/v2/recruitment/candidates/{candidate_id}"
        get_response = api_client.get(get_url)

        assert get_response.status_code == 200
        assert get_response.json()["data"]["id"] == candidate_id

    with allure.step("Update candidate"):
        update_payload = {
            "firstName": "API",
            "lastName": "UpdatedCRUDCandidate",
            "email": "api.updatedcrud@example.com"
        }

        update_response = api_client.put(
            get_url,
            json=update_payload
        )

        assert update_response.status_code == 200
        assert update_response.json()["data"]["id"] == candidate_id

    with allure.step("Verify updated candidate"):
        get_updated_response = api_client.get(get_url)

        assert get_updated_response.status_code == 200
        assert get_updated_response.json()["data"]["firstName"] == update_payload["firstName"]
        assert get_updated_response.json()["data"]["lastName"] == update_payload["lastName"]
        assert get_updated_response.json()["data"]["email"] == update_payload["email"]

    with allure.step("Delete candidate"):
        delete_url = f"{BASE_URL}/api/v2/recruitment/candidates"
        delete_response = api_client.delete(
            delete_url,
            json={"ids": [candidate_id]}
        )

        assert delete_response.status_code == 200
        assert str(candidate_id) in delete_response.json()["data"]

    with allure.step("Verify candidate is deleted"):
        deleted_response = api_client.get(get_url)

        assert deleted_response.status_code == 404
        assert deleted_response.json()["error"]["message"] == "Record Not Found"