# README - Penjelasan Decision Tree untuk Dosen

Dokumen ini adalah ringkasan lengkap tentang Decision Tree dalam sistem DSS Student Stress Prediction.

## 📚 File-File Dokumentasi

### 1. **DECISION_TREE_EXPLANATION.md**
Penjelasan konseptual tentang Decision Tree:
- Apa itu Decision Tree
- Bagaimana cara kerjanya
- Struktur tree (root, internal, leaf nodes)
- Keuntungan dan keterbatasan
- Hyperparameter yang digunakan
- Proses training

**Untuk siapa:** Dosen, mahasiswa, atau siapa saja yang ingin memahami konsep Decision Tree secara mendalam.

### 2. **DECISION_TREE_VISUAL_GUIDE.md**
Panduan cara membaca diagram Decision Tree secara visual:
- Elemen visual (kotak, garis, warna)
- Informasi di setiap node (kondisi, gini, samples, value, class)
- Contoh walkthrough lengkap
- Interpretasi hasil di leaf node
- Tips membaca tree secara efisien

**Untuk siapa:** Mahasiswa atau dosen yang ingin memahami cara membaca visual tree diagram.

### 3. **SYSTEM_INTEGRATION_GUIDE.md**
Integrasi lengkap dari input hingga prediksi:
- Alur lengkap sistem (input → preprocessing → inference → output)
- Komponen-komponen utama
- Preprocessing pipeline
- Decision tree inference untuk 4 targets
- Hasil prediksi dan analisis
- Tampilan di interface
- Contoh kasus lengkap

**Untuk siapa:** Dosen yang ingin memahami sistem secara holistik dan bagaimana semua komponen bekerja bersama.

### 4. **MODAL_DOCUMENTATION.md**
Dokumentasi tentang modal yang menampilkan detail analisis:
- Overview modal
- 4 section di modal (Faktor Utama, Preprocessing, Probabilitas, Rekomendasi)
- UI/UX features
- Technical implementation

**Untuk siapa:** Developer atau dosen yang ingin memahami implementasi frontend.

### 5. **BACKEND_ANALYSIS.md**
Analisis dan perbaikan backend:
- Masalah yang ditemukan dan diperbaiki
- Response structure
- Files modified
- Testing results

**Untuk siapa:** Developer atau dosen yang ingin memahami backend implementation.

---

## 🎯 Penjelasan Decision Tree di Interface

### 1. **Modal Details (Klik "Lihat Detail Analisis")**

#### Section: Penjelasan Decision Tree
Menampilkan:
- Apa itu Decision Tree
- Bagaimana cara kerjanya
- Keuntungan Decision Tree
- Dalam sistem ini ada 4 Decision Trees
- Tips membaca tree

#### Section: Faktor Utama
Menampilkan:
- 4 langkah pertama dari jalur keputusan
- Penjelasan tentang sumber data
- Cara interpretasi

#### Section: Tahapan Preprocessing
Menampilkan:
- Step 1: Input Values (nilai mentah dari form)
- Step 2: Feature Preprocessing (setelah transformasi)
- Penjelasan tentang proses preprocessing

#### Section: Probabilitas Prediksi
Menampilkan:
- Confidence score untuk setiap target
- Progress bar visual
- Penjelasan tentang cara membaca probabilitas

#### Section: Rekomendasi Aksi
Menampilkan:
- Saran tindakan berdasarkan stress level
- Penjelasan tentang setiap level

### 2. **Decision Tree Visualization (Tab "Decision Tree")**

#### Panduan Membaca Tree
Menampilkan:
- Cara membaca Decision Tree
- Struktur tree
- Informasi di setiap node
- Cara mengikuti alur

#### Visual Tree Diagram
Menampilkan:
- Diagram pohon yang dirender dari Graphviz
- Warna node menunjukkan kelas dominan
- Garis menunjukkan arah keputusan

#### Jalur Keputusan
Menampilkan:
- Step-by-step keputusan untuk data Anda
- Format tekstual yang mudah dibaca
- Penjelasan tentang setiap step

---

## 🔍 Cara Dosen Memahami Decision Tree

### Step 1: Pahami Konsep Dasar
Baca **DECISION_TREE_EXPLANATION.md** untuk memahami:
- Apa itu Decision Tree
- Bagaimana cara kerjanya
- Keuntungan dan keterbatasan

### Step 2: Pahami Visual Tree
Baca **DECISION_TREE_VISUAL_GUIDE.md** untuk memahami:
- Elemen visual (kotak, garis, warna)
- Informasi di setiap node
- Cara membaca tree diagram

### Step 3: Pahami Sistem Secara Keseluruhan
Baca **SYSTEM_INTEGRATION_GUIDE.md** untuk memahami:
- Alur lengkap dari input hingga output
- Bagaimana preprocessing bekerja
- Bagaimana 4 trees bekerja bersama
- Contoh kasus lengkap

### Step 4: Coba Sendiri
1. Buka aplikasi di http://localhost:5000
2. Isi form dengan data mahasiswa
3. Klik "Prediksi Tingkat Stres"
4. Klik "Lihat Detail Analisis" untuk melihat modal
5. Buka tab "Decision Tree" untuk melihat diagram
6. Ikuti jalur keputusan sesuai dengan data yang Anda input
7. Verifikasi apakah hasil prediksi masuk akal

---

## 💡 Pertanyaan yang Sering Diajukan

### Q1: Bagaimana cara membaca tree diagram?
**A:** Lihat **DECISION_TREE_VISUAL_GUIDE.md** bagian "Membaca Informasi di Node" dan "Contoh Walkthrough Lengkap".

### Q2: Apa arti gini impurity?
**A:** Ukuran "kemurnian" data di node. Gini = 0 berarti murni (semua data 1 kelas), Gini = 0.5 berarti tercampur (semua kelas sama banyak).

### Q3: Bagaimana cara mengetahui confidence prediksi?
**A:** Lihat "Probabilitas Prediksi" di modal atau di leaf node tree. Confidence = jumlah samples kelas dominan / total samples di leaf node.

### Q4: Mengapa ada 4 Decision Trees?
**A:** Karena ada 4 target prediksi berbeda: Stress Level, Anxiety Level, Final State, dan Intervention Response. Setiap target membutuhkan tree terpisah.

### Q5: Apakah tree bisa overfitting?
**A:** Ya, tapi sistem ini menggunakan hyperparameter untuk mencegahnya: max_depth=10, min_samples_split=20, min_samples_leaf=10.

### Q6: Bagaimana cara verifikasi akurasi model?
**A:** Lihat confidence score untuk setiap prediksi. Confidence tinggi (>80%) berarti model yakin. Jika confidence rendah (<50%), hasil prediksi kurang reliable.

### Q7: Apakah hasil prediksi bisa dijelaskan?
**A:** Ya! Setiap prediksi memiliki "Jalur Keputusan" yang menunjukkan step-by-step alasan mengapa model memberikan prediksi tersebut.

---

## 📊 Struktur Decision Tree dalam Sistem

### Tree 1: Stress Level
- **Input:** 27 features (12 numeric + 15 one-hot encoded)
- **Output:** Low, Medium, High
- **Root Node:** Biasanya Stress_Score atau Anxiety_Score
- **Kedalaman:** Max 10 levels
- **Samples:** 10,000 data training

### Tree 2: Anxiety Level
- **Input:** 27 features
- **Output:** Low, Medium, High
- **Root Node:** Biasanya Anxiety_Score atau Heart_Rate
- **Kedalaman:** Max 10 levels
- **Samples:** 10,000 data training

### Tree 3: Final State
- **Input:** 27 features
- **Output:** Relaxed, Neutral, Stress
- **Root Node:** Kombinasi dari multiple features
- **Kedalaman:** Max 10 levels
- **Samples:** 10,000 data training

### Tree 4: Intervention Response
- **Input:** 27 features
- **Output:** Positive, Neutral, Negative
- **Root Node:** Biasanya Social_Support atau Intervention_Response
- **Kedalaman:** Max 10 levels
- **Samples:** 10,000 data training

---

## 🔧 Hyperparameter Decision Tree

```python
DecisionTreeClassifier(
    max_depth=10,              # Kedalaman maksimal
    min_samples_split=20,      # Minimum untuk split
    min_samples_leaf=10,       # Minimum di leaf
    random_state=42            # Reproducibility
)
```

**Penjelasan:**
- **max_depth=10:** Mencegah tree terlalu dalam (overfitting)
- **min_samples_split=20:** Mencegah split yang terlalu spesifik
- **min_samples_leaf=10:** Memastikan leaf node punya cukup data
- **random_state=42:** Hasil konsisten setiap kali dijalankan

---

## 📈 Metrik Evaluasi

Sistem menggunakan metrik berikut untuk evaluasi:
- **Accuracy:** Persentase prediksi yang benar
- **Precision:** Dari yang diprediksi positif, berapa yang benar
- **Recall:** Dari yang sebenarnya positif, berapa yang terdeteksi
- **F1-Score:** Harmonic mean dari precision dan recall

---

## 🎓 Untuk Keperluan Akademik

### Untuk Skripsi/Thesis
Gunakan dokumentasi ini untuk menjelaskan:
1. **Metodologi:** Gunakan Decision Tree karena interpretable
2. **Implementasi:** Gunakan hyperparameter yang sudah ditentukan
3. **Hasil:** Tampilkan tree diagram dan jalur keputusan
4. **Analisis:** Analisis feature importance dan pola yang ditemukan

### Untuk Paper/Publikasi
Highlight:
1. **Transparansi:** Decision Tree mudah dijelaskan
2. **Akurasi:** Confidence score untuk setiap prediksi
3. **Interpretability:** Setiap keputusan dapat dijelaskan
4. **Praktikalitas:** Dapat digunakan untuk real-world application

---

## 🔗 Referensi Cepat

| Topik | File | Bagian |
|-------|------|--------|
| Konsep Decision Tree | DECISION_TREE_EXPLANATION.md | Apa itu Decision Tree |
| Cara membaca tree | DECISION_TREE_VISUAL_GUIDE.md | Membaca Informasi di Node |
| Alur sistem | SYSTEM_INTEGRATION_GUIDE.md | Alur Lengkap Sistem |
| Gini impurity | DECISION_TREE_EXPLANATION.md | Struktur Decision Tree |
| Confidence score | DECISION_TREE_VISUAL_GUIDE.md | Interpretasi Hasil di Leaf Node |
| Hyperparameter | DECISION_TREE_EXPLANATION.md | Hyperparameter Decision Tree |
| Contoh lengkap | SYSTEM_INTEGRATION_GUIDE.md | Contoh Kasus Lengkap |

---

## ✅ Checklist untuk Dosen

- [ ] Baca DECISION_TREE_EXPLANATION.md
- [ ] Baca DECISION_TREE_VISUAL_GUIDE.md
- [ ] Baca SYSTEM_INTEGRATION_GUIDE.md
- [ ] Buka aplikasi dan isi form
- [ ] Klik "Lihat Detail Analisis" dan baca modal
- [ ] Buka tab "Decision Tree" dan lihat diagram
- [ ] Ikuti jalur keputusan sesuai data Anda
- [ ] Verifikasi hasil prediksi dengan domain knowledge
- [ ] Coba dengan data berbeda untuk melihat pola
- [ ] Analisis feature importance dari root node

---

Semoga dokumentasi ini membantu Anda memahami Decision Tree dalam sistem DSS! 🎓

Jika ada pertanyaan atau butuh klarifikasi lebih lanjut, silakan hubungi developer atau baca dokumentasi yang relevan.
