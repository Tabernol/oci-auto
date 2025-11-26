# GitHub Secrets Template
# Скопіюйте це в Settings → Secrets and variables → Actions

## Обов'язкові secrets:

OCI_USER_OCID=ocid1.user.oc1..aaaaaaaa...
# Де знайти: Profile → User Settings → OCID

OCI_TENANCY_OCID=ocid1.tenancy.oc1..aaaaaaaa...
# Де знайти: Profile → Tenancy → OCID

OCI_FINGERPRINT=aa:bb:cc:dd:ee:ff:00:11:22:33:44:55:66:77:88:99
# Де знайти: Profile → User Settings → API Keys → Fingerprint

OCI_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
(весь вміст .pem файлу)
...
-----END RSA PRIVATE KEY-----
# Важливо: скопіюйте весь ключ включно з BEGIN/END рядками

OCI_REGION=eu-frankfurt-1
# Можливі значення: eu-frankfurt-1, eu-amsterdam-1, us-ashburn-1, uk-london-1
# Повний список: https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm

OCI_COMPARTMENT_OCID=ocid1.compartment.oc1..aaaaaaaa...
# Де знайти: Identity & Security → Compartments → виберіть compartment → OCID
# Або можна використати Tenancy OCID якщо створюєте в root compartment

OCI_AVAILABILITY_DOMAIN=iAcH:EU-FRANKFURT-1-AD-1
# Формат залежить від регіону, приклади:
# eu-frankfurt-1: iAcH:EU-FRANKFURT-1-AD-1, iAcH:EU-FRANKFURT-1-AD-2, iAcH:EU-FRANKFURT-1-AD-3
# us-ashburn-1: wzFh:US-ASHBURN-AD-1, wzFh:US-ASHBURN-AD-2, wzFh:US-ASHBURN-AD-3
# Де знайти: Compute → Instances → Create → Availability Domain dropdown

OCI_SUBNET_OCID=ocid1.subnet.oc1.eu-frankfurt-1.aaaaaaaa...
# Де знайти: Networking → Virtual Cloud Networks → виберіть VCN → Subnets → OCID

OCI_IMAGE_OCID=ocid1.image.oc1.eu-frankfurt-1.aaaaaaaa...
# Популярні образи для A1:
# - Oracle Linux 8 ARM
# - Ubuntu 22.04 ARM  
# - Ubuntu 20.04 ARM
# Де знайти: Compute → Images → або використайте скрипт get-oci-info.sh

SSH_PUBLIC_KEY=ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQ... user@host
# Ваш SSH публічний ключ
# Згенерувати: ssh-keygen -t rsa -b 4096
# Переглянути: cat ~/.ssh/id_rsa.pub

INSTANCE_NAME=my-a1-instance
# Назва інстансу (будь-яка, наприклад: a1-server, ubuntu-a1, my-vps)

---

## Як створити API Key:

1. OCI Console → Profile (іконка праворуч вгорі) → User Settings
2. Resources (ліворуч) → API Keys → Add API Key
3. Generate API Key Pair → Download Private Key (зберігайте .pem файл)
4. Add → з'явиться Configuration File Preview
5. Скопіюйте Fingerprint з preview
6. Вміст .pem файлу використайте як OCI_PRIVATE_KEY

---

## Швидкий старт:

1. Створіть репозиторій на GitHub
2. Додайте файл .github/workflows/oci-instance-creator.yml
3. Додайте всі secrets вище в Settings → Secrets and variables → Actions
4. Workflow запуститься автоматично кожні 10 хвилин
5. Або запустіть вручну: Actions → OCI A1 Instance Creator → Run workflow

---

## Перевірка конфігурації локально (опціонально):

Якщо у вас встановлено OCI CLI:

```bash
# Запустіть helper script
chmod +x get-oci-info.sh
./get-oci-info.sh

# Або вручну перевірте:
oci iam availability-domain list
oci network vcn list --compartment-id <your-compartment-ocid>
oci compute image list --compartment-id <your-tenancy-ocid> --shape "VM.Standard.A1.Flex"
```

---

## Важливі примітки:

⚠️ РЕГІОН: Image OCID відрізняється для різних регіонів! Використовуйте Image OCID з вашого регіону.

⚠️ ARM АРХІТЕКТУРА: A1.Flex це ARM процесори. Переконайтесь що обираєте ARM (aarch64) образи, не x86.

⚠️ ПРИВАТНИЙ КЛЮЧ: Ніколи не комітьте приватний ключ в репозиторій! Тільки через GitHub Secrets.

⚠️ SUBNET: Subnet має бути публічним (або з NAT Gateway) щоб інстанс отримав публічну IP адресу.

✅ БЕЗПЕКА: Всі дані в GitHub Secrets зашифровані та доступні тільки вам.
