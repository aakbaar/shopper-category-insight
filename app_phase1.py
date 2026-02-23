import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

pd.set_option("styler.render.max_elements", 1000000) 
st.set_page_config(layout="wide", page_title="SHOPPER INSIGHT", page_icon="📊")

# --- CUSTOM CSS (SIDEBAR, TABS, & AFFINITY DARK MODE) ---
# --- CUSTOM CSS (SIDEBAR, TABS, & AFFINITY DARK MODE) ---
st.markdown("""
    <style>
    /* 1. SIDEBAR BASE */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
        box-shadow: 10px 0px 70px rgba(0,0,0,0.08) !important;
    }

    /* Judul Sidebar Custom */
    .sidebar-title-custom {
        /* SILAKAN UBAH ANGKA DI BAWAH INI UNTUK BESAR/KECIL FONT */
        font-size: 37px !important; 
        
        font-weight: 800;
        color: #1E293B;
        line-height: 1.1;
        padding: 0px;
        
        /* SILAKAN UBAH ANGKA DI BAWAH INI UNTUK JARAK KE MENU */
        margin-bottom: 50px !important; 
    }

    /* Footer agar menempel di lantai sidebar */
    .sidebar-footer-fixed {
        position: fixed;
        bottom: 10px;
        width: 100%;
        color: #94A3B8 !important;
        font-size: 20px;
        background-color: transparent;
    }

    /* 4. TOMBOL NAVIGASI 3D */
    div[data-testid="stSidebar"] .stRadio label {
        background-color: #F8FAFC !important;
        border-radius: 14px !important;
        padding: 12px 20px !important;
        border: 1px solid #EDF2F7 !important;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }

    /* Efek Aktif Merah */
    div[data-testid="stSidebar"] .stRadio div[data-checked="true"] label {
        background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%) !important;
        color: white !important;
        box-shadow: 0 10px 15px rgba(255, 0, 0, 0.2) !important;
    }

    /* Sembunyikan bullet point radio */
    div[data-testid="stSidebar"] .stRadio [data-testid="stWidgetLabel"] {
        display: none;
    }
    /* 4. FILTER STYLING (DIUBAH AGAR SERAGAM DENGAN TAB) */
    
    /* Wadah utama Selectbox & Multiselect */
    div[data-baseweb="select"] > div {
        background-color: #F0F2F6 !important; 
        border-radius: 12px !important;
        border: 1px solid #DFE1E5 !important;
        padding: 2px 5px !important;
        transition: all 0.2s ease;
    }

    /* Saat Filter di-klik (Focus) */
    div[data-baseweb="select"]:focus-within > div {
        border-color: #FF0000 !important; /* Warna border merah saat aktif */
        box-shadow: 0 0 0 1px #FF0000 !important;
        background-color: #FFFFFF !important;
    }

    /* Styling Tag/Pilihan di Multiselect (Dibuat seperti Tab Aktif) */
    span[data-baseweb="tag"] {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1px solid #DDD !important;
        color: #333 !important;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05) !important;
        font-weight: 500 !important;
    }

    /* Tombol X (Hapus) pada Tag */
    span[data-baseweb="tag"] div[role="button"] {
        color: #FF0000 !important;
    }

    /* Menghilangkan garis bawah default pada input filter */
    div[data-baseweb="select"] input {
        color: #000000 !important;
    }
    /* 5. TAB STYLING (MODERN SEGMENTED DENGAN SEKAT) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #F0F2F6 !important; 
        border-radius: 12px;
        padding: 6px;
        gap: 0px; /* Gap dinolkan agar sekat terlihat menyambung */
        border: 1px solid #DFE1E5;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
    }

    .stTabs [data-baseweb="tab"] {
        height: 35px;
        background-color: transparent !important;
        border-radius: 0px !important; /* Kotak agar sekat konsisten */
        border: none !important;
        border-right: 1px solid #D1D5DB !important; /* INI SEKATNYA */
        color: #4B5563 !important;
        font-weight: 500;
        padding: 0px 20px !important;
        transition: all 0.2s;
    }

    /* Hilangkan sekat pada tab terakhir */
    .stTabs [data-baseweb="tab"]:last-child {
        border-right: none !important;
    }

    /* Styling Tab yang Aktif (Putih & Timbul) */
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important; 
        color: #FF0000 !important; 
        border-radius: 8px !important; /* Tab aktif dibuat melengkung sendiri */
        border-right: none !important; /* Hilangkan sekat saat tab aktif */
        box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
        transform: scale(1.02);
    }

    /* Hilangkan sekat untuk tab tepat sebelum tab yang aktif agar tidak double */
    .stTabs [data-baseweb="tab"]:has(+ [aria-selected="true"]) {
        border-right: none !important;
    }

    /* Menghilangkan garis bawah default Streamlit */
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. DATA LOADERS ---
@st.cache_data
def load_perf_file(level, versi):
    filename = f"perf_{level}_{versi.lower()}.csv"
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return pd.DataFrame()

@st.cache_data
def load_segment_unified():
    if os.path.exists("perf_segmentation_unified.csv"):
        return pd.read_csv("perf_segmentation_unified.csv")
    return pd.DataFrame()

@st.cache_data
def load_loyalty_data():
    try:
        return {
            "br_loy_cat": pd.read_csv("brand_loyalty_category.csv"),
            "br_loy_sub": pd.read_csv("brand_loyalty_subcategory.csv"),
            "br_swi_cat": pd.read_csv("BRAND_SWITCH_CATEGORY.csv"),
            "br_swi_sub": pd.read_csv("BRAND_SWITCH_SUBCATEGORY.csv"),
            "cat_loy": pd.read_csv("CATEGORY_LOYALTY.csv"),
            "sub_loy": pd.read_csv("SUBCATEGORY_LOYALTY.csv")
        }
    except Exception as e:
        st.error(f"Gagal load data switching: {e}")
        return None

@st.cache_data
def load_affinity_data():
    try:
        # MENGGUNAKAN NAMA FILE BARU (_PHASE1)
        return {
            "cat": pd.read_csv("AFFINITY_CAT_PHASE1.csv"),
            "subcat": pd.read_csv("AFFINITY_SUBCAT_PHASE1.csv"),
            "brand_cat": pd.read_csv("AFFINITY_BRAND_CAT_PHASE1.csv"),
            "brand_sub": pd.read_csv("AFFINITY_BRAND_SUBCAT_PHASE1.csv")
        }
    except Exception as e:
        st.error(f"Gagal load affinity data: {e}")
        return None


# --- 2. DISPLAY HELPERS ---
import matplotlib.colors as mcolors

def render_performance_cards(df, is_category=False):
    """Versi Uniform & Clean: Ukuran diperbesar, teks div bocor dihapus"""
    if df.empty:
        return

    # Hitung rata-rata metrik
    metrics = {
        "freq_val": df["PURCHASE_FREQUENCY_AFTER"].mean() if "PURCHASE_FREQUENCY_AFTER" in df.columns else 0,
        "freq_gr": df["PURCHASE_FREQUENCY_GROWTH"].mean() if "PURCHASE_FREQUENCY_GROWTH" in df.columns else 0,
        "spb_val": df["SPB_AFTER"].mean() if "SPB_AFTER" in df.columns else 0,
        "spb_gr": df["SPB_GROWTH"].mean() if "SPB_GROWTH" in df.columns else 0,
        "spt_val": df["SPT_AFTER"].mean() if "SPT_AFTER" in df.columns else 0,
        "spt_gr": df["SPT_GROWTH"].mean() if "SPT_GROWTH" in df.columns else 0,
    }
    
    if is_category:
        metrics["pen_val"] = df["PENETRATION_AFTER"].mean() if "PENETRATION_AFTER" in df.columns else 0
        metrics["pen_gr"] = df["PENETRATION_GROWTH"].mean() if "PENETRATION_GROWTH" in df.columns else 0

    # Indikator Growth (Bubble)
    def get_delta_html(val):
        color = "#E8F5E9" if val > 0 else "#FFEBEE"
        t_color = "#2E7D32" if val > 0 else "#C62828"
        icon = "↑" if val > 0 else "↓"
        return f"""<div style="display:inline-block; background-color:{color}; color:{t_color}; 
                    padding:2px 10px; border-radius:12px; font-size:12px; font-weight:bold; margin-top:4px;">
                    {icon} {val:+.2%}</div>"""

    # Buat Kolom
    cols = st.columns(4 if is_category else 3)
    
    # Style Kotak (Uniform height & padding)
    card_container_style = """
        background-color: #F8F9FA; 
        border-radius: 8px; 
        padding: 15px; 
        min-height: 120px; 
        border: 1px solid #EEE;
        display: flex;
        flex-direction: column;
        justify-content: center;
    """

    # 1. Category Penetration
    if is_category:
        with cols[0]:
            st.markdown(f"""
                <div style="{card_container_style}">
                    <p style="color:#666; font-size:14px; margin:0; font-weight:500;">Category Penetration</p>
                    <div style="font-size:32px; font-weight:bold; color:#000; line-height:1.1;">{metrics['pen_val']:.2%}</div>
                    {get_delta_html(metrics['pen_gr'])}
                </div>
            """, unsafe_allow_html=True)

    # 2. Metrik Lainnya (Dinamis)
    idx_start = 1 if is_category else 0
    m_list = [
        ("Purchase Frequency", metrics['freq_val'], metrics['freq_gr'], "{:.2f}"),
        ("Spend Per Buyer", metrics['spb_val'], metrics['spb_gr'], "Rp {:,.0f}"),
        ("Spend Per Trip", metrics['spt_val'], metrics['spt_gr'], "Rp {:,.0f}")
    ]

    for i, (label, val, gr, fmt) in enumerate(m_list):
        with cols[idx_start + i]:
            st.markdown(f"""
                <div style="{card_container_style}">
                    <p style="color:#666; font-size:14px; margin:0; font-weight:500;">{label}</p>
                    <div style="font-size:32px; font-weight:bold; color:#000; line-height:1.1;">{fmt.format(val)}</div>
                    {get_delta_html(gr)}
                </div>
            """, unsafe_allow_html=True)

# ===============================================================
# GLOBAL HELPERS (Sesuai Kolom Baru)
# ===============================================================

def display_styled_table(df):
    if df.empty:
        st.warning("DATA TIDAK TERSEDIA")
        return

    # Bersihkan kolom yang tidak perlu agar tampilan rapi
    cols_to_drop = [c for c in df.columns if any(x in c for x in ["PROMO_PCT", "BUYER_COUNT"])]
    df = df.drop(columns=cols_to_drop, errors='ignore')
    
    # Identifikasi semua kolom Growth
    growth_cols = [c for c in df.columns if "GROWTH" in c]

    # --- FIX DATA TYPE & NULLS ---
    for col in growth_cols:
        # Paksa konversi ke numeric, yang error (string kosong/teks) jadi NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # --- LOGIKA PEWARNAAN MANUAL ---
    def apply_growth_color(val):
        if pd.isna(val) or val == 0:
            return 'background-color: white; color: black;'
        if val > 0:
            return 'background-color: #d4edda; color: #155724;'
        if val < 0:
            return 'background-color: #f8d7da; color: #721c24;'
        return 'background-color: white; color: black;'

    # --- FORMATTING TAMPILAN ---
    format_dict = {}
    for col in df.columns:
        if "GROWTH" in col or "PENETRATION" in col:
            format_dict[col] = "{:.2%}"
        elif any(x in col for x in ["SPT", "SPB"]):
            format_dict[col] = "Rp {:,.0f}"
        # Pastikan AVG dan PURCHASE_FREQUENCY selalu 2 desimal di belakang koma
        elif "AVG" in col or "PURCHASE_FREQUENCY" in col:
            format_dict[col] = "{:,.2f}"

    # Terapkan styling
    styled_df = df.style.format(format_dict, na_rep="-")
    
    if growth_cols:
        styled_df = styled_df.map(apply_growth_color, subset=growth_cols)

    # Tampilkan di Streamlit
    st.dataframe(
        styled_df,
        use_container_width=True, 
        hide_index=True
    )
    
    # Menambahkan Keterangan Label secara otomatis di bawah semua tabel Performance
    st.caption("ℹ️ Keterangan Tabel = **SPT** (Spend Per Trip) | **SPB** (Spend Per Buyer)")
   
# ===============================================================
# 1. FUNGSI HELPER GLOBAL (WAJIB DI ATAS AGAR TIDAK ERROR)
# ===============================================================

def apply_global_perf(df, sel_sec):
    """Fungsi filter section yang dipanggil di semua tab"""
    if df.empty: return df
    # Cek kolom SECTION (case sensitive)
    s_col = next((c for c in ["SECTION", "section"] if c in df.columns), None)
    if sel_sec and sel_sec != "ALL" and s_col:
        df = df[df[s_col] == sel_sec]
    return df.reset_index(drop=True)

def reorder_final(df, level):
    """Mengatur urutan kolom: Identity -> Metrics Utama -> Sisanya"""
    if df.empty: return df
    cols = df.columns.tolist()
    
    # 1. Tentukan Kolom Identitas Berdasarkan Level
    if level == "category": 
        # Cek jika ini dari tab segmentasi (punya SEGMENT_VALUE)
        if "SEGMENT_VALUE" in cols:
            id_cols = ["SEGMENT_VALUE", "CATEGORY", "SECTION"]
        else:
            id_cols = ["CATEGORY", "SECTION"] 
    elif level == "subcategory": 
        id_cols = ["SUBCATEGORY", "CATEGORY", "SECTION"]
    elif level == "brand": 
        id_cols = ["BRAND", "SUBCATEGORY", "CATEGORY", "SECTION"]
    elif level == "plu":
        id_cols = ["PLU", "DESCP", "CATEGORY", "SECTION"]
    else: 
        id_cols = ["CATEGORY", "SECTION"]

    # 2. Susun Urutan Metrik Secara Baku (Strict Order)
    metric_order = [
        "AVG_QTY_STRUK_MONTH_BEFORE", "AVG_QTY_STRUK_MONTH_AFTER", "AVG_QTY_STRUK_MONTH_GROWTH",
        "AVG_STRUK_MONTH_BEFORE", "AVG_STRUK_MONTH_AFTER", "AVG_STRUK_MONTH_GROWTH",
        "PURCHASE_FREQUENCY_BEFORE", "PURCHASE_FREQUENCY_AFTER", "PURCHASE_FREQUENCY_GROWTH",
        "SPT_BEFORE", "SPT_AFTER", "SPT_GROWTH",
        "SPB_BEFORE", "SPB_AFTER", "SPB_GROWTH"
    ]
    
    # Tambahkan Penetration HANYA untuk level category
    if level == "category":
        metric_order += [
            "PENETRATION_BEFORE", "PENETRATION_AFTER", "PENETRATION_GROWTH"
        ]
    
    # 3. Filter kolom yang benar-benar ada di dalam dataset agar tidak error
    existing_ids = [c for c in id_cols if c in cols]
    existing_metrics = [c for c in metric_order if c in cols]
    others = [c for c in cols if c not in existing_ids and c not in existing_metrics]
    
    # Gabungkan semua dengan urutan yang sudah dipatenkan
    return df[existing_ids + existing_metrics + others]

def render_affinity_tab(df, col_a, col_b, filter_cols, key_prefix, show_qty_impact=True, extra_display_cols=[]):
    """
    Fungsi render yang fleksibel untuk menampilkan Matrix Affinity 
    dan Tabel QTY Impact dengan kolom tambahan.
    """
    global df_p 

    if df.empty:
        st.warning("PILIH KEMBALI SECTION")
        return

    df = df.copy()
    df.columns = [c.lower() for c in df.columns]
    col_a, col_b = col_a.lower(), col_b.lower()
    filter_cols = [f.lower() for f in filter_cols]
    extra_display_cols = [c.lower() for c in extra_display_cols]
    
    df[col_a] = df[col_a].astype(str)
    df[col_b] = df[col_b].astype(str)
    
    numeric_cols = ['trans_ab', 'trans_a', 'trans_b', 'qty_ab', 'avg_qty_b_when_pair']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # 2. Penentuan Total Transaksi (Wajib Benar)
   # 2. Penentuan Total Transaksi (Strict & Unique Only)
    epsilon = 1e-9
    
    # Prioritas 1: Cek apakah angka total transaksi sudah tertanam di dataset affinity
    if 'total_transactions' in df.columns:
        total_trans = df['total_transactions'].iloc[0]
    
    # Prioritas 2: Cek variabel global 'total_struk_global' (Hasil nunique di fungsi main)
    elif 'total_struk_global' in globals():
        total_trans = total_struk_global
        
    # Prioritas 3: Cek langsung ke dataframe performa (df_p) untuk kolom unik
    else:
        try:
            if 'no_struk' in df_p.columns:
                total_trans = df_p['no_struk'].nunique()
            elif 'buyer_id' in df_p.columns:
                total_trans = df_p['buyer_id'].nunique()
            else:
                # Jika tidak ada satupun sumber angka unik, kirim pesan ke user
                st.warning("⚠️ *Data transaksi unik tidak ditemukan. Pastikan data mentah di-load.*")
                total_trans = 0 # Akan menghasilkan skor 0, bukan skor palsu yang membengkak
        except:
            total_trans = 0
            
    # Pastikan total_trans tidak nol agar tidak pembagian nol
    if total_trans <= 0:
        st.error("Gagal menghitung populasi transaksi (Universe). Periksa sumber data Anda.")
        return
    # 3. Kalkulasi Metrik MBA (Raw)
    df['measure_support'] = df['trans_ab'] / (total_trans + epsilon)
    df['measure_confidence'] = df['trans_ab'] / (df['trans_a'] + epsilon)
    
    supp_a = df['trans_a'] / (total_trans + epsilon)
    supp_b = df['trans_b'] / (total_trans + epsilon)
    df['measure_lift'] = df['measure_support'] / ((supp_a * supp_b) + epsilon)

    # 4. Normalisasi (Skala 0-1)
    df['conf_norm'] = df['measure_confidence'].clip(0, 1)
    
    # SUPPORT: Hapus Min-Max Scaling! Gunakan persentase asli probabilitas agar skor tidak membengkak
    df['supp_norm'] = df['measure_support'].clip(0, 1)
    
    # LIFT: Tetap dinormalisasi (Hanya korelasi positif > 1 yang dihitung)
    df['lift_norm'] = df['measure_lift'].apply(lambda x: (x-1)/4 if x > 1 else 0).clip(0, 1)

    # 5. Weighted Score (Konfigurasi Bobot Anda: 70/25/5)
    df['weighted_score'] = (
        (df['supp_norm'] * 0.70) + 
        (df['conf_norm'] * 0.25) + 
        (df['lift_norm'] * 0.05)
    )

    # 6. QTY Impact Calculation
    if 'avg_qty_b_when_pair' in df.columns and df['avg_qty_b_when_pair'].sum() > 0:
        df['qty_impact'] = df['avg_qty_b_when_pair']
    else:
        df['qty_impact'] = np.where(df['trans_ab'] > 0, df['qty_ab'] / (df['trans_ab'] + epsilon), 0)

    # 7. Filter UI Dinamis
    base_df = df.copy()
    cols_ui = st.columns(len(filter_cols))
    sel_dict = {}

    for i, f_col in enumerate(filter_cols):
        with cols_ui[i]:
            if f_col in base_df.columns:
                unique_vals = sorted(base_df[f_col].dropna().unique())
                
                # Mengganti expander+checkbox menjadi st.multiselect layaknya menu Performance
                sel_vals = st.multiselect(f"{f_col.upper()}:", unique_vals, key=f"{key_prefix}_{f_col}")
                
                if sel_vals:
                    sel_dict[f_col] = sel_vals

    df_filtered = base_df.copy()
    for f_col, sel_vals in sel_dict.items():
        if sel_vals:
            df_filtered = df_filtered[df_filtered[f_col].isin(sel_vals)]

    if df_filtered.empty:
        st.warning("Data kosong setelah difilter.")
        return

    # 8. Render Matrix Table
    matrix_weighted = df_filtered.groupby([col_a, col_b])['weighted_score'].mean().unstack().fillna(0)
    
    colors_aff = ["#ffffff", "#84f884"] 
    cmap_aff = mcolors.LinearSegmentedColormap.from_list("soft_aff", colors_aff)

    st.dataframe(
        matrix_weighted.style.format("{:.2%}")
        .background_gradient(cmap=cmap_aff, axis=None, vmin=0, vmax=0.5) 
        .set_properties(**{
            'color': '#333333', 
            'border': '1px solid #F0F0F0',
            'font-size': '12px'
        }),
        use_container_width=True
    )
    # ========================================================
    # 8.5 RENDER TOP 10 AFFINITY (BARU DITAMBAHKAN)
    # ========================================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("###TOP 10 AFFINITY PAIRS")
    st.info("Menampilkan 10 kombinasi pasangan dengan skor Affinity tertinggi")
    
    # Hitung rata-rata weighted_score per pasangan, urutkan dari terbesar, ambil 10 teratas
    top_10_df = df_filtered.groupby([col_a, col_b])['weighted_score'].mean().reset_index()
    top_10_df = top_10_df.sort_values(by='weighted_score', ascending=False).head(10)
    
    # Rapikan nama kolom agar tampil cantik di tabel
    top_10_display = top_10_df.copy()
    top_10_display.columns = [col_a.upper(), col_b.upper(), 'AFFINITY SCORE']
    
    # Render tabel Top 10
    st.dataframe(
        top_10_display.style.format({'AFFINITY SCORE': '{:.2%}'})
        .set_properties(**{
            'background-color': 'transparent', 
            'color': '#333333', 
            'border': '1px solid #EEEEEE',
            'font-size': '12px',
            'font-weight': '500'
        }),
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # 9. RENDER QTY IMPACT (PERUBAHAN 2: MENGHAPUS DUPLIKAT)
    # ========================================================
    if show_qty_impact:
        st.markdown("---")
        st.write("### 🛒 QTY IMPACT")
        st.info("**QTY Impact** -> Rata-rata jumlah unit produk B yang dibeli saat user membeli produk A")

        display_cols = [col_a, col_b] + extra_display_cols + ['qty_impact']
        available_cols = [c for c in display_cols if c in df_filtered.columns]
        
        # MENGHAPUS DUPLIKAT: Kita gunakan drop_duplicates berdasarkan pasangan produk A dan B
        # sehingga tidak ada lagi data yang tampil double.
        df_qty_table = df_filtered[available_cols].drop_duplicates(subset=[col_a, col_b]).sort_values(by="qty_impact", ascending=False)

        st.dataframe(
            df_qty_table.style.format({"qty_impact": "{:.2f}"})
            .set_properties(**{
                'background-color': 'transparent', 
                'color': '#333333', 
                'border': '1px solid #EEEEEE',
                'font-size': '12px'
            }),
            use_container_width=True,
            hide_index=True
        )

df_p = load_perf_file("category", "V1")
def render_plano_matrix(df):
    if df.empty: return
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📊 Ringkasan Matrix Perbandingan Plano")
    
    # Menyiapkan data untuk Pivot (V1 vs V2)
    # Pastikan kolom 'VERSI' dan 'SECTION' ada di data kamu
    try:
        # Kita ambil rata-rata pertumbuhan atau total sales sebagai nilai matrix
        val_col = 'SALES_VALUE' if 'SALES_VALUE' in df.columns else df.select_dtypes(include=[np.number]).columns[0]
        
        pivot_df = df.pivot_table(
            index='SECTION', 
            columns='VERSI', 
            values=val_col, 
            aggfunc='mean'
        ).round(2)
        
        # Tampilkan Matrix dengan Desain Premium
        st.dataframe(
            pivot_df.style.background_gradient(cmap='Reds', axis=1)
            .format("{:,.2f}"),
            use_container_width=True
        )
        st.caption(f"*) Data di atas adalah perbandingan rata-rata {val_col} antara Versi Plano.")
    except Exception as e:
        st.info("Matrix perbandingan tidak tersedia untuk level detail ini.")
def render_static_affinity_matrix():
    try:
        # 1. Ambil data affinity yang sudah di-load di awal
        aff = load_affinity_data()
        if not aff: return
        
        # 2. Gabungkan data Category & Subcategory untuk mendapatkan mapping varian lengkap
        df_map = pd.concat([aff["cat"], aff["subcat"]], ignore_index=True)
        df_map.columns = [c.upper() for c in df_map.columns] # Paksa ke UPPERCASE agar konsisten
        
        # 3. Proses Pivot: Baris = SECTION, Kolom = PLANO_GROUP_FINAL, Isi = KD_VARIANT
        df_pivoted = df_map.pivot_table(
            index='SECTION', 
            columns='PLANO_GROUP_FINAL', 
            values='KD_VARIANT',
            aggfunc=lambda x: ', '.join(x.astype(str).unique())
        ).reset_index().fillna("-")
        
        # 4. Ambil HANYA 3 kolom sesuai permintaan Anda
        cols_to_keep = ['SECTION', 'AFTER_V1', 'AFTER_V2']
        df_display = df_pivoted[[c for c in cols_to_keep if c in df_pivoted.columns]].copy()
        
        # 5. Rename kolom agar sesuai dengan keinginan Anda
        df_display.columns = ['SECTION', 'VERSI PLANO V1', 'VERSI PLANO V2']
        
        # 6. Tampilkan Tabel Statis (Desain disamakan dengan Affinity)
        st.markdown("---")
        with st.expander("📋 MATRIKS VARIAN BY VERSI PLANO (Reference)", expanded=False):
            st.dataframe(
                df_display.style.set_properties(**{
                    'background-color': 'transparent',
                    'color': '#333333',
                    'border': '1px solid #F5F5F5',
                    'font-size': '12px',
                    'text-align': 'left'
                }),
                use_container_width=True,
                hide_index=True # Menghilangkan angka indeks 0, 1, 2 di kiri
            )
        
    except Exception as e:
        st.info(f"Matriks varian belum tersedia: {e}")

def render_switching_cards(total_sw, total_no, top_dest_name, top_dest_pct):
    """Render 3 KPI Cards for Switching Menu (English)"""
    total = total_sw + total_no
    if total == 0: return

    pct_sw = total_sw / total
    pct_no = total_no / total

    card_style = """
        background-color: #F8F9FA; 
        border-radius: 8px; 
        padding: 15px; 
        min-height: 100px; 
        border: 1px solid #EEE;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
        overflow: hidden;
    """

    cols = st.columns(3) # Dibagi rata menjadi 3 kolom
    
    with cols[0]:
        st.markdown(f"""
            <div style="{card_style}; border-bottom: 4px solid #E1B7B3;">
                <p style="color:#666; font-size:13px; margin:0; font-weight:600; text-transform:uppercase;">Switch Rate</p>
                <div style="font-size:32px; font-weight:800; color:#1E293B; line-height:1.2;">{pct_sw:.2%}</div>
                <p style="color:#888; font-size:11px; margin:0;">Total: {total_sw:,} Buyers</p>
            </div>
        """, unsafe_allow_html=True)
        
    with cols[1]:
        st.markdown(f"""
            <div style="{card_style}; border-bottom: 4px solid #AEE3B2;">
                <p style="color:#666; font-size:13px; margin:0; font-weight:600; text-transform:uppercase;">Retention Rate (No Switch)</p>
                <div style="font-size:32px; font-weight:800; color:#1E293B; line-height:1.2;">{pct_no:.2%}</div>
                <p style="color:#888; font-size:11px; margin:0;">Total: {total_no:,} Buyers</p>
            </div>
        """, unsafe_allow_html=True)

    with cols[2]:
        st.markdown(f"""
            <div style="{card_style}; border-bottom: 4px solid #3498DB;">
                <p style="color:#666; font-size:13px; margin:0; font-weight:600; text-transform:uppercase;">Top Destination</p>
                <div style="font-size:32px; font-weight:800; color:#1E293B; line-height:1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{top_dest_name}">{top_dest_name}</div>
                <p style="color:#888; font-size:11px; margin:0;">Share: {top_dest_pct:.2%} of Switchers</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

def main():
    global df_p 
    
    # --- HITUNG DARI DATA MENTAH ---
    global total_struk_global
    if 'df_raw' in globals():
        total_struk_global = df_raw['NO_STRUK'].nunique()
    else:
        # Jika df_raw tidak ada di memory, kita tarik dari Buyer Count Global di df_p
        # Ini adalah proxy paling mendekati jika NO_STRUK tidak tersedia
        total_struk_global = df_p['BUYER_COUNT_BEFORE'].max()
    sections_only = sorted(df_p["SECTION"].unique().tolist())

    # Cari index pertama yang huruf depannya 'B' (Default ke 0 jika tidak ada)
    start_idx = next((i for i, s in enumerate(sections_only) if str(s).startswith('B')), 0)

    st.sidebar.markdown('<p class="sidebar-title-custom">SHOPPER<br>CATEGORY<br>INSIGHT</p>', unsafe_allow_html=True)
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    # 2. MENU: Beri sedikit keterangan jika perlu
    st.sidebar.write("MENU:")
    menu = st.sidebar.radio("", ["📈 PERFORMANCE", "🔄 SWITCHING", "🛒 AFFINITY"], label_visibility="collapsed")

    try:
        sections_only = sorted(df_p["SECTION"].unique().tolist())
    except NameError:
        st.error("Variabel 'df_p' tidak ditemukan. Pastikan data performance sudah di-load di awal file.")
        return

    if menu == "📈 PERFORMANCE":
        col_title, col_plano, col_sec = st.columns([5, 2.5, 2.5])
        with col_title: st.title("📈 PERFORMANCE OVERVIEW")
        with col_plano: sel_plano = st.selectbox("VERSI PLANO", ["V1", "V2"], key="plano_perf")
        with col_sec: 
            # HAPUS ["ALL"] + dan gunakan index=start_idx
            sel_sec = st.selectbox("SECTION FILTER", sections_only, index=start_idx, key="sec_perf")
        st.markdown(f"**Periode Trial Phase 1 [Juli - September 2025]**")

        st.markdown("---")

        # =================================================================
        # FUNGSI SMART CROSS-FILTERING (AGAR FILTER BISA SALING MENYUSUT)
        # =================================================================
        def get_dynamic_options(df, col_name, current_selections, filter_dict):
            temp_df = df.copy()
            for k, v in filter_dict.items():
                if v: # Jika filter lain sedang terisi, saring datanya
                    temp_df = temp_df[temp_df[k].isin(v)]
            # Ambil opsi yang tersisa
            opts = set(temp_df[col_name].dropna().unique())
            # Cegah error Streamlit dengan tetap mempertahankan pilihan yang sedang aktif
            for sel in current_selections:
                opts.add(sel)
            return sorted(list(opts))

        # =================================================================
        t_cat, t_sub, t_brand, t_plu, t_seg = st.tabs(["CATEGORY", "SUBCATEGORY", "BRAND", "PLU", "SEGMENTASI"])

        def apply_filter(df):
            if df.empty: return df
            if sel_sec != "ALL": df = df[df["SECTION"] == sel_sec]
            return df.reset_index(drop=True)

        with t_cat:
            df_f = apply_filter(load_perf_file("category", sel_plano))
            if not df_f.empty:
                card_place = st.container()
                s_l = st.multiselect(" FILTER CATEGORY:", sorted(df_f["CATEGORY"].unique()), key="f_cat")
                if s_l: df_f = df_f[df_f["CATEGORY"].isin(s_l)]
                with card_place:
                    render_performance_cards(df_f, is_category=True)
                display_styled_table(reorder_final(df_f, "category"))
                render_static_affinity_matrix() # Tambahkan di baris terakhir tab

        # ==========================================
        # TAB SUBCATEGORY
        # ==========================================
        # ==========================================
        # TAB SUBCATEGORY
        # ==========================================
        with t_sub:
            df_f = apply_filter(load_perf_file("subcategory", sel_plano))
            if not df_f.empty:
                # Ambil state filter saat ini
                curr_cat = st.session_state.get("m_sub_c", [])
                curr_sub = st.session_state.get("m_sub_s", [])
                
                # Hitung opsi dinamis (Saling menyusut)
                cat_opts = get_dynamic_options(df_f, "CATEGORY", curr_cat, {"SUBCATEGORY": curr_sub})
                sub_opts = get_dynamic_options(df_f, "SUBCATEGORY", curr_sub, {"CATEGORY": curr_cat})
                
                f_cols = st.columns([10, 10]) 
                with f_cols[0]: m_cat = st.multiselect("CAT:", cat_opts, key="m_sub_c")
                with f_cols[1]: m_sub = st.multiselect("SUBCAT:", sub_opts, key="m_sub_s")
                
                # Saring data akhir
                if m_cat: df_f = df_f[df_f["CATEGORY"].isin(m_cat)]
                if m_sub: df_f = df_f[df_f["SUBCATEGORY"].isin(m_sub)]
                
                render_performance_cards(df_f, is_category=False)
                display_styled_table(reorder_final(df_f, "subcategory"))
                render_static_affinity_matrix()

        # ==========================================
        # TAB BRAND
        # ==========================================
        with t_brand:
            df_f = apply_filter(load_perf_file("brand", sel_plano))
            if not df_f.empty:
                curr_cat = st.session_state.get("m_br_c", [])
                curr_sub = st.session_state.get("m_br_s", [])
                curr_br = st.session_state.get("m_br_b", [])
                
                cat_opts = get_dynamic_options(df_f, "CATEGORY", curr_cat, {"SUBCATEGORY": curr_sub, "BRAND": curr_br})
                sub_opts = get_dynamic_options(df_f, "SUBCATEGORY", curr_sub, {"CATEGORY": curr_cat, "BRAND": curr_br})
                br_opts = get_dynamic_options(df_f, "BRAND", curr_br, {"CATEGORY": curr_cat, "SUBCATEGORY": curr_sub})

                f_cols = st.columns([5, 5, 5]) 
                with f_cols[0]: m_cat = st.multiselect("CAT:", cat_opts, key="m_br_c")
                with f_cols[1]: m_sub = st.multiselect("SUBCAT:", sub_opts, key="m_br_s")
                with f_cols[2]: m_br = st.multiselect("BRAND:", br_opts, key="m_br_b")

                if m_cat: df_f = df_f[df_f["CATEGORY"].isin(m_cat)]
                if m_sub: df_f = df_f[df_f["SUBCATEGORY"].isin(m_sub)]
                if m_br: df_f = df_f[df_f["BRAND"].isin(m_br)]

                render_performance_cards(df_f, is_category=False)
                display_styled_table(reorder_final(df_f, "brand"))
                render_static_affinity_matrix()

        # ==========================================
        # TAB PLU
        # ==========================================
        with t_plu:
            df_f = apply_filter(load_perf_file("plu", sel_plano))
            if not df_f.empty:
                curr_cat = st.session_state.get("m_plu_c", [])
                curr_plu = st.session_state.get("m_plu_p", [])
                
                cat_opts = get_dynamic_options(df_f, "CATEGORY", curr_cat, {"PLU": curr_plu})
                plu_opts = get_dynamic_options(df_f, "PLU", curr_plu, {"CATEGORY": curr_cat})

                f_cols = st.columns([5, 5])
                with f_cols[0]: m_cat = st.multiselect("CAT:", cat_opts, key="m_plu_c")
                with f_cols[1]: m_plu = st.multiselect("PLU:", plu_opts, key="m_plu_p")

                if m_cat: df_f = df_f[df_f["CATEGORY"].isin(m_cat)]
                if m_plu: df_f = df_f[df_f["PLU"].isin(m_plu)]

                render_performance_cards(df_f, is_category=False)
                display_styled_table(reorder_final(df_f, "plu"))
                render_static_affinity_matrix()

        # ==========================================
        # TAB SEGMENTASI (BACK TO SUB-TABS DESIGN)
        # ==========================================
        with t_seg:
            df_seg = load_segment_unified()
            if not df_seg.empty:
                # 1. Base Filter (Plano & Section)
                df_seg_f = df_seg[df_seg["VERSI"].str.upper() == sel_plano.upper()].copy()
                df_seg_f = apply_global_perf(df_seg_f, sel_sec) 
                
                # 2. Filter Hierarki Produk (Smart Cross-Filtering)
                curr_cat = st.session_state.get("seg_c", [])
                curr_sub = st.session_state.get("seg_s", [])
                curr_br = st.session_state.get("seg_b", [])
                
                cat_opts = get_dynamic_options(df_seg_f, "CATEGORY", curr_cat, {"SUBCATEGORY": curr_sub, "BRAND": curr_br})
                sub_opts = get_dynamic_options(df_seg_f, "SUBCATEGORY", curr_sub, {"CATEGORY": curr_cat, "BRAND": curr_br})
                br_opts = get_dynamic_options(df_seg_f, "BRAND", curr_br, {"CATEGORY": curr_cat, "SUBCATEGORY": curr_sub})

                f1, f2, f3 = st.columns(3)
                with f1: m_cat_seg = st.multiselect("FILTER CATEGORY", cat_opts, key="seg_c")
                with f2: m_sub_seg = st.multiselect("FILTER SUBCATEGORY", sub_opts, key="seg_s")
                with f3: m_brand_seg = st.multiselect("FILTER BRAND", br_opts, key="seg_b")

                # Terapkan filter hierarki ke dataframe utama tab ini
                if m_cat_seg: df_seg_f = df_seg_f[df_seg_f["CATEGORY"].isin(m_cat_seg)]
                if m_sub_seg: df_seg_f = df_seg_f[df_seg_f["SUBCATEGORY"].isin(m_sub_seg)]
                if m_brand_seg: df_seg_f = df_seg_f[df_seg_f["BRAND"].isin(m_brand_seg)]

                if not df_seg_f.empty:
                    # 3. Render Kartu (Tanpa Category Penetration)
                    # Kita ambil baris unik per SEGMENT_VALUE agar kartu tidak double count
                    df_for_cards = df_seg_f.drop_duplicates(subset=['SEGMENT_TYPE', 'SEGMENT_VALUE', 'CATEGORY'])
                    render_performance_cards(df_for_cards, is_category=False)
                    
                    # 4. Render Sub-Tabs berdasarkan SEGMENT_TYPE
                    seg_list = sorted(df_seg_f["SEGMENT_TYPE"].dropna().unique())
                    tabs_seg = st.tabs([s.upper() for s in seg_list])
                    
                    for i, s_type in enumerate(seg_list):
                        with tabs_seg[i]:
                            # Filter data khusus tipe segmen ini
                            df_tab = df_seg_f[df_seg_f["SEGMENT_TYPE"] == s_type].copy()
                            
                            # Aggregasi untuk Tabel
                            group_cols = ["SEGMENT_VALUE", "CATEGORY", "SECTION"]
                            num_cols = df_tab.select_dtypes(include=[np.number]).columns.tolist()
                            agg_dict = {c: ('mean' if any(x in c for x in ['GROWTH', 'PENETRATION']) else 'sum') for c in num_cols}
                            df_clean = df_tab.groupby(group_cols).agg(agg_dict).reset_index()

                            display_styled_table(reorder_final(df_clean, "category"))
                            render_static_affinity_matrix()
                else:
                    st.warning("Data tidak ditemukan untuk filter ini.")
                    
    elif menu == "🔄 SWITCHING":
        col_title, col_sec_filter = st.columns([6, 4])
        with col_title:
            st.markdown('<h1 style="margin:0;">🔄 SWITCHING & LOYALTY ANALYSIS</h1>', unsafe_allow_html=True)
        with col_sec_filter:
            sel_sec_sw = st.selectbox("SECTION FILTER", sections_only, index=start_idx, key="sec_sw_top")
        st.markdown(f"**Periode Trial Phase 1 [Juli - September 2025]**")

        st.markdown("---")
        loy_data = load_loyalty_data()
        
        if not loy_data:
            st.error("Switching data not found!")
        else:
            tab_configs = [
                {"name": "BRAND LOYALTY (CAT)", "df_key": "br_loy_cat", "filters": ["CATEGORY", "BRAND_BEFORE"], "main_col": "BRAND_BEFORE", "after_col": "BRAND_AFTER", "id_level": ["CATEGORY", "BRAND_BEFORE"]},
                {"name": "BRAND LOYALTY (SUBCAT)", "df_key": "br_loy_sub", "filters": ["SUBCATEGORY", "BRAND_BEFORE"], "main_col": "BRAND_BEFORE", "after_col": "BRAND_AFTER", "id_level": ["SUBCATEGORY", "CATEGORY", "BRAND_BEFORE"]},
                {"name": "BRAND SWITCH (CAT)", "df_key": "br_swi_cat", "filters": ["BRAND", "CATEGORY_BEFORE"], "main_col": "CATEGORY_BEFORE", "after_col": "CATEGORY_AFTER", "id_level": ["BRAND", "CATEGORY_BEFORE"]},
                {"name": "BRAND SWITCH (SUBCAT)", "df_key": "br_swi_sub", "filters": ["BRAND", "SUBCATEGORY_BEFORE"], "main_col": "SUBCATEGORY_BEFORE", "after_col": "SUBCATEGORY_AFTER", "id_level": ["BRAND", "SUBCATEGORY_BEFORE"]},
                {"name": "CATEGORY SWITCHING", "df_key": "cat_loy", "filters": ["SECTION", "CATEGORY_BEFORE"], "main_col": "CATEGORY_BEFORE", "after_col": "CATEGORY_AFTER", "id_level": ["CATEGORY_BEFORE"]},
                {"name": "SUBCATEGORY SWITCHING", "df_key": "sub_loy", "filters": ["CATEGORY", "SUBCATEGORY_BEFORE"], "main_col": "SUBCATEGORY_BEFORE", "after_col": "SUBCATEGORY_AFTER", "id_level": ["CATEGORY", "SUBCATEGORY_BEFORE"]}
            ]

            tabs = st.tabs([cfg["name"] for cfg in tab_configs])
            
            for i, cfg in enumerate(tab_configs):
                with tabs[i]:
                    df_raw = loy_data[cfg["df_key"]].copy()
                    
                    if sel_sec_sw != "ALL":
                        df_raw = df_raw[df_raw["SECTION"] == sel_sec_sw]

                    # --- ROW 1: FILTERS (Single Select with "ALL" Option) ---
                    col_ratios = [3] * len(cfg["filters"]) + [4] 
                    col_filters = st.columns(col_ratios)
                    
                    for j, filt_col in enumerate(cfg["filters"]):
                        with col_filters[j]:
                            if filt_col in df_raw.columns:
                                # Menambahkan opsi "ALL" di urutan paling atas
                                unique_vals = ["ALL"] + sorted(df_raw[filt_col].dropna().unique().tolist())
                                
                                sel_val = st.selectbox(f"{filt_col}:", unique_vals, key=f"sb_sw_{i}_{j}")
                                
                                # Filter hanya berjalan jika user tidak memilih "ALL"
                                if sel_val != "ALL":
                                    df_raw = df_raw[df_raw[filt_col] == sel_val]

                    if df_raw.empty:
                        st.warning("No data available for this filter.")
                        continue
                    
                    st.markdown("<br>", unsafe_allow_html=True)

                    # --- ROW 2: KPI CARDS ---
                    total_sw = df_raw[df_raw["SWITCH_FLAG"] == "SWITCH"]["BUYER_ID"].nunique()
                    total_no = df_raw[df_raw["SWITCH_FLAG"] == "NO_SWITCH"]["BUYER_ID"].nunique()
                    
                    # Logika untuk mencari Top Destination
                    top_dest_name = "-"
                    top_dest_pct = 0.0
                    df_only_sw = df_raw[df_raw["SWITCH_FLAG"] == "SWITCH"]
                    
                    if not df_only_sw.empty:
                        dest_counts = df_only_sw.groupby(cfg["after_col"])["BUYER_ID"].nunique().reset_index()
                        if not dest_counts.empty:
                            top_dest_row = dest_counts.loc[dest_counts["BUYER_ID"].idxmax()]
                            top_dest_name = str(top_dest_row[cfg["after_col"]])
                            top_dest_pct = top_dest_row["BUYER_ID"] / total_sw if total_sw > 0 else 0.0

                    # Panggil render 3 kartu
                    render_switching_cards(total_sw, total_no, top_dest_name, top_dest_pct)

                    # --- ROW 3: AGGREGATION TABLE ---
                    st.markdown("#### 📑 Detailed Switching Data")
                    group_cols = cfg["id_level"] + ["SECTION"]
                    agg_df = df_raw.groupby(group_cols + ["SWITCH_FLAG"])["BUYER_ID"].nunique().unstack(fill_value=0)
                    
                    for col in ["SWITCH", "NO_SWITCH"]:
                        if col not in agg_df.columns: agg_df[col] = 0
                    
                    agg_df["TOTAL"] = agg_df["SWITCH"] + agg_df["NO_SWITCH"]
                    agg_df["% SWITCH"] = (agg_df["SWITCH"] / agg_df["TOTAL"])
                    agg_df["% NO_SWITCH"] = (agg_df["NO_SWITCH"] / agg_df["TOTAL"])
                    
                    table_display = agg_df.reset_index()[group_cols + ["% SWITCH", "% NO_SWITCH"]]
                    table_display = table_display.sort_values([group_cols[0], "% SWITCH"], ascending=[True, False])

                    styled_table = (
                        table_display.style.format({"% SWITCH": "{:.2%}", "% NO_SWITCH": "{:.2%}"})
                        .set_properties(**{'background-color': '#FFFFFF', 'color': '#333333', 'border': '1px solid #F1F5F9'})
                        .background_gradient(cmap="Reds", subset=["% SWITCH"])
                        .background_gradient(cmap="Greens", subset=["% NO_SWITCH"])
                    )
                    st.dataframe(styled_table, use_container_width=True, height=400, hide_index=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # --- ROW 4: TWO PIE CHARTS SIDE BY SIDE ---
                    st.markdown("<br>", unsafe_allow_html=True)
                    col_pie1, col_pie2 = st.columns(2)

                    with col_pie1:
                        # Judul tanpa div pembungkus yang bikin error
                        st.markdown("<h4 style='text-align: center; color: #475569; font-weight: 600;'>SWITCH VS NO SWITCH COMPOSITION</h4>", unsafe_allow_html=True)
                        
                        fig_overall = px.pie(
                            values=[total_sw, total_no], names=["SWITCH", "NO_SWITCH"],
                            hole=0.6, 
                            color_discrete_map={"NO_SWITCH": "#AEE3B2", "SWITCH": "#E1B7B3"} 
                        )
                        fig_overall.update_layout(
                            margin=dict(t=20, b=10, l=10, r=10), # Beri sedikit jarak atas (t=20)
                            height=320, 
                            showlegend=True, 
                            paper_bgcolor='rgba(0,0,0,0)', 
                            plot_bgcolor='rgba(0,0,0,0)'
                        )
                        fig_overall.update_traces(textinfo='percent+label', textfont_size=12)
                        st.plotly_chart(fig_overall, use_container_width=True)

                    with col_pie2:
                        # Judul tanpa div pembungkus
                        st.markdown("<h4 style='text-align: center; color: #475569; font-weight: 600;'>TOP DESTINATION SWITCH</h4>", unsafe_allow_html=True)
                        
                        if not df_only_sw.empty:
                            dest_data = df_only_sw.groupby(cfg["after_col"])["BUYER_ID"].nunique().reset_index()
                            dest_data = dest_data.nlargest(10, "BUYER_ID")
                            
                            premium_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD', '#D4A5A5', '#9B59B6', '#3498DB', '#F1C40F', '#E67E22']
                            
                            fig_dest_pie = px.pie(
                                dest_data, values="BUYER_ID", names=cfg["after_col"],
                                color_discrete_sequence=premium_colors
                            )
                            fig_dest_pie.update_layout(
                                margin=dict(t=20, b=10, l=10, r=10), 
                                height=320, 
                                paper_bgcolor='rgba(0,0,0,0)', 
                                plot_bgcolor='rgba(0,0,0,0)'
                            )
                            fig_dest_pie.update_traces(
                                textinfo='percent', 
                                textfont_size=12, 
                                marker=dict(line=dict(color='#FFFFFF', width=2))
                            )
                            st.plotly_chart(fig_dest_pie, use_container_width=True)
                        else:
                            st.info("No switch data to analyze for this filter.")

                    # Garis pemisah estetik sebelum chart Promo
                    st.markdown("<hr style='border: 1px dashed #E2E8F0; margin: 30px 0;'>", unsafe_allow_html=True)

                    # --- ROW 5: PROMO INFLUENCE ---
                    st.markdown("<h4 style='text-align: center; color: #475569; font-weight: 600;'>PROMO INFLUENCE ON DESTINATION SWITCH</h4>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    top_brands = df_raw.groupby(cfg["after_col"])["BUYER_ID"].nunique().nlargest(15).index
                    df_promo = df_raw[df_raw[cfg["after_col"]].isin(top_brands)]
                    
                    if not df_promo.empty:
                        promo_agg = df_promo.groupby([cfg["after_col"], "PROMO_FLAG"])["BUYER_ID"].nunique().reset_index()
                        totals = promo_agg.groupby(cfg["after_col"])["BUYER_ID"].transform('sum')
                        promo_agg['PERCENTAGE'] = promo_agg['BUYER_ID'] / totals
                        
                        fig_promo = px.bar(
                            promo_agg, x=cfg["after_col"], y="PERCENTAGE", color="PROMO_FLAG",
                            color_discrete_map={"PROMO": "#FAD12D", "NON PROMO": "#642C2C"},
                            barmode="stack",
                            text=promo_agg["PERCENTAGE"].apply(lambda x: f"{x:.1%}") 
                        )
                        fig_promo.update_layout(
                            template='plotly_white', height=400, 
                            xaxis_title="", yaxis_title="Percentage",
                            yaxis=dict(tickformat=".0%"),
                            # Posisi legend agak diangkat agar tidak menabrak bar
                            legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
                            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            margin=dict(t=20, b=0, l=0, r=0)
                        )
                        st.plotly_chart(fig_promo, use_container_width=True)
                    else:
                        st.info("No promo data available.")

    elif menu == "🛒 AFFINITY":
        # ==========================================
        # TOP FILTER HEADER (SECTION & PLANO GROUP)
        # ==========================================
        col_title, col_plano_filter, col_sec_filter = st.columns([5, 2.5, 2.5])
        with col_title:
            st.title("🛒 MARKET BASKET ANALYSIS")

        # SETUP OPSI PLANO
        plano_options = ["BEFORE_V1", "BEFORE_V2", "AFTER_V1", "AFTER_V2", "NOT_TRIAL"]
        st.markdown(f"**Periode Trial Phase 1 [Juli - September 2025]**")
        with col_plano_filter:
            sel_plano = st.selectbox(
                "VERSI PLANO",
                plano_options,
                index=2, # Default ke index 2 ("AFTER_V1")
                key="plano_aff_top"
            )

        with col_sec_filter:
            sel_sec_aff = st.selectbox(
                "SECTION FILTER",
                sections_only,
                key="sec_aff_top_right"
            )

        st.markdown("---")

        aff = load_affinity_data()

        if not aff:
            st.error("Data Affinity tidak ditemukan!")
        else:

            tab1, tab2, tab3, tab4 = st.tabs([
                "CATEGORY",
                "SUB-CATEGORY",
                "BRAND/CAT",
                "BRAND/SUBCAT"
            ])

            # ======================================================
            # FILTER MASTER: MENGAPLIKASIKAN SECTION & PLANO
            # ======================================================
            def filter_affinity_base(df, section_val, plano_val):
                df = df.copy()
                df.columns = [c.lower() for c in df.columns]

                # Filter by Section
                if "section" in df.columns:
                    df["section"] = df["section"].astype(str).str.strip().str.upper()
                    df = df[df["section"] == str(section_val).strip().upper()]

                # Filter by Plano Group Final
                if "plano_group_final" in df.columns:
                    df["plano_group_final"] = df["plano_group_final"].astype(str).str.strip().str.upper()
                    df = df[df["plano_group_final"] == str(plano_val).strip().upper()]

                return df.reset_index(drop=True)

            # ======================================================
            # TAB 1 — CATEGORY
            # ======================================================
            with tab1:
                df_cat = aff["cat"].copy()
                df_f = filter_affinity_base(df_cat, sel_sec_aff, sel_plano)

                categories_in_section = set(df_f["category_a"].astype(str).unique()).intersection(
                    set(df_f["category_b"].astype(str).unique())
                )

                df_f = df_f[
                    df_f["category_a"].astype(str).isin(categories_in_section) &
                    df_f["category_b"].astype(str).isin(categories_in_section)
                ].reset_index(drop=True)

                st.subheader(f"AFFINITY CATEGORY BY SECTION : {sel_sec_aff}")
                render_affinity_tab(df_f, "category_a", "category_b", ["category_a", "category_b"], "c_aff")

            # ======================================================
            # TAB 2 — SUB CATEGORY
            # ======================================================
            with tab2:
                df_sub = aff["subcat"].copy()
                df_f = filter_affinity_base(df_sub, sel_sec_aff, sel_plano)

                valid_sub = set(pd.concat([df_f["subcategory_a"], df_f["subcategory_b"]]).astype(str).unique())

                df_f = df_f[
                    df_f["subcategory_a"].astype(str).isin(valid_sub) &
                    df_f["subcategory_b"].astype(str).isin(valid_sub)
                ].reset_index(drop=True)

                st.subheader(f"AFFINITY SUBCATEGORY BY SECTION : {sel_sec_aff}")
                render_affinity_tab(df_f, "subcategory_a", "subcategory_b", ["subcategory_a", "subcategory_b"], "s_aff")

            # ======================================================
            # TAB 3 — BRAND BY CATEGORY
            # ======================================================
            with tab3:
                df_bc = aff["brand_cat"].copy()
                df_f = filter_affinity_base(df_bc, sel_sec_aff, sel_plano)

                valid_brand = set(pd.concat([df_f["brand_a"], df_f["brand_b"]]).astype(str).unique())

                df_f = df_f[
                    df_f["brand_a"].astype(str).isin(valid_brand) &
                    df_f["brand_b"].astype(str).isin(valid_brand)
                ].reset_index(drop=True)

                st.subheader(f"AFFINITY BRAND BY CATEGORY SECTION : {sel_sec_aff}")
                # show_qty_impact=False untuk menghapus tabel QTY Impact yang anomali
                render_affinity_tab(
                    df_f, 
                    "brand_a", 
                    "brand_b", 
                    ["brand_a", "brand_b", "category_a", "category_b"], 
                    "bc_aff",
                    show_qty_impact=False 
                )

            # ======================================================
            # TAB 4 — BRAND BY SUB CATEGORY
            # ======================================================
            with tab4:
                df_bs = aff["brand_sub"].copy()
                df_f = filter_affinity_base(df_bs, sel_sec_aff, sel_plano)

                valid_brand = set(pd.concat([df_f["brand_a"], df_f["brand_b"]]).astype(str).unique())

                df_f = df_f[
                    df_f["brand_a"].astype(str).isin(valid_brand) &
                    df_f["brand_b"].astype(str).isin(valid_brand)
                ].reset_index(drop=True)

                st.subheader(f"AFFINITY BRAND BY SUBCATEGORY SECTION : {sel_sec_aff}")
                render_affinity_tab(
                    df_f, 
                    "brand_a", 
                    "brand_b", 
                    ["brand_a", "brand_b", "subcategory_a", "subcategory_b"], 
                    "bs_aff",
                    show_qty_impact=False
                )

        # ======================================================
        # TABEL MAPPING REFERENSI (PIVOT VERSION - CLEAN)
        # ======================================================
        st.markdown("---")
        with st.expander("📋 MATRIKS VARIAN BY VERSI PLANO", expanded=False):
            
            # 1. Ambil data unik dari dataset affinity
            df_map = pd.concat([aff["cat"], aff["subcat"]], ignore_index=True)
            df_map.columns = [c.lower() for c in df_map.columns]
            
            # 2. List kolom yang dibutuhkan (Tanpa KD_SECTION)
            cols_needed = ['section', 'kd_variant', 'plano_group_final']
            available = [c for c in cols_needed if c in df_map.columns]
            
            if len(available) == 3:
                # 3. Proses Pivot
                # Index: SECTION, Columns: PLANO_GROUP_FINAL, Values: KD_VARIANT
                df_ref_pivot = df_map[available].drop_duplicates()
                
                df_pivoted = df_ref_pivot.pivot_table(
                    index='section', 
                    columns='plano_group_final', 
                    values='kd_variant',
                    aggfunc=lambda x: ', '.join(x.astype(str).unique())
                ).reset_index().fillna("-")
                
                # Urutkan kolom agar BEFORE muncul sebelum AFTER jika memungkinkan
                cols = df_pivoted.columns.tolist()
                sorted_cols = [cols[0]] + sorted(cols[1:])
                df_pivoted = df_pivoted[sorted_cols]
                
                # 4. Render Tabel
                st.dataframe(
                    df_pivoted.style.set_properties(**{
                        'background-color': 'transparent',
                        'color': '#333333',
                        'border': '1px solid #F5F5F5',
                        'font-size': '12px',
                        'text-align': 'left'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Kolom mapping (Section/Variant/Plano) tidak lengkap di dataset.")


if __name__ == "__main__":
    main()

    