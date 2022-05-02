# fastapi tutorial

[Source](https://fastapi.tiangolo.com/tutorial/)

## Commands

```
python3 -m uvicorn main:app --reload
```

## Local Documentation

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Notes

FastAPI is a class that inherits directly from Starlette. Starlette is a lightweight ASGI framework. ASGI stands for Asynchronous Server Gateway Interface which is a spiritual successor to WSGI which provided a synchronous interface.

## JWT - JSON Web Token

It is not encrypted, so, anyone could recover the information from the contents. See [https://jwt.io/](https://jwt.io/).

But it's signed. So, when you receive a token that you emitted, you can verify that you actually emitted it.