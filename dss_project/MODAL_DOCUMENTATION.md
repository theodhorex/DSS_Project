# Modal Detail Analisis Prediksi - Dokumentasi

## Overview
Hasil prediksi sekarang menampilkan card ringkas dengan button "Lihat Detail Analisis" yang membuka modal lengkap berisi:
1. Faktor Utama
2. Tahapan Preprocessing
3. Probabilitas Prediksi
4. Rekomendasi Aksi

Setiap section dilengkapi dengan penjelasan detail tentang sumber data dan cara interpretasinya.

---

## 1. Faktor Utama

### Apa Ini?
Faktor utama adalah langkah-langkah keputusan pertama yang diambil model Decision Tree berdasarkan input Anda. Ini menunjukkan kondisi mana yang paling mempengaruhi hasil prediksi tingkat stres.

### Sumber Data
Diekstrak dari decision path tree untuk target "Stress Level" dan "Final State" (maksimal 4 langkah pertama).

### Contoh
```
Stress_Score <= 50.00 (value=65.00) -> right
Anxiety_Score <= 60.00 (value=58.00) -> left
Exam_Pressure <= 5.00 (value=7.00) -> right
```

### Interpretasi
- Setiap baris menunjukkan kondisi yang dievaluasi
- `value=X` menunjukkan nilai input Anda
- `-> right/left` menunjukkan arah keputusan di tree

---

## 2. Tahapan Preprocessing

### Apa Ini?
Preprocessing adalah tahapan persiapan data sebelum masuk ke model machine learning.

### Tahapan:

#### Step 1: Input Values
- **Deskripsi:** Nilai-nilai mentah yang Anda input dari form
- **Contoh:**
  - stress_score: 65
  - anxiety_score: 58
  - exam_pressure: 7
  - dst...

#### Step 2: Feature Preprocessing
- **Deskripsi:** Data setelah melalui transformasi
- **Proses yang dilakukan:**
  1. **Imputation:** Mengisi missing values dengan median (numeric) atau most frequent (categorical)
  2. **Normalisasi:** Scaling data numeric jika diperlukan
  3. **Encoding:** Mengubah kategori (text) menjadi angka menggunakan OneHotEncoder
  
- **Contoh Output:**
  ```
  Stress_Score: 65.0000
  Anxiety_Score: 58.0000
  Exam_Pressure: 7.0000
  Sleep_Hours: 5.5000
  ... (dan features lainnya)
  ```

### Sumber Data
Diproses oleh sklearn ColumnTransformer dengan:
- SimpleImputer (untuk numeric dan categorical)
- OneHotEncoder (untuk kategori)

---

## 3. Probabilitas Prediksi

### Apa Ini?
Probabilitas prediksi menunjukkan tingkat keyakinan model untuk setiap kemungkinan output. Semakin tinggi persentase, semakin yakin model dengan prediksi tersebut.

### 4 Target Prediksi:

#### A. Tingkat Stres (Stress Level)
- **Kemungkinan Output:** Low, Medium, High
- **Penjelasan:** Semakin tinggi persentase "High", semakin besar kemungkinan Anda mengalami stres tinggi
- **Contoh:** High: 53%, Medium: 35%, Low: 12%
- **Interpretasi:** Model 53% yakin Anda mengalami stres tinggi

#### B. Tingkat Kecemasan (Anxiety Level)
- **Kemungkinan Output:** Low, Medium, High
- **Penjelasan:** Menunjukkan seberapa yakin model dengan prediksi level kecemasan
- **Contoh:** Medium: 45%, High: 40%, Low: 15%

#### C. Status Akhir (Final State)
- **Kemungkinan Output:** Relaxed, Neutral, Stress
- **Penjelasan:** Status kesehatan mental akhir Anda
- **Contoh:** Relaxed: 60%, Neutral: 30%, Stress: 10%

#### D. Respons Intervensi (Intervention Response)
- **Kemungkinan Output:** Positive, Neutral, Negative
- **Penjelasan:** Apakah intervensi akan memberikan efek positif, netral, atau negatif
- **Contoh:** Positive: 70%, Neutral: 20%, Negative: 10%

### Sumber Data
Dihitung dari `predict_proba()` method DecisionTreeClassifier untuk setiap target output.

### Cara Membaca Progress Bar
- **Panjang bar** = tingkat keyakinan (%)
- **Warna ungu** = probabilitas
- **Nilai di kanan** = persentase

---

## 4. Rekomendasi Aksi

### Apa Ini?
Rekomendasi aksi adalah saran tindakan praktis berdasarkan tingkat stres yang diprediksi.

### Berdasarkan Level Stres:

#### Low Stress
```
✓ Pertahankan rutinitas tidur dan olahraga yang sudah konsisten
✓ Jaga jadwal belajar agar tetap stabil tanpa lembur berlebihan
✓ Terus cek mood dan lakukan refleksi singkat tiap minggu
```

#### Medium Stress
```
✓ Atur ulang prioritas tugas agar beban tidak menumpuk
✓ Tambah sesi relaksasi singkat 10-15 menit setiap hari
✓ Cari dukungan sosial ketika mulai merasa kewalahan
```

#### High Stress
```
✓ Kurangi aktivitas non-prioritas dan fokus pada pemulihan
✓ Diskusikan beban akademik dengan dosen atau mentor
✓ Pertimbangkan konsultasi profesional jika gejala berlanjut
```

#### Critical Stress
```
✓ Segera cari dukungan profesional atau layanan konseling kampus
✓ Ambil jeda dari aktivitas berat untuk stabilisasi emosi
✓ Libatkan orang terdekat untuk pendampingan intensif
```

### Sumber Data
Berdasarkan mapping level stres ke ACTION_RECOMMENDATIONS yang telah ditentukan di script.js.

---

## UI/UX Features

### Button "Apa ini?"
Setiap section memiliki button "Apa ini?" yang bisa diklik untuk:
- Menampilkan penjelasan detail tentang section tersebut
- Menampilkan sumber data
- Menampilkan cara interpretasi

### Styling
- **Faktor Utama:** Background putih dengan border ink
- **Preprocessing:** Background biru (blue-50) untuk visual distinction
- **Probabilitas:** Background ungu (purple-50) dengan progress bar
- **Rekomendasi:** Background amber (amber-100) untuk highlight

### Modal Features
- **Scrollable:** Konten panjang bisa di-scroll
- **Closeable:** Bisa ditutup dengan button "Tutup" atau ESC key
- **Overlay:** Click di luar modal untuk menutup

---

## Technical Implementation

### Backend (Python)
```python
# Response structure
{
  "preprocessing_steps": [
    {
      "step": 1,
      "name": "Input Values",
      "description": "Raw input dari form",
      "data": { ... }
    },
    {
      "step": 2,
      "name": "Feature Preprocessing",
      "description": "Setelah normalisasi, imputation, dan encoding",
      "features": [...],
      "sample_values": [...]
    }
  ],
  "prediction_probabilities": {
    "stress_level": {
      "Low": 0.1234,
      "Medium": 0.3456,
      "High": 0.5310
    },
    ...
  }
}
```

### Frontend (JavaScript)
```javascript
// Render functions
- renderKeyFactorsModal()
- renderPreprocessingStepsModal()
- renderPredictionProbabilitiesModal()
- renderRecommendationsModal()
- setupDetailsModal()

// Toggle info buttons
[data-toggle-info] attribute untuk toggle penjelasan
```

---

## Files Modified

1. **templates/index.html**
   - Remove detail sections dari results card
   - Add "Lihat Detail Analisis" button
   - Add detailsModal dengan penjelasan lengkap

2. **static/js/script.js**
   - Add renderKeyFactorsModal()
   - Add renderPreprocessingStepsModal() dengan penjelasan
   - Add renderPredictionProbabilitiesModal() dengan penjelasan
   - Add renderRecommendationsModal()
   - Add setupDetailsModal() dengan toggle functionality
   - Update displayResults() untuk call modal render functions

3. **utils/predictor.py** (no changes needed)

4. **app.py** (no changes needed)

---

## Testing

Semua endpoint sudah ditest:
- ✅ Modal opens/closes correctly
- ✅ Toggle info buttons work
- ✅ All data renders correctly
- ✅ Responsive design works
- ✅ ESC key closes modal

---

## User Flow

1. User mengisi form dan klik "Prediksi Tingkat Stres"
2. Hasil prediksi ditampilkan di card ringkas dengan:
   - Stress level badge
   - Anxiety level badge
   - Final state
   - Recommendation
   - Confidence bar
   - Explanation
3. User klik "Lihat Detail Analisis" button
4. Modal terbuka menampilkan:
   - Faktor Utama (dengan penjelasan)
   - Tahapan Preprocessing (dengan penjelasan detail)
   - Probabilitas Prediksi (dengan penjelasan untuk setiap target)
   - Rekomendasi Aksi (dengan penjelasan detail)
5. User bisa klik "Apa ini?" untuk toggle penjelasan
6. User bisa close modal dengan button atau ESC key

---

## Keuntungan Design Ini

✅ **Clean UI:** Card hasil prediksi tidak overcrowded
✅ **Detailed Info:** Semua detail ada di modal yang bisa diakses
✅ **Transparent:** Penjelasan lengkap untuk setiap elemen
✅ **Educational:** User bisa belajar tentang proses prediksi
✅ **Accessible:** Toggle buttons untuk show/hide penjelasan
✅ **Responsive:** Works well di mobile dan desktop
