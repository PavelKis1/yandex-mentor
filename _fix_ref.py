import re

path = 'scripts/ref_check.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
functions = []
in_func = False
ref_lines = []

# Логика: собираем функции и словарь раздельно
# ВАЖНО: знаем, что новые функции начинались с 'def parse_url_params'
# и были внутри REF.

# Простой подход: пересобрать файл заново.
# У меня есть все функции в истории диалога.

# Соберу файл заново, гарантируя корректность.
print("Fixing ref_check.py structure...")
# ... (код пересборки)
