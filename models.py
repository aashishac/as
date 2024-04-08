class Product:
    def __init__(self, id, pName, available, pCode, author, price, category, picture):
        self.id = id
        self.pName = pName
        self.available = available
        self.pCode = pCode
        self.author = author
        self.price = price
        self.category = category
        self.picture = picture

class OrderForm(FlaskForm):
    name = StringField('name')
    quantity = IntegerField('Quantity')
    submit = SubmitField('Submit')  # Added SubmitField


# Define User model
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'


