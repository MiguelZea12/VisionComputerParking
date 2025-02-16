from marshmallow import Schema, fields, validate

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    cedula = fields.Str(required=True, validate=validate.Length(min=5, max=20))
    nombre = fields.Str(required=True)
    apellido = fields.Str(required=True)
    telefono = fields.Str()
    direccion = fields.Str()
    fecha_nacimiento = fields.Date()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user = fields.Nested('UserSchema', only=('username', 'email'), dump_only=True)