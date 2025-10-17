from app import db
from app.models import PaymentMethod
from werkzeug.exceptions import BadRequest, NotFound, Conflict

class PaymentMethodService:
    """Servicio para gestionar métodos de pago"""
    
    @staticmethod
    def create_payment_method(name, description=None, is_active=True):
        """
        Crea un nuevo método de pago
        """
        # Validar que no exista el nombre
        existing = PaymentMethod.query.filter_by(name=name).first()
        if existing:
            raise Conflict(f"El método de pago '{name}' ya existe")
        
        payment_method = PaymentMethod(
            name=name,
            description=description,
            is_active=is_active
        )
        
        db.session.add(payment_method)
        db.session.commit()
        
        return payment_method
    
    @staticmethod
    def get_payment_method_by_id(payment_method_id):
        """
        Obtiene un método de pago por ID
        """
        payment_method = PaymentMethod.query.get(payment_method_id)
        if not payment_method:
            raise NotFound(f"Método de pago {payment_method_id} no encontrado")
        return payment_method
    
    @staticmethod
    def get_all_payment_methods(only_active=False):
        """
        Obtiene todos los métodos de pago
        """
        query = PaymentMethod.query
        
        if only_active:
            query = query.filter_by(is_active=True)
        
        return query.all()
    
    @staticmethod
    def update_payment_method(payment_method_id, **kwargs):
        """
        Actualiza un método de pago
        """
        payment_method = PaymentMethodService.get_payment_method_by_id(payment_method_id)
        
        allowed_fields = ['name', 'description', 'is_active']
        
        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                # Validar nombre único si se está actualizando
                if field == 'name':
                    existing = PaymentMethod.query.filter_by(name=value).first()
                    if existing and existing.id != payment_method_id:
                        raise Conflict(f"El nombre '{value}' ya está en uso")
                
                setattr(payment_method, field, value)
        
        db.session.commit()
        return payment_method
    
    @staticmethod
    def delete_payment_method(payment_method_id):
        """
        Elimina un método de pago
        """
        payment_method = PaymentMethodService.get_payment_method_by_id(payment_method_id)
        
        try:
            db.session.delete(payment_method)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise BadRequest(f"Error al eliminar método de pago: {str(e)}")
    
    @staticmethod
    def activate_payment_method(payment_method_id):
        """
        Activa un método de pago
        """
        payment_method = PaymentMethodService.get_payment_method_by_id(payment_method_id)
        payment_method.is_active = True
        db.session.commit()
        return payment_method
    
    @staticmethod
    def deactivate_payment_method(payment_method_id):
        """
        Desactiva un método de pago
        """
        payment_method = PaymentMethodService.get_payment_method_by_id(payment_method_id)
        payment_method.is_active = False
        db.session.commit()
        return payment_method