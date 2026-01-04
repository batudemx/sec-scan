import streamlit as st
import subprocess
import json
import pandas as pd
import altair as alt
import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="DevSecOps Container Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- RENK PALETİ ---
SEVERITY_COLORS = {
    "CRITICAL": "#ff2b2b",
    "HIGH": "#ff9f1c",
    "MEDIUM": "#ffd700",
    "LOW": "#2ec4b6",
    "UNKNOWN": "#a0a0a0"
}

# --- FONKSİYONLAR ---
def run_trivy_scan(image_name):
    command = f"trivy image -f json -q --scanners vuln --timeout 15m {image_name}"
    try:
        process = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if process.returncode != 0:
            st.error(f"Trivy Hatası: {process.stderr}")
            return None
        if not process.stdout.strip():
            st.warning("Trivy boş çıktı döndü.")
            return None
        return json.loads(process.stdout)
    except Exception as e:
        st.error(f"Kritik Hata: {e}")
        return None

def process_trivy_data(json_data):
    vulnerabilities = []
    if "Results" in json_data:
        for result in json_data["Results"]:
            target = result.get("Target", "Bilinmiyor")
            target_type = result.get("Type", "Bilinmiyor")
            if "Vulnerabilities" in result:
                for vuln in result["Vulnerabilities"]:
                    vulnerabilities.append({
                        "ID": vuln.get("VulnerabilityID"),
                        "Paket": vuln.get("PkgName"),
                        "Mevcut Sürüm": vuln.get("InstalledVersion"),
                        "Düzeltilmiş Sürüm": vuln.get("FixedVersion", "Yama Yok ❌"),
                        "Ciddiyet": vuln.get("Severity"),
                        "Açıklama": vuln.get("Description", "Açıklama yok."),
                        "Hedef": target,
                        "Tür": target_type
                    })
    return pd.DataFrame(vulnerabilities)

# --- ARAYÜZ ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/docker.png", width=80)
    st.title("Container Scanner")
    st.markdown("---")
    
    image_input = st.text_input("Docker İmaj Adı:", value="nginx:1.14")
    scan_btn = st.button("🛡️ Taramayı Başlat", type="primary", use_container_width=True)
    
    st.info("Filtreleme yaparken verilerin kaybolmaması için Session State kullanılıyor.")


if scan_btn:
    with st.spinner("🕵️‍♂️ Trivy analizi yapılıyor..."):
        raw_data = run_trivy_scan(image_input)
        if raw_data:
            df = process_trivy_data(raw_data)
            # Veriyi hafızaya atıyoruz
            st.session_state['scan_data'] = df
            st.session_state['image_name'] = image_input
            st.session_state['scan_time'] = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')

if 'scan_data' in st.session_state and st.session_state['scan_data'] is not None:
    df = st.session_state['scan_data']
    img_name = st.session_state['image_name']
    scan_time = st.session_state['scan_time']

    # Başlık Alanı
    st.title("🛡️ DevSecOps Güvenlik Paneli")
    st.markdown(f"**Hedef İmaj:** `{img_name}` | **Tarih:** {scan_time}")
    st.divider()

    if df.empty:
        st.success("🎉 Temiz! Bu imajda zafiyet bulunamadı.")
    else:
        total_vulns = len(df)
        critical_count = len(df[df["Ciddiyet"] == "CRITICAL"])
        high_count = len(df[df["Ciddiyet"] == "HIGH"])
        fixable_count = len(df[df["Düzeltilmiş Sürüm"] != "Yama Yok ❌"])
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Toplam Zafiyet", total_vulns, delta="Risk")
        c2.metric("Kritik Seviye", critical_count, delta_color="inverse")
        c3.metric("Yüksek Seviye", high_count, delta_color="inverse")
        c4.metric("Düzeltilebilir", fixable_count, delta="Fixable")
        
        st.markdown("---")

        # GRAFİKLER
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.subheader("📊 Zafiyet Dağılımı")
            severity_counts = df["Ciddiyet"].value_counts().reset_index()
            severity_counts.columns = ["Ciddiyet", "Adet"]
            chart = alt.Chart(severity_counts).mark_arc(innerRadius=60).encode(
                theta=alt.Theta(field="Adet", type="quantitative"),
                color=alt.Color(field="Ciddiyet", scale=alt.Scale(domain=list(SEVERITY_COLORS.keys()), range=list(SEVERITY_COLORS.values()))),
                tooltip=["Ciddiyet", "Adet"]
            )
            st.altair_chart(chart, use_container_width=True)

        with col_chart2:
            st.subheader("📦 Riskli Paketler")
            top_packages = df["Paket"].value_counts().head(5)
            st.bar_chart(top_packages)

        st.subheader("🔍 Detaylı Analiz")
        
        f1, f2 = st.columns(2)
        with f1:
            sev_filter = st.multiselect("Seviye:", df["Ciddiyet"].unique(), default=["CRITICAL", "HIGH"])
        with f2:
            only_fixable = st.checkbox("Sadece Yaması Olanlar (Fixable)")
        
        filtered_df = df.copy()
        if sev_filter:
            filtered_df = filtered_df[filtered_df["Ciddiyet"].isin(sev_filter)]
        if only_fixable:
            filtered_df = filtered_df[filtered_df["Düzeltilmiş Sürüm"] != "Yama Yok ❌"]
        
        st.dataframe(
            filtered_df,
            use_container_width=True,
            column_config={
                "ID": st.column_config.TextColumn("CVE ID"),
                "Ciddiyet": st.column_config.TextColumn("Risk"),
                "Düzeltilmiş Sürüm": st.column_config.TextColumn("Çözüm"),
            },
            hide_index=True
        )

else:
    st.info("👈 Analize başlamak için sol taraftan bir imaj adı girin.")