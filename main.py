from datetime import date, timedelta

class Article:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def add_quantity(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        self.quantity += amount

    def remove_quantity(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if amount > self.quantity:
            raise ValueError(f"Nicht genug {self.name} vorhanden (nur {self.quantity} {self.unit}).")
        
        self.quantity -= amount
        return True

    def to_dict(self):
        return {
            "type": "article",
            "name": self.name,
            "quantity": self.quantity,
            "unit": self.unit
        }

class Food(Article):
    def __init__(self, name, quantity, unit, expiration_date):
        super().__init__(name, quantity, unit)
        self.expiration_date = date.fromisoformat(expiration_date)

    def is_expired(self):
        return self.days_until_expiry() < 0

    def days_until_expiry(self):
        delta = self.expiration_date - date.today()
        return delta.days

    def to_dict(self):
        return super().to_dict() | {"type": "food", "expiration_date": self.expiration_date.isoformat()}

    def __str__(self):
        text = super().__str__()
        return f"{text}, expires on {self.expiration_date.strftime('%d.%m.%Y')}"

class Basement:
    def __init__(self):
        self.articles = {}

    def add_article(self, article):
        key = article.name.lower()
        if key in self.articles:
            self.articles[key].add_quantity(article.quantity)
        else:
            self.articles[key] = article

    def find_article(self, name):
        key = name.lower()
        if key not in self.articles:
            raise ValueError(f"Article {name} is not in the basement")
        return self.articles.get(name.lower())

    def remove_article(self, name):
        key  = name.lower()
        if key in self.articles:
            del self.articles[key]
            return True
        raise ValueError(f"Article {name} is not in the basement")

    def get_expiring_soon(self, days):
        expiring = {}
        for article in self.articles.values():
            if isinstance(article, Food) and article.days_until_expiry() <= days:
                expiring[article.name] = article
        return expiring

    def __str__(self):
        if not self.articles:
            return "Keller ist leer."
        
        lines = []
        for article in self.articles.values():
            lines.append(str(article))
        return "\n".join(lines)







article1 = Article("Waschmittel", 1, "Tabs (60 Stück)")
article2 = Article("Waschmittel", 1, "Tabs (60 Stück)")
food1 = Food("Milch", 1, "Liter", "2026-09-29")

basement = Basement()
basement.add_article(article1)
basement.add_article(food1)

basement.add_article(article2)

expiring = basement.get_expiring_soon(5)

print(expiring)

if not expiring:
    print("Nichts läuft in den nächsten 7 Tagen ab.")
else:
    print("Läuft bald ab:")
    for article in expiring.values():
        print(f"- {article}")

print(food1.to_dict())

