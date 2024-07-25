import streamlit as st
from streamlit_option_menu import option_menu

from questions import *

@st.cache_data
def load_data(url) :
    df = pd.read_excel(url, engine='openpyxl')
    return df

penjualan = load_data("https://raw.githubusercontent.com/janbu12/monteCarlo/main/datasets/tr_penjualan.xlsx")
produk = load_data("https://raw.githubusercontent.com/janbu12/monteCarlo/main/datasets/ms_produk.xlsx")
karyawan = load_data("https://raw.githubusercontent.com/janbu12/monteCarlo/main/datasets/ms_karyawan.xlsx")
cabang = load_data("https://raw.githubusercontent.com/janbu12/monteCarlo/main/datasets/ms_cabang.xlsx")

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
                           ['1. Deskripsi Model', '2. Metode dan Data', '3. Simulasi dan Hasil Model', '4. Identitas Kelompok'],
                           icons = ["bi bi-box-seam-fill", "bi bi-bar-chart-steps", "bi bi-clipboard-data-fill", "bi bi-person-vcard-fill"],
                           menu_icon = "bi bi-pie-chart-fill",
                           default_index = 0,
                           styles={"nav" : {"font-family" : 'Poppins'},
                                   "menu-title" : {"font-family" : 'Poppins', "font-weight" : "700", "font-size":"30px"},
                                   "menu-icon": {"font-size": "30px"},
                                   "nav-link-selected" : {"font-weight" : "700", "background-color" : "#dc3545"},
                                   "icon" : {"font-size" : "30px"},
                                   "nav-link" : {"--hover-color" : "#dc3545", "display":"flex", "align-items":"center", "gap": "1rem"}})
    
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
                        <li>Mengumpulkan data transaksi karyawan.
                    </list>""", unsafe_allow_html=True)
        with st.expander("2. Mendefinisikan Distribusi Probabilitas:") :
            st.write("""
                        Menganalisis data historis untuk menentukan distribusi probabilitas dari jumlah penjualan, dan jumlah transaksi per karyawan.  
                    """, unsafe_allow_html=True) 
        with st.expander("3. Mengonversi Distribusi Probabilitas ke Frekuensi Kumulatif:") :
            st.write("""
                        Menggunakan distribusi probabilitas untuk membuat tabel frekuensi kumulatif yang akan digunakan sebagai dasar pengelompokkan interval bilangan acak.
                    """, unsafe_allow_html=True) 
        with st.expander("4. Menjalankan Simulasi:") :
            st.write("""
                        Menggunakan bilangan acak yang dikategorikan sesuai dengan distribusi kumulatif untuk mensimulasikan berbagai skenario jumlah penjualan, perubahan harga, dan kinerja karyawan.
                    """, unsafe_allow_html=True) 
        with st.expander("5. Analisis Hasil:") :
            st.write("""
                        Menganalisis hasil keluaran simulasi untuk mendapatkan prediksi yang dapat digunakan sebagai dasar pengambilan keputusan.
                    """, unsafe_allow_html=True)  
            
    with tab3:
        with st.container():
            st.write("<h2>Data Produk</h2>", unsafe_allow_html=True)
            st.write("Ini merupakan data head dari data produk", unsafe_allow_html=True)
            st.dataframe(produk.head())
            
        with st.container():
            st.write("<h2>Data Penjualan</h2>", unsafe_allow_html=True)
            st.write("Ini merupakan data head dari data penjualan", unsafe_allow_html=True)
            st.dataframe(penjualan.head())
        
        with st.container():
            st.write("<h2>Data Karyawan</h2>", unsafe_allow_html=True)
            st.write("Ini merupakan data head dari data karyawan", unsafe_allow_html=True)
            st.dataframe(karyawan.head())
            
        with st.container():
            st.write("<h2>Data Cabang</h2>", unsafe_allow_html=True)
            st.write("Ini merupakan data head dari data cabang", unsafe_allow_html=True)
            st.dataframe(cabang.head())
    
if (selected == '3. Simulasi dan Hasil Model') :
    st.header(f"Simulasi untuk Prediksi Penjualan dan Kinerja Karyawan")
    tab1, tab2 = st.tabs(["Prediksi Penjualan", "Prediksi Kinerja Karyawan"])
    
    with tab1:
        questionPenjualan(produk, penjualan)
        
    with tab2:
        questionKaryawan(karyawan, penjualan, cabang)
        
    
if (selected == '4. Identitas Kelompok') :
    st.header("Identitas Kelompok")
    st.write("""
                <list>
                    <li>Muhamad Singgih Prasetyo    - 10122095</li>
                    <img src="https://raw.githubusercontent.com/janbu12/monteCarlo/main/foto/Mizan.png">
                    <li>Muhammad Mizan Al Mujadid   - 10122096</li>
                    <li>Muhammad Raffy Abdillah              - 10122099</li>
                </list> 
             """, unsafe_allow_html=True)
