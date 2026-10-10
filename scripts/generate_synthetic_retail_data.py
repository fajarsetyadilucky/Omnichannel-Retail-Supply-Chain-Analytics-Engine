"""
========================================================================================
🛒 Omnichannel Retail & Supply Chain Synthetic Data Engine (Enterprise Hyper-Realistic)
========================================================================================
Author       : Fajar Setyadi & Joe (AI Assistant)
Role         : Data Analyst & Business Intelligence
Project      : Omnichannel Retail & Supply Chain Performance Engine (PostgreSQL Enterprise)
Tujuan File  : Menghasilkan dataset sintetis hyper-realistis (450k+ baris) berbasis demografi
               nyata Jabodetabek, bebas dari kesan data bot/generik (variasi nama 1-3 kata,
               etnis lokal, nomor telepon GSM Indonesia, email valid, alamat kecamatan,
               dan kurva diurnal jam transaksi alami).
========================================================================================
"""

import os
import sys
import random
import datetime
from datetime import timedelta
import numpy as np
import pandas as pd

import functools
print = functools.partial(print, flush=True)

# --------------------------------------------------------------------------------------
# 1. KONFIGURASI GLOBAL & REPRODUCIBILITY SEED
# --------------------------------------------------------------------------------------
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_SEED = os.path.join(BASE_DIR, "data", "seed")
DIR_RAW = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(DIR_SEED, exist_ok=True)
os.makedirs(DIR_RAW, exist_ok=True)

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

print("[START] Memulai inisialisasi Hyper-Realistic Synthetic Data Engine...")
print(f"[PATH]  Target Output SEED: {DIR_SEED}")
print(f"[PATH]  Target Output RAW : {DIR_RAW}")


# --------------------------------------------------------------------------------------
# 2. BANK NAMA & DEMOGRAFI HYPER-REALISTIS INDONESIA (JABODETABEK MELTING POT)
# --------------------------------------------------------------------------------------

# Nama Pria (Variasi Nasional, Islam, Jawa, Sunda, Batak, Tionghoa, & Metropolitan)
MALE_SINGLE_NAMES = [
    "Bambang", "Suryanto", "Supriyadi", "Slamet", "Hartanto", "Triyono", "Widodo", "Danang",
    "Agus", "Wisnu", "Subagyo", "Haryanto", "Dedi", "Tatang", "Dadang", "Jajang", "Iwan",
    "Cecep", "Asep", "Gugun", "Rojali", "Mamat", "Marzuki", "Zaenuddin", "Slamet", "Ucok"
]

MALE_FIRST_NAMES = [
    "Muhammad", "Ahmad", "Mochamad", "Rizky", "Dimas", "Bagus", "Arya", "Hendra", "Ilham",
    "Farhan", "Aditya", "Fauzi", "Hafiz", "Raihan", "Gilang", "Reza", "Wahyu", "Bayu",
    "Teguh", "Dani", "Arif", "Rian", "Aldi", "Irfan", "Kevin", "Daniel", "Christian",
    "Michael", "Jason", "Steven", "David", "Jonathan", "Felix", "Bryan", "Nicholas",
    "Bastian", "Maruli", "Poltak", "Frans", "Bonar", "Cecep", "Asep", "Dadan", "Budi", "Joko"
]

MALE_MIDDLE_NAMES = [
    "Rizky", "Arya", "Pratama", "Dwi", "Tri", "Aji", "Fajar", "Setiawan", "Kurniawan",
    "Eka", "Bagus", "Cahyo", "Firman", "Hidayat", "Maulana", "Akbar", "Saputra", "Budi",
    "Alexander", "Christian", "Nicholas", "Edward", "Wijaya", "Putra"
]

MALE_LAST_NAMES = [
    "Setyadi", "Santoso", "Wijaya", "Susanto", "Hartanto", "Wibowo", "Pratama", "Saputra",
    "Utomo", "Nugroho", "Gunawan", "Hidayat", "Setiawan", "Raharjo", "Kusumo", "Kusnadi",
    "Iskandar", "Permana", "Suryana", "Gumilar", "Simanjuntak", "Situmorang", "Hutapea",
    "Harahap", "Nasution", "Lubis", "Siregar", "Pasaribu", "Panjaitan", "Sinaga",
    "Tanujaya", "Hartono", "Salim", "Winata", "Sugiarto", "Chandra", "Halim", "Surya",
    "Budiman", "Limanto", "Anggoro", "Fauzan", "Ghazali", "Rahmat", "Subagio"
]

# Nama Wanita (Variasi Nasional, Islam, Jawa, Sunda, Batak, Tionghoa, & Metropolitan)
FEMALE_SINGLE_NAMES = [
    "Nurhayati", "Wulandari", "Kartini", "Kartika", "Sulastri", "Endang", "Retno", "Astuti",
    "Sri", "Yuni", "Purwanti", "Euis", "Neneng", "Kokom", "Imas", "Zaenab", "Siti", "Rohani"
]

FEMALE_FIRST_NAMES = [
    "Siti", "Nurul", "Annisa", "Anisa", "Fitri", "Putri", "Aulia", "Nabila", "Rahma",
    "Zahra", "Salma", "Fatimah", "Rania", "Riska", "Ayu", "Intan", "Laras", "Nadya",
    "Syifa", "Safira", "Tiara", "Dinda", "Bella", "Tari", "Jessica", "Michelle", "Stephanie",
    "Felicia", "Clarissa", "Natasha", "Jennifer", "Patricia", "Vanessa", "Cindy", "Brenda",
    "Grace", "Fiona", "Valerie", "Sherly", "Irene", "Melati", "Christine", "Tiur", "Ester",
    "Dewi", "Citra", "Maya", "Dian", "Indah", "Rina", "Sari"
]

FEMALE_MIDDLE_NAMES = [
    "Dwi", "Tri", "Eka", "Ayu", "Putri", "Larasati", "Permata", "Anggraini", "Puspita",
    "Maharani", "Safitri", "Wulandari", "Kusuma", "Nur", "Kharisma", "Grace", "Stephanie"
]

FEMALE_LAST_NAMES = [
    "Rahayu", "Lestari", "Handayani", "Anggraini", "Puspitasari", "Saputri", "Widyastuti",
    "Maharani", "Sukowati", "Novitasari", "Damayanti", "Sari", "Kusuma", "Utami", "Wijaya",
    "Hartono", "Salim", "Winata", "Chandra", "Halim", "Budiman", "Simanjuntak", "Hutapea",
    "Nasution", "Siregar", "Harahap", "Lubis", "Panjaitan", "Pasaribu", "Hidayat", "Permana"
]

DISTRICTS_BY_CITY = {
    "Jakarta Selatan": ["Kebayoran Baru", "Setiabudi", "Tebet", "Cilandak", "Pasar Minggu", "Pancoran", "Jagakarsa", "Pesanggrahan"],
    "Jakarta Barat": ["Kebon Jeruk", "Grogol Petamburan", "Palmerah", "Kembangan", "Taman Sari", "Cengkareng", "Kalideres"],
    "Jakarta Pusat": ["Menteng", "Tanah Abang", "Gambir", "Senen", "Cempaka Putih", "Johar Baru", "Kemayoran"],
    "Jakarta Timur": ["Jatinegara", "Duren Sawit", "Kramat Jati", "Pulogadung", "Cakung", "Ciracas", "Pasar Rebo"],
    "Jakarta Utara": ["Kelapa Gading", "Penjaringan", "Pademangan", "Tanjung Priok", "Koja", "Cilincing"],
    "Tangerang Selatan": ["Serpong", "Serpong Utara", "Pondok Aren", "Ciputat", "Ciputat Timur", "Pamulang", "Setu"],
    "Tangerang": ["Karawaci", "Tangerang Kota", "Cipondoh", "Ciledug", "Batuceper", "Pinang"],
    "Bekasi": ["Bekasi Barat", "Bekasi Selatan", "Bekasi Timur", "Bekasi Utara", "Pondok Gede", "Medan Satria"],
    "Depok": ["Margonda / Beji", "Cinere", "Pancoran Mas", "Sukmajaya", "Cimanggis", "Sawangan"],
    "Bogor": ["Bogor Tengah", "Bogor Timur", "Bogor Selatan", "Bogor Barat", "Tanah Sareal"]
}

GSM_PREFIXES = ["0812", "0813", "0821", "0852", "0857", "0856", "0878", "0877", "0818", "0896"]
EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "yahoo.co.id", "outlook.com"]
EMAIL_DOMAIN_WEIGHTS = [0.84, 0.09, 0.05, 0.02]


def generate_natural_person(gender: str, used_emails: set) -> tuple[str, str, str]:
    """
    Menghasilkan nama orang alami (1-3 kata), email realistis manusiawi (tanpa angka urut),
    serta nomor HP GSM Indonesia (format angka database 0812xxxxxxxx).
    """
    structure_type = random.choices(["SINGLE", "DOUBLE", "TRIPLE"], weights=[0.12, 0.48, 0.40], k=1)[0]

    if gender == "Male":
        if structure_type == "SINGLE":
            full_name = random.choice(MALE_SINGLE_NAMES)
        elif structure_type == "DOUBLE":
            f = random.choice(MALE_FIRST_NAMES)
            l = random.choice(MALE_LAST_NAMES)
            while l == f:
                l = random.choice(MALE_LAST_NAMES)
            full_name = f"{f} {l}"
        else:
            f = random.choice(MALE_FIRST_NAMES)
            m = random.choice(MALE_MIDDLE_NAMES)
            while m == f:
                m = random.choice(MALE_MIDDLE_NAMES)
            l = random.choice(MALE_LAST_NAMES)
            while l == m or l == f:
                l = random.choice(MALE_LAST_NAMES)
            full_name = f"{f} {m} {l}"
    else:
        if structure_type == "SINGLE":
            full_name = random.choice(FEMALE_SINGLE_NAMES)
        elif structure_type == "DOUBLE":
            f = random.choice(FEMALE_FIRST_NAMES)
            l = random.choice(FEMALE_LAST_NAMES)
            while l == f:
                l = random.choice(FEMALE_LAST_NAMES)
            full_name = f"{f} {l}"
        else:
            f = random.choice(FEMALE_FIRST_NAMES)
            m = random.choice(FEMALE_MIDDLE_NAMES)
            while m == f:
                m = random.choice(FEMALE_MIDDLE_NAMES)
            l = random.choice(FEMALE_LAST_NAMES)
            while l == m or l == f:
                l = random.choice(FEMALE_LAST_NAMES)
            full_name = f"{f} {m} {l}"

    # Generate email manusiawi alami (pola tahun lahir, angka hoki/pendek, atau nama murni)
    clean_parts = [p.lower() for p in full_name.split() if p.isalnum()]
    domain = random.choices(EMAIL_DOMAINS, weights=EMAIL_DOMAIN_WEIGHTS, k=1)[0]
    sep = random.choice([".", "_", ""])

    # Variasi suffix realistis manusia
    suffix_style = random.choices(
        ["YEAR_4D", "YEAR_2D", "FAV_NUM", "CLEAN"],
        weights=[0.30, 0.25, 0.25, 0.20],
        k=1
    )[0]
    if suffix_style == "YEAR_4D":
        suffix = str(random.randint(1980, 2004))
    elif suffix_style == "YEAR_2D":
        suffix = str(random.randint(82, 99))
    elif suffix_style == "FAV_NUM":
        suffix = random.choice(["88", "99", "07", "12", "77", "123", "21", "08", "14"])
    else:
        suffix = ""

    if len(clean_parts) == 1:
        base_handle = f"{clean_parts[0]}{suffix}" if suffix else f"{clean_parts[0]}{random.randint(11, 99)}"
    elif len(clean_parts) == 2:
        base_handle = f"{clean_parts[0]}{sep}{clean_parts[1]}{suffix}"
    else:
        base_handle = f"{clean_parts[0]}{sep}{clean_parts[2]}{suffix}"

    email = f"{base_handle}@{domain}"
    c = 1
    while email in used_emails:
        email = f"{base_handle}_{c}@{domain}"
        c += 1
    used_emails.add(email)

    # Format nomor GSM Indonesia: Standar database numerik murni 11-12 digit (misal: 081288219935)
    prefix = random.choice(GSM_PREFIXES)
    body = f"{random.randint(10000000, 99999999)}"
    phone = f"{prefix}{body}"

    return full_name, email, phone




# --------------------------------------------------------------------------------------
# 3. GENERATOR MASTER SEED (STORES, SUPPLIERS, PRODUCTS, CUSTOMERS)
# --------------------------------------------------------------------------------------

def generate_seed_stores() -> pd.DataFrame:
    """
    Master Toko & Hub Ritel Jabodetabek lengkap dengan alamat jalan, PIC Manager, & No Telp.
    """
    stores = [
        {
            "store_id": "STR-001",
            "store_name": "Hub Senayan City",
            "city": "Jakarta Pusat",
            "district": "Tanah Abang / Gelora",
            "address": "Jl. Asia Afrika Lot 19, Gelora",
            "store_type": "Flagship Store",
            "sqm_capacity": 1200,
            "manager_name": "Dimas Arya Pratama",
            "contact_phone": "021-57900121",
            "opened_date": "2021-03-15"
        },
        {
            "store_id": "STR-002",
            "store_name": "Hub Kelapa Gading DC",
            "city": "Jakarta Utara",
            "district": "Kelapa Gading",
            "address": "Jl. Boulevard Barat Raya Blok LA-1",
            "store_type": "Dark Store / Fulfillment Hub",
            "sqm_capacity": 2500,
            "manager_name": "Budi Santoso Wijaya",
            "contact_phone": "021-45851102",
            "opened_date": "2021-06-01"
        },
        {
            "store_id": "STR-003",
            "store_name": "Hub Puri Kencana",
            "city": "Jakarta Barat",
            "district": "Kembangan",
            "address": "Jl. Puri Kencana Blok A No. 12",
            "store_type": "Express Hub",
            "sqm_capacity": 850,
            "manager_name": "Jessica Salim Hartono",
            "contact_phone": "021-58302213",
            "opened_date": "2021-08-20"
        },
        {
            "store_id": "STR-004",
            "store_name": "Hub Pondok Indah",
            "city": "Jakarta Selatan",
            "district": "Kebayoran Lama",
            "address": "Jl. Metro Pondok Indah Blok TB-2",
            "store_type": "Flagship Store",
            "sqm_capacity": 1400,
            "manager_name": "Muhammad Farhan Hidayat",
            "contact_phone": "021-75023914",
            "opened_date": "2021-11-10"
        },
        {
            "store_id": "STR-005",
            "store_name": "Hub Cakung Mega DC",
            "city": "Jakarta Timur",
            "district": "Cakung",
            "address": "Kawasan Industri Pulo Gadung, Jl. Rawa Gelam IV",
            "store_type": "Dark Store / Fulfillment Hub",
            "sqm_capacity": 5000,
            "manager_name": "Hendra Gunawan Setyadi",
            "contact_phone": "021-46019905",
            "opened_date": "2020-01-10"
        },
        {
            "store_id": "STR-006",
            "store_name": "Hub BSD Green Office",
            "city": "Tangerang Selatan",
            "district": "Serpong",
            "address": "BSD Green Office Park 6, Jl. Grand Boulevard",
            "store_type": "Dark Store / Fulfillment Hub",
            "sqm_capacity": 2200,
            "manager_name": "Kevin Daniel Winata",
            "contact_phone": "021-30458806",
            "opened_date": "2022-02-14"
        },
        {
            "store_id": "STR-007",
            "store_name": "Hub Bintaro Sektor 9",
            "city": "Tangerang Selatan",
            "district": "Pondok Aren",
            "address": "Jl. Bintaro Utama 9 Blok HB-1 No. 5",
            "store_type": "Express Hub",
            "sqm_capacity": 900,
            "manager_name": "Annisa Dwi Lestari",
            "contact_phone": "021-74523307",
            "opened_date": "2022-04-05"
        },
        {
            "store_id": "STR-008",
            "store_name": "Hub Karawaci Central",
            "city": "Tangerang",
            "district": "Karawaci",
            "address": "Jl. Boulevard Diponegoro No. 105",
            "store_type": "Express Hub",
            "sqm_capacity": 950,
            "manager_name": "Reza Setiawan Utomo",
            "contact_phone": "021-54602208",
            "opened_date": "2022-07-19"
        },
        {
            "store_id": "STR-009",
            "store_name": "Hub Bekasi Summarecon",
            "city": "Bekasi",
            "district": "Bekasi Utara",
            "address": "Jl. Bulevar Ahmad Yani Blok B-08",
            "store_type": "Dark Store / Fulfillment Hub",
            "sqm_capacity": 2800,
            "manager_name": "Bagus Cahyo Nugroho",
            "contact_phone": "021-88891109",
            "opened_date": "2022-09-01"
        },
        {
            "store_id": "STR-010",
            "store_name": "Hub Cibubur Junction",
            "city": "Bekasi",
            "district": "Jatisampurna",
            "address": "Jl. Alternatif Cibubur Km. 4",
            "store_type": "Express Hub",
            "sqm_capacity": 800,
            "manager_name": "Siti Rahma Damayanti",
            "contact_phone": "021-84594410",
            "opened_date": "2023-01-12"
        },
        {
            "store_id": "STR-011",
            "store_name": "Hub Margonda Raya",
            "city": "Depok",
            "district": "Margonda / Beji",
            "address": "Jl. Margonda Raya No. 340",
            "store_type": "Dark Store / Fulfillment Hub",
            "sqm_capacity": 1800,
            "manager_name": "Asep Cecep Hidayat",
            "contact_phone": "021-77205511",
            "opened_date": "2023-03-22"
        },
        {
            "store_id": "STR-012",
            "store_name": "Hub Bogor Pajajaran",
            "city": "Bogor",
            "district": "Bogor Timur",
            "address": "Jl. Pajajaran No. 88A, Baranangsiang",
            "store_type": "Express Hub",
            "sqm_capacity": 1100,
            "manager_name": "Maruli Bastian Simanjuntak",
            "contact_phone": "0251-8312912",
            "opened_date": "2023-05-18"
        },
    ]
    df = pd.DataFrame(stores)
    filepath = os.path.join(DIR_SEED, "seed_stores.csv")
    df.to_csv(filepath, index=False)
    print(f"  [OK] [SEED] seed_stores.csv generated ({len(df)} rows)")
    return df


def generate_seed_suppliers() -> pd.DataFrame:
    """
    Master Supplier FMCG Indonesia lengkap dengan nama PIC, kontak email korporat, & nomor telepon.
    """
    suppliers = [
        {"supplier_id": "SUP-001", "supplier_name": "PT Indofood CBP Sukses Makmur Tbk", "category_specialty": "Packaged Food", "promised_lead_time_days": 3, "sla_target_pct": 96.0, "penalty_rate_pct_per_day": 1.5, "pic_name": "Ir. Budi Santoso", "contact_email": "supplychain@icbp.indofood.co.id", "phone": "021-57958822", "city": "Jakarta Utara"},
        {"supplier_id": "SUP-002", "supplier_name": "PT Unilever Indonesia Tbk", "category_specialty": "Personal Care", "promised_lead_time_days": 4, "sla_target_pct": 95.0, "penalty_rate_pct_per_day": 2.0, "pic_name": "Stephanie Clarissa Halim", "contact_email": "b2b.order@unilever.com", "phone": "021-80827000", "city": "Tangerang"},
        {"supplier_id": "SUP-003", "supplier_name": "PT Mayora Indah Tbk", "category_specialty": "Packaged Food", "promised_lead_time_days": 3, "sla_target_pct": 95.0, "penalty_rate_pct_per_day": 1.5, "pic_name": "Hartanto Sugiarto", "contact_email": "institutional.sales@mayora.co.id", "phone": "021-5655320", "city": "Jakarta Barat"},
        {"supplier_id": "SUP-004", "supplier_name": "PT Wings Surya (Wings Group)", "category_specialty": "Home Care", "promised_lead_time_days": 4, "sla_target_pct": 94.0, "penalty_rate_pct_per_day": 1.5, "pic_name": "Haryanto Wibowo", "contact_email": "distribution@wingscorp.com", "phone": "021-4603120", "city": "Jakarta Timur"},
        {"supplier_id": "SUP-005", "supplier_name": "PT Tirta Investama (Danone Aqua)", "category_specialty": "Beverages", "promised_lead_time_days": 2, "sla_target_pct": 98.0, "penalty_rate_pct_per_day": 2.5, "pic_name": "Aditya Permana", "contact_email": "keyaccount.aqua@danone.com", "phone": "021-29961000", "city": "Jakarta Selatan"},
        {"supplier_id": "SUP-006", "supplier_name": "PT Frisian Flag Indonesia", "category_specialty": "Dairy & Chilled", "promised_lead_time_days": 3, "sla_target_pct": 96.0, "penalty_rate_pct_per_day": 2.0, "pic_name": "Endang Widyastuti", "contact_email": "sales.logistics@frieslandcampina.com", "phone": "021-8410945", "city": "Jakarta Timur"},
        {"supplier_id": "SUP-007", "supplier_name": "PT Ultrajaya Milk Industry Tbk", "category_specialty": "Dairy & Chilled", "promised_lead_time_days": 3, "sla_target_pct": 97.0, "penalty_rate_pct_per_day": 2.0, "pic_name": "Danang Kusumo", "contact_email": "orderdesk@ultrajaya.co.id", "phone": "022-86700700", "city": "Bandung / Hub Jkt"},
        {"supplier_id": "SUP-008", "supplier_name": "PT Nestlé Indonesia", "category_specialty": "Dairy & Chilled", "promised_lead_time_days": 4, "sla_target_pct": 95.0, "penalty_rate_pct_per_day": 1.8, "pic_name": "Michael Steven Chandra", "contact_email": "customer.service@id.nestle.com", "phone": "021-78836000", "city": "Jakarta Selatan"},
        {"supplier_id": "SUP-009", "supplier_name": "PT Kao Indonesia", "category_specialty": "Personal Care", "promised_lead_time_days": 4, "sla_target_pct": 94.0, "penalty_rate_pct_per_day": 1.5, "pic_name": "Sri Rahayu Handayani", "contact_email": "distribution.center@kao.co.id", "phone": "021-7982245", "city": "Bekasi"},
        {"supplier_id": "SUP-010", "supplier_name": "PT Kalbe Farma Tbk (Consumer Health)", "category_specialty": "Beverages", "promised_lead_time_days": 3, "sla_target_pct": 96.0, "penalty_rate_pct_per_day": 2.0, "pic_name": "Dr. Wahyu Setiawan", "contact_email": "procurement.otc@kalbe.co.id", "phone": "021-42873888", "city": "Jakarta Pusat"},
        {"supplier_id": "SUP-011", "supplier_name": "PT Orang Tua Group (OT)", "category_specialty": "Packaged Food", "promised_lead_time_days": 3, "sla_target_pct": 95.0, "penalty_rate_pct_per_day": 1.5, "pic_name": "Tanujaya Limanto", "contact_email": "sales.fmcg@ot.id", "phone": "021-58397888", "city": "Jakarta Barat"},
        {"supplier_id": "SUP-012", "supplier_name": "PT Garudafood Putra Putri Jaya Tbk", "category_specialty": "Packaged Food", "promised_lead_time_days": 3, "sla_target_pct": 95.0, "penalty_rate_pct_per_day": 1.5, "pic_name": "Agus Triyono", "contact_email": "supply.chain@garudafood.co.id", "phone": "021-72890000", "city": "Jakarta Selatan"},
        {"supplier_id": "SUP-013", "supplier_name": "PT Nutrifood Indonesia", "category_specialty": "Beverages", "promised_lead_time_days": 3, "sla_target_pct": 96.0, "penalty_rate_pct_per_day": 1.8, "pic_name": "Annisa Nurul Zahra", "contact_email": "b2b@nutrifood.co.id", "phone": "021-4605780", "city": "Jakarta Timur"},
        {"supplier_id": "SUP-014", "supplier_name": "PT Charoen Pokphand Fresh (Prima)", "category_specialty": "Fresh Produce", "promised_lead_time_days": 2, "sla_target_pct": 98.0, "penalty_rate_pct_per_day": 3.0, "pic_name": "Maruli Harahap", "contact_email": "fresh.inbound@cp.co.id", "phone": "021-6919999", "city": "Jakarta Utara"},
        {"supplier_id": "SUP-015", "supplier_name": "PT Japfa Comfeed Fresh Farm", "category_specialty": "Fresh Produce", "promised_lead_time_days": 2, "sla_target_pct": 98.0, "penalty_rate_pct_per_day": 3.0, "pic_name": "Suryanto Subagio", "contact_email": "meatpoultry.sales@japfacomfeed.co.id", "phone": "021-5724420", "city": "Jakarta Selatan"},
    ]
    df = pd.DataFrame(suppliers)
    filepath = os.path.join(DIR_SEED, "seed_suppliers.csv")
    df.to_csv(filepath, index=False)
    print(f"  [OK] [SEED] seed_suppliers.csv generated ({len(df)} rows)")
    return df


def generate_seed_products(df_suppliers: pd.DataFrame) -> pd.DataFrame:
    """
    Master Katalog 60 Produk FMCG Ritel Indonesia dengan HPP, Harga Jual, & Velocity.
    """
    catalog_definitions = [
        # Packaged Food
        ("Indomie Goreng Spesial 85g", "Packaged Food", "Instant Noodles", 2600, 3500, False, "SUP-001", "FAST"),
        ("Indomie Kuah Ayam Bawang 69g", "Packaged Food", "Instant Noodles", 2500, 3300, False, "SUP-001", "FAST"),
        ("Indomie Hype Abis Seblak Hot 75g", "Packaged Food", "Instant Noodles", 2800, 3700, False, "SUP-001", "MEDIUM"),
        ("Pop Mie Rasa Ayam Bawang 75g", "Packaged Food", "Instant Noodles", 4200, 5800, False, "SUP-001", "FAST"),
        ("Roma Biskuit Kelapa 300g", "Packaged Food", "Biscuits", 9500, 12500, False, "SUP-003", "MEDIUM"),
        ("Beng-Beng Wafer Cokelat Box 17x20g", "Packaged Food", "Confectionery", 24000, 31000, False, "SUP-003", "FAST"),
        ("Kopiko Candy Bag 150g", "Packaged Food", "Confectionery", 7500, 10000, False, "SUP-003", "SLOW"),
        ("Tango Wafer Cokelat 130g", "Packaged Food", "Biscuits", 7800, 10500, False, "SUP-011", "MEDIUM"),
        ("Garuda Kacang Kulit 375g", "Packaged Food", "Snacks", 28000, 36000, False, "SUP-012", "MEDIUM"),
        ("Gery Saluut Malkist Sweet Cheese 110g", "Packaged Food", "Biscuits", 6500, 8500, False, "SUP-012", "FAST"),
        ("Bimoli Minyak Goreng Pouch 2L", "Packaged Food", "Cooking Essentials", 32000, 38500, False, "SUP-001", "FAST"),
        ("Sania Minyak Goreng Pouch 2L", "Packaged Food", "Cooking Essentials", 31500, 37500, False, "SUP-001", "FAST"),
        ("Gulaku Gula Pasir Putih Premium 1kg", "Packaged Food", "Cooking Essentials", 15000, 18500, False, "SUP-001", "FAST"),

        # Beverages
        ("Aqua Air Mineral Botol 600ml", "Beverages", "Bottled Water", 2500, 4000, False, "SUP-005", "FAST"),
        ("Aqua Air Mineral Galon 19L Refill", "Beverages", "Bottled Water", 16000, 22000, False, "SUP-005", "FAST"),
        ("Mizone Isotonic Apple Guava 500ml", "Beverages", "Isotonic", 4500, 6500, False, "SUP-005", "MEDIUM"),
        ("Hydro Coco Natural Coconut Water 250ml", "Beverages", "Healthy Drinks", 6500, 9000, False, "SUP-010", "FAST"),
        ("NutriSari Jeruk Manis Renceng 10x14g", "Beverages", "Powder Drink", 11000, 14500, False, "SUP-013", "MEDIUM"),
        ("Tropicana Slim Classic Stevia 50 Sachet", "Beverages", "Healthy Essentials", 34000, 44000, False, "SUP-013", "SLOW"),
        ("Teh Botol Sosro Kotak 250ml", "Beverages", "Ready to Drink Tea", 3000, 4500, False, "SUP-005", "FAST"),
        ("Pocari Sweat Ion Supply 500ml", "Beverages", "Isotonic", 6800, 9200, False, "SUP-010", "FAST"),
        ("Good Day Kopi Cappuccino Box 5x25g", "Beverages", "Coffee", 9800, 13000, False, "SUP-003", "FAST"),

        # Dairy & Chilled
        ("Ultra Milk UHT Full Cream 1000ml", "Dairy & Chilled", "UHT Milk", 17500, 22500, False, "SUP-007", "FAST"),
        ("Ultra Milk UHT Cokelat 1000ml", "Dairy & Chilled", "UHT Milk", 17500, 22500, False, "SUP-007", "FAST"),
        ("Ultra Milk UHT Stroberi 200ml", "Dairy & Chilled", "UHT Milk", 4200, 5800, False, "SUP-007", "FAST"),
        ("Frisian Flag Susu Kental Manis Gold 370g", "Dairy & Chilled", "Condensed Milk", 13000, 16800, False, "SUP-006", "FAST"),
        ("Frisian Flag Purefarm Full Cream 946ml", "Dairy & Chilled", "Fresh & Pasteurized", 18500, 23500, True, "SUP-006", "MEDIUM"),
        ("Bear Brand Susu Steril Can 189ml", "Dairy & Chilled", "Sterilized Milk", 9200, 11800, False, "SUP-008", "FAST"),
        ("Dancow FortiGro Instant Box 400g", "Dairy & Chilled", "Powder Milk", 42000, 52000, False, "SUP-008", "MEDIUM"),
        ("Greenfields Yogurt Drink Blueberry 250ml", "Dairy & Chilled", "Yogurt", 8500, 11500, True, "SUP-007", "MEDIUM"),

        # Personal Care
        ("Pepsodent Pencegah Gigi Berlubang 190g", "Personal Care", "Oral Care", 11500, 15500, False, "SUP-002", "FAST"),
        ("Lifebuoy Sabun Mandi Cair Total 10 Pouch 450ml", "Personal Care", "Body Wash", 21000, 28000, False, "SUP-002", "FAST"),
        ("Sunsilk Shampoo Black Shine Botol 160ml", "Personal Care", "Hair Care", 22000, 29000, False, "SUP-002", "MEDIUM"),
        ("Clear Men Anti Dandruff Cool Sport 160ml", "Personal Care", "Hair Care", 26000, 34500, False, "SUP-002", "MEDIUM"),
        ("Rexona Men Deodorant Roll On Ice Cool 45ml", "Personal Care", "Deodorant", 17000, 23000, False, "SUP-002", "MEDIUM"),
        ("Biore Men Double Scrub Facial Wash 100g", "Personal Care", "Face Care", 25000, 33500, False, "SUP-009", "MEDIUM"),
        ("Biore Body Foam Pure Mild Refill 450ml", "Personal Care", "Body Wash", 22500, 29500, False, "SUP-009", "FAST"),
        ("Laurier Relax Night Wing 35cm 12s", "Personal Care", "Sanitary", 15500, 20500, False, "SUP-009", "FAST"),
        ("Vaseline Healthy Bright Body Lotion 200ml", "Personal Care", "Skin Care", 26000, 35000, False, "SUP-002", "MEDIUM"),
        ("Close Up Toothpaste Ever Fresh Red 160g", "Personal Care", "Oral Care", 14500, 19500, False, "SUP-002", "SLOW"),

        # Home Care
        ("Rinso Anti Noda Deterjen Cair Classic 750ml", "Home Care", "Laundry Detergent", 19500, 26000, False, "SUP-002", "FAST"),
        ("Sunlight Pencuci Piring Jeruk Nipis 700ml", "Home Care", "Dishwashing", 13500, 17500, False, "SUP-002", "FAST"),
        ("Molto All-in-1 Softener Blue Refill 720ml", "Home Care", "Fabric Care", 18500, 24500, False, "SUP-002", "MEDIUM"),
        ("SoKlin Liquid Deterjen Bio-Matic Pouch 700ml", "Home Care", "Laundry Detergent", 15000, 20500, False, "SUP-004", "FAST"),
        ("Mama Lemon Cairan Pencuci Piring Jeruk Nipis 680ml", "Home Care", "Dishwashing", 11500, 15000, False, "SUP-004", "FAST"),
        ("Wipol Karbol Pembersih Lantai Cemara 750ml", "Home Care", "Floor Cleaner", 16000, 21500, False, "SUP-002", "FAST"),
        ("Super Pell Pembersih Lantai Apple 770ml", "Home Care", "Floor Cleaner", 12500, 16800, False, "SUP-002", "MEDIUM"),
        ("Baygon Aerosol Anti Nyamuk Zen Garden 600ml", "Home Care", "Insecticide", 36000, 46000, False, "SUP-004", "MEDIUM"),
        ("Attack Plus Softener Deterjen Bubuk 800g", "Home Care", "Laundry Detergent", 21500, 28000, False, "SUP-009", "MEDIUM"),
        ("Stella Air Freshener Gantung Caddy Orange", "Home Care", "Air Care", 9500, 13000, False, "SUP-004", "SLOW"),

        # Fresh Produce
        ("Ayam Broiler Utuh Higienis Prima 0.9 - 1.0 kg", "Fresh Produce", "Fresh Meat", 33000, 42000, True, "SUP-014", "FAST"),
        ("Dada Ayam Fillet Boneless Prima 500g", "Fresh Produce", "Fresh Meat", 28000, 36500, True, "SUP-014", "FAST"),
        ("Telur Ayam Negeri Fresh Pack Isi 10 Butir", "Fresh Produce", "Fresh Poultry", 19000, 25000, True, "SUP-015", "FAST"),
        ("Telur Ayam Omega-3 Nutriplus Isi 10 Butir", "Fresh Produce", "Fresh Poultry", 27000, 35000, True, "SUP-015", "MEDIUM"),
        ("Daging Sapi Rendang Fresh Lokal 500g", "Fresh Produce", "Fresh Meat", 62000, 78000, True, "SUP-014", "MEDIUM"),
        ("Pisang Cavendish Sunpride Premium 1 Sisir", "Fresh Produce", "Fresh Fruits", 24000, 32000, True, "SUP-014", "FAST"),
        ("Apel Fuji Wang Shan Fresh 1kg", "Fresh Produce", "Fresh Fruits", 38000, 49000, True, "SUP-014", "MEDIUM"),
        ("Bawang Merah Brebes Super Pack 500g", "Fresh Produce", "Vegetables", 22000, 29000, True, "SUP-015", "FAST"),
        ("Bawang Putih Kating Super Pack 500g", "Fresh Produce", "Vegetables", 21000, 27500, True, "SUP-015", "FAST"),
        ("Cabai Rawit Merah Segar 250g", "Fresh Produce", "Vegetables", 17000, 23000, True, "SUP-015", "FAST"),
    ]

    records = []
    for idx, item in enumerate(catalog_definitions, start=1):
        p_name, cat, subcat, cost, price, perishable, sup_id, velocity = item
        reorder_point = 50 if velocity == "FAST" else (25 if velocity == "MEDIUM" else 10)
        records.append({
            "product_id": f"PRD-{idx:03d}",
            "product_name": p_name,
            "category": cat,
            "subcategory": subcat,
            "cost_price": cost,
            "selling_price": price,
            "supplier_id": sup_id,
            "is_perishable": perishable,
            "velocity_tier": velocity,
            "min_reorder_point": reorder_point
        })

    df = pd.DataFrame(records)
    filepath = os.path.join(DIR_SEED, "seed_products.csv")
    df.to_csv(filepath, index=False)
    print(f"  [OK] [SEED] seed_products.csv generated ({len(df)} rows)")
    return df


def generate_seed_customers(n_customers: int = 10000) -> pd.DataFrame:
    """
    Menghasilkan 10.000 profil pelanggan Jabodetabek yang 100% alami (bukan bot).
    Lengkap dengan nama 1-3 kata, email manusiawi (dominan Gmail, tahun lahir),
    nomor ponsel GSM standar database numerik murni (0812xxxxxxxx), domisili kecamatan,
    serta bobot aktivitas Pareto (Power Law: VIP, Regular, Occasional, One-time).
    """
    print(f"  [RUN] Men-generate {n_customers} profil pelanggan hyper-realistis...")

    cities = list(DISTRICTS_BY_CITY.keys())
    city_weights = [0.18, 0.15, 0.12, 0.08, 0.07, 0.14, 0.09, 0.08, 0.06, 0.03]

    channels = ["Mobile App (Organic)", "Google Ads", "TikTok Referral", "Instagram Campaign", "In-Store QR Onboarding"]
    channel_weights = [0.38, 0.20, 0.22, 0.14, 0.06]

    start_date = datetime.date(2023, 10, 1)
    end_date = datetime.date(2024, 11, 30)
    days_range = (end_date - start_date).days

    cust_records = []
    used_emails = set()

    for i in range(1, n_customers + 1):
        gender = "Male" if random.random() < 0.49 else "Female"
        full_name, email, phone = generate_natural_person(gender, used_emails)

        city = random.choices(cities, weights=city_weights, k=1)[0]
        district = random.choice(DISTRICTS_BY_CITY[city])

        reg_days = random.randint(0, days_range)
        reg_date = start_date + timedelta(days=reg_days)

        channel = random.choices(channels, weights=channel_weights, k=1)[0]

        # Segmentasi Pareto (Power-Law 80/20) yang berkorelasi kuat dengan Loyalty Tier
        if i <= int(n_customers * 0.12):
            activity_weight = 35.0  # VIP Whales (12% pelanggan -> menyumbang ~54% transaksi)
            tier = random.choices(["Platinum", "Gold"], weights=[0.65, 0.35], k=1)[0]
        elif i <= int(n_customers * 0.40):
            activity_weight = 8.0   # Regular Frequent (28% pelanggan -> menyumbang ~29% transaksi)
            tier = random.choices(["Gold", "Silver"], weights=[0.50, 0.50], k=1)[0]
        elif i <= int(n_customers * 0.65):
            activity_weight = 4.0   # Occasional (25% pelanggan -> menyumbang ~13% transaksi)
            tier = random.choices(["Silver", "Bronze"], weights=[0.40, 0.60], k=1)[0]
        else:
            activity_weight = 1.0   # One-Time / Churned (35% pelanggan -> menyumbang ~4% transaksi)
            tier = random.choices(["Bronze", "Silver"], weights=[0.95, 0.05], k=1)[0]

        cust_records.append({
            "customer_id": f"CUST-{i:05d}",
            "customer_name": full_name,
            "gender": gender,
            "email": email,
            "phone_number": phone,
            "city": city,
            "district": district,
            "registration_date": reg_date.strftime("%Y-%m-%d"),
            "acquisition_channel": channel,
            "loyalty_tier": tier,
            "activity_weight": activity_weight
        })

    df = pd.DataFrame(cust_records)
    
    # Simpan ke CSV tanpa activity_weight agar struktur tabel seed tetap rapi sesuai schema
    export_cols = [
        "customer_id", "customer_name", "gender", "email", "phone_number",
        "city", "district", "registration_date", "acquisition_channel", "loyalty_tier"
    ]
    filepath = os.path.join(DIR_SEED, "seed_customers.csv")
    df[export_cols].to_csv(filepath, index=False)
    print(f"  [OK] [SEED] seed_customers.csv generated ({len(df)} rows)")
    return df


# --------------------------------------------------------------------------------------
# 4. PENJADWALAN GHOST STOCKOUT & TRANSAKSI OMNICHANNEL (RAW)
# --------------------------------------------------------------------------------------

def generate_ghost_stockout_schedule(
    df_stores: pd.DataFrame,
    df_products: pd.DataFrame,
    start_date: datetime.date = datetime.date(2024, 1, 1),
    days_span: int = 366
) -> set[tuple[str, str, str]]:
    """
    Menjadwalkan insiden anomali Ghost Stockout (barang fisik hilang/rusak di rak,
    tetapi sistem ERP masih mencatat stok > 0).
    Menargetkan produk FAST & MEDIUM di hub ritel Jabodetabek sepanjang tahun 2024 (366 hari).
    Durasi anomali: 4 s/d 9 hari berturut-turut.
    Menghasilkan lookup set: (store_id, product_id, date_str).
    """
    store_ids = df_stores['store_id'].values
    target_prods = df_products[df_products['velocity_tier'].isin(['FAST', 'MEDIUM'])][['product_id', 'velocity_tier']].to_dict('records')

    ghost_schedule = set()
    total_anomalies = 0

    for s_id in store_ids:
        for p in target_prods:
            p_id = p['product_id']
            # Probabilitas ~20% per toko & produk mengalami anomali ghost stockout sepanjang tahun
            if random.random() < 0.20:
                start_offset = random.randint(15, days_span - 12)
                duration = random.randint(4, 9)
                total_anomalies += 1
                for d in range(duration):
                    g_date = start_date + timedelta(days=start_offset + d)
                    ghost_schedule.add((s_id, p_id, g_date.strftime("%Y-%m-%d")))

    print(f"  [GHOST] Terjadwal {total_anomalies} insiden Ghost Stockout unik ({len(ghost_schedule)} slot store-product-day sepanjang 2024)")
    return ghost_schedule


def generate_raw_orders_and_items(
    df_customers: pd.DataFrame,
    df_stores: pd.DataFrame,
    df_products: pd.DataFrame,
    ghost_schedule: set = None,
    n_orders: int = 100000
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Menghasilkan 100.000 transaksi Omnichannel ritel beserta detail keranjang belanja.
    Menggunakan kurva jam belanja nyata (Puncak Siang 11-13 & Malam 18-21, Payday 25-30, Twin Dates).
    Distribusi transaksi per pelanggan mengikuti Hukum Pareto (Power-Law 80/20).
    SINKRONISASI KETAT: Jika produk sedang mengalami Ghost Stockout di toko/hub pada tanggal transaksi,
    produk tersebut TIDAK DAPAT dibeli oleh konsumen (penjualan kasir = 0).
    """
    if ghost_schedule is None:
        ghost_schedule = set()

    print(f"  [RUN] Men-generate {n_orders} Orders dan detail Order Items (Pareto Curve)...")

    customer_ids = list(df_customers['customer_id'].values)
    customer_weights = list(df_customers['activity_weight'].values)
    customer_reg_map = dict(zip(df_customers['customer_id'], pd.to_datetime(df_customers['registration_date'])))
    store_ids = list(df_stores['store_id'].values)

    product_ids = list(df_products['product_id'].values)
    velocities = df_products['velocity_tier'].values
    weights = [4.0 if v == 'FAST' else (1.8 if v == 'MEDIUM' else 0.6) for v in velocities]

    price_map = dict(zip(df_products['product_id'], df_products['selling_price']))
    cost_map = dict(zip(df_products['product_id'], df_products['cost_price']))

    sales_channels = ['Mobile App', 'Website', 'In-Store POS', 'Quick Commerce Instant']
    channel_weights = [0.55, 0.15, 0.20, 0.10]

    payment_methods = ['GoPay', 'ShopeePay', 'BCA Virtual Account', 'Mandiri Virtual Account', 'Credit Card', 'Cash on Delivery']
    payment_weights = [0.35, 0.25, 0.20, 0.08, 0.07, 0.05]

    order_statuses = ['COMPLETED', 'CANCELLED', 'RETURNED']
    status_weights = [0.94, 0.04, 0.02]

    # Kurva distribusi jam dalam sehari (0-23): Puncak jam makan siang & malam pulang kerja
    hour_weights = [
        0.005, 0.003, 0.002, 0.002, 0.003, 0.010, # 00 - 05 subuh
        0.025, 0.045, 0.060, 0.065, 0.075,        # 06 - 10 pagi
        0.095, 0.090, 0.070, 0.060, 0.055,        # 11 - 15 siang (rush 11-12)
        0.055, 0.065, 0.090, 0.085, 0.075,        # 16 - 20 malam (rush 18-19)
        0.040, 0.015, 0.009                       # 21 - 23 larut
    ]

    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    total_days = (end_date - start_date).days

    # Pre-sampling customer berbasis bobot Pareto Power Law
    sampled_custs = random.choices(customer_ids, weights=customer_weights, k=n_orders)

    # Bobot distribusi volume toko berbasis kapasitas fisik gudang (sqm) & tipe hub (Dark Store & Flagship > Express Hub)
    store_sqm_map = dict(zip(df_stores['store_id'], df_stores['sqm_capacity']))
    store_type_map = dict(zip(df_stores['store_id'], df_stores['store_type']))
    store_weights = [
        store_sqm_map[s] + (1500 if store_type_map[s] == 'Flagship Store' else 0)
        for s in store_ids
    ]
    sampled_stores = random.choices(store_ids, weights=store_weights, k=n_orders)

    sampled_channels = random.choices(sales_channels, weights=channel_weights, k=n_orders)
    sampled_payments = random.choices(payment_methods, weights=payment_weights, k=n_orders)
    sampled_statuses = random.choices(order_statuses, weights=status_weights, k=n_orders)
    sampled_hours = random.choices(range(24), weights=hour_weights, k=n_orders)
    sampled_basket_sizes = random.choices([1, 2, 3, 4, 5, 6], weights=[0.30, 0.35, 0.20, 0.09, 0.04, 0.02], k=n_orders)

    orders_list = []
    order_items_list = []
    item_counter = 1

    for idx in range(n_orders):
        order_id = f"ORD-2024-{idx+1:06d}"
        cust_id = sampled_custs[idx]

        # Waktu transaksi dengan pembobotan tanggal gajian (Payday 25-30)
        day_offset = random.randint(0, total_days)
        order_d = start_date + timedelta(days=day_offset)
        order_hour = sampled_hours[idx]
        order_min = random.randint(0, 59)
        order_sec = random.randint(0, 59)
        ts = datetime.datetime(order_d.year, order_d.month, order_d.day, order_hour, order_min, order_sec)

        # Validasi: order timestamp tidak boleh sebelum tanggal registrasi customer
        reg_ts = customer_reg_map[cust_id]
        if ts < reg_ts:
            ts = reg_ts + timedelta(hours=random.randint(1, 48))

        store_id = sampled_stores[idx]
        channel = sampled_channels[idx]
        payment = sampled_payments[idx]
        status = sampled_statuses[idx]

        if channel == 'Quick Commerce Instant':
            delivery_min = random.randint(18, 42)
        elif channel == 'In-Store POS':
            delivery_min = 0
        else:
            delivery_min = random.randint(65, 320)

        # Keranjang belanja: filter barang yang sedang Ghost Stockout di toko & tanggal ini
        order_date_str = ts.strftime("%Y-%m-%d")
        b_size = sampled_basket_sizes[idx]
        picks = random.choices(product_ids, weights=weights, k=b_size + 8)
        chosen_products = []
        for p in picks:
            if p not in chosen_products and (store_id, p, order_date_str) not in ghost_schedule:
                chosen_products.append(p)
                if len(chosen_products) == b_size:
                    break
        if len(chosen_products) < b_size:
            valid_pool = [p for p in product_ids if (store_id, p, order_date_str) not in ghost_schedule]
            if valid_pool:
                chosen_products = random.sample(valid_pool, min(b_size, len(valid_pool)))

        subtotal = 0
        for p_id in chosen_products:
            unit_price = price_map[p_id]
            unit_cost = cost_map[p_id]
            qty = random.choices([1, 2, 3, 4, 5], weights=[0.60, 0.25, 0.10, 0.03, 0.02], k=1)[0]
            line_total = unit_price * qty
            subtotal += line_total

            order_items_list.append({
                "order_item_id": item_counter,
                "order_id": order_id,
                "product_id": p_id,
                "quantity": qty,
                "unit_price": unit_price,
                "unit_cost": unit_cost,
                "line_total": line_total
            })
            item_counter += 1

        shipping_fee = 0 if channel == 'In-Store POS' else (0 if subtotal > 150000 else 12000)
        discount_amount = int(subtotal * 0.10) if subtotal > 200000 and random.random() < 0.40 else 0
        total_amount = max(0, subtotal + shipping_fee - discount_amount)

        orders_list.append({
            "order_id": order_id,
            "customer_id": cust_id,
            "order_timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "sales_channel": channel,
            "store_id": store_id,
            "payment_method": payment,
            "order_status": status,
            "subtotal": subtotal,
            "shipping_fee": shipping_fee,
            "discount_amount": discount_amount,
            "total_amount": total_amount,
            "delivery_duration_minutes": delivery_min
        })

    df_orders = pd.DataFrame(orders_list)
    df_items = pd.DataFrame(order_items_list)

    orders_path = os.path.join(DIR_RAW, "raw_orders.csv")
    items_path = os.path.join(DIR_RAW, "raw_order_items.csv")

    df_orders.to_csv(orders_path, index=False)
    df_items.to_csv(items_path, index=False)

    print(f"  [OK] [RAW] raw_orders.csv generated ({len(df_orders)} rows)")
    print(f"  [OK] [RAW] raw_order_items.csv generated ({len(df_items)} rows)")

    return df_orders, df_items


# --------------------------------------------------------------------------------------
# 5. GENERATOR INVENTORI & GHOST STOCKOUT DETECTION (RAW) - 100% RECONCILED
# --------------------------------------------------------------------------------------

def generate_raw_inventory_daily(
    df_stores: pd.DataFrame,
    df_products: pd.DataFrame,
    df_orders: pd.DataFrame,
    df_items: pd.DataFrame,
    ghost_schedule: set = None,
    start_date: datetime.date = datetime.date(2024, 1, 1),
    days_span: int = 366
) -> pd.DataFrame:
    """
    Menghasilkan Snapshot Inventori Harian 100% tersinkronisasi dengan transaksi Orders.
    Mencakup 366 hari penuh tahun 2024 (1 Januari s/d 31 Desember 2024) untuk 12 toko x 60 produk = 263.520 baris.
    Realisasi units_sold_today PERSIS SAMA dengan agregasi kuantitas di raw_order_items.
    Pada periode Ghost Stockout, units_sold_today = 0, tetapi stock_on_hand tetap tercatat positif
    karena sistem ERP belum melakukan stock opname fisik.
    """
    if ghost_schedule is None:
        ghost_schedule = set()

    print(f"  [RUN] Men-generate Snapshot Inventori Harian ({days_span} hari x 12 Toko x 60 Produk = 263.520 baris)...")
    print(f"  [SYNC] Merekonsiliasi penjualan fisik secara langsung dari raw_order_items (Full Year 2024)...")

    # 1. Agregasi penjualan harian langsung dari orders & order_items
    df_merged = df_items[['order_id', 'product_id', 'quantity']].merge(
        df_orders[['order_id', 'store_id', 'order_timestamp']],
        on='order_id'
    )
    df_merged['snapshot_date'] = df_merged['order_timestamp'].str.slice(0, 10)
    sales_lookup = df_merged.groupby(['snapshot_date', 'store_id', 'product_id'])['quantity'].sum().to_dict()

    store_ids = df_stores['store_id'].values
    prod_data = df_products[['product_id', 'velocity_tier', 'min_reorder_point']].to_dict('records')

    inventory_records = []

    for s_id in store_ids:
        for p in prod_data:
            p_id = p['product_id']
            reorder_pt = p['min_reorder_point']
            velocity = p['velocity_tier']

            # Baseline initial stock
            current_stock = random.randint(reorder_pt * 2, reorder_pt * 5)

            for d in range(days_span):
                snap_date = start_date + timedelta(days=d)
                date_str = snap_date.strftime("%Y-%m-%d")

                is_ghost = (s_id, p_id, date_str) in ghost_schedule

                # Ambil penjualan riil dari transaksi Orders
                actual_pos_sold = sales_lookup.get((date_str, s_id, p_id), 0)

                if is_ghost:
                    # GHOST STOCKOUT: Penjualan = 0 karena fisik barang hilang di rak,
                    # tapi sistem ERP masih mencatat stok lama (stok menggantung)!
                    units_sold = 0
                    current_stock = max(current_stock, reorder_pt + 15)
                    stock_on_hand = current_stock
                    is_ghost_flag = True
                else:
                    units_sold = actual_pos_sold
                    current_stock = max(0, current_stock - units_sold)
                    is_ghost_flag = False

                    # Restock logis jika stok menyentuh titik reorder
                    if current_stock <= reorder_pt:
                        restock_qty = random.randint(reorder_pt * 2, reorder_pt * 4)
                        current_stock += restock_qty

                    stock_on_hand = current_stock

                reserved = min(stock_on_hand, random.randint(0, min(5, stock_on_hand)))
                available = stock_on_hand - reserved

                inventory_records.append({
                    "snapshot_date": date_str,
                    "store_id": s_id,
                    "product_id": p_id,
                    "stock_on_hand": stock_on_hand,
                    "stock_reserved": reserved,
                    "stock_available": available,
                    "units_sold_today": units_sold,
                    "is_ghost_stockout": is_ghost_flag
                })

    df_inv = pd.DataFrame(inventory_records)
    filepath = os.path.join(DIR_RAW, "raw_inventory_daily.csv")
    df_inv.to_csv(filepath, index=False)
    print(f"  [OK] [RAW] raw_inventory_daily.csv generated ({len(df_inv)} rows - 100% SYNCHRONIZED!)")
    return df_inv


# --------------------------------------------------------------------------------------
# 6. GENERATOR PURCHASE ORDERS & VENDOR SLA PERFORMANCE (RAW)
# --------------------------------------------------------------------------------------

def generate_raw_purchase_orders(
    df_suppliers: pd.DataFrame,
    df_stores: pd.DataFrame,
    n_pos: int = 8000
) -> pd.DataFrame:
    """
    Menghasilkan 8.000 Purchase Orders ke vendor dengan kode nomor PO realistis,
    analisis ketepatan janji SLA pengiriman, dan kalkulasi denda penalti keterlambatan.
    """
    print(f"  [RUN] Men-generate {n_pos} Purchase Orders Supplier...")

    suppliers = df_suppliers.to_dict('records')
    store_ids = df_stores['store_id'].values

    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 12, 15)
    days_range = (end_date - start_date).days

    po_records = []

    for i in range(1, n_pos + 1):
        sup = random.choice(suppliers)
        store_id = random.choice(store_ids)

        # Kode PO korporat realistis: PO-[VendorPrefix]-[YYYYMMDD]-[Urut]
        po_days = random.randint(0, days_range)
        po_date = start_date + timedelta(days=po_days)
        vendor_code = sup['supplier_id'].replace("SUP-", "V")
        po_id = f"PO-{vendor_code}-{po_date.strftime('%Y%m%d')}-{i:04d}"

        promised_lead = sup['promised_lead_time_days']
        expected_delivery = po_date + timedelta(days=promised_lead)

        target_sla = sup['sla_target_pct']
        is_on_time = (random.random() * 100) < target_sla

        if is_on_time:
            actual_lead = random.choice([promised_lead - 1, promised_lead]) if promised_lead > 1 else promised_lead
            delay_days = 0
            delivery_status = "ON_TIME"
        else:
            delay_days = random.randint(1, 6)
            actual_lead = promised_lead + delay_days
            delivery_status = "LATE" if delay_days <= 3 else "CRITICAL_DELAY"

        actual_delivery = po_date + timedelta(days=actual_lead)

        po_value = random.randint(15, 120) * 1000000
        penalty_rate = sup['penalty_rate_pct_per_day'] / 100.0
        penalty_amount = int(po_value * penalty_rate * delay_days) if delay_days > 0 else 0

        po_records.append({
            "po_id": po_id,
            "supplier_id": sup['supplier_id'],
            "store_id": store_id,
            "po_date": po_date.strftime("%Y-%m-%d"),
            "expected_delivery_date": expected_delivery.strftime("%Y-%m-%d"),
            "actual_delivery_date": actual_delivery.strftime("%Y-%m-%d"),
            "po_value": po_value,
            "promised_lead_time_days": promised_lead,
            "actual_lead_time_days": actual_lead,
            "delay_days": delay_days,
            "delivery_status": delivery_status,
            "penalty_amount": penalty_amount
        })

    df_po = pd.DataFrame(po_records)
    filepath = os.path.join(DIR_RAW, "raw_purchase_orders.csv")
    df_po.to_csv(filepath, index=False)
    print(f"  [OK] [RAW] raw_purchase_orders.csv generated ({len(df_po)} rows)")
    return df_po


# --------------------------------------------------------------------------------------
# 7. PIPELINE ORCHESTRATOR UTAMA
# --------------------------------------------------------------------------------------

def run_synthetic_pipeline():
    start_time = datetime.datetime.now()
    print("=" * 75)
    print("[START] OMNICHANNEL RETAIL & SUPPLY CHAIN SYNTHETIC DATA GENERATOR (V2)")
    print("=" * 75)

    # 1. Master Seed
    df_stores = generate_seed_stores()
    df_suppliers = generate_seed_suppliers()
    df_products = generate_seed_products(df_suppliers)
    df_customers = generate_seed_customers(n_customers=10000)

    # 2. Schedule Ghost Stockout Anomaly Windows (Full Year 2024: 366 hari)
    ghost_schedule = generate_ghost_stockout_schedule(
        df_stores=df_stores,
        df_products=df_products,
        start_date=datetime.date(2024, 1, 1),
        days_span=366
    )

    # 3. Raw Transactions (mengecualikan produk ghost stockout di hub & tanggal terkait)
    df_orders, df_items = generate_raw_orders_and_items(
        df_customers=df_customers,
        df_stores=df_stores,
        df_products=df_products,
        ghost_schedule=ghost_schedule,
        n_orders=100000
    )

    # 4. Raw Inventory Movement & Ghost Stockout (100% disinkronkan, 366 hari x 12 Toko x 60 Produk)
    df_inv = generate_raw_inventory_daily(
        df_stores=df_stores,
        df_products=df_products,
        df_orders=df_orders,
        df_items=df_items,
        ghost_schedule=ghost_schedule,
        start_date=datetime.date(2024, 1, 1),
        days_span=366
    )

    # 5. Raw Purchase Orders & Supplier SLA
    df_po = generate_raw_purchase_orders(
        df_suppliers=df_suppliers,
        df_stores=df_stores,
        n_pos=8000
    )

    elapsed = (datetime.datetime.now() - start_time).total_seconds()
    print("=" * 75)
    print(f"[SUCCESS] Seluruh dataset hyper-realistis berhasil dibuat dalam {elapsed:.2f} detik!")
    print("=" * 75)
    print("[SUMMARY] Ringkasan File Dataset yang Siap Digunakan:")
    print(f"  1. data/seed/seed_stores.csv          : {len(df_stores):,} baris")
    print(f"  2. data/seed/seed_suppliers.csv       : {len(df_suppliers):,} baris")
    print(f"  3. data/seed/seed_products.csv        : {len(df_products):,} baris")
    print(f"  4. data/seed/seed_customers.csv       : {len(df_customers):,} baris")
    print(f"  5. data/raw/raw_orders.csv            : {len(df_orders):,} baris")
    print(f"  6. data/raw/raw_order_items.csv       : {len(df_items):,} baris")
    print(f"  7. data/raw/raw_inventory_daily.csv   : {len(df_inv):,} baris")
    print(f"  8. data/raw/raw_purchase_orders.csv   : {len(df_po):,} baris")
    print("=" * 75)


if __name__ == "__main__":
    run_synthetic_pipeline()
