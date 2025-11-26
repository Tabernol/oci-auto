# OCI A1 Instance Auto-Creator

Автоматичне створення A1.Flex інстансу в Oracle Cloud Infrastructure через GitHub Actions.

## 🔧 Налаштування

### 1. Створіть GitHub Repository Secrets

Перейдіть в Settings → Secrets and variables → Actions → New repository secret

Додайте наступні secrets:

#### OCI API Credentials:
- `OCI_USER_OCID` - User OCID (знайти: Profile → User Settings → OCID)
- `OCI_TENANCY_OCID` - Tenancy OCID (знайти: Profile → Tenancy)
- `OCI_FINGERPRINT` - Fingerprint API ключа
- `OCI_PRIVATE_KEY` - Приватний ключ (весь вміст .pem файлу, включно з BEGIN/END)
- `OCI_REGION` - Регіон (наприклад: `eu-frankfurt-1`, `eu-amsterdam-1`)

#### Instance Configuration:
- `OCI_COMPARTMENT_OCID` - Compartment OCID де створювати інстанс
- `OCI_AVAILABILITY_DOMAIN` - Availability Domain (наприклад: `iAcH:EU-FRANKFURT-1-AD-1`)
- `OCI_SUBNET_OCID` - Subnet OCID для інстансу
- `OCI_IMAGE_OCID` - Image OCID (Oracle Linux, Ubuntu тощо)
- `SSH_PUBLIC_KEY` - Ваш SSH публічний ключ
- `INSTANCE_NAME` - Назва інстансу (наприклад: `my-a1-instance`)

---

## 📋 Як знайти потрібні OCID

### User OCID та Tenancy OCID:
1. OCI Console → клік на іконкуProfile (праворуч вгорі)
2. User Settings → копіюєте OCID
3. Tenancy → копіюєте Tenancy OCID

### API Key (Fingerprint та Private Key):
1. Profile → User Settings → API Keys → Add API Key
2. Generate API Key Pair → Download Private Key (.pem файл)
3. Add → скопіюйте Fingerprint

### Compartment OCID:
1. Menu → Identity & Security → Compartments
2. Виберіть потрібний compartment → копіюйте OCID

### Availability Domain:
1. Menu → Compute → Instances → Create Instance
2. В полі "Availability domain" побачите список (наприклад: `iAcH:EU-FRANKFURT-1-AD-1`)
3. Або через CLI: `oci iam availability-domain list`

### Subnet OCID:
1. Menu → Networking → Virtual Cloud Networks
2. Виберіть VCN → Subnets → виберіть subnet → копіюйте OCID

### Image OCID:
Знайти OCID потрібного образу:
1. Menu → Compute → Instances → Create Instance
2. Image → Change Image → виберіть потрібний образ
3. Або через документацію: https://docs.oracle.com/en-us/iaas/images/

**Популярні образи для A1:**
- Oracle Linux 8 ARM
- Ubuntu 22.04 ARM
- Ubuntu 20.04 ARM

Щоб знайти конкретний OCID для вашого регіону, виконайте:
```bash
oci compute image list \
  --compartment-id <your-tenancy-ocid> \
  --operating-system "Oracle Linux" \
  --operating-system-version "8" \
  --shape "VM.Standard.A1.Flex"
```

### SSH Public Key:
Якщо у вас ще немає SSH ключа:
```bash
ssh-keygen -t rsa -b 4096
cat ~/.ssh/id_rsa.pub  # Це ваш публічний ключ
```

---

## 🚀 Використання

### Автоматичний запуск:
Workflow автоматично запускається **кожні 10 хвилин** і намагається створити інстанс.

### Ручний запуск:
1. GitHub → вкладка Actions
2. Виберіть "OCI A1 Instance Creator"
3. Run workflow

### Зміна частоти запуску:
В файлі `.github/workflows/oci-instance-creator.yml` змініть cron:
```yaml
schedule:
  - cron: '*/10 * * * *'  # Кожні 10 хвилин
  # - cron: '*/5 * * * *'  # Кожні 5 хвилин
  # - cron: '0 * * * *'     # Кожну годину
```

---

## 📊 Моніторинг

### Перегляд логів:
GitHub → Actions → виберіть запуск workflow → Try to create A1 instance

### Коли інстанс створено:
Workflow покаже:
```
✅ УСПІХ! Інстанс створено!
Instance ID: ocid1.instance.oc1...
```

**ВАЖЛИВО:** Після успішного створення інстансу **вимкніть workflow** щоб не створювати дублікати:
1. Видаліть файл `.github/workflows/oci-instance-creator.yml`
2. Або відключіть в Actions → workflow → disable

---

## 🔧 Налаштування конфігурації

В файлі `oci-instance-creator.yml` можна змінити:

```python
# Кількість CPU та RAM
shape_config = oci.core.models.LaunchInstanceShapeConfigDetails(
    ocpus=1.0,        # 1-4 CPU
    memory_in_gbs=6.0  # 6-24 GB RAM (мінімум 6 GB на 1 CPU)
)
```

**Always Free limits для A1.Flex:**
- До 4 OCPU
- До 24 GB RAM
- Можна створити 1 інстанс з 4 CPU + 24 GB або декілька менших (наприклад 4x1CPU+6GB)

---

## ⚠️ Troubleshooting

### Помилка "Out of host capacity":
- Це нормально, capacity A1 обмежена
- Workflow буде пробувати кожні 10 хвилин автоматично
- Зазвичай вдається створити за 1-48 годин

### Помилка авторизації:
- Перевірте правильність всіх OCID
- Перевірте що Private Key містить весь текст включно з `-----BEGIN/END-----`
- Перевірте що Fingerprint відповідає Private Key

### Інстанс не запускається:
- Перевірте що Image OCID підходить для A1 (ARM архітектура)
- Перевірте що Subnet дозволяє створення інстансів

---

## 📝 Примітки

- GitHub Actions безкоштовно надає 2000 хвилин/місяць для публічних репозиторіїв
- Після створення інстансу не забудьте вимкнути workflow!

---

## 🎯 Що далі?

Після успішного створення інстансу:
1. Підключіться через SSH: `ssh ubuntu@<public-ip>` або `ssh opc@<public-ip>`
2. Налаштуйте потрібні сервіси
3. Вимкніть цей workflow щоб не створювати дублікати

Успіхів! 🚀
