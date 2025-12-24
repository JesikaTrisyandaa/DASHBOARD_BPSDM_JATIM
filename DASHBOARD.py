import streamlit as st
import pandas as pd
import plotly.express as px
import glob
import os
import numpy as np
import statsmodels.api as sm
import base64
from sklearn.feature_extraction.text import CountVectorizer
import plotly.graph_objects as go
from scipy.stats import f_oneway

st.set_page_config(page_title="Dashboard Monitoring BPSDM JATIM",  
                   page_icon="D:\JES\JESIKA\.vscode\.vscode SEMESTER 5\PROJECT\DATASET MINI PROJECT\DATA_FOTO\BPSDMJATIM.png", 
                   layout="wide")

def set_background_local(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <style>
        /* ===== BACKGROUND ===== */
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: top center;
            background-repeat: no-repeat;
            background-color: #f4f6f9;
        }}

        /* ===== HILANGKAN HEADER PUTIH ===== */
        header[data-testid="stHeader"] {{
            background: transparent !important;
            box-shadow: none !important;
        }}


        div[data-testid="stDecoration"] {{
            display: none !important;
        }}

        /* ===== MAIN AREA ===== */
        .stApp > main {{
            background-color: transparent;
        }}

        /* ===== KONTEN ===== */
        .block-container {{
            padding-top: 4rem;
        }}

        /* ===== OVERLAY (opsional) ===== */
        .overlay {{
            background-color: rgba(255, 255, 255, 0.92);
            padding: 40px;
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
        <style>
        /* Lebarkan area konten utama */
        .block-container {
            max-width: 1400px;   /* bisa 1200px, 1600px, atau 100% */
            padding-left: 3rem;
            padding-right: 3rem;
        }

        /* Kalau mau full sampai samping */
        @media (min-width: 1200px) {
            .block-container {
                max-width: 95%;
            }
        }
        </style>
        """, unsafe_allow_html=True)


set_background_local(r"D:\JES\JESIKA\.vscode\.vscode SEMESTER 5\PROJECT\DATASET MINI PROJECT\DATA_FOTO\BACKGROUND.png")

if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

if "page" not in st.session_state:
    st.session_state.page = "Beranda" 

with st.container():
    if st.button("☰", key="toggle_sidebar"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open
        st.rerun()

folder_path = r"D:/JES/JESIKA/.vscode/.vscode SEMESTER 5/PROJECT/DATASET MINI PROJECT/DATA_SIAP/"
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

if len(csv_files) == 0:
    st.error("❌ Tidak ada file CSV ditemukan di folder DATA_SIAP.")
else:
    df_list = []
    for file in csv_files:
        temp = pd.read_csv(file)
        temp["pelatihan"] = os.path.basename(file).replace(".csv", "")
        df_list.append(temp)

    df_all = pd.concat(df_list, ignore_index=True)
    df_all["nama"] = df_all["nama"].astype(str).str.strip().str.lower()


if st.session_state.sidebar_open:

    with st.sidebar:
        col1, col2 = st.columns([1, 3])

    with col1:
        st.image("D:\JES\JESIKA\.vscode\.vscode SEMESTER 5\PROJECT\DATASET MINI PROJECT\DATA_FOTO\BPSDMJATIM.png", width=400)   # ganti logo.png sesuai file kamu

    with col2:
        st.markdown("### **BPSDM**")

        menu = {
        "🏠 Beranda": "Beranda",
        "📊 Analisis & Visualisasi Data": "Visualisasi",
        "📌 Analisis Kehadiran (KAK IV - VI)": "Kehadiran",
        "⭐ Evaluasi Pelatihan": "Evaluasi",
        "ℹ️ Tentang Sistem": "Tentang",
    }

        st.markdown("""
        <style>

        div.stButton > button, .selected-button {
            background-color: #f0f2f6;
            color: black;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;

            /* AGAR RATA KIRI & TIDAK BERGESER */
            width: 100% !important;
            text-align: left !important;
            display: block !important;
            margin-top: -10px;
        }

        div.stButton > button:hover {
            background-color: #f0f2f6;
            color: #0055A4;
        }

        /* BUTTON AKTIF */
        .selected-button {
            color: #0055A4 !important;
            margin-top: -10px;
        }

        </style>
        """, unsafe_allow_html=True)

        for label, page in menu.items():

                if st.session_state.page == page:
                    st.markdown(
                        f"<div class='selected-button'>{label}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    if st.button(label, key=page):
                        st.session_state.page = page
                        st.rerun()


if st.session_state.page == "Beranda":
    
    st.markdown("""
        <div class="hero-title">
            <h1>Dashboard Monitoring Pelatihan</h1>
            <h2>BPSDM Provinsi Jawa Timur</h2>
            <h3>Bidang Pengembangan Kompetensi Fungsional dan Sosial Kultural</h3>
            <p>
                Sistem monitoring dan evaluasi pelaksanaan program pelatihan
                untuk mendukung pengambilan keputusan
            </p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""
        <style>
        .hero-title {
            max-width: 1100px;
            margin: 0 auto 3rem auto;
            text-align: center;
        }

        .hero-title h1 {
            margin-top: -5;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: -2.6rem;  
            color: #1f2937;
        }

        .hero-title h2 {
            margin-top: -17;           
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: -2rem;  
            color: #1f2937;
        }
        .hero-title h3 {
            margin-top: -17;           
            font-size: 1.9rem;
            font-weight: 700;
            margin-bottom: 0.6rem;
            color: #1f2937;
        }

        .hero-title p {
            font-size: 1.1rem;
            color: #4b5563;
            margin-bottom: -3rem;
            line-height: 1.7;
        }
        </style>
        """, unsafe_allow_html=True)

            
    st.markdown("### Statistik Utama")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Pelatihan", df_all["pelatihan"].nunique())
    col2.metric("Total Peserta", len(df_all))
    col3.metric("Rata-rata Pre-Test", f"{df_all['pre'].mean():.2f}")
    col4.metric("Rata-rata Post-Test", f"{df_all['post'].mean():.2f}")
    col5.metric("Rata-rata Kenaikan Nilai", f"{df_all['perubahan'].mean():.2f}")

    df_view = df_all.copy()
    df_slope = (
        df_view
        .groupby("pelatihan")[["pre", "post"]]
        .mean()
        .reset_index()
        .melt(id_vars="pelatihan", var_name="Tahap", value_name="Nilai")
    )

    fig_slope = px.line(
        df_slope,
        x="Tahap",
        y="Nilai",
        color="pelatihan",
        markers=True,
        title="Perbandingan Nilai Pre-Test dan Post-Test per Pelatihan"
    )

    fig_slope.update_layout(
        xaxis_title="Tahap Evaluasi",
        yaxis_title="Rata-rata Nilai",
    )

    st.plotly_chart(fig_slope, use_container_width=True)


    st.markdown("### Highlight Insight")
    persen_naik = (df_all["perubahan"] > 0).mean() * 100
    pelatihan_tertinggi = (
        df_all.groupby("pelatihan")["perubahan"].mean().idxmax()
    )
    
    custom_nama = {
        "BIBIT": "Pelatihan Penilaian Mutu Bibit Tanaman Hutan",
        "KAK_IV": "Pelatihan Khusus Analis Kebijakan Angkatan IV",
        "KAK_V": "Pelatihan Khusus Analis Kebijakan Angkatan V",
        "KAK_VI": "Pelatihan Khusus Analis Kebijakan Angkatan VI",
        "KASUS_I": "Pelatihan Pejabat Fungsional Pekerja Sosial Manajemen Kasus Angkatan I",
        "KASUS_II": "Pelatihan Pejabat Fungsional Pekerja Sosial Manajemen Kasus Angkatan II",
        "PERENCANAAN_II": "Pelatihan Perencanaan dan Penganggaran Angkatan II",
        "PERENCANAAN_I": "Pelatihan Perencanaan dan Penganggaran Angkatan I",
        "PRAKOM": "Pelatihan Penguatan Jabatan Fungsional Pranata Komputer",
        "SDMA_I": "Pelatihan Analis Sumber Daya Manusia Aparatur Angkatan I",
        "SDMA_II": "Pelatihan Analis Sumber Daya Manusia Aparatur Angkatan II",
    }
    st.markdown(f"""
    - 📈 **{persen_naik:.1f}% peserta mengalami kenaikan nilai**
    - 🏆 **Pelatihan dengan rata-rata kenaikan tertinggi:**  
      **{custom_nama.get(pelatihan_tertinggi, pelatihan_tertinggi)}**
    - ⚠️ **Catatan:** Data kehadiran hanya tersedia untuk  
      **Pelatihan KAK Angkatan III–V**
    """)

    raw_list = df_all["pelatihan"].unique()
    clean_list = [custom_nama.get(x, x) for x in raw_list]

    st.markdown("### Daftar Pelatihan Tahun 2025")
    st.caption("Daftar seluruh program pelatihan yang dianalisis pada dashboard ini.")

    df_pel = pd.DataFrame({"Nama Pelatihan": clean_list})
    df_pel.index += 1
    df_pel.index.name = "No"

    st.dataframe(
        df_pel,
        use_container_width=True,
        height=380
    )
    st.markdown("""
        <style>
        [data-testid="stDataFrame"] table {
            font-size: 14px;
        }

        [data-testid="stDataFrame"] tbody tr:nth-child(even) {
            background-color: #f9fafb;
        }
        </style>
        """, unsafe_allow_html=True)



    st.markdown("### Preview Data Peserta")
    df_show = df_all.copy()
    if "id_peserta" not in df_show.columns:
        df_show["id_peserta"] = ["P{:03d}".format(i) for i in range(1, len(df_show) + 1)]

    kolom_dihapus = [
        "nama", "alamat_surel", "nama_depan",
        "jumlah_hadir", "total_kelas", "persentase_kehadiran"
    ]
    df_show = df_show.drop(columns=[c for c in kolom_dihapus if c in df_show.columns])

    if "persentase_naik" in df_show.columns:
        df_show["persentase_naik"] = df_show["persentase_naik"].round(1).astype(str) + "%"

    rename_kolom = {
        "id_peserta": "ID Peserta",
        "pelatihan": "Nama Pelatihan",
        "pre": "Nilai Pre-Test",
        "post": "Nilai Post-Test",
        "perubahan": "Perubahan Poin",
        "persentase_naik": "Kenaikan Nilai (%)",
        "kategori": "Kategori"
    }
    df_show = df_show.rename(columns={k: v for k, v in rename_kolom.items() if k in df_show.columns})

    df_show = df_show.reset_index(drop=True)
    df_show.index += 1

    st.dataframe(df_show, use_container_width=True)

elif st.session_state.page == "Visualisasi":
    
    st.markdown(
        "<h2 style='text-align:center; font-weight:700;'>📊 Analisis & Visualisasi Data</h2>",
        unsafe_allow_html=True
    )
    for col in ["pre", "post", "perubahan"]:
        df_all[col] = pd.to_numeric(df_all[col], errors="coerce")

    st.markdown("### 🔎 Filter Data")
    colf1, colf2, colf3 = st.columns([3,3,1])

    with colf1:
        raw_list = df_all["pelatihan"].unique()
        custom_nama = {
            "BIBIT": "Pelatihan Penilaian Mutu Bibit Tanaman Hutan",
            "KAK_IV": "Pelatihan Khusus Analis Kebijakan Angkatan IV",
            "KAK_V": "Pelatihan Khusus Analis Kebijakan Angkatan V",
            "KAK_VI": "Pelatihan Khusus Analis Kebijakan Angkatan VI",
            "KASUS_I": "Pelatihan Pejabat Fungsional Pekerja Sosial Manajemen Kasus Angkatan I",
            "KASUS_II": " Pelatihan Pejabat Fungsional Pekerja Sosial Manajemen Kasus Angkatan II",
            "PERENCANAAN_II": "Pelatihan Perencanaan dan Penganggaran Angkatan II",
            "PERENCANAAN_I": "Pelatihan Perencanaan dan Penganggaran Angkatan I",
            "PRAKOM": "Pelatihan Penguatan Jabatan Fungsional Pranata Komputer",
            "SDMA_I": "Pelatihan Analis Sumber Daya Manusia Aparatur Angkatan I",
            "SDMA_II": "Pelatihan Analis Sumber Daya Manusia Aparatur Angkatan II",
        }

        display_list = ["Semua"] + [custom_nama.get(x, x) for x in raw_list]

        pilih_display = st.selectbox("Pilih Pelatihan:", display_list)

        if pilih_display == "Semua":
            pilih_pelatihan = "Semua"
        else:
            reverse_map = {v: k for k, v in custom_nama.items()}
            pilih_pelatihan = reverse_map.get(pilih_display, pilih_display)
    if pilih_display != "Semua":
        st.info(f"📘 **Pelatihan Dipilih:** {pilih_display}")

    with colf2:
        if "kategori" in df_all.columns:
            pilihan_kategori = st.multiselect("Filter Kategori (opsional):", ["Semua"] + list(df_all["kategori"].unique()), default=["Semua"])
        else:
            pilihan_kategori = ["Semua"]
    with colf3:
        top_n = st.number_input("Top N Leaderboard:", min_value=5, max_value=100, value=10, step=5)

    df_view = df_all.copy()
    if pilih_pelatihan != "Semua":
        df_view = df_view[df_view["pelatihan"] == pilih_pelatihan]
    if "kategori" in df_view.columns and not (("Semua" in pilihan_kategori) or (len(pilihan_kategori)==0)):
        df_view = df_view[df_view["kategori"].isin(pilihan_kategori)]

    st.subheader("Ringkasan Statistik")
    total_peserta = len(df_view)
    total_pelatihan = df_view["pelatihan"].nunique()
    avg_pre = df_view["pre"].mean()
    avg_post = df_view["post"].mean()
    avg_change = df_view["perubahan"].mean()
    pct_increase = (df_view["perubahan"] > 0).sum() / (total_peserta if total_peserta>0 else 1) * 100
    min_pre, max_pre = df_view["pre"].min(), df_view["pre"].max()
    min_post, max_post = df_view["post"].min(), df_view["post"].max()
    std_pre, std_post = df_view["pre"].std(), df_view["post"].std()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Peserta", f"{total_peserta}")
    col2.metric("Avg Pre", f"{avg_pre:.2f}" if not np.isnan(avg_pre) else "-")
    col3.metric("Avg Post", f"{avg_post:.2f}" if not np.isnan(avg_post) else "-")
    col4.metric("Avg Perubahan", f"{avg_change:.2f}" if not np.isnan(avg_change) else "-")
    col5.metric("% Peserta Naik", f"{pct_increase:.1f}%")
    
    st.markdown("### Detail Statistik")

    col1, col2, col3, col4, col5  = st.columns(5)
    
    with col1:
        st.metric("Nilai Minimal Pre Test", min_pre)
    with col2:
        st.metric("Nilai Maksimal Pre Test", max_pre)
    with col3:
        st.metric("Nilai Minimal Post Test", min_post)
    with col4:
        st.metric("Nilai Maksimal Post Test", max_post)
    with col5:
        st.metric("Jumlah Pelatihan (terfilter)", total_pelatihan)

    min_change = df_view["perubahan"].min()
    max_change = df_view["perubahan"].max()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Perubahan Minimum", f"{min_change:.2f}")
    col2.metric("Perubahan Maksimum", f"{max_change:.2f}")

    st.markdown("#### Distribusi Nilai")
    col1, col2, col3 = st.columns(3)

    with col1:
        values = df_view["pre"]

        counts, bins = np.histogram(values, bins=10)
        bin_labels = [f"{bins[i]:.1f}–{bins[i+1]:.1f}" for i in range(len(bins)-1)]

        df_hist = pd.DataFrame({
            "Rentang": bin_labels,
            "Jumlah": counts
        })

        max_idx = df_hist["Jumlah"].idxmax()

        fig = px.bar(
            df_hist,
            x="Jumlah",
            y="Rentang",
            orientation="h",
            title="Distribusi Nilai Pre-Test"
        )

        fig.update_traces(
            marker_color=[
                "#ff6b6b" if i == max_idx else "#37c9ef"
                for i in range(len(df_hist))
            ],
            marker_line_color="white",
            marker_line_width=1,
            text=df_hist["Jumlah"],
            textposition="outside"
        )
        st.plotly_chart(fig, use_container_width=True)


    with col2:
        values = df_view["post"]

        counts, bins = np.histogram(values, bins=10)
        bin_labels = [f"{bins[i]:.1f}–{bins[i+1]:.1f}" for i in range(len(bins)-1)]

        df_hist = pd.DataFrame({
            "Rentang": bin_labels,
            "Jumlah": counts
        })

        max_idx = df_hist["Jumlah"].idxmax()

        fig = px.bar(
            df_hist,
            x="Jumlah",
            y="Rentang",
            orientation="h",
            title="Distribusi Nilai Post-Test"
        )

        fig.update_traces(
            marker_color=[
                "#ff6b6b" if i == max_idx else "#37c9ef"
                for i in range(len(df_hist))
            ],
            marker_line_color="white",
            marker_line_width=1,
            text=df_hist["Jumlah"],
            textposition="outside"
        )
        st.plotly_chart(fig, use_container_width=True)


    st.markdown("### Dampak Pelatihan (Pre vs Post Test)")

    df_slope = (
        df_view
        .groupby("pelatihan")[["pre", "post"]]
        .mean()
        .reset_index()
        .melt(id_vars="pelatihan", var_name="Tahap", value_name="Nilai")
    )

    fig_slope = px.line(
        df_slope,
        x="Tahap",
        y="Nilai",
        color="pelatihan",
        markers=True,
        title="Perbandingan Nilai Pre-Test dan Post-Test per Pelatihan"
    )

    fig_slope.update_layout(
        xaxis_title="Tahap Evaluasi",
        yaxis_title="Rata-rata Nilai",
    )

    st.plotly_chart(fig_slope, use_container_width=True)

    with col3:
        values = df_view["perubahan"]

        counts, bins = np.histogram(values, bins=10)
        bin_labels = [
            f"{bins[i]:.1f}–{bins[i+1]:.1f}"
            for i in range(len(bins)-1)
        ]

        df_hist = pd.DataFrame({
            "Rentang Perubahan": bin_labels,
            "Jumlah Peserta": counts
        })

        max_idx = df_hist["Jumlah Peserta"].idxmax()

        fig = px.bar(
            df_hist,
            x="Jumlah Peserta",
            y="Rentang Perubahan",
            orientation="h",
            title="Distribusi Kenaikan Nilai"
        )
        fig.update_traces(
            marker_color=[
                "#ff6b6b" if i == max_idx else "#37c9ef"
                for i in range(len(df_hist))
            ],
            marker_line_color="white",
            marker_line_width=1,
            text=df_hist["Jumlah Peserta"],
            textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Jumlah Peserta",
            yaxis_title="Rentang Kenaikan Nilai",
            bargap=0.2
        )

        st.plotly_chart(fig, use_container_width=True)
    rata_pre = df_view["pre"].mean()
    rata_post = df_view["post"].mean()
    kenaikan = rata_post - rata_pre

    st.info(
        f"""
    **Insight Dampak Pelatihan**

    Rata-rata nilai peserta meningkat dari **{rata_pre:.1f}** (pre-test)
    menjadi **{rata_post:.1f}** (post-test),
    dengan rata-rata kenaikan sebesar **{kenaikan:.1f} poin**.
    Mengindikasikan bahwa pelatihan memberikan
    **dampak positif terhadap peningkatan pemahaman peserta**.
    """
    )

    st.markdown("### 🚨 Analisis Outlier Perubahan Nilai")

    q1 = df_view["perubahan"].quantile(0.25)
    q3 = df_view["perubahan"].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outlier_count = ((df_view["perubahan"] < lower) | (df_view["perubahan"] > upper)).sum()

    st.info(
        f"Ditemukan **{outlier_count} peserta** dengan perubahan nilai ekstrem "
        f"(berdasarkan metode IQR). Outlier ini dapat memengaruhi rata-rata "
        f"dan interpretasi hasil analisis."
    )
    st.markdown("##### Investigasi Peserta Outlier")
    outlier_df = df_view[
        (df_view["perubahan"] < lower) | (df_view["perubahan"] > upper)
    ]
    df_out = outlier_df[
        ["pelatihan", "pre", "post", "perubahan", "kategori"]
    ].reset_index(drop=True)
    df_out.index = df_out.index + 1
    st.dataframe(df_out, use_container_width=True)


    st.markdown("##### Dampak Outlier terhadap Rata-rata Kenaikan Nilai")
    avg_with_outlier = df_view["perubahan"].mean()
    avg_without_outlier = df_view[
        (df_view["perubahan"] >= lower) & (df_view["perubahan"] <= upper)
    ]["perubahan"].mean()
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Rata-rata (dengan outlier)",
        f"{avg_with_outlier:.2f}"
    )
    col2.metric(
        "Rata-rata (tanpa outlier)",
        f"{avg_without_outlier:.2f}"
    )
    selisih = avg_without_outlier - avg_with_outlier
    col3.metric(
        "Selisih",
        f"{selisih:.2f}"
    )
    st.info(
        f"Perbedaan rata-rata kenaikan nilai sebelum dan sesudah penghapusan "
        f"outlier hanya sebesar **{selisih:.2f} poin**. Hal ini menunjukkan bahwa "
        f"outlier tidak memberikan pengaruh signifikan terhadap statistik deskriptif. "
        f"Oleh karena itu, outlier tetap dipertahankan sebagai bagian dari variasi "
        f"alami data untuk menjaga keutuhan analisis."
    )
 
    st.markdown("### Rata-rata Perubahan Nilai per Pelatihan")
    df_bar_change = (
        df_view.groupby("pelatihan")["perubahan"]
        .mean()
        .reset_index()
        .sort_values("perubahan", ascending=False)
    )
    df_bar_change["Highlight"] = [
        "Tertinggi" if i == 0 else "Lainnya"
        for i in range(len(df_bar_change))
    ]
    fig_bar_change = px.bar(
        df_bar_change,
        x="pelatihan",
        y="perubahan",
        text_auto=".2f",
        color="Highlight",
        color_discrete_map={
            "Tertinggi": "#ff6b6b",
            "Lainnya": "#37c9ef"
        },
        title="Rata-rata Kenaikan Nilai per Pelatihan"
    )
    fig_bar_change.update_layout(
        xaxis_title="Pelatihan",
        yaxis_title="Rata-rata Kenaikan Nilai (poin)",
        showlegend=False
    )
    st.plotly_chart(fig_bar_change, use_container_width=True)
    


    st.markdown("### Distribusi Kenaikan Nilai per Angkatan")
    fig_box = px.box(
        df_view,               
        x="pelatihan",
        y="perubahan",
        color="pelatihan",       
        points="all",
        title="Sebaran Kenaikan Nilai Antar Angkatan (KAK IV–VI)",
        labels={
            "pelatihan": "Pelatihan",
            "perubahan": "Perubahan Nilai"
        }
    )
    fig_box.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_box, use_container_width=True)

    if len(df_bar_change) >= 2:
        max_pel = df_bar_change.iloc[0]
        min_pel = df_bar_change.iloc[-1]

        st.info(
            f"Pelatihan dengan **rata-rata kenaikan nilai tertinggi** adalah "
            f"**{max_pel['pelatihan']}** ({max_pel['perubahan']:.2f}). "
            f"Sementara itu, pelatihan dengan kenaikan terendah adalah "
            f"**{min_pel['pelatihan']}** ({min_pel['perubahan']:.2f}). "
            "Perbedaan sebaran nilai menunjukkan variasi efektivitas pelatihan "
            "yang dapat dipengaruhi oleh metode pelaksanaan dan karakteristik peserta."
        )
    else:
        st.info("Data belum cukup untuk menghasilkan insight perbandingan.")

    
    st.markdown(f"### 🥇 Leaderboard Peserta Top {top_n} (Berdasarkan Kenaikan Nilai)")
    df_view = df_view.copy()
    if "id_peserta" not in df_view.columns:
        df_view["id_peserta"] = ["P{:03d}".format(i) for i in range(1, len(df_view) + 1)]
    df_leader = (
        df_view
        .sort_values(by="perubahan", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    df_leader.index = df_leader.index + 1
    if "persentase_naik" in df_leader.columns:
        df_leader["persentase_naik"] = (
            df_leader["persentase_naik"].round(1).astype(str) + "%"
        )

    rename_kolom = {
        "id_peserta": "ID Peserta",
        "pelatihan": "Nama Pelatihan",
        "pre": "Nilai Pre-Test",
        "post": "Nilai Post-Test",
        "perubahan": "Perubahan Poin",
        "persentase_naik": "Kenaikan Nilai (%)",
        "kategori": "Kategori"
    }
    df_leader = df_leader.rename(
        columns={k: v for k, v in rename_kolom.items() if k in df_leader.columns}
    )

    st.dataframe(
        df_leader[
            [
                "ID Peserta",
                "Nama Pelatihan",
                "Nilai Pre-Test",
                "Nilai Post-Test",
                "Perubahan Poin",
                "Kategori"
            ]
        ],
        use_container_width=True
    )

    st.markdown("### Heatmap Korelasi (pre, post, perubahan)")
    cols_for_corr = [c for c in ["pre", "post", "perubahan"] if c in df_view.columns]
    if len(cols_for_corr) > 1:
        corr_mat = df_view[cols_for_corr].corr()
        fig_heat = px.imshow(corr_mat, text_auto=True, title="Matriks Korelasi")
        st.plotly_chart(fig_heat, use_container_width=True)
        if len(cols_for_corr) > 1:
            corr_pre_post = corr_mat.loc["pre", "post"]
            corr_pre_change = corr_mat.loc["pre", "perubahan"]
            corr_post_change = corr_mat.loc["post", "perubahan"]

            st.info(
                f"""
                Hasil analisis korelasi menunjukkan bahwa:
                
                - Korelasi antara **nilai pre-test dan post-test** sebesar **{corr_pre_post:.2f}**, 
                mengindikasikan hubungan {'kuat' if abs(corr_pre_post) >= 0.6 else 'sedang' if abs(corr_pre_post) >= 0.3 else 'lemah'}
                antara kemampuan awal peserta dengan capaian akhir pelatihan.
                - Korelasi antara **nilai pre-test dan perubahan nilai** sebesar **{corr_pre_change:.2f}**, 
                menunjukkan bahwa peserta dengan nilai awal lebih 
                {'tinggi cenderung mengalami peningkatan lebih kecil' if corr_pre_change < 0 else 'rendah cenderung mengalami peningkatan lebih besar'}.
                - Korelasi antara **nilai post-test dan perubahan nilai** sebesar **{corr_post_change:.2f}**, 
                menandakan bahwa peningkatan nilai berkontribusi langsung terhadap capaian akhir peserta.
                """
            )

    else:
        st.info("Kolom numerik yang cukup untuk korelasi tidak tersedia.")

    
    st.markdown("### Distribusi Kategori Hasil Peserta")

    if "kategori" in df_view.columns:
        fig_kat = px.pie(
            df_view,
            names="kategori",
            title="Distribusi Kategori Hasil Peserta",
            color_discrete_sequence=["#ff6b6b","#37c9ef", "#f1c40f"]
        )

        fig_kat.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="white", width=2))
        )

        st.plotly_chart(fig_kat, use_container_width=True)
    else:
        st.info("Kolom kategori tidak tersedia.")



    st.markdown("### Jumlah Peserta per Kategori")

    df_cat_count = (
        df_view["kategori"]
        .value_counts()
        .reset_index()
    )

    df_cat_count.columns = ["Kategori", "Jumlah Peserta"]

    fig_cat_count = px.bar(
        df_cat_count,
        x="Jumlah Peserta",
        y="Kategori",
        orientation="h",                
        text="Jumlah Peserta",
        title="Jumlah Peserta per Kategori",
        color="Jumlah Peserta",          
        color_continuous_scale=["#37c9ef", "#ff6b6b"]
    )

    fig_cat_count.update_traces(
        textposition="outside",
        marker_line_color="white",
        marker_line_width=1
    )

    fig_cat_count.update_layout(
        xaxis_title="Jumlah Peserta",
        yaxis_title="Kategori",
        coloraxis_showscale=False,      
        yaxis=dict(categoryorder="total ascending") 
    )

    st.plotly_chart(fig_cat_count, use_container_width=True)

    st.markdown("### Rata-rata Kenaikan Nilai per Kategori")
    df_cat_mean = (
        df_view
        .groupby("kategori")["perubahan"]
        .mean()
        .reset_index()
        .sort_values("perubahan", ascending=True)
    )

    fig_cat_mean = px.bar(
        df_cat_mean,
        x="perubahan",
        y="kategori",
        orientation="h",                    
        text=df_cat_mean["perubahan"].round(2),
        title="Rata-rata Kenaikan Nilai per Kategori",
        color="perubahan",            
        color_continuous_scale=["#37c9ef","#37c9ef", "#ff6b6b"]
    )

    fig_cat_mean.update_traces(
        textposition="outside",
        marker_line_color="white",
        marker_line_width=1
    )

    fig_cat_mean.update_layout(
        xaxis_title="Rata-rata Kenaikan Nilai (poin)",
        yaxis_title="Kategori",
        coloraxis_showscale=False       
    )

    st.plotly_chart(fig_cat_mean, use_container_width=True)

    if avg_change > 0:
        st.info(
            f"""
    **Dampak Pelatihan Secara Keseluruhan**

    Secara umum, pelatihan menunjukkan dampak positif
    dengan rata-rata kenaikan nilai sebesar **{avg_change:.2f} poin**.
    Mayoritas peserta mengalami peningkatan hasil belajar
    setelah mengikuti pelatihan.
    """
        )
    else:
        st.warning(
            "⚠️ Tidak ditemukan peningkatan nilai yang signifikan "
            "pada hasil belajar peserta."
        )


elif st.session_state.page == "Kehadiran":
    st.markdown(
        "<h2 style='text-align:center; font-weight:700;'>📌 Analisis Kehadiran</h2>",
        unsafe_allow_html=True
    )

    st.success(
        "Analisis kehadiran hanya tersedia untuk "
        "Pelatihan Khusus Analis Kebijakan Angkatan IV–VI"
    )
    df_view = df_all.copy()
    df_kak = df_view[df_view["pelatihan"].isin(["KAK_IV", "KAK_V", "KAK_VI"])]

    if "persentase_kehadiran" not in df_kak.columns or df_kak.empty:
        st.warning(
            "Data kehadiran tidak tersedia untuk pelatihan KAK IV–VI."
        )
    else:
        st.markdown("### Statistik Deskriptif")
        col1, col2, col3 = st.columns(3)
        col1.metric("Rata-rata Kehadiran", f"{df_kak['persentase_kehadiran'].mean():.1f}%")
        col2.metric("Kehadiran Minimum", f"{df_kak['persentase_kehadiran'].min():.1f}%")
        col3.metric("Kehadiran Maksimum", f"{df_kak['persentase_kehadiran'].max():.1f}%")


        df_summary = (
            df_kak
            .groupby("pelatihan")
            .agg(
                Rata_Kehadiran=("persentase_kehadiran", "mean"),
                Std_Kehadiran=("persentase_kehadiran", "std"),
                Rata_Kenaikan=("perubahan", "mean"),
                Std_Kenaikan=("perubahan", "std"),
                Jumlah_Peserta=("perubahan", "count")
            )
            .reset_index()
        )
        st.markdown("### Statistik Kehadiran & Nilai per Angkatan")
        st.caption("Ringkasan performa peserta berdasarkan kehadiran dan kenaikan nilai pada setiap angkatan pelatihan.")

        for _, row in df_summary.iterrows():
            st.markdown(f"#### 🎓 {row['pelatihan']}")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Rata-rata Kehadiran", f"{row['Rata_Kehadiran']:.2f}%")
            c2.metric("Rata-rata Kenaikan Nilai", f"{row['Rata_Kenaikan']:.2f}")
            c3.metric("Jumlah Peserta", int(row["Jumlah_Peserta"]))
            st.markdown(
                f"""
                - **Stabilitas Kehadiran:** Std Dev = {row['Std_Kehadiran']:.2f}
                - **Variasi Kenaikan Nilai:** Std Dev = {row['Std_Kenaikan']:.2f}
                """
            )


        st.markdown("### Pola Kehadiran vs Kenaikan Nilai per Angkatan")
        
        fig_facet = px.scatter(
            df_kak,
            x="persentase_kehadiran",
            y="perubahan",
            facet_col="pelatihan",
            trendline="ols",
            color="pelatihan",
            color_discrete_map={
                "KAK_IV": "#37c9ef",  
                "KAK_V": "#2ecc71",   
                "KAK_VI": "#f39c12"   
            },
            title="Hubungan Kehadiran dan Kenaikan Nilai per Angkatan"
        )

        fig_facet.update_traces(
            marker=dict(size=7, opacity=0.8),
        )

        st.plotly_chart(fig_facet, use_container_width=True)

        st.info(
            "Grafik ini menunjukkan bahwa peserta dengan **kehadiran lebih tinggi** "
            "cenderung memiliki **kenaikan nilai yang lebih baik** di setiap angkatan. "
            "Meski demikian, variasi data menunjukkan bahwa peningkatan nilai tidak "
            "sepenuhnya ditentukan oleh kehadiran saja, melainkan juga faktor lain "
            "dalam proses pelatihan."
        )

        st.markdown("### Distribusi Persentase Kehadiran")
        data = df_kak["persentase_kehadiran"]
        counts, bins = np.histogram(data, bins=10)
        max_idx = np.argmax(counts)
        labels = [
            f"{bins[i]:.1f}–{bins[i+1]:.1f}"
            for i in range(len(bins)-1)
        ]
        colors = [
            "#ff6b6b" if i == max_idx else "#37c9ef"
            for i in range(len(counts))
        ]

        fig = go.Figure(go.Bar(
            x=counts,
            y=labels,
            orientation="h",
            marker_color=colors,
            marker_line_color="white",
            marker_line_width=1,
            text=counts,
            textposition="outside"
        ))

        fig.update_layout(
            title="Distribusi Persentase Kehadiran Peserta",
            xaxis_title="Jumlah Peserta",
            yaxis_title="Rentang Kehadiran",
            bargap=0.2
        )

        st.plotly_chart(fig, use_container_width=True)
        st.info(
        f"Mayoritas peserta berada pada rentang kehadiran "
        f"**{labels[max_idx]}%**, menunjukkan tingkat kehadiran "
        f"yang relatif konsisten selama pelatihan."
    )
     
        st.markdown("### Distribusi Kenaikan Nilai per Angkatan")
        fig_box = px.box(
            df_kak,
            x="pelatihan",
            y="perubahan",
            color="pelatihan",
            points="all",
            color_discrete_map={
                "KAK_IV": "#37c9ef",
                "KAK_V": "#2ecc71",
                "KAK_VI": "#f39c12"
            },
            title="Sebaran Kenaikan Nilai Antar Angkatan (KAK IV–VI)"
        )
        fig_box.update_traces(marker=dict(opacity=0.6))
        st.plotly_chart(fig_box, use_container_width=True)
        median_per_pel = df_kak.groupby("pelatihan")["perubahan"].median()
        max_pel = median_per_pel.idxmax()
        min_pel = median_per_pel.idxmin()

        st.info(
            f"""
        **Insight Sebaran Kenaikan Nilai per Angkatan**

        Boxplot menunjukkan perbedaan sebaran kenaikan nilai antar angkatan.
        Angkatan **{max_pel}** memiliki **median kenaikan nilai tertinggi**,
        sementara **{min_pel}** menunjukkan median terendah.
        Lebar sebaran nilai mengindikasikan tingkat konsistensi hasil belajar
        di masing-masing angkatan.
        """
        )


        st.markdown("### Hubungan Kehadiran dan Kenaikan Nilai")
        fig_scatter = px.scatter(
            df_kak,
            x="persentase_kehadiran",
            y="perubahan",
            color="pelatihan",
            trendline="ols",
            color_discrete_map={
                "KAK_IV": "#37c9ef",
                "KAK_V": "#2ecc71",
                "KAK_VI": "#f39c12"
            },
            title="Kehadiran vs Kenaikan Nilai"
        )

        fig_scatter.update_traces(marker=dict(size=8, opacity=0.75))

        st.plotly_chart(fig_scatter, use_container_width=True)
        st.info(
    """
        **Insight Hubungan Kehadiran dan Kenaikan Nilai**

        Grafik menunjukkan bahwa peserta yang lebih sering hadir
        cenderung mengalami kenaikan nilai yang lebih baik.
        Namun, tidak selalu konsisten pada semua peserta,
        dan kehadiran bukan satu-satunya faktor yang memengaruhi peningkatan nilai.
        """
        )
        df_kak["kategori_kehadiran"] = pd.cut(
            df_kak["persentase_kehadiran"],
            bins=[0, 70, 85, 100],
            labels=["Rendah", "Sedang", "Tinggi"]
        )
        st.markdown("### Sebaran Perubahan Nilai per Kategori Kehadiran")
        fig_box = px.box(
            df_kak,
            x="kategori_kehadiran",
            y="perubahan",
            color="kategori_kehadiran",
            color_discrete_map={
                "Rendah": "#37c9ef",
                "Sedang": "#37c9ef",
                "Tinggi": "#ff6b6b"
            },
            title="Sebaran Perubahan Nilai Berdasarkan Kategori Kehadiran"
        )
        st.plotly_chart(fig_box, use_container_width=True)

        st.markdown("### Perbandingan Rata-rata Kenaikan Nilai KAK IV–VI")
        df_kak_mean = (
            df_kak.groupby("pelatihan")["perubahan"]
            .mean()
            .reset_index()
        )
        fig_kak = px.bar(
            df_kak_mean,
            x="pelatihan",
            y="perubahan",
            text_auto=".2f",
            color="pelatihan",
            color_discrete_map={
                "KAK_IV": "#37c9ef",
                "KAK_V": "#2ecc71",
                "KAK_VI": "#f39c12"
            },
            title="Perbandingan Rata-rata Kenaikan Nilai KAK IV–VI"
        )
        fig_kak.update_traces(
            textposition="outside",
            marker_line_color="white",
            marker_line_width=1
        )
        st.plotly_chart(fig_kak, use_container_width=True)


    st.markdown("### Heatmap Korelasi Kehadiran & Nilai")
    cols_corr = [
        c for c in ["persentase_kehadiran", "pre", "post", "perubahan"]
        if c in df_kak.columns
    ]
    if len(cols_corr) >= 2:
        corr_mat = df_kak[cols_corr].corr()
        fig_heat = px.imshow(
            corr_mat,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale="RdBu",
            zmin=-1,
            zmax=1,
            title="Matriks Korelasi Kehadiran dan Nilai (KAK IV–VI)"
        )

        fig_heat.update_layout(
            xaxis_title="Variabel",
            yaxis_title="Variabel"
        )
        st.plotly_chart(fig_heat, use_container_width=True)

        corr = df_kak["persentase_kehadiran"].corr(df_kak["perubahan"])

        st.info(
            f"Terdapat korelasi sebesar **{corr:.2f}** antara persentase "
            f"kehadiran dan kenaikan nilai peserta. "
            f"Hal ini menunjukkan bahwa tingkat kehadiran berperan "
            f"dalam peningkatan hasil pelatihan."
        )
    else:
        st.info("Kolom numerik tidak cukup untuk membentuk heatmap korelasi.")


    st.markdown("### Regresi Linier per Angkatan")
    st.caption(
        "Analisis ini menunjukkan seberapa besar pengaruh persentase kehadiran "
        "terhadap kenaikan nilai pada masing-masing angkatan."
    )
    for angkatan in sorted(df_kak["pelatihan"].unique()):
        df_sub = df_kak[df_kak["pelatihan"] == angkatan]

        X = sm.add_constant(df_sub["persentase_kehadiran"])
        y = df_sub["perubahan"]
        model = sm.OLS(y, X).fit()
        coef = model.params[1]
        r2 = model.rsquared
        arah = "positif" if coef > 0 else "negatif"

        with st.container():
            st.markdown(f"#### 🎓 {angkatan}")

            col1, col2 = st.columns(2)
            col1.metric(
                "Koefisien Kehadiran",
                f"{coef:.2f}",
                help="Perkiraan perubahan nilai untuk setiap kenaikan 1% kehadiran"
            )
            col2.metric(
                "R² (Daya Jelaskan)",
                f"{r2:.3f}",
                help="Proporsi variasi kenaikan nilai yang dapat dijelaskan oleh variabel kehadiran"

            )

            st.info(
                f"Model regresi menunjukkan hubungan **{arah}** antara kehadiran "
                f"dan kenaikan nilai pada **{angkatan}**. "
                f"Namun, nilai R² yang relatif kecil mengindikasikan bahwa "
                f"faktor lain di luar kehadiran turut memengaruhi hasil pelatihan."
            )

    X = sm.add_constant(df_kak["persentase_kehadiran"])
    y = df_kak["perubahan"]
    model = sm.OLS(y, X).fit()

    intercept = model.params[0]
    coef = model.params[1]
    r2 = model.rsquared

    st.markdown("### Regresi Linier Keseluruhan Angkatan")
    st.caption(
        "Analisis ini menggambarkan pengaruh persentase kehadiran terhadap kenaikan nilai "
        "peserta berdasarkan data gabungan seluruh angkatan."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Intercept", f"{intercept:.2f}")
    col2.metric(
        "Koefisien Kehadiran",
        f"{coef:.2f}",
        help="Perubahan nilai untuk setiap kenaikan 1% kehadiran"
    )
    col3.metric(
        "R² (Daya Jelaskan)",
        f"{r2:.3f}",
        help="Proporsi variasi kenaikan nilai yang dapat dijelaskan oleh variabel kehadiran"
    )

    st.markdown(
        f"**Persamaan Regresi:**  \n"
        f"Perubahan Nilai = **{intercept:.2f} + {coef:.2f} × Kehadiran (%)**"
    )

    arah = "positif" if coef > 0 else "negatif"
    st.info(
        f"Hasil regresi linier menunjukkan hubungan **{arah}** antara "
        f"persentase kehadiran dan kenaikan nilai peserta. "
        f"Setiap peningkatan **1% kehadiran** diperkirakan "
        f"berkaitan dengan perubahan nilai sebesar **{coef:.2f} poin**. "
        f"Namun, nilai **R² = {r2:.3f}** menunjukkan bahwa kehadiran "
        f"hanya menjelaskan sebagian kecil variasi kenaikan nilai. "
        f"Hal ini mengindikasikan bahwa faktor lain seperti kualitas materi, "
        f"metode penyampaian, dan keterlibatan peserta kemungkinan "
        f"memiliki pengaruh yang lebih dominan terhadap hasil pelatihan."
    )
    iv = df_kak[df_kak["pelatihan"]=="KAK_IV"]["perubahan"]
    v  = df_kak[df_kak["pelatihan"]=="KAK_V"]["perubahan"]
    vi = df_kak[df_kak["pelatihan"]=="KAK_VI"]["perubahan"]
    f_stat, p_val = f_oneway(iv, v, vi)
    iv = df_kak[df_kak["pelatihan"] == "KAK_IV"]["perubahan"]
    v  = df_kak[df_kak["pelatihan"] == "KAK_V"]["perubahan"]
    vi = df_kak[df_kak["pelatihan"] == "KAK_VI"]["perubahan"]
    f_stat, p_val = f_oneway(iv, v, vi)

    st.markdown("### Uji Perbedaan Kenaikan Nilai Antar Angkatan (ANOVA)")
    mean_iv = iv.mean()
    mean_v  = v.mean()
    mean_vi = vi.mean()
    st.write("**Rata-rata Kenaikan Nilai per Angkatan:**")
    st.write(f"- KAK IV  : {mean_iv:.2f}")
    st.write(f"- KAK V   : {mean_v:.2f}")
    st.write(f"- KAK VI  : {mean_vi:.2f}")
    st.write(f"**F-statistic** = {f_stat:.3f}")
    st.write(f"**p-value** = {p_val:.4f}")
    if p_val < 0.05:
        angkatan_tertinggi = max(
            {"KAK IV": mean_iv, "KAK V": mean_v, "KAK VI": mean_vi},
            key=lambda x: {"KAK IV": mean_iv, "KAK V": mean_v, "KAK VI": mean_vi}[x]
        )
        st.info(
        f"""
     **Hasil Uji Perbedaan Kenaikan Nilai Antar Angkatan**

    Hasil uji ANOVA menunjukkan **perbedaan kenaikan nilai yang signifikan** 
    antara KAK IV, KAK V, dan KAK VI (p-value < 0.05).

    Berdasarkan rata-rata kenaikan nilai, **{angkatan_tertinggi}** mencatat
    peningkatan tertinggi, sehingga pelaksanaan pelatihan
    pada angkatan tersebut relatif lebih efektif dibandingkan angkatan lainnya.
    """
)
    else:
        st.info(
            "Hasil uji ANOVA menunjukkan **tidak terdapat perbedaan kenaikan nilai yang signifikan** "
            "antar angkatan. Hal ini mengindikasikan bahwa efektivitas pelatihan "
            "relatif konsisten di setiap angkatan."
        )

    st.session_state["df_view"] = df_view
    st.session_state["df_kak"] = df_kak

elif st.session_state.page == "Evaluasi":
    st.markdown(
        "<h2 style='text-align:center; font-weight:700;'>⭐ Evaluasi Pelatihan</h2>",
        unsafe_allow_html=True
    )
    try:
        df = pd.read_csv(
            r"D:\JES\JESIKA\.vscode\.vscode SEMESTER 5\PROJECT\DATASET MINI PROJECT\MONEV_CLEAN\FIXX_MONEV.csv"
        )
        data = pd.read_csv(
            r"D:\JES\JESIKA\.vscode\.vscode SEMESTER 5\PROJECT\DATASET MINI PROJECT\MONEV_CLEAN\MONEV_FIX.csv"
        )
    except:
        st.error("Gagal memuat data evaluasi. Periksa path file CSV.")
        st.stop()
    st.subheader("Ringkasan Evaluasi Peserta")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Responden", df.shape[0])
    col2.metric(
        "Total Kata Unik",
        df["CLEAN_TEXT"].str.split().explode().nunique()
    )

    st.subheader("🌥️ Tema Umum Umpan Balik Peserta")
    wordcloud_path = (
        r"D:\JES\JESIKA\.vscode\.vscode SEMESTER 5\PROJECT\DATASET MINI PROJECT"
        r"\MONEV_CLEAN\wordcloudD.png"
    )
    try:
        st.image(
            wordcloud_path,
            caption="Visualisasi kata yang paling sering muncul dalam evaluasi peserta",
            use_container_width=True
        )
    except:
        st.warning("File WordCloud tidak ditemukan.")


    st.subheader("Distribusi Sentimen Evaluasi Peserta")
    df = pd.read_csv(
            r"D:\JES\JESIKA\.vscode\.vscode SEMESTER 5\PROJECT\DATASET MINI PROJECT\MONEV_CLEAN\dataset_monev.csv"
        )
    if "sentimen" in df.columns:
        df["sentimen"] = df["sentimen"].astype(str).str.capitalize()
        sent_count = df["sentimen"].value_counts().reset_index()
        sent_count.columns = ["Sentimen", "Jumlah"]
        total = sent_count["Jumlah"].sum()
        pos = sent_count[sent_count["Sentimen"]=="Positif"]["Jumlah"].values[0]
        neg = sent_count[sent_count["Sentimen"]=="Negatif"]["Jumlah"].values[0]
        neu = sent_count[sent_count["Sentimen"]=="Netral"]["Jumlah"].values[0]

        c1, c2, c3 = st.columns(3)
        c1.metric("😊 Positif", f"{round(pos/total*100,1)}%")
        c2.metric("😐 Netral", f"{round(neu/total*100,1)}%")
        c3.metric("⚠️ Negatif", f"{round(neg/total*100,1)}%")
        sentiment_colors = {
            "Positif": "#2ecc71",   
            "Netral":  "#37c9ef",   
            "Negatif": "#ff6b6b"  
        }
        fig_pie = px.pie(
            sent_count,
            names="Sentimen",
            values="Jumlah",
            title="Proporsi Sentimen Evaluasi Peserta",
            hole=0.4,
            color="Sentimen",
            color_discrete_map=sentiment_colors
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        fig_bar = px.bar(
            sent_count,
            x="Sentimen",
            y="Jumlah",
            text="Jumlah",
            title="Jumlah Responden per Sentimen",
            color="Sentimen",
            color_discrete_map=sentiment_colors
        )

        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True)

        sent_dominan = sent_count.iloc[0]["Sentimen"]
        persentase = round(
            (sent_count.iloc[0]["Jumlah"] / sent_count["Jumlah"].sum()) * 100, 1
        )
        st.info(
            f"Sentimen **{sent_dominan}** mendominasi evaluasi peserta ({persentase}%). "
            "Namun, hasil penelusuran isi umpan balik menunjukkan bahwa sentimen positif "
            "tidak hanya berisi apresiasi, tetapi juga mengandung masukan kritis yang "
            "bersifat konstruktif. Hal ini mencerminkan keterlibatan aktif peserta dalam "
            "memberikan evaluasi demi peningkatan kualitas pelatihan."
        )

    else:
        st.warning(
            "Kolom **sentimen** tidak ditemukan pada file CSV. "
            "Pastikan label sentimen sudah tersedia."
        )

    st.subheader("Umpan Balik dari Peserta")
    df_view = df.copy()
    df_view = df_view.reset_index(drop=True)
    df_view.insert(0, "No", range(1, len(df_view) + 1))
    df_view = df_view.rename(columns={"CLEAN_NLP": "Evaluasi Peserta"})
    df_view = df_view.rename(columns={"sentimen": "Sentimen"})

    opsi_sentimen = ["Semua"] + sorted(df_view["Sentimen"].unique().tolist())

    filter_sentimen = st.multiselect(
        "Pilih Sentimen",
        options=opsi_sentimen,
        default=["Semua"]
    )

    if "Semua" in filter_sentimen:
        df_filtered = df_view.copy()
    else:
        df_filtered = df_view[df_view["Sentimen"].isin(filter_sentimen)]

    st.dataframe(
        df_filtered[["No", "Evaluasi Peserta", "Sentimen"]],
        hide_index=True,
        use_container_width=True
    )

    st.markdown("""
        <style>
        /* SEMUA TAG */
        span[data-baseweb="tag"] {
            font-weight: 600;
            border-radius: 8px;
            padding: 4px 10px;
            
        }
        """, unsafe_allow_html=True)
    st.session_state["df_view"] = df_view

    if "CLEAN_TEXT" in df.columns:

        text_data = df["CLEAN_TEXT"].dropna().astype(str)

        vectorizer_uni = CountVectorizer(
            stop_words="english",
            max_features=15
        )
        X_uni = vectorizer_uni.fit_transform(text_data)
        unigram_df = pd.DataFrame({
            "Kata Kunci": vectorizer_uni.get_feature_names_out(),
            "Frekuensi": X_uni.toarray().sum(axis=0),
        }).sort_values("Frekuensi", ascending=False)

        unigram_df.index = range(1, len(unigram_df) + 1)

        vectorizer_bi = CountVectorizer(
            stop_words="english",
            ngram_range=(2, 2),
            max_features=10
        )
        X_bi = vectorizer_bi.fit_transform(text_data)

        bigram_df = pd.DataFrame({
            "Frasa Kunci": vectorizer_bi.get_feature_names_out(),
            "Frekuensi": X_bi.toarray().sum(axis=0)
        }).sort_values("Frekuensi", ascending=False)

        bigram_df.index = range(1, len(bigram_df) + 1)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🔑 Kata Kunci Paling Sering Muncul**")
            st.dataframe(unigram_df, use_container_width=True)

        with col2:
            st.markdown("**🧩 Frasa Saran yang Paling Dominan**")
            st.dataframe(bigram_df, use_container_width=True)

    else:
        st.warning("Kolom tidak tersedia untuk analisis teks.")

    tema_keywords = {
        "Materi Pelatihan": ["materi", "konten", "modul", "bahan"],
        "Metode Pembelajaran": ["metode", "diskusi", "praktik", "interaktif"],
        "Fasilitator": ["pemateri", "narasumber", "instruktur", "fasilitator", "pengajar"],
        "Durasi & Jadwal": ["waktu", "durasi", "jadwal", "terlalu lama", "jam", "lama"],
        "Fasilitas & Teknis": ["zoom", "sarana", "audio", "video", "jaringan", "teknis", "lcd", "wifi", "air", "ac", "kamar", "ruang", "remot", "tv", "kelas"],
    }

    def deteksi_tema(teks):
        if pd.isna(teks):
            return ["Lainnya"]

        teks = str(teks).lower()
        tema_terdeteksi = []

        for tema, keywords in tema_keywords.items():
            if any(k in teks for k in keywords):
                tema_terdeteksi.append(tema)

        return tema_terdeteksi if tema_terdeteksi else ["Lainnya"]
    

    df["Tema"] = df["CLEAN_NLP"].apply(deteksi_tema)
    df_tema = df.explode("Tema")
    
    tema_count = (
        df_tema["Tema"]
        .value_counts()
        .reset_index(name="Jumlah")
        .rename(columns={"index": "Tema"})
    )

    df_lainnya = tema_count[tema_count["Tema"] == "Lainnya"]
    df_utama = tema_count[tema_count["Tema"] != "Lainnya"]

    tema_count_final = pd.concat([df_utama, df_lainnya], ignore_index=True)

    tema_count_final.index = range(1, len(tema_count_final) + 1)

    st.subheader("Analisis Tema Dominan Umpan Balik Peserta")
    st.dataframe(tema_count_final, use_container_width=True)
    total_tema = tema_count_final["Jumlah"].sum()

    tema_teratas = tema_count_final.iloc[0]
    tema_terbawah = tema_count_final.iloc[-1]

    persentase_teratas = round((tema_teratas["Jumlah"] / total_tema) * 100, 1)

    tema_dominan = tema_count_final.loc[
        tema_count_final["Tema"] != "Lainnya"
    ].iloc[0]["Tema"]
    komentar_tema = df_tema[
        (df_tema["Tema"] == tema_dominan) &
        (df_tema["CLEAN_NLP"].notna())
    ]["CLEAN_NLP"].unique()

    tema_opsi = tema_count_final["Tema"].tolist()

    tema_pilihan = st.selectbox(
        "Pilih tema untuk melihat komentar peserta:",
        tema_opsi
    )

    komentar_pilihan = df_tema[
        (df_tema["Tema"] == tema_pilihan) &
        (df_tema["CLEAN_NLP"].notna())
    ]["CLEAN_TEXT"].unique()

    with st.expander(f"💬 Komentar Peserta – {tema_pilihan}"):
        for i, komentar in enumerate(komentar_pilihan, start=1):
            st.markdown(f"**{i}.** {komentar}")
        
    st.info(
        f"""
    **Insight Utama Analisis Umpan Balik Peserta**

    • Tema yang paling sering muncul adalah **{tema_teratas['Tema']}**
    dengan **{tema_teratas['Jumlah']} tanggapan** (**{persentase_teratas}%** dari total umpan balik).
    
    Hal ini menunjukkan bahwa perhatian peserta paling banyak tertuju pada aspek **{tema_teratas['Tema'].lower()}**, 
    sehingga aspek tersebut menjadi **prioritas utama untuk evaluasi dan peningkatan kualitas pelatihan**.
    """
    )

elif st.session_state.page == "Tentang":
    st.markdown(
        "<h2 style='text-align:center; font-weight:700;'>ℹ️ Tentang Sistem</h2>",
        unsafe_allow_html=True
    )
    st.markdown("""
    Sistem Monitoring dan Evaluasi Pelatihan ini dikembangkan untuk mendukung proses 
    pemantauan, analisis, dan evaluasi pelaksanaan pelatihan, dirancang untuk menyajikan
    informasi pelatihan secara ringkas, visual, dan mudah dipahami.

    ### Tujuan Pengembangan
    Bertujuan untuk mendukung proses pengambilan keputusan berbasis data
    melalui analisis kehadiran peserta, perbandingan nilai pre-test dan post-test,
    serta evaluasi dan umpan balik peserta pelatihan.

    ### Ruang Lingkup Data
    Data yang digunakan dalam sistem ini meliputi:
    - Data kehadiran peserta pelatihan
    - Data nilai pre-test dan post-test
    - Data evaluasi dari peserta

    ### Metodologi Analisis
    Analisis dilakukan menggunakan statistik deskriptif dan inferensial,
    serta analisis teks untuk mengidentifikasi sentimen dan tema dominan
    dari evaluasi peserta pelatihan.

    ### 👤 Informasi Pengembang
    **Nama**: Jesika Trisyanda  
    **Program Studi**: S1 Sains Data  
    **Institusi**: Universitas Negeri Surabaya  
    **Konteks Pengembangan**: Mini Proyek Magang 
    **Tahun**: 2025
                
    """)
    st.info(
        "Sistem ini dikembangkan sebagai bagian dari kegiatan magang dan digunakan "
        "untuk kepentingan internal monitoring dan evaluasi pelatihan."
    )

