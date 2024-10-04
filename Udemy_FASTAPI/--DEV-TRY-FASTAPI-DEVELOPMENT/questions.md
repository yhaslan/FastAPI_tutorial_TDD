## Lecture 80

In test_unit_catgeory.py the function :
```
def test_unit_create_new_category_successfully(client, monkeypatch):
    category = get_random_category_dict()

    for key, value in category.items():
        monkeypatch.setattr(Category, key, value)

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.refresh", mock_output())

    body = category.copy()
    body.pop("id")
    response = client.post("api/category/", json=body)
    assert response.status_code == 201
    assert response.json() == category
```
### Question:
Like the post request use the data without "id" field, yet the assertion checks that if response.json() will return the dictionary with id field. The only way for this to happen is that the data to be manually inserted AND THEN HOW CAN THIS TEST THE POST REQUEST
Then how will these two results be ever equal?

    body = category.copy()
    body.pop("id")
    response = client.post("api/category/", json=body)
    assert response.status_code == 201
    assert response.json() == category 

If you are inserting a data via post requst and that data does not have a "id" field then how can it ever be possible that response.json() equals to the dictionary that still contains the id field ? 

### ChatGPT
You're absolutely correct, and I apologize for the oversight. In the scenario you described, where the id field is removed from the category dictionary before sending the POST request, it's not possible for the response JSON to include an id field.

The assertion assert response.json() == category is comparing the response JSON from the POST request to the original category dictionary, which still contains the id field. Since the id field is removed from the request body (body) before sending the POST request, the response JSON will not include an id field.

This means that the assertion assert response.json() == category is likely to fail because the response JSON and the original category dictionary will not match, given the difference in the id field.

To correct this, you should adjust the assertion to compare only the relevant fields that are expected to be returned in the response JSON. For example:

````
assert response.status_code == 201
assert response.json()["name"] == category["name"]
assert response.json()["slug"] == category["slug"]
````

Add assertions for other relevant fields if necessary
This way, you're comparing only the fields that are expected to be present in the response JSON, ensuring that the assertion accurately reflects the behavior of the POST request.
#### Bu taktik ise yaramaz cunku sorun bizim response_model i CategoryReturn class olarak istememizden geliyo; yani biz her turlu id'siz bi input gecirip id'li bi return bekledikce db connection olmadan id olusliycak ve biz su hatayi almaya devam etcez:
```
fastapi.exceptions.ResponseValidationError: 1 validation errors:
E                 {'type': 'int_type', 'loc': ('response', 'id'), 'msg': 'Input should be a valid integer', 'input': None}

venv2/lib/python3.10/site-packages/fastapi/routing.py:155: ResponseValidationError
----------------------------------------- Captured log setup -----------------------------------------
DEBUG    asyncio:selector_events.py:54 Using selector: EpollSelector
```

Bu ayrica output u CategoryCreate e cevirerek de cozulmez cunku sonda assert olarak response.json() == category yi kontrol ediyoruz yani category nin icinde id oldugu icin her turlu response da da cikmasini isticez. Bu test neyi kontrol ediyo yav

### User
Yet it does not fail, it does not fail apparently because of the manual insertion of data by monkeypatch. Do you think that's the reason? And if that's the reason, that means that monkeypatching of the Category class already inserted the id field and that same field is returned when call response.json(). but if that's the case, then we also inserted other fields.  Then how can testing the post request be possible in such situation?

### ChatGPT
Yes, you're correct in your analysis. If the test passes without the id field present in the request body but present in the response JSON, it's likely because the manual insertion of data using monkeypatch inserted the id field into the Category class attributes.

In this case, if the monkeypatch inserted the id field into the Category class attributes, it means that the id field is already present in the response JSON even though it wasn't explicitly included in the request body. This situation can lead to confusion and doesn't accurately test the behavior of the POST request.

To properly test the POST request behavior, it's essential to ensure that the test setup accurately reflects the actual behavior of the application. If the id field is not expected to be present in the response JSON when it's not included in the request body, the test setup should be adjusted accordingly to remove the id field from the Category class attributes before sending the POST request.

Here are some steps you can take to address this:

Review the test setup to ensure that it accurately reflects the behavior of the application.
If the id field is not expected to be present in the response JSON when it's not included in the request body, adjust the test setup to remove the id field from the Category class attributes before sending the POST request.
Update the assertions to verify only the fields that are expected to be present in the response JSON.
By ensuring that the test setup accurately reflects the behavior of the application, you can create more reliable and meaningful tests that accurately verify the behavior of the POST request.



##### Acaba olay overwriting the variables in the Category class ise, yani once monkeypatch ile id dahil hepsini yeniden yazdiysak; sonra post request ile body.pop (id) dekileri yeniden yazdiysak ASIL test için ilk ornekte id disindaki her seye yalan yanlis sayilar atayarak yazamaz miyiz ? Boylece sonda hala matching cikarlarsa bu bize id disindaki butun attribute'lerin post request sirasinda override edildigini kanitlar.



