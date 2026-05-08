import urllib.request
import urllib.error
import json
import os
import sys
import re
import ssl

# Вирішуємо проблему з сертифікатами на macOS (M4)
ssl._create_default_https_context = ssl._create_unverified_context


def get_figma_node(url, token):
    # АВТОМАТИЧНА КОРЕКЦІЯ ПОСИЛАННЯ:
    # Якщо посилання містить /site/, ми замінюємо його на /design/
    if '/site/' in url:
        url = url.replace('/site/', '/design/')
        print(f"🔄 Посилання автоматично конвертовано у формат дизайну...")

    # Витягуємо ID файлу
    match = re.search(r'figma\.com\/(?:design|file|site)\/([a-zA-Z0-9]{22,})', url)
    if not match:
        print("❌ Помилка: Не вдалося знайти ID файлу у посиланні.")
        sys.exit(1)

    file_id = match.group(1)

    # Витягуємо Node ID (фрейм)
    node_match = re.search(r'node-id=([^&]+)', url)
    node_id = node_match.group(1).replace('-', ':') if node_match else None

    # Формуємо запит до розробницького API
    api_url = f"https://api.figma.com/v1/files/{file_id}"
    if node_id:
        api_url += f"/nodes?ids={node_id}"

    print(f"📡 Запит до API Figma (Design Mode): {api_url}")

    req = urllib.request.Request(api_url)
    req.add_header('X-Figma-Token', token)

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))

            # Шлях до файлу на Робочому столі
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "figma_design_data.json")

            with open(desktop_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"\n✅ УСПІХ! Дані вашого сайту Habits отримано.")
            print(f"📍 Файл збережено на Робочому столі: {desktop_path}")

    except urllib.error.HTTPError as e:
        print(f"❌ Помилка HTTP {e.code}: {e.reason}")
        error_body = e.read().decode('utf-8')
        print(f"Деталі від Figma: {error_body}")
        if e.code == 403:
            print("\n💡 Порада: Перевірте, чи має ваш токен права 'file_content:read'.")
    except Exception as e:
        print(f"❌ Сталася неочікувана помилка: {e}")


if __name__ == "__main__":
    print("🎨 Anaida Space — Figma Site to JSON Importer\n")

    token = input("1. Вставте ваш TOKEN: ").strip()
    url = input("2. Вставте URL (можна з /site/): ").strip()

    get_figma_node(url, token)
    #figd_XYUeofJazDSQJ8jxKNj6yRYsgXdQLmmvbKimqOTi
#https://www.figma.com/site/GMVuHsrJ7Mr04NG3UI0RfZ/Habits?node-id=1-296&t=j49Mh7UIYJn4CyDF-4
#https://www.figma.com/site/GMVuHsrJ7Mr04NG3UI0RfZ/Habits?node-id=1-296&t=lHyHlN2fUfAee22M-0

