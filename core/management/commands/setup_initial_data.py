from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from core.models import Lanchonete
import os

class Command(BaseCommand):
    help = 'Setup initial data for the application'

    def handle(self, *args, **options):
        self.stdout.write('Verificando conectividade do banco de dados...')
        
        try:
            # Testar conexão com o banco
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result:
                    self.stdout.write(self.style.SUCCESS('✓ Banco de dados conectado com sucesso!'))
                else:
                    self.stdout.write(self.style.ERROR('✗ Falha na conexão com o banco de dados'))
                    return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Erro de conexão com o banco: {e}'))
            return

        # Criar superusuário se não existir
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        
        if not User.objects.filter(username=username).exists():
            try:
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Superusuário "{username}" criado com sucesso!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Erro ao criar superusuário: {e}'))
        else:
            self.stdout.write(f'✓ Superusuário "{username}" já existe.')

        # Criar lanchonete padrão se não existir
        if not Lanchonete.objects.exists():
            try:
                lanchonete = Lanchonete.objects.create(
                    nome='Yummi Delivery',
                    endereco='Rua Principal, 123',
                    telefone='(11) 99999-9999',
                    email='contato@yummi.com',
                    horario_funcionamento='08:00 - 22:00',
                    dias_funcionamento='Segunda a Domingo'
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Lanchonete padrão "{lanchonete.nome}" criada com sucesso!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Erro ao criar lanchonete padrão: {e}'))
        else:
            self.stdout.write('✓ Lanchonete já existe.')

        self.stdout.write(self.style.SUCCESS('Setup inicial concluído com sucesso!'))