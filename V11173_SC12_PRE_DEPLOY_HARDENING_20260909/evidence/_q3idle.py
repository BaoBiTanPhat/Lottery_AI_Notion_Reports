# -*- coding: utf-8 -*-
"""Q3 — CONG IDLE. Chi doc. Khong deploy neu bat ky muc nao FAIL."""
import subprocess, sqlite3, datetime
def sh(x): return subprocess.run(x,shell=True,capture_output=True,text=True).stdout.strip()
ict=sh("TZ=Asia/Ho_Chi_Minh date '+%Y-%m-%d %H:%M:%S'")
utc=sh("TZ=UTC date '+%Y-%m-%d %H:%M:%S'")
print("=== MOC ===  ICT %s  |  UTC %s" % (ict, utc))
gio=int(ict[11:13]); phut=int(ict[14:16])
dat=[]; fail=[]
def ok(t,c,g=""):
    (dat if c else fail).append(t); print("  %s %s  %s" % ("DAT " if c else "FAIL", t, g))

print("\n--- 4.1 tien trinh python nang ngoai service ---")
ps=sh("ps -eo pid,etimes,pcpu,cmd --sort=-pcpu | grep -i '[p]ython' | head -12")
print(ps or "  (khong co)")
pid=sh("systemctl show -p MainPID --value lottery")
nang=[l for l in ps.split("\n") if l.strip() and not l.strip().startswith(pid)
      and "_run_" not in l and float(l.split()[2] or 0) > 5.0]
ok("khong tien trinh python nang ngoai service", len(nang)==0, "%d tien trinh >5%%CPU" % len(nang))

print("\n--- 4.2 job vua chay trong 5 phut qua ---")
c=sqlite3.connect("file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro",uri=True)
c.row_factory=sqlite3.Row
r=c.execute("SELECT job_name, datetime(log_time,'+7 hours') vn FROM scheduler_logs "
            "WHERE datetime(log_time,'+7 hours') >= datetime(?, '-5 minutes') ORDER BY id DESC LIMIT 15",
            (ict,)).fetchall()
for x in r: print("   %s  %s" % (x["vn"], x["job_name"]))
ok("khong job nao chay trong 5 phut qua", len(r)==0, "%d dong" % len(r))

print("\n--- 4.3 moc cron trong 15 phut toi ---")
MOC=[(21,50,"model_latency_shadow"),(22,30,"pnl_forward"),(22,35,"consensus_freeshadow"),
     (22,45,"rescue_candidate"),(23,55,"du_doan_test_auto"),(0,30,"rule_key_registry"),(2,0,"retrain tuan")]
sap=[]
now=gio*60+phut
for h,m,t in MOC:
    d=(h*60+m)-now
    if d<0: d+=1440
    if d<=15: sap.append((d,t))
for d,t in sap: print("   con %d phut: %s" % (d,t))
ok("khong moc cron nao trong 15 phut toi", len(sap)==0, "%d moc" % len(sap))

print("\n--- 4.4 writer dang giu DB ---")
w=sh("ls -la /root/Lottery_AI_Test/data/lottery_ai.db-wal /root/Lottery_AI_Test/data/lottery_ai.db-shm 2>/dev/null")
print(w or "   (khong co wal/shm)")
ok("khong co WAL/SHM ton dong", w=="", "co tep lock" if w else "")

print("\n--- 4.5 dich vu ---")
for k in ("MainPID","NRestarts","ActiveState","SubState"):
    print("   %-12s %s" % (k, sh("systemctl show -p %s --value lottery" % k)))
h=sh("curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/api/health")
ok("health = 200", h=="200", h)
ok("ActiveState = active", sh("systemctl show -p ActiveState --value lottery")=="active")

print("\n--- 4.6 du_doan_test_auto con chay khong (tan toi 23:55) ---")
r2=c.execute("SELECT COUNT(*) n, MAX(datetime(log_time,'+7 hours')) t FROM scheduler_logs "
             "WHERE job_name='du_doan_test_auto' AND substr(datetime(log_time,'+7 hours'),1,10)=?",
             (ict[:10],)).fetchone()
print("   du_doan_test_auto hom nay: %s dong, dong cuoi %s" % (r2["n"], r2["t"]))

print("\n" + "="*66)
print("CONG IDLE: %d DAT / %d FAIL" % (len(dat), len(fail)))
if fail: print("  FAIL:", " · ".join(fail))
print("KET LUAN:", "PASS — duoc phep sang Q4" if not fail else "KHONG PASS — hoan sang cua so 00:00-05:00")
print("="*66)
