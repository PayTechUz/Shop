# PayTech UZ Django 💳

Simple Django REST API for creating orders with **Payme** and **Click** payment integration.

## 🚀 Quick Start

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Setup environment variables:**

```bash
cp .env.example .env
# Edit .env with your payment gateway credentials
```

3. **Run migrations:**

```bash
python manage.py migrate
```

4. **Start server:**

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## 📋 API Usage

### Create Order

**POST** `/api/orders/create`

```json
{
  "product_name": "Test Product",
  "amount": "100.00",
  "payment_type": "payme" // click, atmos
}
```

**Response:**

```json
{
  "order_id": 1,
  "payment_url": "https://test.paycom.uz/...",
  "payment_type": "payme", // click, atmos
  "amount": "100.00",
  "status": "pending"
}
```

**Payment Types:**

- `payme` - Payme payment gateway
- `click` - Click payment gateway

## 🧪 Test with cURL

```bash
curl -X POST http://127.0.0.1:8000/api/orders/create \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Test Product",
    "amount": "100.00",
    "payment_type": "payme" // click, atmos
  }'
```

## ⚙️ Configuration

Create `.env` file with your payment gateway credentials:

```env
# PayTechUZ License Key (Required)
PAYTECH_LICENSE_API_KEY=your_license_api_key # you can get it from @muhammadali_me on Telegram

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
ATMOS_TERMINAL_ID=your_atmos_terminal_id # optional
ATMOS_API_KEY=your_atmos_api_key
ATMOS_TEST_MODE=True
```

## ✨ Features

- 💳 **Payme** payment gateway integration
- 🔗 **Click** payment gateway integration
- 🚀 Simple REST API
- ✅ Order management
- 🔒 Input validation & error handling
