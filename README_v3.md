# WiFi Hunter Professional Tools Suite v3.0

## Overview

**WiFi Hunter** هي مجموعة احترافية متقدمة من أدوات الشبكات المصممة للاختبار الأمني والتحليل المتقدم. تتضمن ثلاث أدوات رئيسية تعمل بشكل متكامل:

1. **Scanner Network** (wifi_hunter.py) - ماسح الشبكة الذكي
2. **MAC Address Changer** (mac_simple.ps1) - تغيير عنوان MAC
3. **Professional Network Tools** (professional_network_tools.py) - أداة الاعتراض المتقدمة

---

## 🎯 الأداة 1: WiFi Hunter Network Scanner

### المميزات:
- ✅ فحص شامل للشبكة باستخدام بروتوكول ARP
- ✅ كشف نوع الجهاز (iPhone, Android, Linux, Windows, Router)
- ✅ تصفية حسب البائع
- ✅ البحث عن جهاز بـ IP أو MAC
- ✅ عرض إحصائيات مفصلة
- ✅ واجهة ملونة احترافية

### الاستخدام:

```bash
# فحص الشبكة الأساسي
python wifi_hunter.py -t 192.168.1.0/24

# مع خيارات متقدمة
python wifi_hunter.py -t 192.168.1.0/24 -timeout 5 -retries 3 -v

# البحث عن جهاز معين
python wifi_hunter.py -t 192.168.1.0/24 -search-ip 192.168.1.5

# البحث عن MAC معين
python wifi_hunter.py -t 192.168.1.0/24 -search-mac "ac:9b:0a"

# تصفية حسب البائع
python wifi_hunter.py -t 192.168.1.0/24 -filter-vendor apple
```

### CLI Arguments:
```
-t, --target      نطاق IP (مثال: 192.168.1.0/24)
-timeout          مهلة الانتظار بالثواني (افتراضي: 3)
-retries          عدد محاولات إعادة المحاولة (افتراضي: 1)
-search-ip        البحث عن IP محدد
-search-mac       البحث عن MAC محدد
-filter-vendor    تصفية حسب نوع الجهاز
-v, --verbose     تفعيل الوضع المفصل
-i, --interface   واجهة الشبكة (اختياري)
```

---

## 🎯 الأداة 2: MAC Address Changer

### المميزات:
- ✅ تغيير عنوان MAC للمحولات
- ✅ قائمة تفاعلية للمحولات
- ✅ نسخ احتياطي تلقائي للقيم الأصلية
- ✅ استعادة الأصلي بضغطة واحدة
- ✅ دعم صيغ متعددة (AA:BB:CC:DD:EE:FF و AABBCCDDEEFF)

### الاستخدام:

```powershell
# تشغيل الأداة (يتطلب صلاحيات Admin)
powershell -ExecutionPolicy Bypass -File mac_simple.ps1
```

### العمليات المتاحة:
1. عرض المحولات النشطة
2. تغيير عنوان MAC
3. استعادة MAC الأصلي
4. الخروج

---

## 🎯 الأداة 3: Professional Network Tools v3.0

### المميزات الرئيسية:

#### 1️⃣ **ARP Spoofing الاحترافي**
- تحويل المسار بين هدف والبوابة
- استعادة تلقائية عند الإيقاف
- معدل ضخ قابل للتخصيص

#### 2️⃣ **DNS Sniffer متقدم**
- التقاط جميع استعلامات DNS
- تحديد الاستعلامات الأكثر تكراراً
- حفظ السجلات في ملفات

#### 3️⃣ **DNS Cache Poisoning** (اختياري)
- حقن عناوين IP وهمية
- تحويل حركة المستخدم إلى خوادم مخصصة
- تكوين مرن عبر config.json

#### 4️⃣ **كشف الأجهزة المحمولة**
- تحديد أجهزة iPhone/iPad تلقائياً
- كشف أجهزة Android
- تسجيل الأجهزة المكتشفة

#### 5️⃣ **استخراج بيانات الاعتماد**
- البحث عن كلمات المرور في الحركة HTTP
- التقاط بيانات تسجيل الدخول
- حفظ في ملف منفصل مع timestamp

#### 6️⃣ **تحليل حركة HTTP/HTTPS**
- عد طلبات HTTP و HTTPS منفصلة
- تتبع الجلسات النشطة
- حساب البيانات المنقولة بالكامل

#### 7️⃣ **حجب المجالات**
- قائمة المجالات المحجوبة قابلة للتخصيص
- إعادة توجيه تلقائي عند الحجب
- تسجيل محاولات الوصول

#### 8️⃣ **نظام السجلات المتقدم**
- ملف log DNS منفصل
- ملف بيانات الاعتماد
- ملف الجلسات (JSON)
- إحصائيات شاملة

#### 9️⃣ **التحليل والإحصائيات**
- إجمالي الرزم المنقولة
- البيانات المنقولة بالكيلوبايت
- عدد عناوين IP الفريدة
- أفضل 5 استعلامات DNS
- الأجهزة المحمولة المكتشفة
- بيانات الاعتماد المنقولة

### الاستخدام:

```bash
# الوضع الكامل (ARP Spoofing + DNS Sniffer)
python professional_network_tools.py -t 192.168.1.100 -g 192.168.1.1

# وضع ARP Spoofing فقط
python professional_network_tools.py -t 192.168.1.100 -g 192.168.1.1 -m spoof

# وضع DNS Sniffer فقط
python professional_network_tools.py -t 192.168.1.100 -g 192.168.1.1 -m sniff

# مع ملف الإعدادات المخصص
python professional_network_tools.py -t 192.168.1.100 -g 192.168.1.1 -c config.json

# وضع مفصل
python professional_network_tools.py -t 192.168.1.100 -g 192.168.1.1 -v
```

### CLI Arguments:
```
-t, --target (مطلوب)   IP الهدف
-g, --gateway (مطلوب)  IP البوابة
-m, --mode             الوضع: full | spoof | sniff (افتراضي: full)
-v, --verbose          تفعيل الوضع المفصل
-c, --config           ملف الإعدادات JSON
```

### ملف الإعدادات (config.json):

```json
{
  "domain_blocking": true,
  "blocked_domains": [
    "ads.google.com",
    "tracking.com",
    "analytics.google.com"
  ],
  "dns_poisoning": false,
  "credential_capture": true,
  "mobile_detection": true,
  "ssl_interception": true,
  "session_capture": true,
  "fake_ips": {
    "ads.google.com": "192.168.1.1",
    "tracking.com": "192.168.1.1"
  }
}
```

### ملفات السجلات:

سيتم حفظ جميع البيانات في مجلد `logs/`:

- `dns_log_YYYYMMDD_HHMMSS.txt` - استعلامات DNS
- `sessions_YYYYMMDD_HHMMSS.json` - جلسات الشبكة
- `credentials_YYYYMMDD_HHMMSS.txt` - بيانات الاعتماد
- `stats_YYYYMMDD_HHMMSS.json` - الإحصائيات الشاملة
- `network_log_YYYYMMDD_HHMMSS.json` - سجل الشبكة الكامل

---

## 📋 متطلبات التثبيت

### Python Requirements:
```bash
pip install scapy>=2.4.5 colorama>=0.4.3
```

### Windows Requirements:
- صلاحيات Administrator
- PowerShell 5.1+
- Python 3.7+
- Scapy 2.4.5+
- Colorama 0.4.3+

### تثبيت المكتبات:
```bash
# Linux/Mac
pip install -r requirements.txt

# Windows
python -m pip install -r requirements.txt
```

---

## 🔐 ملاحظات الأمان

⚠️ **تحذير:**
- هذه الأدوات مخصصة للاختبار الأمني المصرح به فقط
- استخدام هذه الأدوات على شبكة لا تملكها قد يكون غير قانوني
- الاستخدام على مسؤوليتك الشخصية

✅ **التطبيقات القانونية:**
- اختبار أمان شبكتك الخاصة
- بحث أمني معتمد
- تدريب على أمن الشبكات
- اختبار الاختراق المصرح به

---

## 📊 مثال على المخرجات

```
╔════════════════════════════════════════════════════╗
║  WiFi Hunter Professional Tools Suite v3.0        ║
║  Advanced Network Interception + Full Analysis    ║
║  ARP Spoofing | DNS Sniffer | Credential Capture │
║  SSL/HTTPS Interception | Mobile Detection        ║
║  Session Capture | Domain Blocking | Logging      ║
╚════════════════════════════════════════════════════╝

[CONFIGURATION]
  Target: 192.168.1.100
  Gateway: 192.168.1.1
  Mode: full
  Features: DNS Poisoning=False, Blocking=True, Creds=True

[*] Verifying connectivity...
[+] Target MAC: ac:9b:0a:xx:xx:xx
[+] Gateway MAC: b0:95:75:xx:xx:xx

[*] ARP Spoofing Active

[09:15:32] DNS: google.com
[09:15:33] DNS: youtube.com [BLOCKED]
[!] CREDENTIALS FOUND! ['password123']
[+] Mobile Device: Apple iPhone/iPad

[PROFESSIONAL STATISTICS REPORT]
  Total Packets: 1542
  Data Transferred: 45.23 KB
  Duration: 120s
  Unique IPs: 8
  
Network Activity:
  HTTP: 256 | HTTPS: 512 | DNS: 128
  
Top DNS Queries:
  1. google.com (45)
  2. youtube.com (23)
  3. facebook.com (18)
```

---

## 🐛 استكشاف الأخطاء

### المشكلة: "Permission Denied"
```bash
# الحل: شغل بصلاحيات Admin
sudo python professional_network_tools.py ...  # Linux/Mac
# أو: شغل Command Prompt/PowerShell as Administrator  # Windows
```

### المشكلة: "No module named scapy"
```bash
pip install scapy colorama
```

### المشكلة: واجهة الشبكة غير صحيحة
```bash
# حدد الواجهة يدويا
python professional_network_tools.py -t 192.168.1.100 -g 192.168.1.1 -i eth0
```

---

## 📞 الدعم والمساعدة

للمزيد من المساعدة:
- تحقق من الإعدادات في config.json
- استخدم `-v` للحصول على تفاصيل أكثر
- تأكد من صلاحيات Administrator
- تحقق من أن IP الهدف والبوابة صحيحة

---

**إصدار:** v3.0  
**آخر تحديث:** 2024  
**الترخيص:** للاستخدام التعليمي والاختبار الأمني فقط
