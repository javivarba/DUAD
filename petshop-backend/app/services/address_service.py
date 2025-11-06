from app import db
from app.models import Address
from werkzeug.exceptions import BadRequest, NotFound

class AddressService:
    """Servicio para gestionar direcciones"""
    
    @staticmethod
    def create_address(user_id, full_name, phone, address_line1, city, state, 
                      postal_code, address_line2=None, country='Costa Rica', is_default=False):
        """
        Crea una nueva dirección para un usuario
        """
        # Si se marca como default, quitar default de las otras
        if is_default:
            Address.query.filter_by(user_id=user_id, is_default=True).update({'is_default': False})
        
        address = Address(
            user_id=user_id,
            full_name=full_name,
            phone=phone,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            is_default=is_default
        )
        
        db.session.add(address)
        db.session.commit()
        
        return address
    
    @staticmethod
    def get_address_by_id(address_id):
        """
        Obtiene una dirección por ID
        """
        address = Address.query.get(address_id)
        if not address:
            raise NotFound(f"Dirección {address_id} no encontrada")
        return address
    
    @staticmethod
    def get_addresses_by_user(user_id):
        """
        Obtiene todas las direcciones de un usuario
        """
        return Address.query.filter_by(user_id=user_id).order_by(Address.is_default.desc()).all()
    
    @staticmethod
    def get_default_address(user_id):
        """
        Obtiene la dirección por defecto de un usuario
        """
        address = Address.query.filter_by(user_id=user_id, is_default=True).first()
        if not address:
            raise NotFound("No hay dirección por defecto configurada")
        return address
    
    @staticmethod
    def update_address(address_id, **kwargs):
        """
        Actualiza una dirección
        """
        address = AddressService.get_address_by_id(address_id)
        
        # Campos permitidos
        allowed_fields = [
            'full_name', 'phone', 'address_line1', 'address_line2',
            'city', 'state', 'postal_code', 'country', 'is_default'
        ]
        
        # Si se marca como default, quitar default de las otras del mismo usuario
        if kwargs.get('is_default') is True:
            Address.query.filter_by(
                user_id=address.user_id, 
                is_default=True
            ).update({'is_default': False})
        
        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                setattr(address, field, value)
        
        db.session.commit()
        return address
    
    @staticmethod
    def delete_address(address_id):
        """
        Elimina una dirección
        """
        address = AddressService.get_address_by_id(address_id)
        
        db.session.delete(address)
        db.session.commit()
        
        return True
    
    @staticmethod
    def set_default_address(address_id, user_id):
        """
        Establece una dirección como la predeterminada
        """
        address = AddressService.get_address_by_id(address_id)
        
        # Verificar que la dirección pertenece al usuario
        if address.user_id != user_id:
            raise BadRequest("La dirección no pertenece al usuario")
        
        # Quitar default de las otras
        Address.query.filter_by(user_id=user_id, is_default=True).update({'is_default': False})
        
        # Marcar esta como default
        address.is_default = True
        db.session.commit()
        
        return address