from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField, \
    FieldList, validators, Form, FormField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, NumberRange, URL, Regexp
from wtforms.widgets import TextArea


# class LoginForm(FlaskForm):
#     username = StringField(label='Username', validators=[DataRequired()])
#     password = PasswordField(label='Password', validators=[Length(min=2, max=18)])
#     remember = BooleanField(label='Remember Me')
#     submit = SubmitField(label='Submit')


# class DataForm(FlaskForm):
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     age = IntegerField("Age", validators=[InputRequired(), NumberRange(0, 120)])
#     homepage = StringField("Homepage", validators=[DataRequired(), Regexp("https?://.*")])
#     description = TextAreaField('Description', widget=TextArea())
#     language = SelectField(u'Language', choices=[('he', 'Hebrew'), ('en', 'English'), ('fr', 'French')])
#     submit = SubmitField('Compute')
class EdgeItem(FlaskForm):
    validators = [
        DataRequired(),
        NumberRange(min=0, message="Node numbers can only be positive integers!")
    ]
    from_node = IntegerField(validators=validators)
    to_node = IntegerField(validators=validators)


class EnvyFreeMatchingCSVForm(FlaskForm):
    file = FileField(validators=[
        FileRequired(),
        FileAllowed(['csv'], 'CSVs only!')]
    )
    submit = SubmitField(label='submit')


class EnvyFreeMatchingForm(FlaskForm):
    # name = StringField('name', validators=[DataRequired()])
    edges = FieldList(FormField(EdgeItem), min_entries=2)
    submit = SubmitField(label='submit')


class Button(FlaskForm):
    button = SubmitField(label='button')
