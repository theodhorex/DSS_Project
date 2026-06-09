# DSS Project — Student Stress Prediction

<p align="center">
  <img src="logo.png" alt="DSS Project Logo" width="200">
</p>

Sistem Pendukung Keputusan (Decision Support System) untuk memprediksi tingkat stres mahasiswa menggunakan Decision Tree. Dibangun dengan **Flask + scikit-learn + Tailwind CSS + vanilla JS**.

Memprediksi 4 output target dari 13 input indikator psikologis, akademik, fisik, dan sosial. Dilengkapi visualisasi pohon keputusan (Graphviz DOT), decision path step-by-step, probabilitas per kelas, dan rekomendasi aksi.

---

## Daftar Isi

- [Arsitektur](#arsitektur)
- [13 Input Features](#13-input-features)
- [4 Output Targets](#4-output-targets)
- [Setup](#setup)
- [Training Model](#training-model)
- [Menjalankan Server](#menjalankan-server)
- [API Endpoints](#api-endpoints)
- [Frontend](#frontend)
- [Testing](#testing)
- [Encoding Pipeline](#encoding-pipeline)
- [Feature Importance](#feature-importance)
- [Akurasi Model](#akurasi-model)
- [Cara Membaca Decision Tree](#cara-membaca-decision-tree)
- [Troubleshooting](#troubleshooting)

---

## Arsitektur

```
dss_project/
├── app.py                     # Flask API (routes, validasi, CORS)
├── train_model.py             # Training pipeline, encoding, CV
├── model.pkl                  # Trained model (4 trees)
├── input_sendiri.py           # CLI interaktif test prediksi
├── test_all.py                # Test suite otomatis (72 cases)
├── test_dummy.py              # Dummy test cepat
├── requirements.txt           # Dependencies
├── README.md
│
├── templates/
│   └── index.html             # Frontend form + tree viz + modal detail
│
├── static/
│   ├── css/
│   │   └── style.css          # Custom CSS (tree grid, dropdown, reveal anim)
│   └── js/
│       └── script.js          # Form stepper, validation, tree render, API calls
│
└── utils/
    ├── __init__.py
    └── predictor.py           # Predictor class: prediksi, decision path, DOT, feature importance
```

### Peran setiap file

| File | Fungsi |
|------|--------|
| `app.py` | Routes Flask, validasi payload, serve frontend & API |
| `train_model.py` | Baca dataset, pipeline preprocessing, train 4 trees, simpan model.pkl |
| `utils/predictor.py` | Load model, prediksi, format decision path, export DOT, feature importance |
| `templates/index.html` | Halaman utama (861 baris): form 4-step, hasil prediksi, tree viz, modal detail |
| `static/js/script.js` | 1341 baris: stepper, dropdown, validasi frontend, render tree, animasi reveal |
| `static/css/style.css` | 409 baris: brutalist design, tree grid, dropdown, scrollbar kustom |

---

## 13 Input Features

Form terdiri dari 4 langkah (step), total 13 indikator:

### Step 1 — Metrik Psikologis (2 indikator)

| Field | Label | Tipe | Range |
|-------|-------|------|-------|
| reward_score | Apresiasi Diri | slider (step 0.5) | 0 – 10 |
| mood_state | Kondisi Mood | dropdown | Calm / Neutral / Tense / Fatigued |

### Step 2 — Indikator Akademik (4 indikator)

| Field | Label | Tipe | Range |
|-------|-------|------|-------|
| exam_pressure | Tekanan Ujian | number | 0 – 10 |
| assignment_load | Beban Tugas | number | 0 – 10 |
| study_hours | Jam Belajar | number (step 0.5) | 0 – 24 |
| attendance | Kehadiran | slider | 0 – 100 |

### Step 3 — Kesehatan Fisik (4 indikator)

| Field | Label | Tipe | Range |
|-------|-------|------|-------|
| sleep_hours | Jam Tidur | number (step 0.5) | 0 – 24 |
| heart_rate | Detak Jantung | number | 40 – 200 |
| physical_activity | Aktivitas Fisik | number | 0 – 10 |
| screen_time | Screen Time | number (step 0.5) | 0 – 24 |

### Step 4 — Sosial & Perilaku (3 indikator)

| Field | Label | Tipe | Range |
|-------|-------|------|-------|
| social_support | Dukungan Sekitar | number | 0 – 10 |
| facial_emotion | Ekspresi Wajah | dropdown | Neutral / Happy / Sad / Angry / Surprised |
| caffeine_intake | Konsumsi Kafein | slider (step 0.5) | 0 – 10 |

---

## 4 Output Targets

| Target | Kelas Output | Contoh Decision Path |
|--------|-------------|---------------------|
| **stress_level** | Low / Medium / High | `Mood_State <= 0.50 (value=2.00 -> Tense) -> right` |
| **anxiety_level** | Low / Medium / High | `Exam_Pressure <= 7.50 (value=8.00) -> right` |
| **final_state** | Relaxed / Neutral / Stress | `Reward_Score <= 6.50 (value=2.00) -> left` |
| **intervention_response** | Positive / Neutral / Negative | `Mood_State <= 1.50 (value=2.00 -> Tense) -> right` |

---

## Setup

### 1. Clone & virtual environment

```bash
cd dss_project
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Linux/Mac
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Dependencies utama:
- `flask`, `flask-cors` — web server
- `scikit-learn` — DecisionTreeClassifier, MultiOutputClassifier, pipeline
- `pandas`, `numpy`, `joblib` — data processing & model serialization
- `requests` — testing

### 3. Dataset

Letakkan dataset di root project. Nama file yang didukung:
- `dataset.csv`
- `psychological_regulation_dataset.csv`

Kolom yang harus ada: 13 feature columns + 4 target columns (Stress_Level, Anxiety_Level, Final_State, Intervention_Response).

Jika kolom `Intervention_Response` tidak ada tapi ada `Previous_Intervention`, training script akan otomatis menggunakan `Previous_Intervention` sebagai fallback.

---

## Training Model

```bash
python train_model.py
```

### Proses training:

1. **Load dataset** — deteksi otomatis file CSV yang tersedia
2. **Split features** — numeric (11), ordinal (Mood_State), one-hot (Facial_Emotion)
3. **Pipeline** — ColumnTransformer → MultiOutputClassifier(DecisionTreeClassifier)
4. **Train-test split** — 70:30, stratify pada Stress_Level
5. **5-fold cross validation** — akurasi per target
6. **Evaluasi** — accuracy, classification report per target
7. **Export rules** — top decision rules dari tiap tree
8. **Save model** — `model.pkl`

### Parameter Decision Tree

| Parameter | Nilai | Alasan |
|-----------|-------|--------|
| max_depth | 4 | Cukup dalam untuk akurasi tinggi, mudah divisualisasikan |
| min_samples_split | 20 | Mencegah overfitting ke noise |
| min_samples_leaf | 10 | Leaf node minimal 10 sampel — lebih generalizable |
| random_state | 42 | Reproducible |

---

## Menjalankan Server

```bash
python app.py
```

Server berjalan di `http://localhost:5000` dengan debug mode.

Flask otomatis reload saat ada perubahan kode. Untuk production, nonaktifkan `debug=True`.

---

## API Endpoints

### `GET /` — Halaman utama

Render `templates/index.html`.

### `GET /health` — Status server

```json
{"model_loaded": true, "status": "healthy"}
```

### `POST /predict` — Prediksi utama

**Request body** (JSON, semua field wajib):

```json
{
  "exam_pressure": 2,
  "assignment_load": 2,
  "study_hours": 3,
  "attendance": 90,
  "sleep_hours": 8,
  "heart_rate": 70,
  "physical_activity": 7,
  "screen_time": 3,
  "caffeine_intake": 1,
  "social_support": 8,
  "reward_score": 8,
  "facial_emotion": "Happy",
  "mood_state": "Calm"
}
```

**Response:**

```json
{
  "success": true,
  "predictions": {
    "stress_level": "Low",
    "anxiety_level": "Low",
    "final_state": "Relaxed",
    "intervention_response": "Neutral"
  },
  "confidence": 0.99,
  "explanation": "Kondisi stres terpantau rendah. ...",
  "decision_paths": {
    "stress_level": [
      "Mood_State <= 0.50 (value=0.00 -> Calm) -> left"
    ],
    "anxiety_level": [...],
    "final_state": [...],
    "intervention_response": [...]
  },
  "preprocessing_steps": [...],
  "prediction_probabilities": {
    "stress_level": {"Low": 0.85, "Medium": 0.12, "High": 0.03},
    ...
  }
}
```

### `GET /tree` — DOT strings untuk visualisasi

Mengembalikan 4 DOT string (format Graphviz) untuk dirender di frontend via Viz.js atau fallback grid.

### `GET /feature-importance` — Feature importance

Feature importance per target:

```json
{
  "success": true,
  "feature_importances": {
    "stress_level": {
      "Mood_State (0=Calm,1=Neutral,2=Tense,3=Fatigued)": 0.9518,
      "Exam_Pressure": 0.0481
    },
    "anxiety_level": {
      "Exam_Pressure": 0.6590,
      "Social_Support": 0.3076,
      ...
    },
    ...
  }
}
```

### `GET /dataset-preview` — Preview dataset

20 baris pertama + metadata.

---

## Frontend

### Form Stepper (4 langkah)

Navigasi step-by-step dengan:
- **Step indicator** — dot buttons di atas form
- **Progress bar** — visual progress 25%/50%/75%/100%
- **Validasi per step** — tidak bisa lanjut jika ada field kosong/invalid
- **Tombol** — Kembali / Lanjut / Prediksi Tingkat Stres

### Hasil Prediksi

Setelah submit, ditampilkan:
1. **Badge** — Stress Level & Anxiety Level dengan warna (hijau/kuning/oranye/merah)
2. **Final State** — status akhir kesehatan mental
3. **Rekomendasi Intervensi** — saran aksi
4. **Confidence Bar** — tingkat keyakinan model
5. **Explanation** — penjelasan naratif Bahasa Indonesia

### Visualisasi Pohon Keputusan

4 tab (Stress, Kecemasan, Status Akhir, Intervensi):
- **Tree diagram** — dirender via Viz.js (SVG) dengan fallback grid layout
- **Node warna** — split condition = biru monospace, leaf node = hijau
- **Jalur keputusan** — step-by-step dalam bentuk teks
- **Help box** — cara membaca decision tree

### Modal Detail Analisis

Berisi 5 panel:
1. **Penjelasan Decision Tree** — teori & cara kerja
2. **Faktor Utama** — decision path untuk input Anda
3. **Tahapan Preprocessing** — transformasi data (input mentah → encoded)
4. **Probabilitas Prediksi** — distribusi keyakinan per kelas
5. **Rekomendasi Aksi** — saran berdasarkan level stres

### Panduan Cepat

Sidebar dengan instruksi singkat penggunaan.

---

## Testing

### Test Suite Otomatis (72 test cases)

```bash
python test_all.py
```

Mencakup:
- **Happy path** — low stress, high stress, medium, all min, all max (TC01–05)
- **Boundary Value Analysis** — setiap field di min/max/bawah/atas (TC06–09)
- **Negative cases** — field hilang, nilai invalid, string di numerik (TC10–14)
- **Edge cases** — stres ekstrem, rileks ekstrem, tidur 0, kombinasi kategorikal, dll (TC15–24)

Output: `72 PASS / 0 FAIL out of 72 tests`.

### Input Interaktif

```bash
python input_sendiri.py
```

Isi nilai tiap field manual, lihat hasil prediksi + decision path + probabilitas. Bisa input ulang tanpa restart.

### Dummy Test Cepat

```bash
python test_dummy.py
```

Test dengan 2 profil (low & high stress) yang sudah divalidasi.

---

## Encoding Pipeline

Detail preprocessing di `train_model.py`:

```
ColumnTransformer
├── num:   SimpleImputer(median)    → 11 numeric features
├── cat_ordinal: OrdinalEncoder      → Mood_State (Calm=0, Neutral=1, Tense=2, Fatigued=3)
└── cat_onehot: OneHotEncoder        → Facial_Emotion (5 binary columns)
```

### Mengapa OrdinalEncoder untuk Mood_State?

Mood_State memiliki urutan psikologis yang jelas:
- **Calm** (0) → tingkat stres terendah
- **Neutral** (1) → baseline
- **Tense** (2) → tingkat stres meningkat
- **Fatigued** (3) → kelelahan, stres tinggi

Dengan ordinal encoding, tree dapat membuat split bermakna seperti `Mood_State <= 1.50` (batas Neutral/Tense). One-hot encoding sebelumnya membuat tiap kategori terpisah tanpa urutan, sehingga tree kehilangan informasi ordinal.

### Threshold 0.5 / 1.5 / 2.5 pada Mood_State

Threshold ini adalah **batas antar kategori**:
- `<= 0.50` → Calm (Low stress)
- `0.50 < x <= 1.50` → Neutral (Medium stress)
- `1.50 < x <= 2.50` → Tense (High stress)
- `> 2.50` → Fatigued (Medium stress — berdasarkan data training)

---

## Feature Importance

### Stress Level

| Fitur | Importance |
|-------|-----------|
| Mood_State | 0.9518 |
| Exam_Pressure | 0.0481 |

Mood_State mendominasi karena ordinal encoding memberikan informasi kategorikal yang kuat untuk memisahkan level stres.

### Anxiety Level

| Fitur | Importance | Justifikasi |
|-------|-----------|-------------|
| Exam_Pressure | 0.6590 | Tekanan ujian adalah pemicu kecemasan antisipatif terkuat |
| Social_Support | 0.3076 | Dukungan sosial rendah meningkatkan persepsi ancaman |
| Screen_Time | 0.0278 | Paparan layar berlebih berkontribusi pada kecemasan |
| Mood_State | 0.0055 | Mood tense/fatigued mencerminkan kecemasan |

### Final State

| Fitur | Importance |
|-------|-----------|
| Reward_Score | 1.0000 |

Hanya Reward_Score yang digunakan — semakin rendah apresiasi diri, semakin mungkin status akhir = Stress.

### Intervention Response

| Fitur | Importance |
|-------|-----------|
| Mood_State | 0.5451 |
| Reward_Score | 0.3632 |
| Social_Support | 0.0910 |
| Study_Hours | 0.0007 |

---

## Akurasi Model

| Target | Akurasi Test | CV Mean ± Std | Presisi (weighted) | Recall (weighted) |
|--------|:-----------:|:-------------:|:------------------:|:-----------------:|
| Stress_Level | **97.9%** | 97.4% ± 0.08% | 0.98 | 0.98 |
| Anxiety_Level | **90.2%** | 90.2% ± 0.62% | 0.91 | 0.90 |
| Final_State | **100%** | 100% ± 0.00% | 1.00 | 1.00 |
| Intervention_Response | **73.2%** | 72.1% ± 1.39% | 0.77 | 0.73 |

Dataset: 10.000 baris, 70% train / 30% test.

---

## Cara Membaca Decision Tree

### Struktur

```
Root Node (pertanyaan pertama)
├── Jika kondisi TRUE (≤ threshold atau IS true)
│   ├── Internal Node (pertanyaan lanjutan)
│   │   ├── Leaf Node (hasil prediksi)
│   │   └── Leaf Node
│   └── Leaf Node
└── Jika kondisi FALSE (> threshold atau IS false)
    ├── Leaf Node
    └── Leaf Node
```

### Informasi di setiap node

- **Kondisi split** — pertanyaan, misal `Mood_State <= 0.50`
- **Samples** — jumlah data training di node tersebut
- **Value** — distribusi kelas [Low, Medium, High]
- **Class** — kelas dominan
- **Warna** — semakin gelap = semakin yakin

### Contoh decision path (input high stress)

```
1. Mood_State <= 0.50 (value=2.00 -> Tense) -> right
   → Mood = Tense (nilai 2), berada di atas threshold 0.50 → cabang kanan
2. Mood_State <= 1.50 (value=2.00 -> Tense) -> right
   → Nilai 2 > 1.50 → masih cabang kanan
3. Mood_State <= 2.50 (value=2.00 -> Tense) -> left
   → Nilai 2 <= 2.50 → cabang kiri → leaf = High stress
```

---

## Troubleshooting

### "Connection refused" saat test

```bash
# Pastikan Flask sudah jalan
python app.py
# Di terminal lain, baru jalankan test
python test_all.py
```

### "Model is not loaded"

```bash
# Model belum dilatih atau file model.pkl tidak ditemukan
python train_model.py
```

### File dataset tidak terdeteksi

```bash
# Cek file CSV di root project
dir *.csv
# Harus ada dataset.csv atau psychological_regulation_dataset.csv
```

### Error validasi saat prediksi

Periksa:
- Semua 13 field terisi
- Nilai numerik dalam range yang ditentukan
- mood_state ∈ {Calm, Neutral, Tense, Fatigued}
- facial_emotion ∈ {Neutral, Happy, Sad, Angry, Surprised}

### Port 5000 sudah terpakai

Ubah port di `app.py` baris terakhir:
```python
app.run(host="0.0.0.0", port=5001, debug=True)
```

---

## Catatan Teknis

- Decision tree **tidak menggunakan scaling** — threshold pada fitur numerik langsung dibandingkan dengan nilai input asli (misal `Exam_Pressure <= 7.50` dalam range 0–10).
- Threshold desimal (0.5, 1.5, 2.5) pada Mood_State bukanlah "stress score" — ini adalah **batas antar kategori ordinal** yang dihasilkan oleh OrdinalEncoder.
- Urutan split tree ditentukan oleh **Gini impurity gain**, bukan prioritas subjektif. Fitur dengan informasi terbanyak secara statistik akan muncul di root node.
- Untuk `Intervention_Response`, akurasi 73.2% masih di bawah target 80% — kemungkinan karena distribusi kelas yang tidak seimbang atau hubungan non-linear yang kompleks.
- Frontend menggunakan **Tailwind CDN** + **Viz.js CDN** — koneksi internet diperlukan saat pertama kali load.

---

## Lisensi

Proyek ini dikembangkan untuk keperluan tugas akademik DSS (Decision Support System). Tidak ada lisensi khusus — hak cipta tetap milik pengembang.
