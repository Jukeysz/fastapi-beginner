from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def html_must_be_correct():
    client = TestClient(app)

    response = client.get("/")
    assert response.text == """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>"""

    assert response.status_code == HTTPStatus.OK
