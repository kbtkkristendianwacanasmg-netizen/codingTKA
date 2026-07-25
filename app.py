import random
import streamlit as st
from PIL import Image

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Game Wajah Anak TK", page_icon="🎨", layout="centered"
)

st.title("🧩 Pasang Bagian Wajah!")
st.write("Pilih bagian wajah yang cocok di setiap posisi!")

# State untuk menyimpan acakan kunci jawaban & skor
if "game_started" not in st.session_state:
    st.session_state.game_started = True
    st.session_state.skor = 0

# Pilihan opsi untuk anak TK
OPSI_MATA = ["👀 Mata Lengkap", "🕶️ Kacamata Hitam", "😉 Mata Merem Sebelah"]
OPSI_HIDUNG = ["👃 Hidung Badut (Merah)", "👃 Hidung Biasa", "🐱 Hidung Kucing"]
OPSI_MULUT = ["😀 Senyum Lebar", "👅 Melet Lucu", "😮 Kaget"]

# Tombol untuk Mengacak Tantangan Baru
if st.button("🔄 Acak Game Baru"):
    st.session_state.target_mata = random.choice(OPSI_MATA)
    st.session_state.target_hidung = random.choice(OPSI_HIDUNG)
    st.session_state.target_mulut = random.choice(OPSI_MULUT)
    st.rerun()

# Set kunci jawaban pertama kali
if "target_mata" not in st.session_state:
    st.session_state.target_mata = random.choice(OPSI_MATA)
    st.session_state.target_hidung = random.choice(OPSI_HIDUNG)
    st.session_state.target_mulut = random.choice(OPSI_MULUT)

# Tampilkan Petunjuk Tantangan
st.info(
    f"🎯 **Tantangan Saat Ini:**\n"
    f"- Mata: **{st.session_state.target_mata}**\n"
    f"- Hidung: **{st.session_state.target_hidung}**\n"
    f"- Mulut: **{st.session_state.target_mulut}**"
)

st.subheader("Bantu lengkapi wajahnya di bawah ini:")

# Form Pilih Bagian Wajah (Interaktif untuk Anak-anak)
pilihan_mata = st.selectbox("1. Pilih Mata:", OPSI_MATA)
pilihan_hidung = st.selectbox("2. Pilih Hidung:", OPSI_HIDUNG)
pilihan_mulut = st.selectbox("3. Pilih Mulut:", OPSI_MULUT)

# Cek Hasil
if st.button("🎉 Periksa Hasil!", type="primary"):
    is_mata_benar = pilihan_mata == st.session_state.target_mata
    is_hidung_benar = pilihan_hidung == st.session_state.target_hidung
    is_mulut_benar = pilihan_mulut == st.session_state.target_mulut

    if is_mata_benar and is_hidung_benar and is_mulut_benar:
        st.balloons()  # Efek balon terbang!
        st.success("🌟 HORE! KANIN HEBAT! Semua bagian wajah sudah benar! 🌟")
    else:
        st.error("OOPS! Masih ada yang belum cocok. Coba periksa lagi ya! 🧐")
