from wtforms import Field, SelectField
from pprint import pprint

def BooleanSelectFieldHelper(ControlLabel,TrueLabel,FalseLabel):
    return SelectField(ControlLabel,
        choices=[('', 'N/A'),
                 ('true', TrueLabel),
                 ('false', FalseLabel)]
    )


def get_common_fields(wtform,db_model):
    # Get list of WTForm attributes in the form
    # These are the 'StringField/IntegerField/etc' members of the class
    form_fields = set([x for x in vars(wtform) if isinstance(getattr(wtform,x),Field)])
    #pprint(form_fields)

    # Get list of python attributes from the db.Model object.
    # These are the the 'db.Columns' members defined in the model sub-class.
    db_model_fields = db_model.__table__.columns.keys()
    #pprint(db_model_fields)

    # Only keep those with names matching the form's attribute,
    copy_fields = set([x for x in db_model_fields if x in form_fields])
    #pprint(copy_fields)

    return copy_fields



def convert_to_db_type(x):
    if x is None:
        return None
    if isinstance(x,bool):
        return x
    if isinstance(x,str):
        if x.strip() == '':
            return None
    return x

def copy_wtform_to_db_model(wtform,db_model):
    fields = get_common_fields(wtform,db_model)
    for attr_name in fields:
        src = getattr(wtform,attr_name)
        dst = getattr(db_model,attr_name)
        #print("type of db_model.", attr_name," = ", str(type(dst)))
        #print("type of wtform.", attr_name," = ", str(type(src.data)))
        setattr(db_model,attr_name, convert_to_db_type(src.data))



def copy_db_model_to_wtform(wtform,db_model):
    fields = get_common_fields(wtform,db_model)
    for attr_name in fields:
        src = getattr(db_model,attr_name)
        dst = getattr(wtform,attr_name)
        dst.data = src
