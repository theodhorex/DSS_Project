# Integrasi Lengkap: Dari Input hingga Prediksi

## 🔄 Alur Lengkap Sistem DSS

```
┌─────────────────────────────────────────────────────────────────┐
│                    MAHASISWA MENGISI FORM                       │
│  (15 indikator: stress, anxiety, sleep, exam pressure, dll)    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PREPROCESSING DATA                           │
│  ├─ Input Values: Nilai mentah dari form                       │
│  ├─ Imputation: Mengisi missing values                         │
│  ├─ Normalization: Scaling data numeric                        │
│  └─ Encoding: Mengubah kategori menjadi angka                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  DECISION TREE INFERENCE                        │
│  ├─ Tree 1: Prediksi Stress Level (Low/Medium/High)           │
│  ├─ Tree 2: Prediksi Anxiety Level (Low/Medium/High)          │
│  ├─ Tree 3: Prediksi Final State (Relaxed/Neutral/Stress)     │
│  └─ Tree 4: Prediksi Intervention Response (Pos/Neu/Neg)      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  HASIL PREDIKSI & ANALISIS                      │
│  ├─ Predictions: 4 hasil prediksi                              │
│  ├─ Confidence: Tingkat keyakinan model                        │
│  ├─ Decision Paths: Jalur keputusan step-by-step              │
│  ├─ Probabilities: Confidence untuk setiap kelas               │
│  └─ Explanation: Penjelasan human-readable                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  TAMPILAN DI INTERFACE                          │
│  ├─ Results Card: Ringkasan hasil prediksi                     │
│  ├─ Details Modal: Penjelasan lengkap                          │
│  ├─ Decision Tree Visualization: Diagram pohon                 │
│  └─ Recommendations: Saran tindakan                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Komponen-Komponen Utama

### 1. **Form Input (15 Indikator)**

#### Tier 1: Metrik Psikologis (4 indikator)
- **Stress Score** (0-100): Seberapa berat beban pikiran
- **Anxiety Score** (0-100): Seberapa sering merasa gugup/cemas
- **Reward Score** (0-100): Kepuasan dengan pencapaian
- **Mood State** (kategori): Suasana hati saat ini

#### Tier 2: Indikator Akademik (4 indikator)
- **Exam Pressure** (0-10): Tingkat stres menghadapi ujian
- **Assignment Load** (0-10): Banyaknya tugas kuliah
- **Study Hours** (0-24): Rata-rata waktu belajar per hari
- **Attendance** (0-100): Persentase kehadiran

#### Tier 3: Kesehatan Fisik (4 indikator)
- **Sleep Hours** (0-24): Durasi tidur per malam
- **Heart Rate** (40-200): Detak jantung rata-rata
- **Physical Activity** (0-10): Tingkat aktivitas fisik
- **Screen Time** (0-24): Waktu di depan layar per hari

#### Tier 4: Sosial & Perilaku (3 indikator)
- **Social Support** (0-10): Dukungan dari teman/keluarga
- **Facial Emotion** (kategori): Ekspresi wajah yang ditunjukkan
- **Intervention Response** (kategori): Efek bantuan/saran sebelumnya

---

### 2. **Preprocessing Pipeline**

#### Step 1: Input Values
```python
{
  "stress_score": 65,
  "anxiety_score": 58,
  "exam_pressure": 7,
  "sleep_hours": 5.5,
  "social_support": 6,
  "heart_rate": 82,
  "physical_activity": 3,
  "assignment_load": 8,
  "study_hours": 4,
  "attendance": 85,
  "screen_time": 6.5,
  "facial_emotion": "Neutral",
  "mood_state": "Anxious",
  "intervention_response": "Positive",
  "reward_score": 45
}
```

#### Step 2: Feature Preprocessing
```python
# Numeric Features: SimpleImputer + StandardScaler
Stress_Score: 65.0000
Anxiety_Score: 58.0000
Exam_Pressure: 7.0000
Sleep_Hours: 5.5000
Social_Support: 6.0000
Heart_Rate: 82.0000
Physical_Activity: 3.0000
Assignment_Load: 8.0000
Study_Hours: 4.0000
Attendance: 85.0000
Screen_Time: 6.5000
Reward_Score: 45.0000

# Categorical Features: OneHotEncoder
Facial_Emotion=Happy: 0
Facial_Emotion=Sad: 0
Facial_Emotion=Angry: 0
Facial_Emotion=Neutral: 1
Facial_Emotion=Surprised: 0
Mood_State=Happy: 0
Mood_State=Sad: 0
Mood_State=Anxious: 1
Mood_State=Neutral: 0
Mood_State=Excited: 0
Intervention_Response=Positive: 1
Intervention_Response=Neutral: 0
Intervention_Response=Negative: 0
```

---

### 3. **Decision Tree Inference**

#### Tree 1: Stress Level Prediction

**Input:** 27 features (12 numeric + 15 one-hot encoded)

**Process:**
```
Root: Stress_Score <= 50.00?
├─ NO (65 > 50) → Right
│
└─ Sleep_Hours <= 6.5?
   ├─ YES (5.5 <= 6.5) → Left
   │
   └─ Anxiety_Score <= 60.00?
      ├─ YES (58 <= 60) → Left
      │
      └─ Exam_Pressure <= 5.00?
         ├─ NO (7 > 5) → Right
         │
         └─ LEAF: HIGH (confidence: 85%)
```

**Output:** "High" dengan confidence 0.85

#### Tree 2: Anxiety Level Prediction
- Proses serupa dengan Tree 1
- Output: "Medium" dengan confidence 0.72

#### Tree 3: Final State Prediction
- Proses serupa dengan Tree 1
- Output: "Relaxed" dengan confidence 0.78

#### Tree 4: Intervention Response Prediction
- Proses serupa dengan Tree 1
- Output: "Positive" dengan confidence 0.81

---

### 4. **Hasil Prediksi & Analisis**

#### Predictions
```json
{
  "stress_level": "High",
  "anxiety_level": "Medium",
  "final_state": "Relaxed",
  "intervention_response": "Positive"
}
```

#### Confidence
```
Average confidence = (0.85 + 0.72 + 0.78 + 0.81) / 4 = 0.79 (79%)
```

#### Decision Paths
```json
{
  "stress_level": [
    "Stress_Score <= 50.00 (value=65.00) -> right",
    "Sleep_Hours <= 6.5 (value=5.5) -> left",
    "Anxiety_Score <= 60.00 (value=58.00) -> left",
    "Exam_Pressure <= 5.00 (value=7.00) -> right"
  ],
  "anxiety_level": [...],
  "final_state": [...],
  "intervention_response": [...]
}
```

#### Prediction Probabilities
```json
{
  "stress_level": {
    "Low": 0.05,
    "Medium": 0.10,
    "High": 0.85
  },
  "anxiety_level": {
    "Low": 0.15,
    "Medium": 0.72,
    "High": 0.13
  },
  "final_state": {
    "Relaxed": 0.78,
    "Neutral": 0.15,
    "Stress": 0.07
  },
  "intervention_response": {
    "Positive": 0.81,
    "Neutral": 0.12,
    "Negative": 0.07
  }
}
```

#### Explanation
```
"High stress detected due to elevated stress score (65) and high exam 
pressure (7). Positive recommended."
```

---

## 🎨 Tampilan di Interface

### 1. **Results Card**

```
┌─────────────────────────────────────────┐
│          HASIL PREDIKSI                 │
├─────────────────────────────────────────┤
│ Stres: High  │  Kecemasan: Medium       │
├─────────────────────────────────────────┤
│ Status Akhir: Relaxed                   │
├─────────────────────────────────────────┤
│ Saran Intervensi: Positive              │
├─────────────────────────────────────────┤
│ Tingkat Keyakinan: 79%                  │
│ ████████████████░░░░░░░░░░░░░░░░░░░░░░  │
├─────────────────────────────────────────┤
│ High stress detected due to elevated    │
│ stress score (65) and high exam         │
│ pressure (7). Positive recommended.     │
├─────────────────────────────────────────┤
│ [Lihat Detail Analisis]                 │
└─────────────────────────────────────────┘
```

### 2. **Details Modal**

#### Section 1: Penjelasan Decision Tree
- Apa itu Decision Tree
- Bagaimana cara kerjanya
- Keuntungan Decision Tree
- Tips membaca tree

#### Section 2: Faktor Utama
```
Faktor Utama (4 langkah pertama dari jalur keputusan):
1. Stress_Score <= 50.00 (value=65.00) -> right
2. Sleep_Hours <= 6.5 (value=5.5) -> left
3. Anxiety_Score <= 60.00 (value=58.00) -> left
4. Exam_Pressure <= 5.00 (value=7.00) -> right
```

#### Section 3: Tahapan Preprocessing
```
Step 1: Input Values
- stress_score: 65
- anxiety_score: 58
- exam_pressure: 7
- ... (15 indikator)

Step 2: Feature Preprocessing
- Stress_Score: 65.0000
- Anxiety_Score: 58.0000
- Exam_Pressure: 7.0000
- ... (27 features)
```

#### Section 4: Probabilitas Prediksi
```
Tingkat Stres:
├─ Low: 5%     ░░░░░░░░░░░░░░░░░░░░
├─ Medium: 10% ██░░░░░░░░░░░░░░░░░░
└─ High: 85%   ████████████████████

Tingkat Kecemasan:
├─ Low: 15%    ███░░░░░░░░░░░░░░░░░
├─ Medium: 72% ███████████████░░░░░░
└─ High: 13%   ██░░░░░░░░░░░░░░░░░░

... (Final State dan Intervention Response)
```

#### Section 5: Rekomendasi Aksi
```
Berdasarkan prediksi "High Stress":
✓ Kurangi aktivitas non-prioritas dan fokus pada pemulihan
✓ Diskusikan beban akademik dengan dosen atau mentor
✓ Pertimbangkan konsultasi profesional jika gejala berlanjut
```

### 3. **Decision Tree Visualization**

```
Tab 1: Tingkat Stres
┌──────────────────────────────────────┐
│ [Cara Membaca Decision Tree]          │
│ ├─ Struktur Tree                      │
│ ├─ Informasi di setiap node           │
│ ├─ Cara mengikuti alur                │
│ └─ Jalur keputusan Anda               │
├──────────────────────────────────────┤
│ [VISUAL TREE DIAGRAM]                 │
│ (Rendered menggunakan Graphviz)       │
├──────────────────────────────────────┤
│ Jalur Keputusan:                      │
│ 1. Stress_Score <= 50.00 -> right     │
│ 2. Sleep_Hours <= 6.5 -> left         │
│ 3. Anxiety_Score <= 60.00 -> left     │
│ 4. Exam_Pressure <= 5.00 -> right     │
└──────────────────────────────────────┘

Tab 2: Tingkat Kecemasan
[Serupa dengan Tab 1]

Tab 3: Status Akhir
[Serupa dengan Tab 1]

Tab 4: Intervensi
[Serupa dengan Tab 1]
```

---

## 🔗 Hubungan Antar Komponen

### Input → Preprocessing → Tree Inference

```
Form Input (15 indikator)
        ↓
Preprocessing Pipeline
├─ Step 1: Input Values (15 features)
└─ Step 2: Feature Preprocessing (27 features)
        ↓
Decision Tree Inference (4 trees)
├─ Tree 1: Stress Level
├─ Tree 2: Anxiety Level
├─ Tree 3: Final State
└─ Tree 4: Intervention Response
        ↓
Results & Analysis
├─ Predictions (4 hasil)
├─ Confidence (rata-rata)
├─ Decision Paths (4 paths)
├─ Probabilities (4 sets)
└─ Explanation (human-readable)
        ↓
Interface Display
├─ Results Card (ringkasan)
├─ Details Modal (penjelasan lengkap)
├─ Decision Tree Visualization (diagram)
└─ Recommendations (saran tindakan)
```

### Faktor Utama → Jalur Keputusan → Probabilitas

```
Faktor Utama (4 langkah pertama)
        ↓
Jalur Keputusan Lengkap (semua langkah)
        ↓
Leaf Node (hasil akhir)
        ↓
Probabilitas Prediksi (confidence untuk setiap kelas)
```

---

## 💡 Contoh Kasus Lengkap

### Input Mahasiswa A
```
Stress Score: 65
Anxiety Score: 58
Exam Pressure: 7
Sleep Hours: 5.5
Social Support: 6
Heart Rate: 82
Physical Activity: 3
Assignment Load: 8
Study Hours: 4
Attendance: 85
Screen Time: 6.5
Facial Emotion: Neutral
Mood State: Anxious
Intervention Response: Positive
Reward Score: 45
```

### Preprocessing
```
Input Values: 15 features
Feature Preprocessing: 27 features (12 numeric + 15 one-hot)
```

### Tree Inference
```
Tree 1 (Stress Level):
  Stress_Score (65) > 50 → Right
  Sleep_Hours (5.5) <= 6.5 → Left
  Anxiety_Score (58) <= 60 → Left
  Exam_Pressure (7) > 5 → Right
  → LEAF: High (confidence: 85%)

Tree 2 (Anxiety Level):
  Anxiety_Score (58) > 50 → Right
  Mood_State (Anxious) → Match
  Heart_Rate (82) > 80 → Right
  → LEAF: Medium (confidence: 72%)

Tree 3 (Final State):
  Stress_Score (65) > 50 → Right
  Sleep_Hours (5.5) <= 6.5 → Left
  Social_Support (6) > 5 → Right
  → LEAF: Relaxed (confidence: 78%)

Tree 4 (Intervention Response):
  Intervention_Response (Positive) → Match
  Social_Support (6) > 5 → Right
  → LEAF: Positive (confidence: 81%)
```

### Results
```
Predictions:
- Stress Level: High
- Anxiety Level: Medium
- Final State: Relaxed
- Intervention Response: Positive

Confidence: 79%

Decision Paths: (seperti di atas)

Probabilities:
- Stress Level: Low 5%, Medium 10%, High 85%
- Anxiety Level: Low 15%, Medium 72%, High 13%
- Final State: Relaxed 78%, Neutral 15%, Stress 7%
- Intervention Response: Positive 81%, Neutral 12%, Negative 7%

Explanation:
"High stress detected due to elevated stress score (65) and high exam 
pressure (7). Positive recommended."
```

### Interface Display
```
Results Card:
- Stres: High
- Kecemasan: Medium
- Status Akhir: Relaxed
- Saran: Positive
- Confidence: 79%

Details Modal:
- Penjelasan Decision Tree
- Faktor Utama (4 langkah)
- Preprocessing Steps (2 steps)
- Probabilitas Prediksi (4 targets)
- Rekomendasi Aksi (3 saran)

Decision Tree Visualization:
- Tree Tingkat Stres (dengan jalur keputusan)
- Tree Tingkat Kecemasan (dengan jalur keputusan)
- Tree Status Akhir (dengan jalur keputusan)
- Tree Intervensi (dengan jalur keputusan)
```

---

## 🎓 Untuk Dosen

### Transparansi Model
✅ Setiap keputusan dapat dijelaskan step-by-step
✅ Dapat melihat alasan mengapa model memberikan prediksi tertentu
✅ Dapat memverifikasi logika tree dengan domain knowledge

### Verifikasi Akurasi
✅ Dapat melihat confidence score untuk setiap prediksi
✅ Dapat melihat distribusi kelas di setiap node
✅ Dapat menganalisis decision paths untuk anomali

### Analisis Pola
✅ Dapat melihat fitur mana yang paling penting (root node)
✅ Dapat melihat interaksi antar fitur (internal nodes)
✅ Dapat melihat threshold yang digunakan model

### Improvement
✅ Dapat mengidentifikasi fitur yang perlu ditambahkan
✅ Dapat melihat apakah ada bias dalam data
✅ Dapat membuat rekomendasi untuk improvement model

---

Semoga dokumentasi ini membantu memahami sistem DSS secara menyeluruh! 🎓
