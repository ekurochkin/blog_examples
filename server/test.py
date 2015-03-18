# coding: utf8
import requests as _rest

URI = "http://localhost:9005/api/user"


def test_1_post():
    payload = {"name": "Barac", "l_name": "Obama", "permalink": 1}
    r = _rest.post(URI, json=payload, headers={"Content-Type": "application/json"})
    assert r.status_code == 200 


def test_2_get():
    r = _rest.get(URI, params={"permalink": 1})
    assert r.status_code == 200


def test_3_patch():
    r = _rest.patch(URI, data={"m_name": "Vladimirovich"})
    assert r.status_code == 200


def test_4_delete():
    r = _rest.delete(URI, params={"permalink": 1})
    assert r.status_code == 200
