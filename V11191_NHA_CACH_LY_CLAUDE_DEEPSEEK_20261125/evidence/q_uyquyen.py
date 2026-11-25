import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "/root/Lottery_AI_Test/web/backend")
import _v11185_roster_goi_token as R

CA = [
    ("claude-opus-4-6", "MN", "official"), ("claude-opus-4-6", "MT", "official"),
    ("claude-opus-4-6", "MB", "official"), ("claude-sonnet-4-6", "MN", "official"),
    ("claude-sonnet-4-6", "MT", "official"), ("claude-opus-4-6", "MT", "combo_super"),
    ("deepseek-reasoner", "MN", "official"), ("deepseek-reasoner", "MT", "combo_super"),
    ("deepseek-v4-pro-real", "MT", "shadow"), ("deepseek-v4-pro-real", "MB", "shadow"),
    ("gpt-5.4", "MB", "official"),
]
for m, reg, ec in CA:
    kq, ct = R.uy_quyen_goi(m, reg, ec, caller="V11191-kiem")
    print("%-22s %-3s %-12s => %-20s %s" % (m, reg, ec, kq, str(ct.get("ly_do"))[:70]))
