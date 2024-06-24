import os

from django.core.management.base import BaseCommand
from django.conf import settings
from bulletin_board_app.tasks import send_email_for_all


class Command(BaseCommand):
    help = 'Аргументом команды является название html файла по пути bulletin_board_app/templates/'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = False  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('template_name', type=str)

    def handle(self, *args, **options):
        file_is_exist = os.path.isfile(
            os.path.join(
                settings.BASE_DIR, 'bulletin_board_app/templates/' + options["template_name"] + '.html'
            )
        )
        if file_is_exist:
            answer = input(
                f'Вы правда хотите отправить всем пользователям письмо'
                f' по шаблону "{options["template_name"]}"? yes/no: '
            )
            if answer == 'yes':
                send_email_for_all.apply_async([options['template_name']])
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Рассылка писем по шаблону "{options["template_name"]}" запущена.'
                    )
                )
                return
            else:
                self.stdout.write(self.style.ERROR('Отменено'))
        else:
            self.stdout.write(self.style.ERROR(f'Шаблона "{options["template_name"]}" не существует.'))
