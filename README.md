# pdfjsonl
Bu Python kodu, PDF dosyalarını okuyarak içeriklerini JSONL formatına çeviren asenkron ve çok iş parçacıklı (multithreaded) bir uygulamadır. Tkinter kullanılarak bir grafik arayüz (GUI) sağlanır ve kullanıcı birden fazla PDF dosyası seçip JSONL dosyası oluşturabilir.
Bu kod, PDF dosyalarını JSONL formatına çevirme işlemi sırasında gelişmiş metin işleme ve hata yönetimi özelliklerine sahiptir. İşte detayları:

1️⃣ Tkinter ile Kullanıcı Arayüzü (GUI)

✔ PDF dosyalarını seçmek ve işlemek için grafiksel arayüz sunar.

✔ Kullanıcılar, düğmelere tıklayarak işlem yapabilir.

✔ İlerleme durumu yüzde olarak gösterilir.

✔ İşlem tamamlandığında bilgilendirme mesajları görüntülenir.

2️⃣ PDF'den Metin Çıkarma (PyPDF2)

✔ PyPDF2 kütüphanesi kullanılarak PDF içerisindeki metinler okunur.

✔ PDF sayfalarında metin olup olmadığı kontrol edilir, eksik sayfalara [UYARI: Sayfa okunamadı] eklenir.

✔ PDF hataları yönetilir, böylece okuma hataları uygulamayı durdurmaz.

3️⃣ Cümle Bazlı Ayrıştırma

✔ Metinler cümle bazlı olarak JSONL formatına ayrılır.

✔ Regex (RegEx) ile noktalama işaretlerine göre cümleler bölünür (.? gibi işaretlerden sonra bölme yapılır).

✔ Çok kısa (2 karakterden küçük) veya sadece noktalama içeren cümleler filtrelenir (örneğin ".", "!", "?" gibi girdiler çıkartılır).

4️⃣ Unicode Karakter Temizleme (Hata Önleme)

✔ Hatalı veya geçersiz Unicode karakterleri kaldırılır (\ud835 gibi hatalar temizlenir).

✔ unicodedata modülü ile geçersiz ve surrogate karakterler temizlenir.

✔ JSON kaydetme sırasında UTF-8 hatalarını önlemek için errors="ignore" seçeneği kullanılır.

5️⃣ JSONL Formatında Kaydetme

✔ JSONL (JSON Lines) formatında her satır, ayrı bir JSON nesnesi olarak kaydedilir.

✔ Veriler satır satır kaydedildiği için büyük dosyalarda daha verimli çalışır.

6️⃣ Asenkron ve Çok İş Parçacıklı Çalışma (Hızlı İşleme)

✔ Asenkron (async) ve multithreading desteğiyle aynı anda birden fazla PDF işleyebilir.

✔ ThreadPoolExecutor(max_workers=5) kullanarak 5 farklı PDF dosyası eşzamanlı işlenebilir.

✔ asyncio kullanımı sayesinde işlem ana programı kilitlemeden çalışır.

Kullanım Senaryoları

Bu kod, özellikle aşağıdaki durumlar için ideal bir çözümdür:

📌 Makine Öğrenimi (NLP) için Eğitim Verisi Hazırlama → PDF kitaplarından, makalelerden veya raporlardan veri çıkarıp JSONL formatında model eğitiminde kullanabilirsiniz.

📌 Akademik ve Araştırma Çalışmaları → PDF belgelerindeki bilgileri temizleyerek analiz için uygun hale getirebilirsiniz.

📌 Büyük Ölçekli Metin Analizi → PDF'lerden büyük miktarda veri çıkarıp, Python ile analiz veya duygu analizi yapabilirsiniz.

📌 Veri Seti Temizleme ve Formatlama → Bozuk veya yanlış karakterleri otomatik olarak temizleyen bir sistemdir.

Bu kodun sıfırdan çalışabilmesi için Python ortamını hazırlamanız ve gerekli bağımlılıkları yüklemeniz gerekiyor. 
python converter.py ile çalıştırabilirsiniz.

pyinstaller --onefile --noconsole --icon=app.ico converter.py ile exe çıktısı alıp çalıştırabilirsiniz.

