from app import app,db
from app.models import Hotel


@app.shell_context_processor
def make_shell_context():
    return {'hotel': Hotel,"db":db}