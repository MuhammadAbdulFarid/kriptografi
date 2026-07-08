"""
=========================================================
KAMUS BAHASA ISYARAT DENGAN ALGORITMA GENETIKA (GA)
=========================================================
Tugas   : Implementasi Algoritma Genetika untuk mencari kata
          dalam kamus bahasa isyarat.
Metode  : Setiap kata dikodekan menjadi rangkaian biner ASCII
          (8 bit per huruf). GA digunakan untuk "mencari" /
          mencocokkan kata target melalui proses evolusi
          (populasi -> fitness -> seleksi roulette wheel ->
          crossover -> mutasi -> generasi baru).
=========================================================
"""

import random

# =========================================================
# 1. DATASET KAMUS BAHASA ISYARAT (minimal 10 data)
# =========================================================
kamus = [
    {"kata": "HALO",     "deskripsi": "Tangan terbuka diangkat setinggi bahu, digoyangkan ke kiri-kanan."},
    {"kata": "TERIMA",   "deskripsi": "Kedua tangan didekatkan ke dada seolah menerima sesuatu."},
    {"kata": "KASIH",    "deskripsi": "Tangan kanan menyentuh dagu lalu digerakkan ke depan (seperti meniup ciuman)."},
    {"kata": "TOLONG",   "deskripsi": "Tangan kanan mengepal di atas telapak tangan kiri, diangkat ke atas."},
    {"kata": "MAAF",     "deskripsi": "Tangan mengepal digosokkan melingkar di dada."},
    {"kata": "IYA",      "deskripsi": "Tangan mengepal, ibu jari ke atas, digerakkan naik turun (seperti mengangguk)."},
    {"kata": "TIDAK",    "deskripsi": "Jari telunjuk dan jari tengah dirapatkan ke ibu jari, dibuka-tutup seperti mulut bicara."},
    {"kata": "NAMA",     "deskripsi": "Jari telunjuk dan tengah kedua tangan disilangkan membentuk huruf N."},
    {"kata": "SAYA",     "deskripsi": "Telunjuk menunjuk ke dada sendiri."},
    {"kata": "KAMU",     "deskripsi": "Telunjuk menunjuk ke arah lawan bicara."},
    {"kata": "SELAMAT",  "deskripsi": "Kedua tangan mengepal diangkat lalu dibuka ke depan seperti gerakan merayakan."},
    {"kata": "PAGI",     "deskripsi": "Tangan kanan digerakkan dari bawah ke atas melewati lengan kiri, seperti matahari terbit."},
]

# =========================================================
# 2. FUNGSI ENCODING / DECODING (representasi biner ASCII)
# =========================================================
def encode_word(word):
    """Mengubah kata menjadi rangkaian biner (8 bit per karakter)."""
    return "".join(format(ord(c), "08b") for c in word.upper())

def decode_binary(binary_str):
    """Mengubah rangkaian biner kembali menjadi kata."""
    chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    return "".join(chr(int(c, 2)) for c in chars if len(c) == 8)

# =========================================================
# 3. STATE GLOBAL UNTUK MENYIMPAN HASIL SETIAP TAHAP GA
# =========================================================
GA = {
    "target_kata": None,
    "target_bin": None,
    "populasi": [],       # list of binary strings
    "fitness": [],        # list of int
    "probabilitas": [],   # probabilitas seleksi roulette
    "kumulatif": [],      # probabilitas kumulatif
    "mating_pool": [],    # individu hasil seleksi roulette
    "hasil_crossover": [],
    "hasil_mutasi": [],
    "generasi_baru": [],
    "generasi_ke": 0,
    "ukuran_populasi": 6,
    "mutation_rate": 0.03,
}

# =========================================================
# 4. FUNGSI-FUNGSI ALGORITMA GENETIKA
# =========================================================
def buat_populasi_awal(panjang_bit, ukuran):
    populasi = []
    for _ in range(ukuran):
        individu = "".join(random.choice("01") for _ in range(panjang_bit))
        populasi.append(individu)
    return populasi

def hitung_fitness(individu, target):
    """Fitness = jumlah bit yang sama dengan target (semakin besar semakin mirip)."""
    return sum(1 for a, b in zip(individu, target) if a == b)

def seleksi_roulette(populasi, fitness):
    total_fitness = sum(fitness)
    if total_fitness == 0:
        probabilitas = [1 / len(fitness)] * len(fitness)
    else:
        probabilitas = [f / total_fitness for f in fitness]

    kumulatif = []
    total = 0
    for p in probabilitas:
        total += p
        kumulatif.append(total)

    mating_pool = []
    for _ in range(len(populasi)):
        r = random.random()
        for i, batas in enumerate(kumulatif):
            if r <= batas:
                mating_pool.append(populasi[i])
                break
        else:
            mating_pool.append(populasi[-1])

    return probabilitas, kumulatif, mating_pool

def crossover(mating_pool):
    hasil = []
    pool = mating_pool.copy()
    random.shuffle(pool)
    for i in range(0, len(pool) - 1, 2):
        induk1, induk2 = pool[i], pool[i + 1]
        titik = random.randint(1, len(induk1) - 1)
        anak1 = induk1[:titik] + induk2[titik:]
        anak2 = induk2[:titik] + induk1[titik:]
        hasil.append((induk1, induk2, titik, anak1, anak2))
    if len(pool) % 2 == 1:
        hasil.append((pool[-1], pool[-1], 0, pool[-1], pool[-1]))
    return hasil

def mutasi(hasil_crossover, mutation_rate):
    hasil_mutasi = []
    for induk1, induk2, titik, anak1, anak2 in hasil_crossover:
        anak1_mutasi = list(anak1)
        anak2_mutasi = list(anak2)
        posisi_mutasi_1 = []
        posisi_mutasi_2 = []
        for i in range(len(anak1_mutasi)):
            if random.random() < mutation_rate:
                anak1_mutasi[i] = "1" if anak1_mutasi[i] == "0" else "0"
                posisi_mutasi_1.append(i)
        for i in range(len(anak2_mutasi)):
            if random.random() < mutation_rate:
                anak2_mutasi[i] = "1" if anak2_mutasi[i] == "0" else "0"
                posisi_mutasi_2.append(i)
        hasil_mutasi.append({
            "anak1_sebelum": anak1,
            "anak1_sesudah": "".join(anak1_mutasi),
            "posisi_mutasi_1": posisi_mutasi_1,
            "anak2_sebelum": anak2,
            "anak2_sesudah": "".join(anak2_mutasi),
            "posisi_mutasi_2": posisi_mutasi_2,
        })
    return hasil_mutasi

# =========================================================
# 5. FUNGSI-FUNGSI MENU
# =========================================================
def tampilkan_kamus():
    print("\n=== DAFTAR KAMUS BAHASA ISYARAT ===")
    print(f"{'No':<4}{'Kata':<12}{'Deskripsi Gerakan'}")
    print("-" * 70)
    for i, entri in enumerate(kamus, 1):
        print(f"{i:<4}{entri['kata']:<12}{entri['deskripsi']}")
    print(f"\nTotal kata dalam kamus: {len(kamus)}")

def cari_kata():
    print("\n=== CARI KATA (Pencarian Linear) ===")
    kata_dicari = input("Masukkan kata yang dicari: ").strip().upper()
    ditemukan = False
    for entri in kamus:
        if entri["kata"] == kata_dicari:
            print(f"\nKata ditemukan!")
            print(f"Kata       : {entri['kata']}")
            print(f"Deskripsi  : {entri['deskripsi']}")
            ditemukan = True
            break
    if not ditemukan:
        print(f"Kata '{kata_dicari}' tidak ditemukan dalam kamus.")

def jalankan_algoritma_genetika():
    print("\n=== JALANKAN ALGORITMA GENETIKA ===")
    print("GA berikut mensimulasikan proses pencarian kata dengan cara")
    print("mengevolusi populasi acak agar mendekati/menyamai kode biner")
    print("dari kata target yang dipilih (minimal 1 generasi).\n")

    tampilkan_kamus()
    kata_target = input("\nPilih salah satu KATA di atas sebagai target pencarian GA: ").strip().upper()

    daftar_kata = [e["kata"] for e in kamus]
    if kata_target not in daftar_kata:
        print("Kata tidak ada dalam kamus. Proses GA dibatalkan.")
        return

    target_bin = encode_word(kata_target)
    panjang_bit = len(target_bin)
    ukuran_populasi = GA["ukuran_populasi"]

    # 1) Populasi awal
    populasi = buat_populasi_awal(panjang_bit, ukuran_populasi)

    # 2) Fitness
    fitness = [hitung_fitness(ind, target_bin) for ind in populasi]

    # 3) Seleksi roulette
    probabilitas, kumulatif, mating_pool = seleksi_roulette(populasi, fitness)

    # 4) Crossover
    hasil_crossover = crossover(mating_pool)

    # 5) Mutasi
    hasil_mutasi = mutasi(hasil_crossover, GA["mutation_rate"])

    # 6) Generasi baru
    generasi_baru = []
    for hm in hasil_mutasi:
        generasi_baru.append(hm["anak1_sesudah"])
        generasi_baru.append(hm["anak2_sesudah"])
    generasi_baru = generasi_baru[:ukuran_populasi]

    # Simpan semua ke state global supaya bisa ditampilkan lewat menu 4-9
    GA["target_kata"] = kata_target
    GA["target_bin"] = target_bin
    GA["populasi"] = populasi
    GA["fitness"] = fitness
    GA["probabilitas"] = probabilitas
    GA["kumulatif"] = kumulatif
    GA["mating_pool"] = mating_pool
    GA["hasil_crossover"] = hasil_crossover
    GA["hasil_mutasi"] = hasil_mutasi
    GA["generasi_baru"] = generasi_baru
    GA["generasi_ke"] = 1

    print(f"\nProses GA untuk kata target '{kata_target}' SELESAI (1 generasi).")
    print("Silakan buka menu 4 s/d 9 untuk melihat detail tiap tahap.")

    # Evaluasi hasil generasi ke-1
    print("\n--- Ringkasan Hasil Generasi ke-1 ---")
    best_awal = max(fitness)
    fitness_baru = [hitung_fitness(ind, target_bin) for ind in generasi_baru]
    best_baru = max(fitness_baru)
    print(f"Fitness terbaik populasi awal   : {best_awal}/{panjang_bit}")
    print(f"Fitness terbaik generasi ke-1   : {best_baru}/{panjang_bit}")
    if best_baru > best_awal:
        print("Kesimpulan: Populasi generasi ke-1 LEBIH MENDEKATI target dibanding populasi awal.")
    elif best_baru == best_awal:
        print("Kesimpulan: Fitness generasi ke-1 SAMA dengan populasi awal.")
    else:
        print("Kesimpulan: Fitness generasi ke-1 belum lebih baik, perlu generasi tambahan.")

def cek_ga_sudah_jalan():
    if GA["target_kata"] is None:
        print("\nBelum ada proses GA yang dijalankan. Silakan pilih menu 3 terlebih dahulu.")
        return False
    return True

def tampilkan_populasi():
    if not cek_ga_sudah_jalan():
        return
    print(f"\n=== POPULASI AWAL (Target: {GA['target_kata']} | Bit: {GA['target_bin']}) ===")
    for i, ind in enumerate(GA["populasi"], 1):
        print(f"Individu {i}: {ind}  -> decode: {decode_binary(ind)!r}")

def hasil_fitness():
    if not cek_ga_sudah_jalan():
        return
    print(f"\n=== HASIL PERHITUNGAN FITNESS ===")
    print(f"Target biner : {GA['target_bin']}  (kata: {GA['target_kata']})")
    print(f"{'Individu':<10}{'Kromosom':<40}{'Fitness'}")
    for i, (ind, fit) in enumerate(zip(GA["populasi"], GA["fitness"]), 1):
        print(f"{i:<10}{ind:<40}{fit}/{len(GA['target_bin'])}")

def seleksi_roulette_tampil():
    if not cek_ga_sudah_jalan():
        return
    print(f"\n=== SELEKSI ROULETTE WHEEL ===")
    print(f"{'Individu':<10}{'Fitness':<10}{'Probabilitas':<15}{'Kumulatif'}")
    for i, (fit, prob, kum) in enumerate(zip(GA["fitness"], GA["probabilitas"], GA["kumulatif"]), 1):
        print(f"{i:<10}{fit:<10}{prob:<15.4f}{kum:.4f}")
    print("\nHasil individu terpilih (mating pool):")
    for i, ind in enumerate(GA["mating_pool"], 1):
        print(f"  Slot {i}: {ind}")

def crossover_tampil():
    if not cek_ga_sudah_jalan():
        return
    print(f"\n=== HASIL CROSS OVER (Single-Point) ===")
    for i, (induk1, induk2, titik, anak1, anak2) in enumerate(GA["hasil_crossover"], 1):
        print(f"\nPasangan {i} (titik potong = {titik}):")
        print(f"  Induk 1 : {induk1}")
        print(f"  Induk 2 : {induk2}")
        print(f"  Anak 1  : {anak1}")
        print(f"  Anak 2  : {anak2}")

def mutasi_tampil():
    if not cek_ga_sudah_jalan():
        return
    print(f"\n=== HASIL MUTASI (rate = {GA['mutation_rate']}) ===")
    for i, hm in enumerate(GA["hasil_mutasi"], 1):
        print(f"\nPasangan {i}:")
        print(f"  Anak 1 sebelum : {hm['anak1_sebelum']}")
        print(f"  Anak 1 sesudah : {hm['anak1_sesudah']}  (posisi mutasi: {hm['posisi_mutasi_1']})")
        print(f"  Anak 2 sebelum : {hm['anak2_sebelum']}")
        print(f"  Anak 2 sesudah : {hm['anak2_sesudah']}  (posisi mutasi: {hm['posisi_mutasi_2']})")

def generasi_baru_tampil():
    if not cek_ga_sudah_jalan():
        return
    target_bin = GA["target_bin"]
    print(f"\n=== POPULASI GENERASI KE-{GA['generasi_ke']} ===")
    print(f"{'Individu':<10}{'Kromosom':<40}{'Decode':<15}{'Fitness'}")
    for i, ind in enumerate(GA["generasi_baru"], 1):
        fit = hitung_fitness(ind, target_bin)
        decoded = decode_binary(ind)
        print(f"{i:<10}{ind:<40}{decoded!r:<15}{fit}/{len(target_bin)}")

    fit_list = [hitung_fitness(ind, target_bin) for ind in GA["generasi_baru"]]
    print(f"\nFitness terbaik generasi ke-{GA['generasi_ke']}: {max(fit_list)}/{len(target_bin)}")
    if max(fit_list) == len(target_bin):
        print(f"Kata target '{GA['target_kata']}' BERHASIL ditemukan (cocok 100%)!")

# =========================================================
# 6. MAIN PROGRAM (MENU)
# =========================================================
def main():
    while True:
        print("\n" + "=" * 55)
        print("=== Kamus Bahasa Isyarat ===")
        print("=" * 55)
        print("1. Tampilkan Kamus")
        print("2. Cari Kata")
        print("3. Jalankan Algoritma Genetika")
        print("4. Tampilkan Populasi")
        print("5. Hasil Fitness")
        print("6. Seleksi Roulette")
        print("7. Cross Over")
        print("8. Mutasi")
        print("9. Generasi Baru")
        print("10. Keluar")
        pilihan = input("Pilih menu (1-10): ").strip()

        if pilihan == "1":
            tampilkan_kamus()
        elif pilihan == "2":
            cari_kata()
        elif pilihan == "3":
            jalankan_algoritma_genetika()
        elif pilihan == "4":
            tampilkan_populasi()
        elif pilihan == "5":
            hasil_fitness()
        elif pilihan == "6":
            seleksi_roulette_tampil()
        elif pilihan == "7":
            crossover_tampil()
        elif pilihan == "8":
            mutasi_tampil()
        elif pilihan == "9":
            generasi_baru_tampil()
        elif pilihan == "10":
            print("\nTerima kasih. Program selesai.")
            break
        else:
            print("\nPilihan tidak valid. Masukkan angka 1-10.")

if __name__ == "__main__":
    main()