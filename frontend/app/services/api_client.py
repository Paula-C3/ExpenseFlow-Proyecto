import requests
import streamlit as st

BASE_URL = "http://backend:8000"  

def _headers():
    return {
        "Authorization": f"Bearer {st.session_state['token']}"
    }

def login(email, password):
    res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    return res

def get_requests():
    res = requests.get(f"{BASE_URL}/requests", headers=_headers())
    return res

def get_request_detail(request_id):
    res = requests.get(f"{BASE_URL}/requests/{request_id}", headers=_headers())
    return res

def create_request(data):
    res = requests.post(f"{BASE_URL}/requests", json=data, headers=_headers())
    return res