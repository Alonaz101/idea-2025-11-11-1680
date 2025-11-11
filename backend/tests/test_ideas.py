import pytest
from backend.app import app
from flask import json

@pytest.fixture
s
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Sample valid idea data
valid_idea = {
    "title": "New Idea",
    "description": "This is a new idea description.",
    "author": "Tester"
}

# Sample invalid idea data (missing title)
invalid_idea_missing_title = {
    "description": "Missing title field.",
    "author": "Tester"
}

# Test GET /api/ideas - get all ideas
def test_get_all_ideas(client):
    response = client.get('/api/ideas')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

# Test POST /api/ideas - create valid idea
def test_create_idea_valid(client):
    response = client.post('/api/ideas', json=valid_idea)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['title'] == valid_idea['title']

# Test POST /api/ideas - create idea invalid (missing title)
def test_create_idea_invalid_missing_title(client):
    response = client.post('/api/ideas', json=invalid_idea_missing_title)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

# Test GET /api/ideas/<id> - get existing idea
def test_get_idea_by_id(client):
    # First create a new idea
    post_resp = client.post('/api/ideas', json=valid_idea)
    idea_id = json.loads(post_resp.data)['id']
    # Now get it
    get_resp = client.get(f'/api/ideas/{idea_id}')
    assert get_resp.status_code == 200
    data = json.loads(get_resp.data)
    assert data['id'] == idea_id

# Test GET /api/ideas/<id> - get non-existent idea
def test_get_idea_not_found(client):
    response = client.get('/api/ideas/999999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

# Test PUT /api/ideas/<id> - update existing idea valid
def test_update_idea_valid(client):
    post_resp = client.post('/api/ideas', json=valid_idea)
    idea_id = json.loads(post_resp.data)['id']
    update_data = {"title": "Updated Title"}
    put_resp = client.put(f'/api/ideas/{idea_id}', json=update_data)
    assert put_resp.status_code == 200
    data = json.loads(put_resp.data)
    assert data['title'] == "Updated Title"

# Test PUT /api/ideas/<id> - update existing idea invalid (empty payload)
def test_update_idea_invalid(client):
    post_resp = client.post('/api/ideas', json=valid_idea)
    idea_id = json.loads(post_resp.data)['id']
    put_resp = client.put(f'/api/ideas/{idea_id}', json={})
    assert put_resp.status_code == 400
    data = json.loads(put_resp.data)
    assert 'error' in data

# Test PUT /api/ideas/<id> - update non-existent idea
def test_update_idea_not_found(client):
    put_resp = client.put('/api/ideas/999999', json={"title": "Non-existent"})
    assert put_resp.status_code == 404
    data = json.loads(put_resp.data)
    assert 'error' in data

# Test DELETE /api/ideas/<id> - delete existing idea
def test_delete_idea(client):
    post_resp = client.post('/api/ideas', json=valid_idea)
    idea_id = json.loads(post_resp.data)['id']
    del_resp = client.delete(f'/api/ideas/{idea_id}')
    assert del_resp.status_code == 204

# Test DELETE /api/ideas/<id> - delete non-existent idea
def test_delete_idea_not_found(client):
    del_resp = client.delete('/api/ideas/999999')
    assert del_resp.status_code == 404
    data = json.loads(del_resp.data)
    assert 'error' in data

# Validation tests could be added if model validation functions/classes are present in app.py
