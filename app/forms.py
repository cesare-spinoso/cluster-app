from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired

# For the random cluster form
class RandomClusterForm(FlaskForm):
    numpoints = IntegerField('Number of points to cluster (>= 30): ',
                             validators=[DataRequired(),
                                         NumberRange(min=30, message='Please pick a number >= 30.')])
    numclusters = IntegerField('Number of clusters (2 to 4): ',
                               validators=[DataRequired(),
                                           NumberRange(min=2, max=4, message='Please enter a number between 2 and 4.')])
    maxiter = IntegerField('Maximum number of iterations (5 to 9): ',
                           validators=[DataRequired(),
                                       NumberRange(min=5, max=9, message='Please enter a number between 5 and 9.')])
    submit = SubmitField('Cluster!')

# To cluster again
class CustomClusterForm(FlaskForm):
    numclusters = IntegerField('Number of clusters (2 to 4): ',
                               validators=[DataRequired(),
                                           NumberRange(min=2, max=4, message='Please enter a number between 2 and 4.')])
    maxiter = IntegerField('Maximum number of iterations (5 to 9): ',
                           validators=[DataRequired(),
                                       NumberRange(min=5, max=9, message='Please enter a number between 5 and 9.')])
    submit = SubmitField('Cluster!')