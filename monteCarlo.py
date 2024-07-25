import streamlit as st
from streamlit_option_menu import option_menu

from questions import *

@st.cache_data
def load_data(url) :
    df = pd.read_excel(url, engine='openpyxl')
    return df

penjualan = load_data("https://raw.githubusercontent.com/janbu12/monteCarlo/main/datasets/tr_penjualan.xlsx")
produk = load_data("https://raw.githubusercontent.com/janbu12/monteCarlo/main/datasets/ms_produk.xlsx")
# karyawan = pd.read_excel("./datasets/ms_karyawan.xlsx")
# kategori = pd.read_excel("./datasets/ms_kategori.xlsx")
# kota = pd.read_excel("./datasets/ms_kota.xlsx")
# propinsi = pd.read_excel("./datasets/ms_propinsi.xlsx")
# cabang = pd.read_excel("./datasets/ms_cabang.xlsx")

st.markdown("""
    <header>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
    </header>
    <style>
        html, body, h1, h2, h3, p, b, nav-link [class*="css"] {font-family: 'Poppins', sans-serif;}
    </style>
""", unsafe_allow_html=True)

with st.sidebar :
    selected = option_menu('Monte Carlo',
                           ['1. Deskripsi Model', '2. Metode dan Data', '3. Simulasi dan Hasil Model', '4.', '5.', '6.'],
                           icons = ["person-circle", "person-workspace", "person-badge-fill", "person-circle", "person-workspace", "person-badge-fill"],
                           menu_icon = "person-lines-fill",
                           default_index = 0,
                           styles={"nav" : {"font-family" : 'Poppins'},
                                   "menu-title" : {"font-family" : 'Poppins', "font-weight" : "700"},
                                   "nav-link-selected" : {"font-weight" : "700", "background-color" : "#dc3545"},
                                   "icon" : {"font-size" : "20px"},
                                   "nav-link" : {"--hover-color" : "#dc3545"}})
    
if (selected == '1. Deskripsi Model') :
    st.header(f"Penjelasan Mengenai Model yang akan dibuat")
    # with st.expander("Penjelasan Mengenai Model yang akan dibuat") :
    st.write("Untuk mengurangi kemungkinan kekurangan atau kelebihan stok, peramalan penjualan adalah proses perencanaan inventaris agar lebih akurat. Prediksi ini juga mendukung rencana pemasaran dan promosi berdasarkan tren penjualan.")
    st.write("Prediksi kinerja karyawan merupakan proses untuk mengevaluasi kinerja karyawan sehingga dapat mengetahui karyawan dengan kinerja yang baik dan yang kurang baik dalam beberapa waktu ke depan. Sehingga, perusahaan dapat mengambil keputusan untuk memberi penghargaan atau pelatihan tambahan bahkan pemecatan karyawan.")
    st.write("Model prediksi yang akan dibuat menggunakan metode Monte Carlo yang bertujuan untuk melihat jumlah penjualan pertahun, dan kinerja karyawan berdasarkan jumlah transaksi yang ia tangani di masa yang akan datang.")

    
if (selected == '2. Metode dan Data') :
    st.header(f"Penjelasan Mengenai Metode dan Data yang akan digunakan")
    tab1 ,tab2, tab3= st.tabs(["Metode", "Langkah - Langkah Metode", "Data"])
    
    with tab1:
        st.write("Metode yang digunakan untuk membuat model prediksi di atas menggunakan Monte Carlo. Metode ini merupakan metode analisis numerik yang melibatkan pengambilan sampel eksperimen bilangan acak. Umum digunakan untuk mensimulasikan sistem pengendalian persediaan. Simulasi dengan metode Monte Carlo adalah bentuk simulasi probabilistik berdasarkan proses randomisasi (acak) yang melibatkan variabel-variabel data yang dikumpulkan berdasarkan data masa lalu maupun distribusi probabilitas teoritis.")
        
    with tab2:
        st.write("Langkah - langkah metode Monte Carlo yang digunakan adalah sebagai berikut:")
        with st.expander("1. Mengumpulkan Data Historis:") :
            st.write("""<list>
                        <li>Mengumpulkan data penjualan.
                        <li>Mengumpulkan data harga.
                        <li>Mengumpulkan data transaksi karyawan.
                    </list>""", unsafe_allow_html=True) 
    
if (selected == '3. Simulasi dan Hasil Model') :
    st.header(f"Simulasi untuk Prediksi Penjualan dan Kinerja Karyawan")
    tab1, tab2 = st.tabs(["Prediksi Penjualan", "Prediksi Kinerja Karyawan"])
    
    with tab1:
        questionPenjualan(produk, penjualan)
        
    # with tab2:
        
    
if (selected == '4.') :
    st.header(f"4.")
    
if (selected == '5.') :
    st.header(f"5.")
    
if (selected == '6.') :
    st.header(f"6.")
    
