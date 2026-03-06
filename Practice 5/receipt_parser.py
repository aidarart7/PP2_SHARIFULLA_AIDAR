import re
import textwrap

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

matches = re.findall(
    r"\d+\.\n(.+?)\n([\d,]+)\s*x\s*([\d\s,]+)\n([\d\s,]+)\nСтоимость",
    text,
    re.DOTALL
)
datetime = re.search(r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}", text)

payment = re.search(r"(Банковская карта|Наличные|Card|Cash)", text)

total = 0
line_width = 80
name_width = 50

print(f"{'PRODUCT':<{name_width}} {'AMOUNT x PRICE = TOTAL'}")
print("-"*line_width)

for item in matches:
    name = item[0].strip()
    amount = item[1].replace(",", ".")
    price = item[2].replace(" ", "")
    total_price = item[3].replace(" ", "").replace(",", ".")
    total += float(total_price)

    wrapped_name = textwrap.wrap(name, width=name_width)
    for i, line in enumerate(wrapped_name):
        if i == 0:
            print(f"{line:<{name_width}} {amount} x {price} = {total_price}")
        else:
            print(f"{line:<{name_width}}")

print("-"*line_width)
print(f"{'TOTAL':<{name_width}} {round(total,2)}\n")

print("DateTime:", datetime.group() if datetime else "Not found")
print("Payment:", payment.group() if payment else "Not found")