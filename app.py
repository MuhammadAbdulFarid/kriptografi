"""
================================================
TUGAS KRIPTOGRAFI - No. 16 s/d Selesai
Topik  : MD5 Checksum untuk Deteksi Perubahan Data Profil User
================================================
Deskripsi:
    Program ini menggunakan fungsi hash MD5 untuk membuat checksum
    dari data profil user (nama, email, nomor HP). Admin dapat
    mendeteksi apakah data profil pernah dimodifikasi dengan
    membandingkan hash awal dan hash baru.
"""

import hashlib

import streamlit as st


# ─────────────────────────────────────────────
# Fungsi: membuat hash MD5 dari data profil
# ─────────────────────────────────────────────
def buat_hash_md5(nama: str, email: str, nomor_hp: str) -> str:
    """
    Membuat checksum MD5 dari gabungan data profil user.
    Data digabung dengan separator '|' agar unik per kombinasi.

    Parameter:
        nama      -- nama lengkap user
        email     -- alamat email user
        nomor_hp  -- nomor HP user

    Return:
        string hash MD5 (32 karakter hex)
    """
    data_gabung = f"nama:{nama}|email:{email}|hp:{nomor_hp}"
    hash_md5 = hashlib.md5(data_gabung.encode("utf-8")).hexdigest()
    return hash_md5


def bandingkan_data(data_awal: dict, hash_awal: str, data_baru: dict, hash_baru: str) -> tuple[bool, list[tuple[str, str, str]]]:
    """Membandingkan dua data profil dan mengembalikan status perubahan."""
    perubahan = []
    fields = [
        ("Nama", data_awal["nama"], data_baru["nama"]),
        ("Email", data_awal["email"], data_baru["email"]),
        ("Nomor HP", data_awal["nomor_hp"], data_baru["nomor_hp"]),
    ]
    for field, lama, baru in fields:
        if lama != baru:
            perubahan.append((field, lama, baru))

    return hash_awal == hash_baru, perubahan


def main():
    st.set_page_config(page_title="Deteksi Perubahan Data Profil", page_icon="🛡️", layout="centered")

    st.title("Sistem Deteksi Perubahan Data Profil User")
    st.caption("Menggunakan checksum MD5 untuk membandingkan data profil awal dan data profil baru.")

    if "data_awal" not in st.session_state:
        st.session_state.data_awal = None
        st.session_state.hash_awal = None
        st.session_state.data_baru = None
        st.session_state.hash_baru = None

    st.subheader("1. Data Profil Awal")
    with st.form("form_awal"):
        nama_awal = st.text_input("Nama", key="nama_awal")
        email_awal = st.text_input("Email", key="email_awal")
        nomor_hp_awal = st.text_input("Nomor HP", key="nomor_hp_awal")
        simpan_awal = st.form_submit_button("Simpan Data Awal")

    if simpan_awal:
        data_awal = {
            "nama": nama_awal.strip(),
            "email": email_awal.strip(),
            "nomor_hp": nomor_hp_awal.strip(),
        }
        hash_awal = buat_hash_md5(data_awal["nama"], data_awal["email"], data_awal["nomor_hp"])
        st.session_state.data_awal = data_awal
        st.session_state.hash_awal = hash_awal
        st.session_state.data_baru = None
        st.session_state.hash_baru = None
        st.success("Hash MD5 awal berhasil disimpan.")

    if st.session_state.hash_awal:
        st.code(st.session_state.hash_awal, language="text")

    st.subheader("2. Data Profil Baru")
    if st.session_state.data_awal is None:
        st.info("Isi dan simpan data profil awal terlebih dahulu.")
    else:
        with st.form("form_baru"):
            nama_baru = st.text_input("Nama baru", key="nama_baru")
            email_baru = st.text_input("Email baru", key="email_baru")
            nomor_hp_baru = st.text_input("Nomor HP baru", key="nomor_hp_baru")
            cek_perubahan = st.form_submit_button("Bandingkan Data")

        if cek_perubahan:
            data_baru = {
                "nama": nama_baru.strip(),
                "email": email_baru.strip(),
                "nomor_hp": nomor_hp_baru.strip(),
            }
            hash_baru = buat_hash_md5(data_baru["nama"], data_baru["email"], data_baru["nomor_hp"])
            st.session_state.data_baru = data_baru
            st.session_state.hash_baru = hash_baru

    if st.session_state.hash_awal and st.session_state.hash_baru:
        cocok, perubahan = bandingkan_data(
            st.session_state.data_awal,
            st.session_state.hash_awal,
            st.session_state.data_baru,
            st.session_state.hash_baru,
        )

        st.subheader("3. Laporan Integritas")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Hash Awal")
            st.code(st.session_state.hash_awal, language="text")
        with col2:
            st.write("Hash Baru")
            st.code(st.session_state.hash_baru, language="text")

        if cocok:
            st.success("DATA TIDAK BERUBAH")
            st.write("Hash MD5 identik. Integritas data terjaga.")
        else:
            st.warning("DATA TELAH DIMODIFIKASI")
            st.write("Hash MD5 berbeda. Terdeteksi perubahan pada data profil user.")

            if perubahan:
                st.write("Kolom yang berubah:")
                for field, lama, baru in perubahan:
                    st.markdown(f"- **{field}**: `{lama}` → `{baru}`")


if __name__ == "__main__":
    main()