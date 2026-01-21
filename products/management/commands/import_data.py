from django.core.management.base import BaseCommand
from django.db import connections
from products.models import Product, Category
from slugify import slugify


class Command(BaseCommand):
    help = 'Імпортує товари з з зовнішньої бази даних PostgreSQL'

    def handle(self, *args, **kwargs):
        self.stdout.write('Розпочато процес підключення...')
        
        try:
            with connections['external_db'].cursor() as cursor:
                cursor.execute("SELECT item_name, cost, info FROM old_items WHERE is_active = TRUE")
                rows = cursor.fetchall()
            
            if not rows:
                self.stdout.write(self.style.WARNING('Дані для імпорту не знайдені.'))
                return

            category, _ = Category.objects.get_or_create(
                name='Імпортовані товари',
                slug='imported-products'
            )
            
            success_count = 0
            
            for row in rows:
                item_name, cost, info = row
                
                product, created = Product.objects.get_or_create(
                    title=item_name,
                    category=category,
                    defaults={
                        'slug': slugify(item_name),
                        'description': info or '',
                        'price': cost,
                        'available': True
                    }
                )
                
                if created:
                    success_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Додано: {item_name}'))
                
            self.stdout.write(self.style.SUCCESS(f'Імпорт завершено. Додано {success_count} товарів.'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Помилка під час імпорту: {e}'))
            