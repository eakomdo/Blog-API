from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class Registration(FlaskForm):
    class Meta:
        csrf = False  
        
    first_name = StringField(validators=[DataRequired(), Length(min=6, max=100)])
    last_name = StringField(validators=[DataRequired(), Length(min=6, max=100)])
    username = StringField(validators=[DataRequired(), Length(min=6, max=100)])
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')])

    
class Login(FlaskForm):
    class Meta:
        csrf = False 
        
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    
    

class UpdateAccount(FlaskForm):
    class Meta:
        csrf = False  
        
    first_name = StringField(validators=[DataRequired(), Length(min=6, max=100)])
    last_name = StringField(validators=[DataRequired(), Length(min=6, max=100)])
    username = StringField(validators=[DataRequired(), Length(min=6, max=100)])
    email = StringField(validators=[DataRequired(), Email()])
