def test_tasks_list_response_401(anon_client):
    response = anon_client.post('/api/v1/todo/tasks')
    assert response.status_code == 403
