# 1. Altyapı olarak Python 3.9'un hafif sürümünü (Slim) kullanıyoruz
FROM python:3.9-slim

# 2. Çalışma klasörünü oluştur
WORKDIR /app

# 3. Gerekli sistem araçlarını yükle (Curl, Trivy'yi indirmek için lazım)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. TRIVY KURULUMU (Linux versiyonu)
# Resmi script ile Trivy'yi indirip /usr/local/bin içine kuruyoruz.
# Böylece "PATH" sorunu asla yaşamayacağız.
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# 5. Python kütüphanelerini yükle
# requirements.txt ile uğraşmayalım, direkt buraya yazalım:
RUN pip install --no-cache-dir streamlit pandas altair

# 6. Proje dosyalarını (app.py vb.) kutunun içine kopyala
COPY . .

# 7. Streamlit'in kullandığı 8501 portunu dışarı aç
EXPOSE 8501

# 8. Konteyner çalıştığında ne yapsın?
# Streamlit uygulamasını başlat
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]