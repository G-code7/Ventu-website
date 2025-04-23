import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Optional, EqualTo
from werkzeug.security import generate_password_hash
from .models import db, User, TourPlan, Provider, Client, Reservation, FavoriteTourPlan

class UserAdminView(ModelView):
    column_list = ['username', 'email', 'role', 'status', 'phone', 'created_at']
    column_filters = ['role', 'status']
    column_searchable_list = ['username', 'email']
    column_sortable_list = ['created_at', 'username']
    
    form_columns = ['username', 'email', 'role', 'status', 'phone', 'password', 'confirm']
    form_excluded_columns = ['password_hash', 'created_at', 'providers', 'clients']
    
    form_overrides = {
        'status': SelectField,
        'role': SelectField
    }
    
    form_args = {
        'username': {'validators': [DataRequired("Nombre de usuario requerido")]},
        'email': {'validators': [DataRequired(), Email("Formato de email inválido")]},
        'role': {
            'choices': [('provider', 'Proveedor'), ('client', 'Cliente')],
            'validators': [DataRequired()]
        },
        'status': {
            'choices': [('active', 'Activo'), ('inactive', 'Inactivo')]
        }
    }
    
    form_extra_fields = {
        'password': PasswordField('Contraseña', validators=[
            Optional(),
            EqualTo('confirm', message='Las contraseñas deben coincidir')
        ]),
        'confirm': PasswordField('Confirmar Contraseña')
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password_hash = generate_password_hash(form.password.data)
        elif is_created:
            raise ValueError("La contraseña es obligatoria para nuevos usuarios")
        
        if is_created:
            try:
                if model.role == 'provider':
                    db.session.add(Provider(user=model))
                elif model.role == 'client':
                    db.session.add(Client(user=model))
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise ValueError(f"Error creando relación: {str(e)}")

class TourPlanAdminView(ModelView):
    column_list = ['title', 'provider', 'price', 'start_date', 'available_spots']
    column_filters = ['price', 'available_spots']
    column_searchable_list = ['title', 'description']
    list_template = 'admin/list.html'
    
    form_args = {
        'title': {'validators': [DataRequired()]},
        'price': {'validators': [DataRequired()]},
        'available_spots': {'validators': [DataRequired()]}
    }
    
    def after_model_change(self, form, model, is_created):
        if is_created:
            return self.redirect('/admin/tourplanview/')

class ReservationAdminView(ModelView):
    column_list = ['client', 'tour_plan', 'status', 'reservation_date']
    form_choices = {
        'status': [
            ('active', 'Activa'),
            ('cancelled', 'Cancelada'),
            ('completed', 'Completada')
        ]
    }

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'clave-secreta-por-defecto')
    
    admin = Admin(
        app, 
        name='Panel Administrativo',
        template_mode='bootstrap3',
        url='/admin',
        endpoint='admin'
    )
    
    admin.add_view(UserAdminView(User, db.session, name='Usuarios', endpoint='users'))
    admin.add_view(TourPlanAdminView(TourPlan, db.session, name='Tours', endpoint='tourplans'))
    admin.add_view(ReservationAdminView(Reservation, db.session, name='Reservas', endpoint='reservations'))
    
    admin.add_view(ModelView(Provider, db.session, name='Proveedores', category='Relaciones'))
    admin.add_view(ModelView(Client, db.session, name='Clientes', category='Relaciones'))
    admin.add_view(ModelView(FavoriteTourPlan , db.session, name='Favoritos', category='Relaciones'))