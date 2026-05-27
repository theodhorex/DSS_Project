# Decision Tree - Penjelasan Lengkap

## 📚 Apa itu Decision Tree?

Decision Tree adalah model machine learning yang membuat keputusan dengan cara mirip seperti diagram alur atau pohon keputusan yang Anda lihat di kehidupan sehari-hari. Model ini mengajukan pertanyaan beruntun tentang data Anda dan berdasarkan jawaban, model akan terus menggali lebih dalam hingga mencapai kesimpulan akhir.

### Analogi Sederhana
Bayangkan Anda ingin menentukan apakah harus membawa payung:
1. **Pertanyaan pertama (Root):** "Apakah hari ini akan hujan?"
   - Jika YA → lanjut ke pertanyaan berikutnya
   - Jika TIDAK → Kesimpulan: Tidak perlu payung

2. **Pertanyaan kedua:** "Apakah Anda akan keluar rumah?"
   - Jika YA → Kesimpulan: Bawa payung
   - Jika TIDAK → Kesimpulan: Tidak perlu payung

Itulah cara kerja Decision Tree!

---

## 🌳 Struktur Decision Tree

### 1. **Root Node (Akar)**
- Node paling atas di tree
- Berisi pertanyaan/kondisi pertama yang paling penting untuk membedakan data
- Contoh: "Stress_Score <= 50.00?"
- Ini adalah fitur yang paling berpengaruh terhadap hasil prediksi

### 2. **Internal Nodes (Cabang)**
- Node-node di tengah tree
- Berisi pertanyaan-pertanyaan lanjutan berdasarkan jawaban sebelumnya
- Setiap internal node memiliki 2 cabang: kiri (TRUE/<=) dan kanan (FALSE/>)

### 3. **Leaf Nodes (Daun)**
- Node paling bawah di tree
- Berisi hasil prediksi akhir (contoh: "High", "Medium", "Low")
- Tidak ada pertanyaan lagi, hanya kesimpulan

### 4. **Split (Pembagian)**
- Proses membagi data berdasarkan kondisi tertentu
- Contoh: Membagi data berdasarkan "Stress_Score <= 50.00"
- Tujuan: Memisahkan data sehingga setiap kelompok lebih "murni" (homogen)

---

## 📊 Informasi di Setiap Node

Setiap node dalam tree menampilkan informasi berikut:

### Contoh Node:
```
Stress_Score <= 50.00
gini = 0.45
samples = 5000
value = [1500, 2000, 1500]
class = Medium
```

**Penjelasan:**
- **Stress_Score <= 50.00** → Kondisi/pertanyaan yang diajukan
- **gini = 0.45** → Gini impurity (ukuran kemurnian data di node ini, 0 = murni, 0.5 = tercampur)
- **samples = 5000** → Jumlah data training yang masuk ke node ini
- **value = [1500, 2000, 1500]** → Distribusi kelas (Low: 1500, Medium: 2000, High: 1500)
- **class = Medium** → Kelas yang paling dominan di node ini

### Warna Node:
- **Warna lebih gelap** = Kelas lebih dominan (model lebih yakin)
- **Warna lebih terang** = Kelas tercampur (model kurang yakin)

---

## 🎯 Cara Membaca Decision Tree

### Step-by-Step:

1. **Mulai dari Root Node (paling atas)**
   - Lihat kondisi di node tersebut
   - Contoh: "Stress_Score <= 50.00?"

2. **Cek apakah nilai Anda memenuhi kondisi**
   - Jika stress_score Anda = 65, apakah 65 <= 50? TIDAK (FALSE)
   - Jika stress_score Anda = 45, apakah 45 <= 50? YA (TRUE)

3. **Ikuti garis ke arah yang sesuai**
   - Jika TRUE/<=: ikuti garis ke **KIRI**
   - Jika FALSE/>: ikuti garis ke **KANAN**

4. **Ulangi proses sampai mencapai Leaf Node**
   - Leaf node adalah kotak paling bawah tanpa pertanyaan lagi
   - Nilai di leaf node adalah hasil prediksi Anda

### Contoh Walkthrough:

Misalkan Anda memiliki:
- Stress_Score = 65
- Anxiety_Score = 58
- Exam_Pressure = 7

**Alur di Tree Stress Level:**

```
Root: Stress_Score <= 50.00?
├─ 65 <= 50? TIDAK → Ke KANAN
│
├─ Node: Anxiety_Score <= 60.00?
│  ├─ 58 <= 60? YA → Ke KIRI
│  │
│  ├─ Node: Exam_Pressure <= 5.00?
│  │  ├─ 7 <= 5? TIDAK → Ke KANAN
│  │  │
│  │  └─ Leaf: HIGH (Hasil Prediksi)
```

**Kesimpulan:** Stress Level Anda = HIGH

---

## 🔍 Jalur Keputusan Anda

Di bawah setiap tree visual, ada section "Jalur Keputusan" yang menampilkan penjelasan tekstual dari alur yang Anda ikuti. Contoh:

```
1. Stress_Score <= 50.00 (value=65.00) -> right
2. Anxiety_Score <= 60.00 (value=58.00) -> left
3. Exam_Pressure <= 5.00 (value=7.00) -> right
```

**Penjelasan:**
- **Step 1:** Kondisi adalah "Stress_Score <= 50.00", nilai Anda adalah 65.00, arah adalah RIGHT (ke kanan)
- **Step 2:** Kondisi adalah "Anxiety_Score <= 60.00", nilai Anda adalah 58.00, arah adalah LEFT (ke kiri)
- **Step 3:** Kondisi adalah "Exam_Pressure <= 5.00", nilai Anda adalah 7.00, arah adalah RIGHT (ke kanan)

---

## 🎓 4 Decision Trees dalam Sistem Ini

Sistem DSS ini menggunakan **4 Decision Trees terpisah** untuk memprediksi 4 target berbeda:

### 1. **Tree Tingkat Stres (Stress Level)**
- **Target:** Low, Medium, High
- **Tujuan:** Memprediksi tingkat stres Anda
- **Fitur Penting:** Stress Score, Anxiety Score, Exam Pressure, Sleep Hours
- **Interpretasi:** Semakin tinggi stres, semakin banyak aktivitas yang perlu dikurangi

### 2. **Tree Tingkat Kecemasan (Anxiety Level)**
- **Target:** Low, Medium, High
- **Tujuan:** Memprediksi tingkat kecemasan Anda
- **Fitur Penting:** Anxiety Score, Heart Rate, Mood State, Sleep Hours
- **Interpretasi:** Kecemasan berbeda dengan stres - lebih fokus pada perasaan khawatir

### 3. **Tree Status Akhir (Final State)**
- **Target:** Relaxed, Neutral, Stress
- **Tujuan:** Memprediksi status kesehatan mental keseluruhan
- **Fitur Penting:** Kombinasi semua indikator
- **Interpretasi:** Kesimpulan holistik tentang kondisi psikologis Anda

### 4. **Tree Respons Intervensi (Intervention Response)**
- **Target:** Positive, Neutral, Negative
- **Tujuan:** Memprediksi apakah intervensi akan efektif
- **Fitur Penting:** Social Support, Mood State, Intervention Response History
- **Interpretasi:** Membantu menentukan strategi intervensi yang tepat

---

## ✅ Keuntungan Decision Tree

### Interpretability (Mudah Dipahami)
- Setiap keputusan dapat dijelaskan dengan logika sederhana
- Tidak seperti neural network yang "black box"
- Dosen dapat memahami alasan setiap prediksi

### Transparency (Transparan)
- Dapat menunjukkan alasan keputusan step-by-step
- Setiap fitur yang digunakan terlihat jelas
- Mudah untuk audit dan verifikasi

### No Special Preprocessing
- Tidak perlu normalisasi data khusus
- Dapat menangani missing values
- Cocok untuk data dengan banyak kategori

### Explainable AI
- Cocok untuk aplikasi yang membutuhkan penjelasan (healthcare, finance, education)
- Memenuhi persyaratan transparansi dan akuntabilitas

---

## ⚠️ Keterbatasan Decision Tree

### Overfitting
- Jika tree terlalu dalam, bisa belajar noise dari data training
- Solusi: Menggunakan max_depth dan min_samples_leaf untuk membatasi ukuran tree

### Bias terhadap Fitur Dominan
- Fitur yang sangat penting bisa mendominasi tree
- Fitur lain yang juga penting bisa diabaikan

### Instability
- Perubahan kecil di data training bisa menghasilkan tree yang sangat berbeda
- Solusi: Menggunakan ensemble methods seperti Random Forest

---

## 🔧 Hyperparameter Decision Tree dalam Sistem Ini

Sistem ini menggunakan DecisionTreeClassifier dari sklearn dengan konfigurasi:

```python
DecisionTreeClassifier(
    max_depth=10,              # Kedalaman maksimal tree
    min_samples_split=20,      # Minimum samples untuk split
    min_samples_leaf=10,       # Minimum samples di leaf node
    random_state=42            # Untuk reproducibility
)
```

**Penjelasan:**
- **max_depth=10:** Tree tidak boleh lebih dari 10 level (mencegah overfitting)
- **min_samples_split=20:** Hanya split jika ada minimal 20 samples (mencegah split yang terlalu spesifik)
- **min_samples_leaf=10:** Setiap leaf node harus punya minimal 10 samples (mencegah leaf yang terlalu kecil)
- **random_state=42:** Untuk memastikan hasil yang konsisten setiap kali dijalankan

---

## 📈 Proses Training Decision Tree

### 1. **Data Preparation**
- Dataset 10,000 mahasiswa dengan 15 indikator
- Split menjadi training (80%) dan testing (20%)
- Preprocessing: imputation, normalization, encoding

### 2. **Tree Building**
- Algoritma CART (Classification and Regression Trees)
- Setiap node mencari split terbaik yang meminimalkan Gini impurity
- Proses berlanjut sampai mencapai stopping criteria (max_depth, min_samples_split, dll)

### 3. **Pruning (Optional)**
- Menghapus branches yang tidak meningkatkan akurasi
- Mencegah overfitting

### 4. **Evaluation**
- Ditest dengan data testing
- Dihitung accuracy, precision, recall, F1-score
- Dibandingkan dengan baseline models

---

## 🎯 Cara Menggunakan Informasi Decision Tree

### Untuk Mahasiswa:
1. **Pahami jalur keputusan Anda** - Lihat step-by-step keputusan yang diambil model
2. **Identifikasi faktor kunci** - Mana indikator yang paling mempengaruhi hasil
3. **Ambil tindakan** - Fokus pada indikator yang paling berpengaruh untuk improvement

### Untuk Dosen:
1. **Verifikasi logika model** - Apakah keputusan tree masuk akal?
2. **Analisis pola** - Apa pola umum yang ditemukan model?
3. **Improve model** - Apakah ada fitur yang perlu ditambahkan/dihapus?

### Untuk Peneliti:
1. **Analisis feature importance** - Fitur mana yang paling penting?
2. **Interpretasi hasil** - Apa insight dari tree structure?
3. **Publikasi** - Gunakan untuk paper/thesis dengan penjelasan yang jelas

---

## 📚 Referensi

- Breiman, L., Friedman, J., Stone, C. J., & Olshen, R. A. (1984). Classification and Regression Trees.
- Scikit-learn Decision Tree Documentation: https://scikit-learn.org/stable/modules/tree.html
- Interpretable Machine Learning: https://christophm.github.io/interpretable-ml-book/

---

## 💡 Tips untuk Memahami Tree Lebih Baik

1. **Mulai dari Root Node** - Pahami pertanyaan pertama yang paling penting
2. **Ikuti alur Anda** - Trace jalur keputusan untuk data Anda sendiri
3. **Bandingkan dengan orang lain** - Lihat bagaimana jalur berbeda untuk data berbeda
4. **Cek Leaf Node** - Pahami distribusi kelas di leaf node (confidence)
5. **Baca Jalur Keputusan** - Gunakan penjelasan tekstual untuk pemahaman lebih mudah

---

## 🔗 Hubungan dengan Bagian Lain Sistem

- **Faktor Utama (Key Factors):** Menampilkan 4 langkah pertama dari jalur keputusan
- **Jalur Keputusan:** Penjelasan tekstual lengkap dari alur di tree
- **Probabilitas Prediksi:** Confidence score untuk setiap kelas di leaf node
- **Rekomendasi Aksi:** Tindakan praktis berdasarkan hasil prediksi tree

---

Semoga penjelasan ini membantu Anda memahami Decision Tree dengan lebih baik! 🎓
