# 1. GÜNCELLEME: 'slim' yerine daha yeni ve güvenli olan 'slim-bookworm' (Debian 12) sürümünü kullanıyoruz.
FROM python:3.9-slim-bookworm

# 2. Çalışma klasörünü oluştur
WORKDIR /app

# 3. KRİTİK GÜNCELLEME:
# apt-get upgrade -y komutunu ekledik. Bu, imaj oluşturulurken linux paketlerini son sürüme çeker ve açıkları kapatır.
# Curl'ü de yine Trivy indirmek için kuruyoruz.
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# 4. TRIVY KURULUMU (Senin uygulaman bunu kullandığı için KALMALI)
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# 5. Python kütüphanelerini yükle
RUN pip install --no-cache-dir streamlit pandas altair

# 6. Proje dosyalarını kopyala
COPY . .

# 7. Portu dışarı aç
EXPOSE 8501

# 8. Başlat
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]