def test_tasks_list_response_401(anon_client):
    anon_client.headers.update({'Authorization': 'Bearer Wtf'})
    response = anon_client.get('/api/v1/todo/tasks')
    assert response.status_code == 401


def test_tasks_list_response_200(auth_client):
    response = auth_client.get('/api/v1/todo/tasks')
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_tasks_detail_response_200(auth_client, random_task):
    task_obj = random_task
    response = auth_client.get(f'/api/v1/todo/tasks/{task_obj.id}')
    assert response.status_code == 200


def test_tasks_detail_response_404(auth_client):
    response = auth_client.get('/api/v1/todo/tasks/10000')
    assert response.status_code == 404
