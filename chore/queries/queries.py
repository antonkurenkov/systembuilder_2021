from models.commits_info import DBAssemblyInformation
from database import DBSession


def create_new_commit(session: DBSession, author, commit_message, commit_id, assembly, date):
    new_assembly = DBAssemblyInformation(
        author=author,
        commit_message=commit_message,
        commit_id=commit_id,
        assembly=assembly,
        date=date
    )
    session.add_model(new_assembly)
