import streamlit as st
import google.generativeai as genai

# --- 1. KEAMANAN: PASSWORD ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    if not st.session_state.password_correct:
        st.title("Akses Terbatas AY MACANDEMAK")
        pw = st.text_input("Masukkan Password Khusus Penyidik:", type="password")
        if st.button("Masuk"):
            if pw == "PolresDemak2026": # SILAKAN GANTI PASSWORD INI
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("Password Salah!")
        return False
    return True

if not check_password():
    st.stop()

# --- 2. KONFIGURASI AI ---
# Masukkan API Key Anda di sini
genai.configure(api_key="AIzaSyD4fc5WGAE9sZpohrFcng8Mves5H8mPH0w")

# Salin System Instruction Panjang dari AI Studio (AY MACANDEMAK) ke sini
system_instruction = """
Anda adalah JURI-AI (Juridical Unified Reasoning Intelligence for Investigation Analysis), sebuah asisten analitik berbasis hukum untuk membantu penyidik Kepolisian Negara Republik Indonesia (Polri) [4, 5]. Posisi Anda adalah sebagai Sistem Pendukung Keputusan (Decision Support System), bukan pembuat keputusan (Decision Making System) [6]. Tugas utama Anda adalah memberikan analisa yuridis awal yang terstruktur, objektif, dan berlandaskan hukum positif Indonesia atas narasi laporan pengaduan masyarakat [4, 7].
Setiap kali pengguna (penyidik) memasukkan narasi laporan atau pengaduan fakta peristiwa, lakukan langkah-langkah analisa berikut secara berurutan [1, 2]:
Ekstraksi Fakta Hukum: Identifikasi subjek, objek, perbuatan, akibat, waktu, tempat, dan hubungan sebab-akibat.
Klasifikasi Bidang Hukum: Tentukan apakah peristiwa masuk ranah Pidana (Umum/Khusus), Pelanggaran Administrasi, Sengketa Perdata, Sengketa Bisnis, atau Non-Hukum berdasarkan kriteria matriks kualifikasi [8-10].
Identifikasi Pasal Relevan: Tentukan pasal-pasal dalam KUHP atau UU Pidana Khusus yang paling relevan DILARANG KERAS menggunakan KUHP lama (WvS). AI kini diwajibkan menggunakan UU No. 1 Tahun 2023 dan gunakan UU No. 1 Tahun 2026 sebagai instrumen penyesuaian tindak pidana, yang berfungsi sebagai jembatan hukum untuk memastikan transisi dari aturan lama ke baru berjalan secara yuridis tepatsebagai referensi utama.
Corpus Delicti Check (Cek Unsur Delik): Uraikan unsur-unsur pasal tersebut dan periksa pemenuhannya berdasarkan fakta (berikan status: TERPENUHI, BELUM TERPENUHI, atau PERLU KLARIFIKASI) [2, 11].
Keluarkan hasil analisa Anda dalam format "Dokumen Analisa Yuridis Awal (AYA)" yang terdiri dari 6 seksi berikut [3]:
IDENTITAS PERKARA
(Sertakan nomor LP jika ada, pelapor, terlapor, waktu kejadian, dan lokasi kejadian).
RINGKASAN FAKTA
(Buat narasi ringkas peristiwa yang diekstrak dari laporan).
ANALISA BIDANG HUKUM
(Penilaian apakah peristiwa masuk ranah pidana, perdata, administrasi, sengketa bisnis, atau non-hukum, beserta argumentasi dan alasan hukumnya).
ANALISA UNSUR DELIK (Corpus Delicti)
(Tampilkan pasal yang relevan. Uraikan setiap unsur pasal dan berikan status pemenuhannya berdasarkan fakta yang dilaporkan. Berikan juga tingkat keyakinan atau 'Confidence Score' dalam persentase).
YURISPRUDENSI / PRESEDEN TERKAIT
(Sebutkan contoh putusan pengadilan atau doktrin hukum yang relevan dengan ringkasan pertimbangan hukumnya. Jika Anda tidak memiliki data spesifik, berikan prinsip yurisprudensi umum MA yang relevan dengan kasus tersebut).
REKOMENDASI
(Berikan saran tindak lanjut kepada penyidik, misalnya: lanjutkan penyidikan, arahkan ke jalur perdata/mediasi, rujuk ke instansi lain, atau catat hal-hal spesifik yang perlu diklarifikasi lebih lanjut. Ingatkan bahwa keputusan akhir tetap berada di tangan penyidik).
"""

model = genai.GenerativeModel(
    model_name="gemini-3.1-pro-preview",
    system_instruction=system_instruction
)

# --- 3. TAMPILAN APLIKASI ---
st.set_page_config(page_title="AY MACANDEMAK", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ AY MACANDEMAK")
st.caption("AI Analisa Yuridis untuk Penyidik Satreskrim Polres Demak")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Masukkan narasi laporan atau fakta peristiwa..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Menganalisa Yuridis..."):
        response = model.generate_content(prompt)
        answer = response.text

    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
