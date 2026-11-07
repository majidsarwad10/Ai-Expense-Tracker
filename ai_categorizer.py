"""Transparent keyword-based expense category suggestions.

This is a lightweight baseline, not a trained machine-learning model.
Users can override every suggestion in the expense form.
"""

CATEGORY_KEYWORDS = {
    "Food": {"restaurant", "lunch", "dinner", "breakfast", "grocery", "groceries", "cafe", "coffee", "pizza"},
    "Transport": {"uber", "taxi", "fuel", "petrol", "bus", "train", "metro", "parking"},
    "Shopping": {"clothes", "shirt", "shoes", "amazon", "shopping", "electronics"},
    "Bills": {"electricity", "water", "internet", "phone", "mobile", "recharge", "rent"},
    "Health": {"doctor", "medicine", "pharmacy", "hospital", "clinic"},
    "Entertainment": {"movie", "cinema", "netflix", "music", "game", "concert"},
    "Education": {"book", "course", "tuition", "school", "college", "exam"},
}


def suggest_category(description: str) -> str:
    """Suggest a category based on words in the description."""
    words = set(description.lower().replace("-", " ").replace("/", " ").split())
    for category, keywords in CATEGORY_KEYWORDS.items():
        if words & keywords:
            return category
    return "Other"
