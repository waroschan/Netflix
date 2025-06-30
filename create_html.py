import csv
import sys
import urllib.parse

csv.field_size_limit(sys.maxsize)

html_rows = ''
try:
    with open('C:\\GeminiCLI\\Netflix\\NetflixViewingHistory.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for i, row in enumerate(reader):
            if row:
                title = row[0]
                date_str = row[1] # Original date string like "M/D/YY"

                # Parse and reformat date_str to YYYY/MM/DD
                parts = date_str.split('/')
                month = int(parts[0])
                day = int(parts[1])
                year_short = int(parts[2])

                # Handle 2-digit year (e.g., '25' -> 2025, '98' -> 1998)
                full_year = 2000 + year_short if year_short < 70 else 1900 + year_short

                # Format month and day with leading zeros if necessary
                formatted_month = f'{month:02d}'
                formatted_day = f'{day:02d}'

                formatted_date = f'{full_year}/{formatted_month}/{formatted_day}'

                display_title = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

                search_query = urllib.parse.quote_plus(f"{title} Netflix")
                google_search_url = f"https://www.google.com/search?q={search_query}"

                linked_title = f'<a href="{google_search_url}" target="_blank">{display_title}</a>'

                html_rows += f'            <tr>\n                <td>{linked_title}</td>\n                <td>{formatted_date}</td>\n            </tr>\n'
except FileNotFoundError:
    html_rows = "<tr><td colspan=\"2\">エラー: NetflixViewingHistory.csv が見つかりません。</td></tr>"
except Exception as e:
    html_rows = f"<tr><td colspan=\"2\">エラー: {e}</td></tr>"

# テンプレートファイルを読み込む
with open('C:\\GeminiCLI\\Netflix\\history_template.html', 'r', encoding='utf-8') as f:
    full_html = f.read()

# プレースホルダーを生成した行で置き換える
full_html = full_html.replace("<!-- HISTORY_ROWS_PLACEHOLDER -->", html_rows)

# 最終的なHTMLファイルに書き込む
with open('C:\\GeminiCLI\\Netflix\\history.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("history.html has been updated with the new date format.")
