import json

with open('/Users/anhlee/Downloads/source/data/reading/reading_tests.json', 'r', encoding='utf-8') as f:
    json_data = f.read()

with open('/Users/anhlee/Downloads/source/reading_template.html', 'r', encoding='utf-8') as f:
    template = f.read()

output_html = template.replace('__JSON_DATA__', json_data)

with open('/Users/anhlee/Downloads/source/reading.html', 'w', encoding='utf-8') as f:
    f.write(output_html)

try:
    with open('/Users/anhlee/Downloads/Listening/reading.html', 'w', encoding='utf-8') as f:
        f.write(output_html)
except Exception:
    pass

print("reading.html rebuilt successfully!")
