def add_sample(client, **overrides):
    data = {
        "title": "Lunch at cafe",
        "amount": "250.50",
        "category": "",
        "expense_date": "2026-10-01",
        "notes": "Team lunch",
    }
    data.update(overrides)
    return client.post("/expenses", data=data, follow_redirects=True)


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Track your spending" in response.data


def test_add_expense_and_suggest_category(client):
    response = add_sample(client)
    assert response.status_code == 200
    assert b"Lunch at cafe" in response.data
    assert b"Food" in response.data


def test_reject_invalid_amount(client):
    response = add_sample(client, amount="-20")

    assert response.status_code == 200
    assert b"valid positive amount" in response.data
    assert b"No expenses yet" in response.data

def test_edit_expense(client):
    add_sample(client)
    response = client.post("/expenses/1/edit", data={
        "title": "Updated lunch",
        "amount": "300",
        "category": "Food",
        "expense_date": "2026-10-02",
        "notes": "",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Updated lunch" in response.data
def test_delete_expense(client):
    add_sample(client)

    response = client.post(
        "/expenses/1/delete",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"No expenses yet" in response.data
    assert b"Team lunch" not in response.data

def test_csv_export(client):
    add_sample(client)
    response = client.get("/export")
    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert b"Lunch at cafe" in response.data


def test_dashboard_loads(client):
    add_sample(client)
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert b"Your spending dashboard" in response.data
