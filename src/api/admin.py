import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import PasswordField, SelectField  # Importación añadida
from wtforms.validators import DataRequired, Email, Optional, EqualTo
from werkzeug.security import generate_password_hash
from .models import db, User, TourPlan, Provider, Client, Reservation, Favorite_tour_plan

# =====================================
# Vista Personalizada para Usuarios
# =====================================
class UserAdminView(ModelView):
    column_list = ['username', 'email', 'role', 'status', 'phone', 'created_at']
    column_filters = ['role', 'status']
    column_searchable_list = ['username', 'email']
    column_sortable_list = ['created_at', 'username']
    
    # Añadir 'password' y 'confirm' a form_columns
    form_columns = ['username', 'email', 'role', 'status', 'phone', 'password', 'confirm']
    
    form_excluded_columns = ['password_hash', 'created_at', 'providers', 'clients']
    form_overrides = {
        'status': SelectField,
        'role': SelectField
    }
    
    form_args = {
        'username': {'validators': [DataRequired("Campo obligatorio")]},
        'email': {'validators': [DataRequired(), Email("Formato inválido")]},
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
            raise ValueError("Contraseña requerida para nuevos usuarios")
        
        if is_created:
            if model.role == 'provider':
                db.session.add(Provider(user=model))
            elif model.role == 'client':
                db.session.add(Client(user=model))
            db.session.commit()

# =====================================
# Vista Personalizada para Tours
# =====================================
class TourPlanAdminView(ModelView):
    column_list = ['title', 'provider', 'price', 'start_date', 'available_spots']
    column_filters = ['provider', 'price']
    column_searchable_list = ['title', 'description']
    
    form_args = {
        'title': {'validators': [DataRequired()]},
        'price': {'validators': [DataRequired()]},
        'available_spots': {'validators': [DataRequired()]}
    }

# =====================================
# Vista Personalizada para Reservaciones
# =====================================
class ReservationAdminView(ModelView):
    column_list = ['client', 'tour_plan', 'status', 'reservation_date']
    form_choices = {
        'status': [
            ('active', 'Activa'),
            ('cancelled', 'Cancelada'),
            ('completed', 'Completada')
        ]
    }

# =====================================
# Configuración del Panel Administrativo
# =====================================
def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'dev-key')
    
    admin = Admin(app, name='Panel Administrativo', template_mode='bootstrap3')
    
    # Vistas principales
    admin.add_view(UserAdminView(User, db.session, name='Usuarios'))
    admin.add_view(TourPlanAdminView(TourPlan, db.session, name='Tours'))
    admin.add_view(ReservationAdminView(Reservation, db.session, name='Reservas'))
    
    # Vistas adicionales
    admin.add_view(ModelView(Provider, db.session, name='Proveedores'))
    admin.add_view(ModelView(Client, db.session, name='Clientes'))
    admin.add_view(ModelView(Favorite_tour_plan, db.session, name='Favoritos'))