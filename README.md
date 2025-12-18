# PayTech UZ Django 💳

Django REST API loyihasi **Payme**, **Click** va **Atmos** to'lov tizimlarini integratsiyalash uchun. **PaymentService** klassi orqali to'lovlarni yaratish va webhook'lar orqali to'lov holatini kuzatish.

## 🚀 Quick Start

### 1. Virtual Environment yaratish

```bash
python3 -m venv venv
source venv/bin/activate  # MacOS/Linux
# yoki
venv\Scripts\activate     # Windows
```

### 2. Dependencies o'rnatish

```bash
pip install -r requirements.txt
```

### 3. Environment variables sozlash

```bash
cp .env.example .env
# .env faylini to'lov tizimlaringiz ma'lumotlari bilan to'ldiring
```

### 4. Database migratsiyalari

```bash
python manage.py migrate
```

### 5. Serverni ishga tushirish

```bash
python manage.py runserver
```

Server manzil: **http://127.0.0.1:8000/**

---

## 📋 API Endpoints

### 1. Order yaratish

**Endpoint:** `POST /api/orders/create`

**Request Body:**

```json
{
  "product_name": "Premium Subscription",
  "amount": "50000.00",
  "payment_type": "payme"
}
```

**Response (Success - 201):**

```json
{
  "invoice_id": 42,
  "payment_url": "https://checkout.paycom.uz/..."
}
```

**Payment Types:**
- `payme` - Payme to'lov tizimi
- `click` - Click to'lov tizimi
- `atmos` - Atmos to'lov tizimi

---

## 🧪 cURL Examples

### Payme to'lovi yaratish

```bash
curl -X POST http://127.0.0.1:8000/api/orders/create \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Banana",
    "amount": 50000,
    "payment_type": "payme"
  }'
```

### Click to'lovi yaratish

```bash
curl -X POST http://127.0.0.1:8000/api/orders/create \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Apple",
    "amount": 30000,
    "payment_type": "click"
  }'
```

### Atmos to'lovi yaratish

```bash
curl -X POST http://127.0.0.1:8000/api/orders/create \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Orange",
    "amount": 20000,
    "payment_type": "atmos"
  }'
```

---

## ⚙️ Configuration

`.env` fayli namunasi:

```env
# PayTechUZ License Key (Majburiy)
PAYTECH_LICENSE_API_KEY=your_license_api_key
# License olish: https://docs.pay-tech.uz/console yoki @muhammadali_me (Telegram)

# Payme Configuration
PAYME_ID=your_payme_id
PAYME_KEY=your_payme_key

# Click Configuration
CLICK_SERVICE_ID=your_service_id
CLICK_MERCHANT_ID=your_merchant_id
CLICK_MERCHANT_USER_ID=your_merchant_user_id
CLICK_SECRET_KEY=your_secret_key

# Atmos Configuration
ATMOS_CONSUMER_KEY=your_atmos_consumer_key
ATMOS_CONSUMER_SECRET=your_atmos_consumer_secret
ATMOS_STORE_ID=your_atmos_store_id
ATMOS_TERMINAL_ID=your_atmos_terminal_id  # optional
ATMOS_API_KEY=your_atmos_api_key
ATMOS_TEST_MODE=True
```

---

## 🪝 Webhook Endpoints

To'lov tizimlaridan keladigan webhook'larni qabul qilish uchun:

- **Payme Webhook:** `POST /api/payments/payme/webhook/`
- **Click Webhook:** `POST /api/payments/click/webhook/`
- **Atmos Webhook:** `POST /api/payments/atmos/webhook/`

Webhook'lar avtomatik ravishda order holatini yangilaydi:
- `successfully_payment()` - To'lov muvaffaqiyatli amalga oshirilganda
- `cancelled_payment()` - To'lov bekor qilinganda

---



## 📚 Additional Resources

- [PayTech UZ Documentation](https://docs.pay-tech.uz)
- [Payme API Docs](https://developer.paycom.uz)
- [Click API Docs](https://docs.click.uz)

---

## 📝 License

MIT License

---

## 👨‍💻 Support

Savol yoki yordam kerak bo'lsa:
- Telegram: [@muhammadali_me](https://t.me/muhammadali_me)
- Documentation: [docs.pay-tech.uz](https://docs.pay-tech.uz)
