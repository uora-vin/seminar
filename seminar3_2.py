import re

def parse_log_line(line):
    r"""
    line (str) — одна строка лога.
    tuple(str, str, str) — (время, уровень, сообщение),
    None — если строка не подходит под шаблон

    Регулярное выражение: r"(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+(\w+)\s+(.*)"

    (\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}) — дата и время;
    \s+                                    — пробелы-разделители;
    (\w+)                                  — уровень лога;
    \s+                                    — пробелы после уровня;
    (.*)                                   — текст сообщения.
    """

    pattern = r"(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+(\w+)\s+(.*)"
    match = re.match(pattern, line)
    if match:
        time_stamp = match.group(1)
        level = match.group(2)
        message = match.group(3)
        return time_stamp, level, message
    return None


def filter_by_level(lines, levels):
    """
    lines (list[str])             — список строк лога.
    levels (set[str] | list[str]) — набор уровней {"ERROR", "WARN"}).
    list[tuple(str, str, str)] — список (время, уровень, сообщение)
    """

    result = []
    for line in lines:
        parsed = parse_log_line(line)
        if parsed is None:
            continue
        time_stamp, level, message = parsed
        if level in levels:
            result.append((time_stamp, level, message))
    return result


def filter_by_ip(lines):
    r"""
    lines (list[str]) — список строк лога.
    list[tuple(str, str, str)] — список (время, уровень, сообщение), в которых найден IP-адрес.

    Регулярное выражение для IP-адреса:  r"(?:\d{1,3}\.){3}\d{1,3}"
    \d{1,3}  — от 1 до 3 цифр (одна часть адреса);
    \.       — точка-разделитель
    """

    ip_pattern =  r"(?:\d{1,3}\.){3}\d{1,3}"
    result = []
    for line in lines:
        parsed = parse_log_line(line)
        if parsed is None:
            continue
        time_stamp, level, message = parsed
        if re.search(ip_pattern, message):
            result.append((time_stamp, level, message))
    return result


def print_results(title, results):
    """
    title (str) — заголовок для вывода.
    results (list[tuple]) — список (время, уровень, сообщение).
    """
    if not results:
        print("Ничего не найдено.")
        return
    for time_stamp, level, message in results:
        print(f"{time_stamp} {level:<6} {message}")



filename = "тест.txt"
try:
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"Ошибка: файл '{filename}' не найден.")

# Задача 1: строки с уровнем ERROR или WARN(WARNING)
error_warn_lines = filter_by_level(lines, {"ERROR", "WARN", "WARNING"})
print_results("Строки с уровнем ERROR или WARN", error_warn_lines)

# Задача 2: строки, где упоминается IP-адрес
ip_lines = filter_by_ip(lines)
print_results("Строки с упоминанием IP-адреса", ip_lines)
