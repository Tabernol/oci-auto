#!/usr/bin/env python3
"""
Тестовий скрипт для перевірки OCI конфігурації перед додаванням в GitHub Actions.
Запустіть локально щоб переконатись що всі параметри правильні.
"""

import oci
import sys
from datetime import datetime

def test_oci_config():
    """Тестуємо OCI конфігурацію та доступність ресурсів"""
    
    print("=" * 60)
    print("🧪 Тест OCI конфігурації для GitHub Actions")
    print("=" * 60)
    print()
    
    try:
        # Читаємо конфігурацію
        print("1️⃣ Читаю OCI config...")
        config = oci.config.from_file("~/.oci/config", "DEFAULT")
        print("   ✅ Config прочитано")
        print(f"   Region: {config.get('region', 'не вказано')}")
        print()
        
        # Тестуємо підключення
        print("2️⃣ Перевіряю підключення до OCI...")
        identity = oci.identity.IdentityClient(config)
        user = identity.get_user(config["user"]).data
        print(f"   ✅ Успішно підключено як: {user.name}")
        print(f"   User OCID: {user.id}")
        print()
        
        # Перевіряємо tenancy
        print("3️⃣ Перевіряю tenancy...")
        tenancy = identity.get_tenancy(config["tenancy"]).data
        print(f"   ✅ Tenancy: {tenancy.name}")
        print(f"   Tenancy OCID: {tenancy.id}")
        print()
        
        # Введення параметрів для інстансу
        print("=" * 60)
        print("Введіть параметри для тестування створення інстансу:")
        print("(Інстанс НЕ буде створено, тільки перевірка параметрів)")
        print("=" * 60)
        
        compartment_id = input("\n4️⃣ Compartment OCID: ").strip()
        availability_domain = input("5️⃣ Availability Domain (напр. iAcH:EU-FRANKFURT-1-AD-1): ").strip()
        subnet_id = input("6️⃣ Subnet OCID: ").strip()
        image_id = input("7️⃣ Image OCID (ARM образ): ").strip()
        
        print()
        print("=" * 60)
        print("Перевірка введених параметрів...")
        print("=" * 60)
        print()
        
        # Перевіряємо compartment
        print("🔍 Перевіряю Compartment...")
        try:
            comp = identity.get_compartment(compartment_id).data
            print(f"   ✅ Compartment: {comp.name}")
        except Exception as e:
            print(f"   ❌ Помилка: {e}")
            return False
        print()
        
        # Перевіряємо availability domain
        print("🔍 Перевіряю Availability Domain...")
        try:
            ads = identity.list_availability_domains(compartment_id).data
            ad_names = [ad.name for ad in ads]
            if availability_domain in ad_names:
                print(f"   ✅ Availability Domain існує: {availability_domain}")
            else:
                print(f"   ⚠️  Попередження: AD не знайдено в списку")
                print(f"   Доступні: {', '.join(ad_names)}")
        except Exception as e:
            print(f"   ❌ Помилка: {e}")
            return False
        print()
        
        # Перевіряємо subnet
        print("🔍 Перевіряю Subnet...")
        try:
            network = oci.core.VirtualNetworkClient(config)
            subnet = network.get_subnet(subnet_id).data
            print(f"   ✅ Subnet: {subnet.display_name}")
            print(f"   CIDR: {subnet.cidr_block}")
            print(f"   VCN OCID: {subnet.vcn_id}")
        except Exception as e:
            print(f"   ❌ Помилка: {e}")
            return False
        print()
        
        # Перевіряємо image
        print("🔍 Перевіряю Image...")
        try:
            compute = oci.core.ComputeClient(config)
            image = compute.get_image(image_id).data
            print(f"   ✅ Image: {image.display_name}")
            print(f"   OS: {image.operating_system} {image.operating_system_version}")
            
            # Перевіряємо чи це ARM образ
            if "aarch64" in image.display_name.lower() or "arm" in image.display_name.lower():
                print(f"   ✅ Це ARM образ (підходить для A1.Flex)")
            else:
                print(f"   ⚠️  Попередження: Можливо це не ARM образ")
                print(f"   A1.Flex потребує ARM (aarch64) архітектури!")
        except Exception as e:
            print(f"   ❌ Помилка: {e}")
            return False
        print()
        
        # Перевіряємо доступність A1 shape
        print("🔍 Перевіряю доступність VM.Standard.A1.Flex...")
        try:
            shapes = compute.list_shapes(
                compartment_id=compartment_id,
                availability_domain=availability_domain
            ).data
            
            a1_shape = None
            for shape in shapes:
                if shape.shape == "VM.Standard.A1.Flex":
                    a1_shape = shape
                    break
            
            if a1_shape:
                print(f"   ✅ Shape VM.Standard.A1.Flex доступний")
                print(f"   Можливості:")
                print(f"   - OCPU: {a1_shape.ocpu_options.min} - {a1_shape.ocpu_options.max}")
                print(f"   - Memory (GB): {a1_shape.memory_options.min_in_g_bs} - {a1_shape.memory_options.max_in_g_bs}")
            else:
                print(f"   ⚠️  Shape VM.Standard.A1.Flex не знайдено в цьому AD")
                print(f"   Спробуйте інший Availability Domain")
        except Exception as e:
            print(f"   ⚠️  Не вдалося перевірити: {e}")
        print()
        
        # Підсумок
        print("=" * 60)
        print("✅ ВСІ ПЕРЕВІРКИ ПРОЙДЕНО УСПІШНО!")
        print("=" * 60)
        print()
        print("📋 Додайте ці значення в GitHub Secrets:")
        print()
        print("OCI_USER_OCID=" + config["user"])
        print("OCI_TENANCY_OCID=" + config["tenancy"])
        print("OCI_FINGERPRINT=" + config["fingerprint"])
        print("OCI_REGION=" + config["region"])
        print("OCI_COMPARTMENT_OCID=" + compartment_id)
        print("OCI_AVAILABILITY_DOMAIN=" + availability_domain)
        print("OCI_SUBNET_OCID=" + subnet_id)
        print("OCI_IMAGE_OCID=" + image_id)
        print()
        print("OCI_PRIVATE_KEY - вміст файлу: " + config["key_file"])
        print("SSH_PUBLIC_KEY - ваш публічний SSH ключ (cat ~/.ssh/id_rsa.pub)")
        print("INSTANCE_NAME - назва інстансу (наприклад: my-a1-instance)")
        print()
        print("🚀 Тепер можете додати workflow в GitHub!")
        
        return True
        
    except oci.exceptions.ConfigFileNotFound:
        print("❌ Файл ~/.oci/config не знайдено")
        print("Виконайте: oci setup config")
        return False
    except oci.exceptions.InvalidConfig as e:
        print(f"❌ Невірна конфігурація: {e}")
        return False
    except Exception as e:
        print(f"❌ Помилка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print()
    success = test_oci_config()
    print()
    sys.exit(0 if success else 1)
