#!/usr/bin/env python3
# ============================================================
# SHEBANG - указывает, что скрипт выполняется через Python 3
# Позволяет запускать скрипт напрямую: ./send_telegram_notification.py
# ============================================================

# ============================================================
# ИМПОРТ НЕОБХОДИМЫХ МОДУЛЕЙ
# ============================================================
import os  # Модуль для работы с переменными окружения и системными функциями
import sys  # Модуль для работы с системными функциями (exit, stderr, stdout)
import argparse  # Модуль для парсинга аргументов командной строки
import requests  # Модуль для отправки HTTP запросов к Telegram Bot API


# ============================================================
# ФУНКЦИЯ ОТПРАВКИ СООБЩЕНИЯ В TELEGRAM
# ============================================================
def send_telegram_message(bot_token, chat_id, message):
    """
    Отправляет сообщение в Telegram через Bot API.

    Args:
        bot_token (str): Токен бота, полученный от @BotFather
        chat_id (str): ID чата или группы, куда отправляется сообщение
        message (str): Текст сообщения с HTML форматированием

    Returns:
        bool: True если отправка успешна, False при ошибке
    """

    # Формируем URL для Telegram Bot API метода sendMessage
    # Формат: https://api.telegram.org/bot{TOKEN}/sendMessage
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    # ============================================================
    # ПОДГОТОВКА ДАННЫХ ДЛЯ POST ЗАПРОСА
    # ============================================================

    # Словарь с параметрами для отправки сообщения
    data = {
        'chat_id': chat_id,  # ID чата получателя
        'text': message,  # Текст сообщения
        'parse_mode': 'HTML',  # Режим парсинга (HTML разметка для форматирования)
        'disable_web_page_preview': False  # Разрешаем превью ссылок в сообщении
    }

    # ============================================================
    # ОТПРАВКА HTTP POST ЗАПРОСА К TELEGRAM API
    # ============================================================

    # Блок try-except для обработки возможных сетевых ошибок
    try:
        # Отправляем POST запрос к Telegram API
        # data - параметры запроса (будут отправлены в теле запроса)
        # timeout=30 - максимальное время ожидания ответа (30 секунд)
        # Если сервер не ответит за 30 сек, возникнет исключение Timeout
        response = requests.post(url, data=data, timeout=30)

        # ============================================================
        # ОБРАБОТКА ОТВЕТА ОТ TELEGRAM API
        # ============================================================

        # Проверяем HTTP статус код ответа
        # 200 - успешная отправка сообщения
        if response.status_code == 200:
            print("Telegram notification sent successfully")
            return True
        else:
            # При неуспешной отправке выводим детальную информацию об ошибке
            print(f"Failed to send Telegram notification")
            print(f"HTTP Status: {response.status_code}")  # HTTP код ошибки
            print(f"Response: {response.text}")  # Тело ответа с описанием ошибки
            return False

    # Обрабатываем исключения, связанные с сетевыми запросами
    # RequestException - базовый класс для всех исключений requests
    # Включает: Timeout, ConnectionError, HTTPError и др.
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram notification: {e}")
        return False


# ============================================================
# ФУНКЦИЯ ФОРМАТИРОВАНИЯ СООБЩЕНИЯ С HTML РАЗМЕТКОЙ
# ============================================================
def format_message(total, passed, failed, success_rate, duration=None,
                   report_url=None, branch=None, commit_sha=None,
                   commit_msg=None, pipeline_status=None, pipeline_url=None):
    """
    Создает форматированное HTML сообщение для Telegram с результатами тестов.

    Args:
        total (int): Общее количество тестов
        passed (int): Количество пройденных тестов
        failed (int): Количество упавших тестов
        success_rate (float): Процент успешности
        duration (str, optional): Длительность выполнения
        report_url (str, optional): Ссылка на Allure отчет
        branch (str, optional): Название git ветки
        commit_sha (str, optional): SHA коммита
        commit_msg (str, optional): Сообщение коммита
        pipeline_status (str, optional): Статус pipeline (success/failed)
        pipeline_url (str, optional): Ссылка на pipeline

    Returns:
        str: Отформатированное HTML сообщение
    """

    # ============================================================
    # ОПРЕДЕЛЕНИЕ EMOJI СТАТУСА НА ОСНОВЕ РЕЗУЛЬТАТОВ
    # ============================================================

    # Выбираем emoji в зависимости от результатов тестов
    # ✅ - если все тесты прошли успешно
    # ❌ - если есть упавшие тесты или других проблем
    if pipeline_status == "success" or (failed == 0 and total > 0):
        status_emoji = "✅"
    else:
        status_emoji = "❌"

    # ============================================================
    # ФОРМИРОВАНИЕ ЗАГОЛОВКА СООБЩЕНИЯ
    # ============================================================

    # Начинаем формировать сообщение с emoji и заголовка
    # <b> - HTML тег для жирного текста в Telegram
    message = f"{status_emoji} <b>Результаты прогона тестов"

    # Если указана ветка, добавляем ее в заголовок
    if branch:
        message += f" на ветке {branch}"

    # Закрываем тег <b> и добавляем два переноса строки
    message += "</b>\n\n"

    # ============================================================
    # БЛОК СТАТИСТИКИ ТЕСТОВ
    # ============================================================

    # Добавляем секцию с результатами
    # 📊 - emoji для визуального выделения статистики
    message += f"📊 <b>Результаты:</b>\n"
    # • - маркер списка для каждого пункта статистики
    message += f"• Успешных: <b>{passed}</b>\n"
    message += f"• Упавших: <b>{failed}</b>\n"
    message += f"• Всего: <b>{total}</b>\n\n"

    # ============================================================
    # ПРОЦЕНТ УСПЕШНОСТИ
    # ============================================================

    # 📈 - emoji для метрики процента успеха
    message += f"📈 <b>Процент успеха:</b> {success_rate}%\n"

    # ============================================================
    # ДЛИТЕЛЬНОСТЬ ВЫПОЛНЕНИЯ (ОПЦИОНАЛЬНО)
    # ============================================================

    # Если передана длительность, добавляем её в сообщение
    if duration:
        # ⏱️ - emoji часов для длительности
        message += f"⏱️ <b>Длительность:</b> {duration}\n"

    # ============================================================
    # ИНФОРМАЦИЯ О КОММИТЕ (ОПЦИОНАЛЬНО)
    # ============================================================

    # Если есть информация о коммите, добавляем блок с деталями
    if commit_sha and commit_msg:
        # Обрезаем длинное сообщение коммита для компактности
        # Если сообщение > 100 символов, обрезаем до 97 и добавляем "..."
        if len(commit_msg) > 100:
            commit_msg = commit_msg[:97] + "..."

        # 📝 - emoji для информации о коммите
        # <code> - HTML тег для моноширинного шрифта (как в терминале)
        message += f"\n📝 <b>Коммит:</b> <code>{commit_sha}</code>\n"
        message += f"{commit_msg}\n"

    # ============================================================
    # ССЫЛКА НА ALLURE ОТЧЕТ (ОПЦИОНАЛЬНО)
    # ============================================================

    # Если указан URL отчета, добавляем кликабельную ссылку
    if report_url:
        # 🔗 - emoji для ссылки
        # <a href='URL'>Текст</a> - HTML тег для гиперссылки в Telegram
        message += f"\n🔗 <a href='{report_url}'>Открыть Allure отчет</a>"

    # ============================================================
    # ССЫЛКА НА PIPELINE (ОПЦИОНАЛЬНО)
    # ============================================================

    # Если указан URL pipeline, добавляем ссылку на него
    if pipeline_url:
        message += f"\n🔗 <a href='{pipeline_url}'>Открыть пайплайн</a>"

    # Возвращаем полностью сформированное сообщение
    return message


# ============================================================
# ГЛАВНАЯ ФУНКЦИЯ - ТОЧКА ВХОДА В ПРОГРАММУ
# ============================================================
def main():
    """
    Главная функция, которая координирует работу скрипта:
    1. Парсит аргументы командной строки
    2. Получает credentials из переменных окружения
    3. Формирует сообщение
    4. Отправляет уведомление в Telegram
    """

    # ============================================================
    # СОЗДАНИЕ ПАРСЕРА АРГУМЕНТОВ КОМАНДНОЙ СТРОКИ
    # ============================================================

    # ArgumentParser для обработки CLI аргументов
    parser = argparse.ArgumentParser(
        description='Send CI/CD test results notification to Telegram'
    )

    # ============================================================
    # ОБЯЗАТЕЛЬНЫЕ АРГУМЕНТЫ (required=True)
    # ============================================================

    # Эти аргументы должны быть переданы обязательно, иначе скрипт завершится с ошибкой

    parser.add_argument('--total', type=int, required=True,
                        help='Total number of tests')
    parser.add_argument('--passed', type=int, required=True,
                        help='Number of passed tests')
    parser.add_argument('--failed', type=int, required=True,
                        help='Number of failed tests')
    parser.add_argument('--success-rate', type=float, required=True,
                        help='Success rate percentage')

    # ============================================================
    # ОПЦИОНАЛЬНЫЕ АРГУМЕНТЫ (required не указан = False по умолчанию)
    # ============================================================

    # Эти аргументы могут быть переданы, но не обязательны

    parser.add_argument('--duration',
                        help='Test execution duration')
    parser.add_argument('--report-url',
                        help='Allure report URL')
    parser.add_argument('--branch',
                        help='Git branch name')
    parser.add_argument('--commit-sha',
                        help='Git commit SHA')
    parser.add_argument('--commit-msg',
                        help='Git commit message')
    parser.add_argument('--pipeline-status',
                        help='Pipeline status (success/failed)')
    parser.add_argument('--pipeline-url',
                        help='Pipeline url')

    # Парсим все переданные аргументы
    args = parser.parse_args()

    # ============================================================
    # ПОЛУЧЕНИЕ CREDENTIALS ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ
    # ============================================================

    # os.getenv() получает значение переменной окружения
    # Токен бота - секретный ключ для доступа к Telegram Bot API
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    # ID чата - уникальный идентификатор чата/группы для отправки уведомлений
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    # ============================================================
    # ВАЛИДАЦИЯ ОБЯЗАТЕЛЬНЫХ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ
    # ============================================================

    # Проверяем наличие токена бота
    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is required")
        # Выходим с кодом ошибки 1
        sys.exit(1)

    # Проверяем наличие ID чата
    if not chat_id:
        print("Error: TELEGRAM_CHAT_ID environment variable is required")
        sys.exit(1)

    # ============================================================
    # ПОЛУЧЕНИЕ ДОПОЛНИТЕЛЬНОЙ ИНФОРМАЦИИ
    # ============================================================

    # Используем значение из аргументов или fallback на переменные окружения GitLab
    # Оператор 'or' вернет первое истинное значение (не None, не пустая строка)

    # Название ветки: из аргумента или из CI_COMMIT_REF_NAME, или 'unknown'
    branch = args.branch or os.getenv('CI_COMMIT_REF_NAME', 'unknown')
    # Короткий SHA коммита: из аргумента или из CI_COMMIT_SHORT_SHA, или 'unknown'
    commit_sha = args.commit_sha or os.getenv('CI_COMMIT_SHORT_SHA', 'unknown')
    # Сообщение коммита: из аргумента или из CI_COMMIT_MESSAGE, или 'No commit message'
    commit_msg = args.commit_msg or os.getenv('CI_COMMIT_MESSAGE', 'No commit message')
    # Статус pipeline: из аргумента или из CI_JOB_STATUS, или 'unknown'
    pipeline_status = args.pipeline_status or os.getenv('CI_JOB_STATUS', 'unknown')
    # URL pipeline: из аргумента или из CI_PIPELINE_URL, или 'unknown'
    pipeline_url = args.pipeline_url or os.getenv('CI_PIPELINE_URL', 'unknown')

    # ============================================================
    # ВЫВОД ИНФОРМАЦИИ О ПОДГОТОВКЕ УВЕДОМЛЕНИЯ (ДЛЯ ЛОГОВ)
    # ============================================================

    print("Preparing Telegram notification...")
    print(f"Branch: {branch}")
    print(f"Tests: {args.passed}/{args.total} passed ({args.success_rate}%)")
    # Если передана длительность, выводим её
    if args.duration:
        print(f"Duration: {args.duration}")

    # ============================================================
    # ФОРМИРОВАНИЕ СООБЩЕНИЯ
    # ============================================================

    # Вызываем функцию format_message со всеми собранными параметрами
    message = format_message(
        total=args.total,
        passed=args.passed,
        failed=args.failed,
        success_rate=args.success_rate,
        duration=args.duration,
        report_url=args.report_url,
        branch=branch,
        commit_sha=commit_sha,
        commit_msg=commit_msg,
        pipeline_status=pipeline_status,
        pipeline_url=pipeline_url
    )

    # ============================================================
    # ОТПРАВКА УВЕДОМЛЕНИЯ
    # ============================================================

    print("Sending notification to Telegram...")

    # Вызываем функцию отправки сообщения
    if send_telegram_message(bot_token, chat_id, message):
        # Успешная отправка
        print("Notification sent successfully!")
        # Выходим с кодом успеха 0
        sys.exit(0)
    else:
        # Неудачная отправка, но не критично для pipeline
        # Выводим предупреждение, но завершаем с кодом 0, чтобы не упал pipeline
        print("⚠️  Failed to send notification, but pipeline will continue")
        sys.exit(0)  # Код 0 позволяет pipeline продолжить работу


# ============================================================
# ТОЧКА ВХОДА СКРИПТА
# ============================================================

# Стандартная Python конструкция для определения точки входа
# Код выполняется только при прямом запуске скрипта
# Не выполнится, если скрипт импортирован как модуль
if __name__ == '__main__':
    main()