<<<<<<< HEAD
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
=======
try:
    import streamlit as st  # type: ignore[reportMissingImports]
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "Streamlit belum terpasang. Install dulu dengan: pip install streamlit"
    ) from exc
import hashlib
import json
from datetime import datetime

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sistem Auth SHA-256",
    page_icon="🔐",
    layout="centered",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { max-width: 700px; }
    .hash-box {
        background: #f0faf5;
        border: 1px solid #5DCAA5;
        border-radius: 8px;
        padding: 10px 14px;
        font-family: monospace;
        font-size: 12px;
        word-break: break-all;
        color: #085041;
        margin-top: 6px;
    }
    .user-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 8px;
    }
    .badge-success {
        background: #d1fae5; color: #065f46;
        padding: 3px 10px; border-radius: 99px;
        font-size: 12px; font-weight: 600;
    }
    .badge-danger {
        background: #fee2e2; color: #7f1d1d;
        padding: 3px 10px; border-radius: 99px;
        font-size: 12px; font-weight: 600;
    }
    .title-area { text-align: center; margin-bottom: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ─────────────────────────────────────────────────────────
if "users" not in st.session_state:
    st.session_state.users = {}   # { username: { hash, created_at } }

if "login_status" not in st.session_state:
    st.session_state.login_status = None   # dict hasil login terakhir

# ─── Helper Functions ──────────────────────────────────────────────────────────

def hash_sha256(password: str) -> str:
    """Mengubah password menjadi hash SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username: str, password: str):
    """Melakukan registrasi user baru."""
    if not username or not password:
        return False, "⚠️ Username dan password tidak boleh kosong."
    if username in st.session_state.users:
        return False, f"⚠️ Username **{username}** sudah terdaftar."
    h = hash_sha256(password)
    st.session_state.users[username] = {
        "hash": h,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return True, h


def login_user(username: str, password: str):
    """Memverifikasi login user."""
    if not username or not password:
        return None, "⚠️ Username dan password tidak boleh kosong."
    input_hash = hash_sha256(password)
    if username not in st.session_state.users:
        return False, input_hash
    stored_hash = st.session_state.users[username]["hash"]
    match = input_hash == stored_hash
    return match, input_hash


# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="title-area">
    <h2>🔐 Sistem Registrasi & Login</h2>
    <p style="color:#6b7280; font-size:14px;">Password diamankan dengan hashing SHA-256</p>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab_reg, tab_login, tab_data = st.tabs(["📝 Registrasi", "🔑 Login", "🗄️ Data Tersimpan"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — REGISTRASI
# ══════════════════════════════════════════════════════════════════════════════
with tab_reg:
    st.subheader("Registrasi User Baru")

    with st.form("form_register", clear_on_submit=True):
        reg_username = st.text_input("Username", placeholder="Masukkan username...")
        reg_password = st.text_input("Password", type="password", placeholder="Masukkan password...")
        submitted_reg = st.form_submit_button("✅ Daftar & Simpan", use_container_width=True)

    if submitted_reg:
        success, result = register_user(reg_username, reg_password)
        if success:
            st.success(f"User **{reg_username}** berhasil didaftarkan!")
            st.markdown("**Hash SHA-256 password yang disimpan:**")
            st.markdown(f'<div class="hash-box">{result}</div>', unsafe_allow_html=True)
            st.info("🛡️ Password asli **tidak** disimpan — hanya hash-nya.")
        else:
            st.error(result)

    # Preview hash real-time
    st.divider()
    st.markdown("**🔍 Preview Hash SHA-256**")
    preview_pass = st.text_input(
        "Ketik password untuk melihat hash-nya:",
        type="password",
        key="preview_input",
        placeholder="Ketik di sini..."
    )
    if preview_pass:
        preview_hash = hash_sha256(preview_pass)
        st.markdown(f'<div class="hash-box">{preview_hash}</div>', unsafe_allow_html=True)
        st.caption(f"Panjang hash: {len(preview_hash)} karakter (256-bit)")
    else:
        st.markdown('<div class="hash-box" style="color:#9ca3af;">— Ketik password di atas —</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — LOGIN
# ══════════════════════════════════════════════════════════════════════════════
with tab_login:
    st.subheader("Login User")

    with st.form("form_login", clear_on_submit=True):
        login_username = st.text_input("Username", placeholder="Masukkan username...", key="lu")
        login_password = st.text_input("Password", type="password", placeholder="Masukkan password...", key="lp")
        submitted_login = st.form_submit_button("🔓 Masuk", use_container_width=True)

    if submitted_login:
        result, input_hash = login_user(login_username, login_password)
        if result is None:
            st.error(input_hash)
        else:
            # Simpan status ke session untuk ditampilkan
            stored_hash = st.session_state.users.get(login_username, {}).get("hash", None)
            st.session_state.login_status = {
                "username": login_username,
                "success": result,
                "input_hash": input_hash,
                "stored_hash": stored_hash,
            }

    if st.session_state.login_status:
        ls = st.session_state.login_status
        st.divider()
        st.markdown("**📋 Detail Verifikasi**")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Username", ls["username"])
        with col2:
            status_text = "✅ Berhasil" if ls["success"] else "❌ Gagal"
            st.metric("Status Login", status_text)

        st.markdown("**Hash dari password yang diinput:**")
        st.markdown(f'<div class="hash-box">{ls["input_hash"]}</div>', unsafe_allow_html=True)

        if ls["stored_hash"]:
            st.markdown("**Hash yang tersimpan di database:**")
            st.markdown(f'<div class="hash-box">{ls["stored_hash"]}</div>', unsafe_allow_html=True)

            if ls["success"]:
                st.markdown('<span class="badge-success">✓ Hash Cocok — Login Berhasil</span>', unsafe_allow_html=True)
                st.success(f"Selamat datang, **{ls['username']}**! 🎉")
            else:
                st.markdown('<span class="badge-danger">✗ Hash Tidak Cocok — Login Ditolak</span>', unsafe_allow_html=True)
                st.error("Password salah. Hash tidak cocok dengan data tersimpan.")
        else:
            st.error(f"Username **{ls['username']}** tidak ditemukan dalam database.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — DATA TERSIMPAN
# ══════════════════════════════════════════════════════════════════════════════
with tab_data:
    st.subheader("Data User Tersimpan")

    users = st.session_state.users

    if not users:
        st.info("Belum ada user yang terdaftar. Silakan lakukan registrasi terlebih dahulu.")
    else:
        st.caption(f"Total user terdaftar: **{len(users)}**")
        st.divider()

        for i, (uname, udata) in enumerate(users.items(), 1):
            with st.expander(f"👤 {uname}  ·  {udata['created_at']}"):
                st.markdown(f"**Username:** `{uname}`")
                st.markdown(f"**Terdaftar:** {udata['created_at']}")
                st.markdown("**Hash SHA-256 Password:**")
                st.markdown(f'<div class="hash-box">{udata["hash"]}</div>', unsafe_allow_html=True)

        st.divider()
        # Export sebagai JSON
        if st.button("📥 Export Data (JSON)", use_container_width=True):
            json_data = json.dumps(users, indent=2, ensure_ascii=False)
            st.download_button(
                label="⬇️ Download users.json",
                data=json_data,
                file_name="users.json",
                mime="application/json",
                use_container_width=True,
            )

        # Tombol hapus semua
        if st.button("🗑️ Hapus Semua Data", type="secondary", use_container_width=True):
            st.session_state.users = {}
            st.session_state.login_status = None
            st.rerun()


# ─── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center; font-size:12px; color:#9ca3af;'>"
    "SHA-256 · hashlib · Streamlit · Tugas Keamanan Data"
    "</p>",
    unsafe_allow_html=True,
)
>>>>>>> 243f530 (Upload kodingan baru ke repo lama)
