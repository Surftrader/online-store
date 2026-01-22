import json
import os
from django.core.management.base import BaseCommand
from products.models import Product, Category
from slugify import slugify


class Command(BaseCommand):
    help = 'Імпортує товари з JSON файлу'

    def add_arguments(self, parser):
        parser.add_argument('json_path', type=str, help='Шлях до JSON файлу')

    def handle(self, *args, **kwargs):
        json_path = kwargs['json_path']
        
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'Файл за адресою {json_path} не знайдено'))
            return
        
        self.stdout.write('Розпочато процес імпорту...')
        
        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if not data:
                self.stdout.write(self.style.WARNING('Дані для імпорту не знайдені у файлі.'))
                return
            
            success_count = 0
            
            for item in data:
                category_name = item.get('category', 'Імпортовані товари')
                category, _ = Category.objects.get_or_create(
                    name=category_name,
                    defaults={'slug':slugify(category_name)}
                )
                
                product, created = Product.objects.get_or_create(
                    title=item.get('title'),
                    category=category,
                    defaults={
                        'slug': slugify(item.get('title')),
                        'description': item.get('description', ''),
                        'price': item.get('price'),
                        'available': True
                    }
                )
                
                if created:
                    success_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Додано: {item.get("title")}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Пропущено (вже існує): {item.get("title")}'))    
                
            self.stdout.write(self.style.SUCCESS(f'Імпорт завершено. Додано {success_count} нових товарів.'))
        
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Помилка. Файл має некоректний формат JSON.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Помилка під час імпорту: {e}'))
