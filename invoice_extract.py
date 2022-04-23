import re

import pdfplumber
import pandas as pd
from collections import namedtuple

Inv = namedtuple('Inv', 'vend_num vend_name inv_dt due_dt inv_amt net_amt description')

with pdfplumber.open('/home/oem/PycharmProjects/alibaba/apreports (1).pdf') as pdf:
    page = pdf.pages[15]
    text = page.extract_text()

new_vend_re = re.compile(r'^\d{3} [A-Z].*')
inv_line_re = re.compile(r'(\d{6}) (\d{6}) ([\d,]+\.\d{2}) [\sP]*([\d,]+\.\d{2}) [YN ]*\d (.*?) [*\s\d]')

line_items = []
for line in text.split('\n'):
    if new_vend_re.match(line):
        vend_num, *vend_name = line.split()
        vend_name = ' '.join(vend_name)

    line = inv_line_re.search(line)
    if line:
        inv_dt = line.group(1)
        due_dt = line.group(2)
        inv_amt = line.group(3)
        net_amt = line.group(4)
        desc = line.group(5)
        line_items.append(Inv(vend_num, vend_name, inv_dt, due_dt, inv_amt, net_amt, desc))

df = pd.DataFrame(line_items)
df.to_csv('invoice.csv')
