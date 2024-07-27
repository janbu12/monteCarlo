import pandas as pd, numpy as np, streamlit as st

def lcg(seed, a, c, m, n):
    values = []
    for _ in range(n):
        seed = (a * seed + c) % m
        values.append(seed)
    return values

def get_prediksi(angka_acak, intervalsAcak, intervals):
    for (lower_acak, upper_acak), (lower, upper) in zip(intervalsAcak, intervals):
        if lower_acak <= angka_acak <= upper_acak:
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

    # Menghitung interval angka acak
    # boundaries_df['Interval Angka Acak'] = boundaries_df['Jumlah Angka Acak'].cumsum()

    # Menentukan batas bawah acak dan batas atas acak
    boundaries_df['Batas Bawah Acak'] = np.concatenate(([0], boundaries_df['Jumlah Angka Acak'].iloc[:-1].values + 1))
    boundaries_df['Batas Atas Acak'] = boundaries_df['Jumlah Angka Acak']

    # Menampilkan DataFrame hasil
    
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
        st.write("<h4>Distribusi Frekuensi dan Distribusi Probabilitas Untuk Kebutuhan Prediksi</h4>", unsafe_allow_html=True)
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
                            <li>dll</li>
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
                        </list><br><br>Oleh karena itu perusahaan harus memiliki beberapa strategi untuk menangani produk yang berkemungkinan 
                        penjualannya stagnand, dan menyiapkan jumlah produksi untuk produk yang memiliki prediksi baik
                     """, unsafe_allow_html=True) 
            

def questionKaryawan(dataset1, dataset2, dataset3):
    # Menggabungkan penjualan dengan karyawan berdasarkan kode_kasir
    penjualan_karyawan = dataset2.merge(dataset1, left_on='kode_kasir', right_on='kode_karyawan', suffixes=('_penjualan', '_karyawan'))

    # Membuat kolom nama lengkap
    penjualan_karyawan['nama_lengkap'] = penjualan_karyawan['nama_depan'] + ' ' + penjualan_karyawan['nama_belakang']

    # Mengganti nama kolom untuk konsistensi
    penjualan_karyawan.rename(columns={'kode_cabang_penjualan': 'kode_cabang'}, inplace=True)

    # Menggabungkan dengan tabel cabang
    penjualan_karyawan_cabang = penjualan_karyawan.merge(dataset3, on='kode_cabang', suffixes=('_penjualan', '_cabang'))

    # Konversi tgl_transaksi menjadi format tanggal
    penjualan_karyawan_cabang['tgl_transaksi'] = pd.to_datetime(penjualan_karyawan_cabang['tgl_transaksi'])

    # Tambahkan kolom bulan dan tahun
    penjualan_karyawan_cabang['bulan'] = penjualan_karyawan_cabang['tgl_transaksi'].dt.strftime('%B')
    penjualan_karyawan_cabang['tahun'] = penjualan_karyawan_cabang['tgl_transaksi'].dt.year

    # Agregasi penjualan per bulan
    monthly_sales = penjualan_karyawan_cabang.groupby(['kode_kasir', 'nama_lengkap', 'nama_cabang', 'bulan', 'tahun']).agg(
        jumlah_penjualan=('jumlah_pembelian', 'sum')
    ).reset_index()

    # Pivot tabel untuk mendapatkan format lebar
    pivot_table = monthly_sales.pivot_table(
        index=['kode_kasir', 'nama_lengkap', 'nama_cabang'],
        columns=['bulan', 'tahun'],
        values='jumlah_penjualan',
        fill_value=0
    )

    # Menyusun ulang kolom untuk bulan-bulan dalam setahun
    pivot_table.columns = [f'{bulan}_{tahun}' for bulan, tahun in pivot_table.columns]
    pivot_table = pivot_table.reset_index()
    
    all_months_data = pd.concat([pivot_table[col] for col in pivot_table.columns[3:]])

    # Menghitung nilai minimum dan maksimum dari semua data bulanan
    min_val = all_months_data.min()
    max_val = all_months_data.max()

    # Menentukan ukuran interval (misalkan 6 interval kelas)
    interval_size = (max_val - min_val) // 8
    bins = np.arange(min_val, max_val + interval_size + 1, interval_size)

    # Menghitung frekuensi
    intervals = pd.cut(all_months_data, bins=bins, include_lowest=True)
    frequency = intervals.value_counts().sort_index()

    # Menentukan batas bawah dan batas atas
    interval_boundaries = [(interval.left, interval.right) for interval in frequency.index]
    boundaries_df_karyawan = pd.DataFrame(interval_boundaries, columns=['Batas Bawah', 'Batas Atas'])
    boundaries_df_karyawan['Frekuensi'] = frequency.values

    # Menghitung probabilitas
    boundaries_df_karyawan['Probabilitas'] = boundaries_df_karyawan['Frekuensi'] / boundaries_df_karyawan['Frekuensi'].sum()

    # Menghitung probabilitas kumulatif
    boundaries_df_karyawan['Probabilitas Kumulatif'] = boundaries_df_karyawan['Probabilitas'].cumsum()

    # Menghitung jumlah angka acak
    total_random_numbers = 100
    boundaries_df_karyawan['Jumlah Angka Acak'] = (total_random_numbers * boundaries_df_karyawan['Probabilitas Kumulatif']).round().astype(int)

    # Menentukan batas bawah acak dan batas atas acak
    boundaries_df_karyawan['Batas Bawah Acak'] = np.concatenate(([0], boundaries_df_karyawan['Jumlah Angka Acak'].iloc[:-1].values + 1))
    boundaries_df_karyawan['Batas Atas Acak'] = boundaries_df_karyawan['Jumlah Angka Acak']
    
    
    # Bulan Januari
    januari = pivot_table[["kode_kasir", "nama_lengkap", "nama_cabang", "January_2008"]].copy()

    a = 1664525
    c = 1013904223
    m = 2**32
    seed = 4123

    num_values = len(januari)
    lcg_values = lcg(seed, a, c, m, num_values + 1)
    januari.loc[:, 'Zi-1'] = lcg_values[:-1]
    januari.loc[:, 'Zi'] = lcg_values[1:]

    januari.loc[:, 'Angka Acak'] = januari['Zi'] % 101  # Generate random numbers

    intervalsAcak = list(zip(boundaries_df_karyawan['Batas Bawah Acak'], boundaries_df_karyawan['Batas Atas Acak']))
    intervals= list(zip(boundaries_df_karyawan['Batas Bawah'], boundaries_df_karyawan['Batas Atas']))

    januari.loc[:, 'Prediksi'] = januari['Angka Acak'].apply(lambda x: get_prediksi(x, intervalsAcak, intervals))
    
    # Bulan Februari
    februari = pivot_table[["kode_kasir", "nama_lengkap", "nama_cabang", "February_2008"]].copy()

    a = 1664525
    c = 1013904223
    m = 2**32
    seed = 51232

    num_values = len(februari)
    lcg_values = lcg(seed, a, c, m, num_values + 1)
    februari.loc[:, 'Zi-1'] = lcg_values[:-1]
    februari.loc[:, 'Zi'] = lcg_values[1:]

    februari.loc[:, 'Angka Acak'] = februari['Zi'] % 101  # Generate random numbers

    intervalsAcak = list(zip(boundaries_df_karyawan['Batas Bawah Acak'], boundaries_df_karyawan['Batas Atas Acak']))
    intervals= list(zip(boundaries_df_karyawan['Batas Bawah'], boundaries_df_karyawan['Batas Atas']))

    februari.loc[:, 'Prediksi'] = februari['Angka Acak'].apply(lambda x: get_prediksi(x, intervalsAcak, intervals))
    
    # Bulan Maret
    maret = pivot_table[["kode_kasir", "nama_lengkap", "nama_cabang","March_2008"]].copy()

    a = 1664525
    c = 1013904223
    m = 2**32
    seed = 65231

    num_values = len(februari)
    lcg_values = lcg(seed, a, c, m, num_values + 1)
    maret.loc[:, 'Zi-1'] = lcg_values[:-1]
    maret.loc[:, 'Zi'] = lcg_values[1:]

    maret.loc[:, 'Angka Acak'] = maret['Zi'] % 101  # Generate random numbers

    intervalsAcak = list(zip(boundaries_df_karyawan['Batas Bawah Acak'], boundaries_df_karyawan['Batas Atas Acak']))
    intervals= list(zip(boundaries_df_karyawan['Batas Bawah'], boundaries_df_karyawan['Batas Atas']))

    maret.loc[:, 'Prediksi'] = maret['Angka Acak'].apply(lambda x: get_prediksi(x, intervalsAcak, intervals))
    
    # Bulan April
    april = pivot_table[["kode_kasir", "nama_lengkap", "nama_cabang","April_2008"]].copy()

    a = 1664525
    c = 1013904223
    m = 2**32
    seed = 12412

    num_values = len(februari)
    lcg_values = lcg(seed, a, c, m, num_values + 1)
    april.loc[:, 'Zi-1'] = lcg_values[:-1]
    april.loc[:, 'Zi'] = lcg_values[1:]

    april.loc[:, 'Angka Acak'] = april['Zi'] % 101  # Generate random numbers

    intervalsAcak = list(zip(boundaries_df_karyawan['Batas Bawah Acak'], boundaries_df_karyawan['Batas Atas Acak']))
    intervals= list(zip(boundaries_df_karyawan['Batas Bawah'], boundaries_df_karyawan['Batas Atas']))

    april.loc[:, 'Prediksi'] = april['Angka Acak'].apply(lambda x: get_prediksi(x, intervalsAcak, intervals))
    
    # Bulan Mei
    mei = pivot_table[["kode_kasir", "nama_lengkap", "nama_cabang","May_2008"]].copy()

    a = 1664525
    c = 1013904223
    m = 2**32
    seed = 24512

    num_values = len(februari)
    lcg_values = lcg(seed, a, c, m, num_values + 1)
    mei.loc[:, 'Zi-1'] = lcg_values[:-1]
    mei.loc[:, 'Zi'] = lcg_values[1:]

    mei.loc[:, 'Angka Acak'] = mei['Zi'] % 101  # Generate random numbers

    intervalsAcak = list(zip(boundaries_df_karyawan['Batas Bawah Acak'], boundaries_df_karyawan['Batas Atas Acak']))
    intervals= list(zip(boundaries_df_karyawan['Batas Bawah'], boundaries_df_karyawan['Batas Atas']))

    mei.loc[:, 'Prediksi'] = mei['Angka Acak'].apply(lambda x: get_prediksi(x, intervalsAcak, intervals))
    
    # Bulan Juni
    juni = pivot_table[["kode_kasir", "nama_lengkap", "nama_cabang","June_2008"]].copy()

    a = 1664525
    c = 1013904223
    m = 2**32
    seed = 71252

    num_values = len(februari)
    lcg_values = lcg(seed, a, c, m, num_values + 1)
    juni.loc[:, 'Zi-1'] = lcg_values[:-1]
    juni.loc[:, 'Zi'] = lcg_values[1:]

    juni.loc[:, 'Angka Acak'] = juni['Zi'] % 101  # Generate random numbers

    intervalsAcak = list(zip(boundaries_df_karyawan['Batas Bawah Acak'], boundaries_df_karyawan['Batas Atas Acak']))
    intervals= list(zip(boundaries_df_karyawan['Batas Bawah'], boundaries_df_karyawan['Batas Atas']))

    juni.loc[:, 'Prediksi'] = juni['Angka Acak'].apply(lambda x: get_prediksi(x, intervalsAcak, intervals))
    
    # Bulan Juli
    juli = pivot_table[["kode_kasir", "nama_lengkap", "nama_cabang","July_2008"]].copy()

    a = 1664525
    c = 1013904223
    m = 2**32
    seed = 85912

    num_values = len(februari)
    lcg_values = lcg(seed, a, c, m, num_values + 1)
    juli.loc[:, 'Zi-1'] = lcg_values[:-1]
    juli.loc[:, 'Zi'] = lcg_values[1:]

    juli.loc[:, 'Angka Acak'] = juli['Zi'] % 101  # Generate random numbers

    intervalsAcak = list(zip(boundaries_df_karyawan['Batas Bawah Acak'], boundaries_df_karyawan['Batas Atas Acak']))
    intervals= list(zip(boundaries_df_karyawan['Batas Bawah'], boundaries_df_karyawan['Batas Atas']))

    juli.loc[:, 'Prediksi'] = juli['Angka Acak'].apply(lambda x: get_prediksi(x, intervalsAcak, intervals))
    
    # Bulan Agustus
    agustus = pivot_table[["kode_kasir", "nama_lengkap", "nama_cabang","August_2008"]].copy()

    a = 1664525
    c = 1013904223
    m = 2**32
    seed = 105123

    num_values = len(februari)
    lcg_values = lcg(seed, a, c, m, num_values + 1)
    agustus.loc[:, 'Zi-1'] = lcg_values[:-1]
    agustus.loc[:, 'Zi'] = lcg_values[1:]

    agustus.loc[:, 'Angka Acak'] = juli['Zi'] % 101  # Generate random numbers

    intervalsAcak = list(zip(boundaries_df_karyawan['Batas Bawah Acak'], boundaries_df_karyawan['Batas Atas Acak']))
    intervals= list(zip(boundaries_df_karyawan['Batas Bawah'], boundaries_df_karyawan['Batas Atas']))

    agustus.loc[:, 'Prediksi'] = agustus['Angka Acak'].apply(lambda x: get_prediksi(x, intervalsAcak, intervals))
    
    # Bulan September
    september = pivot_table[["kode_kasir", "nama_lengkap", "nama_cabang","September_2008"]].copy()

    a = 1664525
    c = 1013904223
    m = 2**32
    seed = 51662

    num_values = len(februari)
    lcg_values = lcg(seed, a, c, m, num_values + 1)
    september.loc[:, 'Zi-1'] = lcg_values[:-1]
    september.loc[:, 'Zi'] = lcg_values[1:]

    september.loc[:, 'Angka Acak'] = juli['Zi'] % 101  # Generate random numbers

    intervalsAcak = list(zip(boundaries_df_karyawan['Batas Bawah Acak'], boundaries_df_karyawan['Batas Atas Acak']))
    intervals= list(zip(boundaries_df_karyawan['Batas Bawah'], boundaries_df_karyawan['Batas Atas']))

    september.loc[:, 'Prediksi'] = september['Angka Acak'].apply(lambda x: get_prediksi(x, intervalsAcak, intervals))
    
    # Bulan Oktober
    oktober = pivot_table[["kode_kasir", "nama_lengkap", "nama_cabang","October_2008"]].copy()

    a = 1664525
    c = 1013904223
    m = 2**32
    seed = 86125

    num_values = len(februari)
    lcg_values = lcg(seed, a, c, m, num_values + 1)
    oktober.loc[:, 'Zi-1'] = lcg_values[:-1]
    oktober.loc[:, 'Zi'] = lcg_values[1:]

    oktober.loc[:, 'Angka Acak'] = oktober['Zi'] % 101  # Generate random numbers

    intervalsAcak = list(zip(boundaries_df_karyawan['Batas Bawah Acak'], boundaries_df_karyawan['Batas Atas Acak']))
    intervals= list(zip(boundaries_df_karyawan['Batas Bawah'], boundaries_df_karyawan['Batas Atas']))

    oktober.loc[:, 'Prediksi'] = oktober['Angka Acak'].apply(lambda x: get_prediksi(x, intervalsAcak, intervals))
    
    # Bulan November
    november = pivot_table[["kode_kasir", "nama_lengkap", "nama_cabang","November_2008"]].copy()

    a = 1664525
    c = 1013904223
    m = 2**32
    seed = 92512

    num_values = len(februari)
    lcg_values = lcg(seed, a, c, m, num_values + 1)
    november.loc[:, 'Zi-1'] = lcg_values[:-1]
    november.loc[:, 'Zi'] = lcg_values[1:]

    november.loc[:, 'Angka Acak'] = november['Zi'] % 101  # Generate random numbers

    intervalsAcak = list(zip(boundaries_df_karyawan['Batas Bawah Acak'], boundaries_df_karyawan['Batas Atas Acak']))
    intervals= list(zip(boundaries_df_karyawan['Batas Bawah'], boundaries_df_karyawan['Batas Atas']))

    november.loc[:, 'Prediksi'] = november['Angka Acak'].apply(lambda x: get_prediksi(x, intervalsAcak, intervals))
    
    # Bulan Desember
    desember = pivot_table[["kode_kasir", "nama_lengkap", "nama_cabang","December_2008"]].copy()

    a = 1664525
    c = 1013904223
    m = 2**32
    seed = 962551

    num_values = len(februari)
    lcg_values = lcg(seed, a, c, m, num_values + 1)
    desember.loc[:, 'Zi-1'] = lcg_values[:-1]
    desember.loc[:, 'Zi'] = lcg_values[1:]

    desember.loc[:, 'Angka Acak'] = november['Zi'] % 101  # Generate random numbers

    intervalsAcak = list(zip(boundaries_df_karyawan['Batas Bawah Acak'], boundaries_df_karyawan['Batas Atas Acak']))
    intervals= list(zip(boundaries_df_karyawan['Batas Bawah'], boundaries_df_karyawan['Batas Atas']))

    desember.loc[:, 'Prediksi'] = desember['Angka Acak'].apply(lambda x: get_prediksi(x, intervalsAcak, intervals))
    
    januari = januari[['kode_kasir', 'nama_lengkap', 'nama_cabang', 'Zi-1', 'Zi', 'Angka Acak', 'Prediksi']]    
    februari = februari[['kode_kasir', 'nama_lengkap', 'nama_cabang', 'Zi-1', 'Zi', 'Angka Acak', 'Prediksi']]    
    maret = maret[['kode_kasir', 'nama_lengkap', 'nama_cabang', 'Zi-1', 'Zi', 'Angka Acak', 'Prediksi']]    
    april = april[['kode_kasir', 'nama_lengkap', 'nama_cabang', 'Zi-1', 'Zi', 'Angka Acak', 'Prediksi']]    
    mei = mei[['kode_kasir', 'nama_lengkap', 'nama_cabang', 'Zi-1', 'Zi', 'Angka Acak', 'Prediksi']]    
    juni = juni[['kode_kasir', 'nama_lengkap', 'nama_cabang', 'Zi-1', 'Zi', 'Angka Acak', 'Prediksi']]    
    juli = juli[['kode_kasir', 'nama_lengkap', 'nama_cabang', 'Zi-1', 'Zi', 'Angka Acak', 'Prediksi']]    
    agustus = agustus[['kode_kasir', 'nama_lengkap', 'nama_cabang', 'Zi-1', 'Zi', 'Angka Acak', 'Prediksi']]    
    september = september[['kode_kasir', 'nama_lengkap', 'nama_cabang', 'Zi-1', 'Zi', 'Angka Acak', 'Prediksi']]    
    oktober = oktober[['kode_kasir', 'nama_lengkap', 'nama_cabang', 'Zi-1', 'Zi', 'Angka Acak', 'Prediksi']]    
    november = november[['kode_kasir', 'nama_lengkap', 'nama_cabang', 'Zi-1', 'Zi', 'Angka Acak', 'Prediksi']]    
    desember = desember[['kode_kasir', 'nama_lengkap', 'nama_cabang', 'Zi-1', 'Zi', 'Angka Acak', 'Prediksi']]    

    with st.container():
        st.write("<h4>Hasil penggabungan data penjualan produk, karyawan, dan cabang, lalu menjumlahkan semua transaksi berdasarkan bulan</h4>", unsafe_allow_html=True)
        st.dataframe(pivot_table, use_container_width=True, hide_index=True)
        st.write("<br>", unsafe_allow_html=True)
        
    with st.container():
        st.write("<h4>Distribusi Frekuensi dan Distribusi Probabilitas Untuk Kebutuhan Prediksi</h4>", unsafe_allow_html=True)
        st.dataframe(boundaries_df_karyawan, hide_index=True, use_container_width=True)
        st.write("<br>", unsafe_allow_html=True)
        
    with st.container():
        st.write("<h2>Hasil Model Simulasi Prediksi Kinerja Karyawan Berdasarkan Banyaknya Transaksi Menggunakan LCG</h2>", unsafe_allow_html=True)
        
        st.write("<h4>Bulan Januari</h4>", unsafe_allow_html=True)
        st.dataframe(januari.style.highlight_max(subset='Prediksi', axis=0, color='#198754'), use_container_width=True, hide_index=True)
        st.write("<br>", unsafe_allow_html=True)
        
        st.write("<h4>Bulan Februari</h4>", unsafe_allow_html=True)
        st.dataframe(februari.style.highlight_max(subset='Prediksi', axis=0, color='#198754'), use_container_width=True, hide_index=True)
        st.write("<br>", unsafe_allow_html=True)
        
        st.write("<h4>Bulan Maret</h4>", unsafe_allow_html=True)
        st.dataframe(maret.style.highlight_max(subset='Prediksi', axis=0, color='#198754'), use_container_width=True, hide_index=True)
        st.write("<br>", unsafe_allow_html=True)
        
        st.write("<h4>Bulan April</h4>", unsafe_allow_html=True)
        st.dataframe(april.style.highlight_max(subset='Prediksi', axis=0, color='#198754'), use_container_width=True, hide_index=True)
        st.write("<br>", unsafe_allow_html=True)
        
        st.write("<h4>Bulan Mei</h4>", unsafe_allow_html=True)
        st.dataframe(mei.style.highlight_max(subset='Prediksi', axis=0, color='#198754'), use_container_width=True, hide_index=True)
        st.write("<br>", unsafe_allow_html=True)
        
        st.write("<h4>Bulan Juni</h4>", unsafe_allow_html=True)
        st.dataframe(juni.style.highlight_max(subset='Prediksi', axis=0, color='#198754'), use_container_width=True, hide_index=True)
        st.write("<br>", unsafe_allow_html=True)
        
        st.write("<h4>Bulan Juli</h4>", unsafe_allow_html=True)
        st.dataframe(juli.style.highlight_max(subset='Prediksi', axis=0, color='#198754'), use_container_width=True, hide_index=True)
        st.write("<br>", unsafe_allow_html=True)
        
        st.write("<h4>Bulan Agustus</h4>", unsafe_allow_html=True)
        st.dataframe(agustus.style.highlight_max(subset='Prediksi', axis=0, color='#198754'), use_container_width=True, hide_index=True)
        st.write("<br>", unsafe_allow_html=True)
        
        st.write("<h4>Bulan September</h4>", unsafe_allow_html=True)
        st.dataframe(september.style.highlight_max(subset='Prediksi', axis=0, color='#198754'), use_container_width=True, hide_index=True)
        st.write("<br>", unsafe_allow_html=True)
        
        st.write("<h4>Bulan Oktober</h4>", unsafe_allow_html=True)
        st.dataframe(oktober.style.highlight_max(subset='Prediksi', axis=0, color='#198754'), use_container_width=True, hide_index=True)
        st.write("<br>", unsafe_allow_html=True)
        
        st.write("<h4>Bulan November</h4>", unsafe_allow_html=True)
        st.dataframe(november.style.highlight_max(subset='Prediksi', axis=0, color='#198754'), use_container_width=True, hide_index=True)
        st.write("<br>", unsafe_allow_html=True)
        
        st.write("<h4>Bulan Desember</h4>", unsafe_allow_html=True)
        st.dataframe(desember.style.highlight_max(subset='Prediksi', axis=0, color='#198754'), use_container_width=True, hide_index=True)
        st.write("<br>", unsafe_allow_html=True)
        
        with st.expander("Kesimpulan dari Model Simulasi diatas:") :
            st.write("""
                        Dari simulasi diatas kita bisa melihat bahwa terdapat prediksi kinerja karyawan yang meningkat atau konstan, oleh karena
                        itu perusahaan dapat memberi pengghargaan atau pelatihan tambahan pada karyawan yang bersangkutan
                     """)
    
        
        
    
    
