from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Regexp


class EnvyFreeMatchingCSVAndTextForm(FlaskForm):
    file = FileField(label="* Edges CSV File", validators=[
        FileAllowed(['csv'], 'CSVs only!')]
                     )
    top_nodes = TextAreaField(label='* Top Nodes', validators=[
        Regexp("^((([0-9])+,)*)(([0-9])+)$", message="Bad Top Nodes input")
    ])
    submit = SubmitField(label='submit')


class EnvyFreeMatchingListAndTextForm(FlaskForm):
    top_nodes = TextAreaField(label='Top Nodes (Inferred automatically if input is empty)')
    submit = SubmitField(label='submit')
