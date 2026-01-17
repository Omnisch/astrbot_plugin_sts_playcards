from collections import defaultdict
import importlib.util
import pprint
from pathlib import Path

# -------- 动态加载 card_dict.py --------
card_path = Path("intermediate/card_dict.py").resolve()

spec = importlib.util.spec_from_file_location("card_dict", card_path)
if spec is not None and spec.loader is not None:
    card_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(card_module)

card_dict = card_module.card_dict


# -------- 构建反转映射 --------
rev_dict = defaultdict(list)

for id_, values in card_dict.items():
    for v in values:
        rev_dict[v].append(id_)

# 转成普通 dict (避免运行时依赖 defaultdict)
rev_dict = dict(rev_dict)


# -------- 写入 rev_dict.py --------
output_path = Path("rev_dict.py")

with output_path.open("w", encoding="utf-8") as f:
    f.write("# This file is auto-generated. Do not edit manually.\n\n")
    f.write("rev_dict = ")
    pprint.pprint(rev_dict, stream=f, width=120)

print(f"Generated {output_path}")
