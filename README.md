# 🏨 Talkmania - Sistema de Gestión Hotelera

Sistema de reservas y gestión de hoteles desarrollado con Django.

## 🚀 Características

- ✅ Gestión de hoteles y habitaciones
- ✅ Sistema de reservas
- ✅ Autenticación de usuarios (clientes y administradores)
- ✅ Recuperación de contraseña por email
- ✅ Sistema de reseñas
- ✅ Códigos QR para verificación de reservas
- ✅ Panel de administración
- ✅ Diseño moderno y responsivo

## 📋 Requisitos Previos

- Python 3.8 o superior
- MySQL 5.7 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/talkmania.git
cd talkmania
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y configura tus variables:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edita el archivo `.env` con tus configuraciones:

```env
# Django Secret Key
SECRET_KEY=tu-clave-secreta-aqui

# Database Configuration
DB_NAME=talkmania_db
DB_USER=root
DB_PASSWORD=tu-contraseña-mysql
DB_HOST=localhost
DB_PORT=3306

# Email Configuration (Gmail)
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
DEFAULT_FROM_EMAIL=Talkmania <tu-email@gmail.com>

# Debug Mode
DEBUG=True
```

> **Nota para Gmail**: Necesitas generar una "Contraseña de aplicación" en tu cuenta de Google:
> 1. Ve a tu cuenta de Google → Seguridad
> 2. Activa la verificación en 2 pasos
> 3. Genera una contraseña de aplicación
> 4. Usa esa contraseña en `EMAIL_HOST_PASSWORD`

### 5. Crear base de datos

Crea la base de datos en MySQL:

```sql
CREATE DATABASE talkmania_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Ejecutar migraciones

```bash
python manage.py migrate
```

### 7. Crear superusuario

```bash
python manage.py createsuperuser
```

> El comando personalizado automáticamente asignará el rol de "administrador" al superusuario.

### 8. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

Abre tu navegador en: `http://127.0.0.1:8000`

## 👥 Roles de Usuario

- **Cliente**: Puede buscar hoteles, hacer reservas y dejar reseñas
- **Administrador**: Puede gestionar hoteles, habitaciones y ver todas las reservas
- **Staff**: Puede verificar códigos QR de reservas

## 📁 Estructura del Proyecto

```
talkmania/
├── Talkmania/          # Configuración del proyecto
├── talkmaniaApp/       # App principal (hoteles, reservas)
├── usuarios/           # App de autenticación y usuarios
├── templates/          # Templates HTML
├── static/            # Archivos estáticos (CSS, JS, imágenes)
├── .env.example       # Plantilla de variables de entorno
├── requirements.txt   # Dependencias del proyecto
└── manage.py         # Script de gestión de Django
```

## 🛠️ Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic

# Ejecutar tests
python manage.py test
```

## 🎨 Tecnologías Utilizadas

- **Backend**: Django 5.0
- **Base de Datos**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Autenticación**: Django Auth
- **Email**: SMTP (Gmail)
- **QR Codes**: qrcode + Pillow

## 📧 Configuración de Email

El sistema envía emails para:
- Confirmación de reservas
- Recuperación de contraseña

Asegúrate de configurar correctamente las variables de email en el archivo `.env`.

## 🔒 Seguridad

- Las contraseñas se almacenan hasheadas
- CSRF protection habilitado
- Variables sensibles en archivo `.env` (no incluido en el repositorio)
- Validación de permisos por rol de usuario

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Vicente Díaz

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Si tienes alguna pregunta o problema, por favor abre un issue en el repositorio.
