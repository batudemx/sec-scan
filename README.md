# DevSecOps Pipeline: Otomatik, Güvenli ve Kesintisiz Dağıtım Mimarisi

Bu proje, modern yazılım geliştirme süreçlerinde **hız** ve **güvenliği** bir araya getiren uçtan uca bir DevSecOps boru hattı (pipeline) uygulamasıdır. Geliştirilen mimari sayesinde, koddaki değişiklikler otomatik olarak derlenir, güvenlik zafiyetlerine karşı taranır ve AWS bulut altyapısı üzerindeki Kubernetes (K3s) kümesinde **sıfır kesinti (zero-downtime)** ile canlıya alınır.

##  Projenin Temel Özellikleri

* **Sola Kaydırılmış Güvenlik:** Kodu canlıya almadan önce Trivy ile CI/CD hattında otomatik zafiyet (CVE) taraması.
* **Kesintisiz Dağıtım :** Kubernetes'in "Rolling Update" stratejisi sayesinde, uygulama güncellenirken kullanıcı tarafında hiçbir erişim kesintisi yaşanmaz. Eski podlar, yenileri tamamen hazır olana kadar hizmet vermeye devam eder.
* **Tam Otomasyon:** GitHub Actions ile tetiklenen otonom süreç; manuel sunucu yapılandırması ve FTP/SSH ile dosya taşıma devrini bitirir.
* **Hafif ve Performanslı Altyapı:** Edge ve IoT cihazları için optimize edilmiş K3s (Lightweight Kubernetes) kullanılarak AWS EC2 üzerinde minimum kaynak tüketimi sağlanmıştır.

## Kullanılan Teknolojiler

* **Bulut Sağlayıcı:** AWS (EC2)
* **Konteynerizasyon:** Docker, Docker Hub
* **Orkestrasyon:** Kubernetes (K3s)
* **CI/CD Otomasyonu:** GitHub Actions
* **Güvenlik Taraması:** Aqua Security Trivy
* **Arayüz (Frontend):** Python tabanlı Streamlit SPA

##  Sistem Mimarisi ve İş Akışı

Sistem, bir geliştiricinin `main` dalına kod göndermesiyle (push) tetiklenir ve aşağıdaki adımları otonom olarak gerçekleştirir:

1.  **Build (Derleme):** Yeni Docker imajı oluşturulur.
2.  **Scan (Güvenlik Taraması):** Trivy, imajı işletim sistemi ve kütüphane seviyesindeki kritik açıklara karşı tarar.
3.  **Push (Kayıt):** Güvenlik onayından geçen imaj Docker Hub'a yüklenir.
4.  **Deploy (Dağıtım):** GitHub Actions, AWS sunucusuna SSH ile bağlanarak Kubernetes'e `rollout restart` komutunu gönderir. K3s, yeni imajı çeker ve kesintisiz geçişi başlatır.

> **Sistem Akış Şeması:**
<img width="797" height="460" alt="image" src="https://github.com/user-attachments/assets/dae3381e-50b8-456a-a931-82f2d8c1a67a" />


## Performans ve Sonuçlar

Geleneksel (manuel) dağıtım yöntemleriyle karşılaştırıldığında bu proje;
* Ortalama dağıtım süresini **15 dakikadan ~3 dakikaya** düşürmüş (%500 hız artışı),
* Servis kesinti süresini (Downtime) **sıfır (0)** saniyeye indirmiştir.

### Kesintisiz Dağıtım Kanıtı (Rolling Update in Action)
<img width="822" height="350" alt="image" src="https://github.com/user-attachments/assets/d60d48de-8ac0-48a6-984f-519326490828" />




