from luizalabs_project import app

client = app.test_client()

def test_customer_endpoints():
    response = client.get('/api/customer/all')

    assert response.status_code == 200
    assert 'message' in response.json

    response = client.get('/api/customer/123456')

    assert response.status_code == 200
    assert 'message' in response.json

    response = client.post('/api/customer')

    assert response.status_code == 200
    assert 'message' in response.json

    response = client.put('/api/customer')

    assert response.status_code == 200
    assert 'message' in response.json

    response = client.delete('/api/customer')

    assert response.status_code == 200
    assert 'message' in response.json

def test_products_endpoints():

    response = client.post('/api/favorite')

    assert response.status_code == 200
    assert 'message' in response.json

    response = client.delete('/api/favorite')

    assert response.status_code == 200
    assert 'message' in response.json

    response = client.get('/api/favorites/123456')

    assert response.status_code == 200
    assert 'message' in response.json
