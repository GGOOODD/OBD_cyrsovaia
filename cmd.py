import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import UserModel
from sqlalchemy import select, delete

engine = create_engine("sqlite:///./site.db")
new_session = sessionmaker(engine, expire_on_commit=False)


@click.command()
@click.argument('user_id', type=int)
@click.option('--admin-status', is_flag=True, help='Set admin status to True if present.')
def update_admin_status(user_id: int, admin_status: bool):
    """
    Change admin status of user <USER_ID> to <ADMIN_STATUS>.
    """
    with new_session() as session:
        query = select(UserModel).filter_by(id=user_id)
        result = session.execute(query)
        user_field = result.scalars().first()
        if user_field is None:
            click.echo('user not found.')
            return
        user_field.admin = admin_status
        session.commit()
        click.echo(f'id={user_field.id}    admin_status={user_field.admin}')

if __name__ == '__main__':
    update_admin_status()
