# FastAPI Tutorial

In this repo I worked through the FastAPI tutorial to learn more about the framework. There is also an advanced tutorial with more information available.

[Tutorial](https://fastapi.tiangolo.com/tutorial/)  
[Advanced Tutorial](https://fastapi.tiangolo.com/advanced/)

## General Commands

To start the app run:

```
python3 -m uvicorn src.main:app --reload
```

### Unit Testing

To run the unit tests run: 

```
python3 -m pytest -v -s
```

## Local Documentation

- http://127.0.0.1:8000/documentation
- http://127.0.0.1:8000/redoc (Not enabled)

## API URL

- ~/api/v1/openapi.json

## Notes

FastAPI is a class that inherits directly from Starlette. Starlette is a lightweight ASGI framework. ASGI stands for Asynchronous Server Gateway Interface which is a spiritual successor to WSGI which provided a synchronous interface.

## JWT - JSON Web Token

It is not encrypted, so, anyone could recover the information from the contents. See [https://jwt.io/](https://jwt.io/).

But it's signed. So, when you receive a token that you emitted, you can verify that you actually emitted it.

### Auth Example

In our example John Doe's password is `secret`.

## Project Structure

[Common Project Structures](https://iq-inc.com/importerror-attempted-relative-import/#common-project-structures)


## Dependencies

- `pip3 install -U pytest`
- `pip3 install -U requests`
- `pip3 install -U pytest-mock`