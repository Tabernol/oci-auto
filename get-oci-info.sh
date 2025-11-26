#!/bin/bash
# Helper script для швидкого отримання всіх необхідних OCID з OCI

echo "==================================="
echo "OCI Configuration Helper"
echo "==================================="
echo ""

# Перевірка чи встановлено OCI CLI
if ! command -v oci &> /dev/null; then
    echo "❌ OCI CLI не встановлено"
    echo "Встановіть: pip install oci-cli"
    echo "Налаштуйте: oci setup config"
    exit 1
fi

echo "📋 Збираємо інформацію з OCI..."
echo ""

# Tenancy OCID
echo "1️⃣ TENANCY OCID:"
TENANCY_OCID=$(oci iam compartment list --all --compartment-id-in-subtree true --query 'data[0]."compartment-id"' --raw-output 2>/dev/null || oci iam availability-domain list --query 'data[0]."compartment-id"' --raw-output)
echo "$TENANCY_OCID"
echo ""

# User OCID
echo "2️⃣ USER OCID:"
USER_OCID=$(oci iam user list --query 'data[0].id' --raw-output 2>/dev/null || echo "Запустіть: oci iam user list")
echo "$USER_OCID"
echo ""

# Region
echo "3️⃣ CURRENT REGION:"
REGION=$(oci iam region-subscription list --query 'data[0]."region-name"' --raw-output 2>/dev/null)
echo "$REGION"
echo ""

# Compartments
echo "4️⃣ COMPARTMENTS (перші 5):"
oci iam compartment list --all --query 'data[0:5].[name,id]' --output table 2>/dev/null
echo ""

# Availability Domains
echo "5️⃣ AVAILABILITY DOMAINS:"
oci iam availability-domain list --query 'data[].[name]' --output table 2>/dev/null
echo ""

# VCNs та Subnets
echo "6️⃣ VCNs та SUBNETS:"
echo "VCNs в root compartment:"
VCN_ID=$(oci network vcn list --compartment-id "$TENANCY_OCID" --query 'data[0].id' --raw-output 2>/dev/null)
oci network vcn list --compartment-id "$TENANCY_OCID" --query 'data[].[display-name,id]' --output table 2>/dev/null

if [ ! -z "$VCN_ID" ]; then
    echo ""
    echo "Subnets в першому VCN:"
    oci network subnet list --compartment-id "$TENANCY_OCID" --vcn-id "$VCN_ID" --query 'data[].[display-name,id]' --output table 2>/dev/null
fi
echo ""

# Images для A1
echo "7️⃣ ДОСТУПНІ ARM IMAGES (Oracle Linux та Ubuntu):"
echo "Oracle Linux 8 ARM:"
oci compute image list \
    --compartment-id "$TENANCY_OCID" \
    --operating-system "Oracle Linux" \
    --operating-system-version "8" \
    --shape "VM.Standard.A1.Flex" \
    --query 'data[0].[display-name,id]' \
    --output table 2>/dev/null

echo ""
echo "Ubuntu 22.04 ARM:"
oci compute image list \
    --compartment-id "$TENANCY_OCID" \
    --operating-system "Canonical Ubuntu" \
    --operating-system-version "22.04" \
    --shape "VM.Standard.A1.Flex" \
    --query 'data[0].[display-name,id]' \
    --output table 2>/dev/null

echo ""
echo "Ubuntu 20.04 ARM:"
oci compute image list \
    --compartment-id "$TENANCY_OCID" \
    --operating-system "Canonical Ubuntu" \
    --operating-system-version "20.04" \
    --shape "VM.Standard.A1.Flex" \
    --query 'data[0].[display-name,id]' \
    --output table 2>/dev/null

echo ""
echo "==================================="
echo "✅ Готово!"
echo ""
echo "📝 Скопіюйте потрібні OCID в GitHub Secrets"
echo "==================================="
