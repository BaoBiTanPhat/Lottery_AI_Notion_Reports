# -*- coding: utf-8 -*-
"""Nền ĐÚNG cho một bộ K đuôi (RM-18) + nền cho reciprocal rank.

Với b = tỉ lệ đuôi đã về trong ngày (|tập đuôi| / 100), một Top-K CHỌN NGẪU NHIÊN có:
    P(hit@k) = 1 - (1-b)^k
    E[RR]    = sum_{i=1..K} b*(1-b)^(i-1) / i
Cấm so hit@k của Top-K với b (nền của MỘT số) — đó đúng là RM-18.
"""
import json
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")
D = "/root/Lottery_AI_Test/artifacts/v11178/eod_2026-09-11.json"
d = json.loads(open(D, encoding="utf-8").read())


def nen_hit(b, k):
    return 1 - (1 - b) ** k


def nen_rr(b, K=10):
    s = 0.0
    for i in range(1, K + 1):
        s += b * ((1 - b) ** (i - 1)) / i
    return s


print("=" * 96)
print("  NEN DUNG CHO BO-K (RM-18) — ngay 2026-09-11")
print("=" * 96)
for reg in ("MN", "MT", "MB"):
    A = d["actual"][reg]
    n = A["n_tails"]
    b = n / 100.0
    print("\n  %s · %d/100 duoi da ve => b=%.2f" % (reg, n, b))
    print("     NEN ngau nhien: hit@1=%.3f hit@3=%.3f hit@5=%.3f hit@10=%.3f · E[RR]=%.4f"
          % (nen_hit(b, 1), nen_hit(b, 3), nen_hit(b, 5), nen_hit(b, 10), nen_rr(b)))
    o = d["official"][reg]
    if o.get("cham"):
        c = o["cham"]
        print("     [1] OFFICIAL   : hit@1=%d hit@3=%d hit@5=%d hit@10=%d rank=%s RR=%.4f"
              % (c["diagnostic_counterfactual_hit@1"], c["diagnostic_counterfactual_hit@3"],
                 c["diagnostic_counterfactual_hit@5"], c["diagnostic_counterfactual_hit@10"],
                 c["winning_tail_rank"], c["reciprocal_rank"]))
        print("         so voi nen : hit@1 %+.3f · hit@3 %+.3f · hit@5 %+.3f · hit@10 %+.3f · RR %+.4f"
              % (c["diagnostic_counterfactual_hit@1"] - nen_hit(b, 1),
                 c["diagnostic_counterfactual_hit@3"] - nen_hit(b, 3),
                 c["diagnostic_counterfactual_hit@5"] - nen_hit(b, 5),
                 c["diagnostic_counterfactual_hit@10"] - nen_hit(b, 10),
                 c["reciprocal_rank"] - nen_rr(b)))

for ec in ("MT_DELTA_LIVE", "MB_DELTA_LIVE"):
    K = d["per_execution_class"][ec]["regions"]
    for reg, R in K.items():
        if R.get("trang_thai") != "SCORED":
            continue
        b = d["actual"][reg]["n_tails"] / 100.0
        per = R["branch_3_PER_MODEL"]
        rrs = [(v["cham"]["reciprocal_rank"], m) for m, v in per.items() if v.get("cham")]
        h1 = [v["cham"]["diagnostic_counterfactual_hit@1"] for v in per.values() if v.get("cham")]
        h3 = [v["cham"]["diagnostic_counterfactual_hit@3"] for v in per.values() if v.get("cham")]
        h10 = [v["cham"]["diagnostic_counterfactual_hit@10"] for v in per.values() if v.get("cham")]
        if not rrs:
            continue
        tb = sum(x for x, _ in rrs) / len(rrs)
        print("\n  %s · %s · %d model co Top-K (b=%.2f)" % (ec, reg, len(rrs), b))
        print("     [3] PER-MODEL  : RR tot nhat=%.4f (%s) · RR TRUNG BINH=%.4f"
              % (max(rrs)[0], max(rrs)[1], tb))
        print("         E[RR] ngau nhien=%.4f  =>  trung binh %+.4f so voi ngau nhien"
              % (nen_rr(b), tb - nen_rr(b)))
        print("         hit@1 tb=%.3f (nen %.3f) · hit@3 tb=%.3f (nen %.3f) · hit@10 tb=%.3f (nen %.3f)"
              % (sum(h1) / len(h1), nen_hit(b, 1), sum(h3) / len(h3), nen_hit(b, 3),
                 sum(h10) / len(h10), nen_hit(b, 10)))
print("\n" + "=" * 96)
print("  KET LUAN: moi so tren la diagnostic_counterfactual_hit cua mot ngay,")
print("  va MOI system_action_decision deu la ABSTAIN — khong quyet dinh nao da xay ra.")
print("=" * 96)
