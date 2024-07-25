import pandas as pd, numpy as np, streamlit as st

def lcg(seed, a, c, m, n):
    values = []
    for _ in range(n):
        seed = (a * seed + c) % m
        values.append(seed)
    return values

def get_prediksi(angka_acak, intervalsAcak, intervals):
    for (lower_acak, upper_acak), (lower, upper) in zip(intervalsAcak, intervals):
        if lower_acak <= angka_acak < upper_acak:
            return np.ceil((lower + upper) / 2)
    return np.nan


def questionPenjualan(dataset1, dataset2):
    # st.write("<h3>Simulasi Prediksi Penjualan Produk Selama 1 tahun Kedepan</h3>", unsafe_allow_html=True)
    
    penjualan_produk = dataset2.merge(dataset1, on='kode_produk', suffixes=('_penjualan', '_produk'), validate='m:1')
    penjualan_produk = penjualan_produk.groupby(['kode_produk', 'nama_produk'])['jumlah_pembelian'].sum().reset_index()
    
    # Menentukan batas bawah dan batas atas
    min_val = penjualan_produk['jumlah_pembelian'].min()
    max_val = penjualan_produk['jumlah_pembelian'].max()
    interval_size = (max_val - min_val) // 6  # Misalkan 6 interval kelas
    bins = np.arange(min_val, max_val + interval_size + 1, interval_size)  # Perbaiki batas atas

    # Menghitung frekuensi
    penjualan_produk['Interval'] = pd.cut(penjualan_produk['jumlah_pembelian'], bins=bins, include_lowest=True)
    frequency = penjualan_produk['Interval'].value_counts().sort_index()

    # Menentukan batas bawah dan batas atas
    interval_boundaries = [(interval.left, interval.right) for interval in frequency.index]
    boundaries_df = pd.DataFrame(interval_boundaries, columns=['Batas Bawah', 'Batas Atas'])
    boundaries_df['Frekuensi'] = frequency.values

    # Menghitung probabilitas
    boundaries_df['Probabilitas'] = boundaries_df['Frekuensi'] / boundaries_df['Frekuensi'].sum()

    # Menghitung probabilitas kumulatif
    boundaries_df['Probabilitas Kumulatif'] = boundaries_df['Probabilitas'].cumsum()

    # Menghitung jumlah angka acak
    total_random_numbers = 100
    boundaries_df['Jumlah Angka Acak'] = (total_random_numbers * boundaries_df['Probabilitas Kumulatif']).round().astype(int)

    boundaries_df['Batas Bawah Acak'] = np.concatenate(([0], boundaries_df['Jumlah Angka Acak'].iloc[:-1].values))
    boundaries_df['Batas Atas Acak'] = boundaries_df['Jumlah Angka Acak']
    
    a = 1664525
    c = 1013904223
    m = 2**32
    seed = 123456789

    num_values = len(penjualan_produk)
    lcg_values = lcg(seed, a, c, m, num_values + 1)
    penjualan_produk['Zi-1'] = lcg_values[:-1]
    penjualan_produk['Zi'] = lcg_values[1:]

    penjualan_produk['Angka Acak'] = penjualan_produk['Zi'] % 101

    intervalsAcak = list(zip(boundaries_df['Batas Bawah Acak'], boundaries_df['Batas Atas Acak']))
    intervals= [(b.left, b.right) for b in penjualan_produk['Interval']]

    penjualan_produk['Prediksi'] = penjualan_produk['Angka Acak'].apply(lambda x: get_prediksi(x, intervalsAcak, intervals))
    
    penjualan_setahun = penjualan_produk[['kode_produk', 'nama_produk', 'jumlah_pembelian']]
    
    simulasiPrediksi = penjualan_produk[['kode_produk', 'nama_produk', 'Zi-1', 'Zi', 'Angka Acak', 'Prediksi']]
    
    
    
    with st.container():
        st.write("<h4>Hasil penggabungan data produk dan penjualan produk, lalu menjumlahkan semua penjualannya</h4>", unsafe_allow_html=True)
        st.dataframe(penjualan_setahun.style.highlight_max(subset='jumlah_pembelian', axis=0, color='#198754')
                     .highlight_min(subset='jumlah_pembelian', axis=0, color='#dc3545'), 
                     use_container_width=True, hide_index=True)
        st.write("<br>", unsafe_allow_html=True)
        
    with st.container():
        st.write("<h4>Distribusi Frekuensi Untuk Kebutuhan Prediksi</h4>", unsafe_allow_html=True)
        st.dataframe(boundaries_df, hide_index=True, use_container_width=True)
        st.write("<br>", unsafe_allow_html=True)
        
    with st.container():
        st.write("<h4>Hasil Model Simulasi Prediksi Penjualan Produk Menggunakan LCG</h4>", unsafe_allow_html=True)
        st.dataframe(simulasiPrediksi.style.highlight_max(subset='Prediksi', axis=0, color='#198754')
                     .highlight_min(subset='Prediksi', axis=0, color='#dc3545'), 
                     use_container_width=True, hide_index=True)
        st.write("<br>", unsafe_allow_html=True)
        
        
    with st.expander("Kesimpulan dari Model Simulasi diatas:") :
            st.write("""
                        Kesimpulannya adalah produk dengan prediksi tertinggi atau berkemungkinan memiliki penjualan yang baik:
                        <list>
                            <li>PROD-0000001: bawang merah 1kg</li>
                            <li>PROD-0000007: ketimun 1 kg</li>
                            <li>PROD-0000010: ubi kayu basah 1 kg</li>
                            <li>PROD-0000014: telur ayam ras 1 kg</li>
                            <li>PROD-0000020: snack gurih 1 ons</li>
                            <li>PROD-0000022: kacang mete 1 kg</li>
                            <li>PROD-0000029: alpukat 1 kg</li>
                            <li>PROD-0000036: nangka 1 kg</li>
                            <li>PROD-0000039: rambutan 1 kg</li>
                            <li>PROD-0000020: snack gurih 1 ons</li>
                            <li>PROD-0000020: snack gurih 1 ons</li>
                        </list><br>
                        Lalu produk dengan prediksi terkecil atau berkemungkinan memiliki penjualan yang stagnand:
                        <list>
                            <li>PROD-0000002: bawang putih 1 kg</li>
                            <li>PROD-0000003: buncis 1 kg</li>
                            <li>PROD-0000004: kacang panjang 1 kg</li>
                            <li>PROD-0000006: kentang 1 kg</li>
                            <li>PROD-0000009: tomat 1 kg</li>
                            <li>PROD-0000011: ubi jalar 1 kg</li>
                            <li>PROD-0000013: susu kotak (800 ml)</li>
                            <li>PROD-0000015: telur ayam kampung 1 kg</li>
                            <li>PROD-0000021: kacang goreng 1 kg</li>
                            <li>PROD-0000027: jeruk 1 kg</li>
                            <li>dll
                        </list><br><br>
                        Oleh karena itu perusahaan harus memiliki beberapa strategi untuk menangani produk yang berkemungkinan penjualannya stagnand
                     """, unsafe_allow_html=True) 
        
    
        
        
    
    
