from ai_categorizer import suggest_category


def test_food_category():
    assert suggest_category("Lunch at cafe") == "Food"


def test_transport_category():
    assert suggest_category("Uber ride") == "Transport"


def test_unknown_category():
    assert suggest_category("Something unusual") == "Other"


def test_case_insensitive():
    assert suggest_category("COFFEE") == "Food"
