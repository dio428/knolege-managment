import click
from app import create_app, db
from app.models import User

app = create_app()

@app.cli.command("create-admin")
@click.argument("username")
@click.argument("password")
def create_admin(username, password):
    """Creates a new admin user."""
    if User.query.filter_by(username=username).first():
        print("User already exists.")
        return
    user = User(username=username, is_admin=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    print(f"Admin user {username} created successfully.")

if __name__ == "__main__":
    app.run(debug=True)
