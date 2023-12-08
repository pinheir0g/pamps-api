import typer
from rich.console import Console
from rich.table import Table  # Adiciona layouts nas saídas do terminal
from sqlmodel import Session, select

from .config import settings
from .db import engine
from .models import User, Social, Post, Like, SQLModel


main = typer.Typer(name="Pamps CLI")

@main.command()
def shell():
    """Opens interactive Shell"""
    _vars = {
        "settings": settings,
        "engine": engine,
        "select": select,
        "session": Session(engine),
        "User": User,
        "Post": Post,
        "Social": Social,
        "Like": Like

    }
    typer.echo(f"Auto imports: {list(_vars.keys())}")
    try:
        from IPython import start_ipython

        start_ipython(
            argv=["--ipython-dir=/tmp", "--no-banner"], user_ns=_vars
        )
    except ImportError:
        import code
        code.InteractiveConsole(_vars).interact()   # Cria terminal interativo

@main.command()
def user_list():
    """Lists all Users"""
    table = Table(title="Pamps users")
    fields = ["username", "email"]
    for header in fields:
        table.add_column(header, style="magenta")

    with Session(engine) as session:
        users = session.exec(select(User))  # Query SQL no banco de dados
        for user in users:
            table.add_row(user.username, user.email)

    Console().print(table)


@main.command()
def create_user(email: str, username: str, password: str):
    """Create user"""
    with Session(engine) as session:
        user = User(email=email, username=username, password=password)
        session.add(user)
        session.commit()
        session.refresh(user)
        typer.echo(f"created {username} user")
        return user
    
@main.command()
def reset_db(
    force: bool = typer.Option(
        False, "--force", "-f", help="Run with no confirmation"
    )
):
    """Resets the database tables"""
    force = force or typer.confirm("Are you sure?")
    if force:
        SQLModel.metadata.drop_all(engine)
