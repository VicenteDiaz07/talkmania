from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


class Command(createsuperuser.Command):
    help = 'Crea un superusuario con rol de administrador'

    def handle(self, *args, **options):
        # Llamar al comando original de createsuperuser
        super().handle(*args, **options)
        
        # Obtener el usuario recién creado por su username
        username = options.get('username')
        if username:
            from usuarios.models import User
            try:
                user = User.objects.get(username=username)
                # Cambiar el rol a administrador
                user.rol = 'administrador'
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Superusuario "{username}" creado con rol: Administrador')
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING('⚠️ No se pudo actualizar el rol automáticamente')
                )
