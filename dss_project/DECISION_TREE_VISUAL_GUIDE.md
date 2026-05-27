# Panduan Visual Decision Tree - Cara Membaca Diagram

## 📊 Struktur Visual Tree

Ketika Anda membuka tab "Decision Tree" di aplikasi, Anda akan melihat diagram pohon yang terlihat seperti ini:

```
                    ┌─────────────────────────┐
                    │  Stress_Score <= 50.00  │
                    │  gini = 0.45            │
                    │  samples = 10000        │
                    │  value = [3000, 4000, 3000] │
                    │  class = Medium         │
                    └────────────┬────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼ TRUE (<=)               ▼ FALSE (>)
            ┌──────────────────┐      ┌──────────────────┐
            │ Anxiety_Score... │      │ Sleep_Hours...   │
            │ ...              │      │ ...              │
            └──────────────────┘      └──────────────────┘
                    │                         │
            ┌───────┴───────┐         ┌───────┴───────┐
            ▼               ▼         ▼               ▼
        ┌────────┐     ┌────────┐ ┌────────┐     ┌────────┐
        │  LOW   │     │MEDIUM  │ │ HIGH   │     │ HIGH   │
        └────────┘     └────────┘ └────────┘     └────────┘
```

---

## 🎨 Elemen Visual

### 1. **Kotak (Node)**

Setiap kotak mewakili satu node dalam tree. Ada 3 jenis:

#### **Root Node (Kotak Paling Atas)**
```
┌─────────────────────────────────┐
│ Stress_Score <= 50.00           │  ← Kondisi/Pertanyaan
│ gini = 0.45                     │  ← Gini impurity
│ samples = 10000                 │  ← Jumlah data
│ value = [3000, 4000, 3000]      │  ← Distribusi kelas
│ class = Medium                  │  ← Kelas dominan
└─────────────────────────────────┘
```

#### **Internal Node (Kotak Tengah)**
- Sama seperti root node, tapi ada di tengah tree
- Memiliki pertanyaan dan 2 cabang (kiri dan kanan)

#### **Leaf Node (Kotak Paling Bawah)**
```
┌──────────────┐
│ class = HIGH │  ← Hasil prediksi
│ samples = 500│  ← Jumlah data yang sampai ke sini
└──────────────┘
```

### 2. **Garis (Edges)**

Garis menghubungkan node parent dengan node child:

```
                Parent Node
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼ TRUE/<=               ▼ FALSE/>
    Child Left             Child Right
```

- **Garis ke KIRI:** Untuk kondisi TRUE atau <= (memenuhi kondisi)
- **Garis ke KANAN:** Untuk kondisi FALSE atau > (tidak memenuhi kondisi)

### 3. **Warna Node**

Warna background node menunjukkan kelas mana yang paling dominan:

```
┌─────────────────────┐
│ class = LOW         │  ← Warna HIJAU (Low dominan)
│ value = [800, 100, 50] │
└─────────────────────┘

┌─────────────────────┐
│ class = MEDIUM      │  ← Warna KUNING (Medium dominan)
│ value = [100, 800, 100] │
└─────────────────────┘

┌─────────────────────┐
│ class = HIGH        │  ← Warna MERAH (High dominan)
│ value = [50, 100, 800] │
└─────────────────────┘
```

**Semakin gelap warna = semakin yakin model dengan prediksi tersebut**

---

## 📖 Membaca Informasi di Node

### Contoh Node Lengkap:

```
┌──────────────────────────────────┐
│ Stress_Score <= 50.00            │  ← KONDISI
│ gini = 0.4567                    │  ← GINI IMPURITY
│ samples = 5000                   │  ← JUMLAH SAMPLES
│ value = [1500, 2000, 1500]       │  ← DISTRIBUSI KELAS
│ class = Medium                   │  ← KELAS DOMINAN
└──────────────────────────────────┘
```

### Penjelasan Detail:

#### **1. Kondisi (Stress_Score <= 50.00)**
- Pertanyaan yang diajukan di node ini
- Jika nilai Anda memenuhi kondisi → ikuti garis KIRI
- Jika nilai Anda tidak memenuhi kondisi → ikuti garis KANAN

**Contoh:**
- Jika stress_score Anda = 45, apakah 45 <= 50? **YA** → KIRI
- Jika stress_score Anda = 65, apakah 65 <= 50? **TIDAK** → KANAN

#### **2. Gini Impurity (gini = 0.4567)**
- Ukuran "kemurnian" data di node ini
- Range: 0 sampai 0.5
- **Gini = 0** → Data sangat murni (semua sama kelas)
- **Gini = 0.5** → Data sangat tercampur (semua kelas sama banyak)

**Interpretasi:**
```
gini = 0.0    ← Murni (semua data 1 kelas)
gini = 0.2    ← Cukup murni
gini = 0.45   ← Tercampur
gini = 0.5    ← Sangat tercampur (50-50)
```

#### **3. Samples (samples = 5000)**
- Jumlah data training yang masuk ke node ini
- Semakin ke bawah, semakin kecil jumlahnya (data terbagi-bagi)

**Contoh:**
```
Root: samples = 10000 (semua data)
  ├─ Left: samples = 6000 (60% data)
  └─ Right: samples = 4000 (40% data)
```

#### **4. Value (value = [1500, 2000, 1500])**
- Distribusi kelas di node ini
- Format: [Low, Medium, High] atau [Relaxed, Neutral, Stress]
- Jumlah total = samples

**Contoh:**
```
value = [1500, 2000, 1500]
├─ Low: 1500 (30%)
├─ Medium: 2000 (40%)
└─ High: 1500 (30%)
```

#### **5. Class (class = Medium)**
- Kelas yang paling banyak di node ini
- Ini adalah prediksi jika kita stop di node ini
- Biasanya digunakan di leaf node

---

## 🎯 Contoh Walkthrough Lengkap

Misalkan Anda memiliki data:
- **Stress_Score = 65**
- **Anxiety_Score = 58**
- **Exam_Pressure = 7**
- **Sleep_Hours = 5.5**

### Step 1: Mulai dari Root Node

```
┌──────────────────────────────────┐
│ Stress_Score <= 50.00            │
│ gini = 0.45                      │
│ samples = 10000                  │
│ value = [3000, 4000, 3000]       │
│ class = Medium                   │
└──────────────────────────────────┘
```

**Pertanyaan:** Apakah Stress_Score <= 50.00?
**Jawaban:** Apakah 65 <= 50? **TIDAK** → Ikuti garis ke KANAN

### Step 2: Internal Node (Kanan)

```
┌──────────────────────────────────┐
│ Sleep_Hours <= 6.5               │
│ gini = 0.42                      │
│ samples = 4000                   │
│ value = [1000, 1500, 1500]       │
│ class = Medium                   │
└──────────────────────────────────┘
```

**Pertanyaan:** Apakah Sleep_Hours <= 6.5?
**Jawaban:** Apakah 5.5 <= 6.5? **YA** → Ikuti garis ke KIRI

### Step 3: Internal Node (Kiri)

```
┌──────────────────────────────────┐
│ Anxiety_Score <= 60.00           │
│ gini = 0.40                      │
│ samples = 2500                   │
│ value = [500, 1000, 1000]        │
│ class = Medium                   │
└──────────────────────────────────┘
```

**Pertanyaan:** Apakah Anxiety_Score <= 60.00?
**Jawaban:** Apakah 58 <= 60? **YA** → Ikuti garis ke KIRI

### Step 4: Leaf Node (Hasil Akhir)

```
┌──────────────────────────────────┐
│ class = MEDIUM                   │
│ samples = 1200                   │
│ value = [200, 800, 200]          │
└──────────────────────────────────┘
```

**HASIL PREDIKSI: MEDIUM**

---

## 🔍 Interpretasi Hasil di Leaf Node

### Contoh Leaf Node:

```
┌──────────────────────────────────┐
│ class = HIGH                     │
│ samples = 500                    │
│ value = [50, 150, 300]           │
└──────────────────────────────────┘
```

**Interpretasi:**
- **Prediksi:** HIGH (kelas dominan)
- **Confidence:** 300/500 = 60% (model 60% yakin)
- **Distribusi:**
  - Low: 50 (10%)
  - Medium: 150 (30%)
  - High: 300 (60%)

**Artinya:** Model memprediksi HIGH dengan confidence 60%. Ada 30% kemungkinan MEDIUM dan 10% kemungkinan LOW.

---

## 📊 Membandingkan Leaf Nodes

### Leaf Node dengan Confidence Tinggi:

```
┌──────────────────────────────────┐
│ class = HIGH                     │
│ samples = 500                    │
│ value = [10, 30, 460]            │
└──────────────────────────────────┘
```

**Confidence:** 460/500 = **92%** ✅ (Sangat yakin)

### Leaf Node dengan Confidence Rendah:

```
┌──────────────────────────────────┐
│ class = HIGH                     │
│ samples = 500                    │
│ value = [150, 170, 180]          │
└──────────────────────────────────┘
```

**Confidence:** 180/500 = **36%** ⚠️ (Kurang yakin)

---

## 🎨 Pola Visual yang Perlu Diperhatikan

### 1. **Tree yang Seimbang**
```
        Root
       /    \
      /      \
    Node    Node
    / \      / \
   L   L    L   L
```
✅ Baik - Data terbagi merata

### 2. **Tree yang Tidak Seimbang**
```
        Root
       /    \
      /      \
    Node    Node
    / \        \
   L   L        L
```
⚠️ Kurang ideal - Data tidak merata

### 3. **Tree yang Terlalu Dalam**
```
        Root
         |
        Node
         |
        Node
         |
        Node
         |
        Leaf
```
⚠️ Berisiko overfitting - Terlalu kompleks

---

## 💡 Tips Membaca Tree Secara Efisien

1. **Fokus pada Root Node** - Ini adalah fitur paling penting
2. **Ikuti alur Anda** - Trace jalur untuk data Anda sendiri
3. **Perhatikan Gini** - Semakin kecil gini, semakin murni node
4. **Cek Samples** - Semakin banyak samples, semakin reliable
5. **Lihat Leaf Node** - Ini adalah hasil akhir dan confidence-nya
6. **Baca Jalur Keputusan** - Gunakan penjelasan tekstual untuk clarity

---

## 🔗 Hubungan dengan Jalur Keputusan Tekstual

Jalur keputusan tekstual di bawah tree adalah penjelasan dari alur visual:

**Visual Tree:**
```
Root: Stress_Score <= 50.00?
  ├─ KANAN (65 > 50)
  │
  └─ Sleep_Hours <= 6.5?
      ├─ KIRI (5.5 <= 6.5)
      │
      └─ Anxiety_Score <= 60.00?
          ├─ KIRI (58 <= 60)
          │
          └─ HASIL: MEDIUM
```

**Jalur Keputusan Tekstual:**
```
1. Stress_Score <= 50.00 (value=65.00) -> right
2. Sleep_Hours <= 6.5 (value=5.5) -> left
3. Anxiety_Score <= 60.00 (value=58.00) -> left
```

Keduanya menunjukkan hal yang sama, hanya format berbeda!

---

## 🎓 Latihan: Coba Baca Tree Sendiri

Cobalah untuk:
1. Isi form dengan data Anda
2. Klik "Prediksi"
3. Buka tab "Decision Tree"
4. Mulai dari Root Node
5. Ikuti alur sesuai dengan nilai Anda
6. Lihat Leaf Node sebagai hasil akhir
7. Bandingkan dengan "Jalur Keputusan" tekstual
8. Pahami mengapa model memberikan prediksi tersebut

---

Semoga panduan ini membantu Anda memahami visual Decision Tree dengan lebih baik! 🎓
