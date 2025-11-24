## Solución: Cambiar rol de usuario a Administrador

El problema es que tu usuario `admin1` tiene `rol='cliente'` en la base de datos, pero debería tener `rol='administrador'`.

### Opción 1: Usar el script Python (Recomendado)

1. Abre el archivo [`cambiar_rol_admin.py`](file:///c:/Users/vicen/OneDrive/Escritorio/talkmania/cambiar_rol_admin.py)
2. Cambia `username = 'admin1'` por tu nombre de usuario si es diferente
3. Ejecuta:
```bash
python manage.py shell < cambiar_rol_admin.py
```

### Opción 2: Desde el shell de Django

```bash
python manage.py shell
```

Luego ejecuta:
```python
from usuarios.models import User
user = User.objects.get(username='admin1')
user.rol = 'administrador'
user.save()
print(f'Usuario actualizado: {user.get_rol_display()}')
exit()
```

### Opción 3: Desde el Admin de Django

1. Ve a `http://localhost:8000/admin/`
2. Inicia sesión como superusuario
3. Ve a "Usuarios" → "Users"
4. Busca tu usuario `admin1`
5. Cambia el campo "Rol" de "Cliente" a "Administrador"
6. Guarda

### Verificación

Después de cambiar el rol, cierra sesión y vuelve a iniciar sesión. Deberías ver:
- ✅ Dashboard muestra "Administrador"
- ✅ Botón "🏨 Crear Hotel" visible en navbar
- ✅ Botón "Crear Hotel" en acciones rápidas del dashboard

### Valores correctos del rol

Según [`usuarios/models.py`](file:///c:/Users/vicen/OneDrive/Escritorio/talkmania/usuarios/models.py#L6-L10):
- `'cliente'` → Cliente
- `'administrador'` → Administrador ✅ (este es el correcto)
- `'staff'` → Staff
