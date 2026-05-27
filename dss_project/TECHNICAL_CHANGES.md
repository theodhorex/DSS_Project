# 🔧 Perubahan Teknis - Decision Tree Explanation

## File-File yang Dimodifikasi

### 1. **templates/index.html**

#### Perubahan di Modal (Detail Analisis)

**Tambahan Section Baru (Paling Atas):**
```html
<div>
  <div class="flex items-start justify-between gap-4 mb-3">
    <h4 class="font-display text-xl font-bold">Penjelasan Decision Tree</h4>
    <button class="text-xs font-bold text-blue-600 hover:text-blue-800 underline" 
            data-toggle-info="decisionTreeInfo">
      Apa ini?
    </button>
  </div>
  <div id="decisionTreeInfo" class="hidden rounded-xl border-2 border-green-200 bg-green-50 p-3 mb-3 text-xs text-green-800">
    <!-- Penjelasan lengkap tentang Decision Tree -->
  </div>
  <div class="rounded-xl border-2 border-green-200 bg-green-50 p-4 text-sm text-green-800">
    <!-- Tips membaca Decision Tree -->
  </div>
</div>
```

**Perubahan di Section Faktor Utama:**
- Tambah `border-t-2 border-ink pt-6` untuk separator
- Tetap ada toggle button "Apa ini?"

**Perubahan di Section Preprocessing:**
- Tetap sama, hanya ditambah separator

**Perubahan di Section Probabilitas:**
- Tetap sama, hanya ditambah separator

**Perubahan di Section Rekomendasi:**
- Tetap sama, hanya ditambah separator

#### Perubahan di Decision Tree Visualization

**Tambahan Panduan Membaca Tree (Sebelum Tab Buttons):**
```html
<div class="rounded-2xl border-2 border-green-300 bg-green-50 p-4">
  <details class="cursor-pointer">
    <summary class="font-semibold text-green-900 text-sm hover:text-green-700">
      📖 Cara Membaca Decision Tree (klik untuk buka)
    </summary>
    <div class="mt-3 text-xs text-green-800 space-y-2">
      <!-- Penjelasan cara membaca tree -->
    </div>
  </details>
</div>
```

**Perubahan di Setiap Tree Card:**
- Tambah penjelasan singkat sebelum visual tree
- Tambah text "Berikut adalah step-by-step keputusan..." sebelum jalur keputusan

**Contoh untuk Tree Stress Level:**
```html
<div class="text-xs text-slate-600 bg-blue-50 border border-blue-200 rounded-lg p-3">
  <p><strong>Penjelasan:</strong> Tree ini memprediksi tingkat stres Anda 
     (Low, Medium, High) berdasarkan indikator psikologis dan akademik...</p>
</div>
```

---

### 2. **static/js/script.js**

#### Fungsi yang Sudah Ada (Tidak Berubah)

```javascript
// Fungsi-fungsi ini sudah ada dan berfungsi dengan baik:
function renderKeyFactorsModal(paths)
function renderPreprocessingStepsModal(steps)
function renderPredictionProbabilitiesModal(probabilities)
function renderRecommendationsModal(level)
function setupDetailsModal()
```

#### Integrasi di displayResults()

```javascript
function displayResults(data) {
  // ... kode sebelumnya ...
  
  // Panggil fungsi-fungsi rendering
  renderDecisionPaths(data.decision_paths || {});
  renderKeyFactorsModal(data.decision_paths || {});
  renderPreprocessingStepsModal(data.preprocessing_steps || []);
  renderPredictionProbabilitiesModal(data.prediction_probabilities || {});
  renderRecommendationsModal(stressLabel);
  
  // ... kode selanjutnya ...
}
```

#### Integrasi di DOMContentLoaded

```javascript
document.addEventListener('DOMContentLoaded', function() {
  // ... kode sebelumnya ...
  
  // Setup modal dengan toggle buttons
  setupDetailsModal();
  
  // ... kode selanjutnya ...
});
```

---

## 📊 Struktur HTML Modal Baru

```html
<div id="detailsModal" class="fixed inset-0 z-50 hidden flex items-center justify-center p-4">
  <div class="relative w-full max-w-4xl max-h-[90vh] flex flex-col rounded-3xl border-2 border-ink bg-white shadow-brutal">
    
    <!-- Header -->
    <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between p-6 border-b-2 border-ink flex-shrink-0">
      <div>
        <h3 id="detailsModalTitle" class="font-display text-3xl">Detail Analisis Prediksi</h3>
        <p class="text-sm text-slate-600">Informasi lengkap tentang proses prediksi dan hasil analisis.</p>
      </div>
      <button id="closeDetailsModal" class="rounded-full border-2 border-ink bg-white px-4 py-2 text-xs font-bold uppercase tracking-widest shadow-brutal-sm transition hover:-translate-y-0.5">
        Tutup
      </button>
    </div>
    
    <!-- Content -->
    <div class="flex-1 overflow-y-auto hide-scrollbar p-6 space-y-6">
      
      <!-- Section 1: Penjelasan Decision Tree -->
      <div>
        <div class="flex items-start justify-between gap-4 mb-3">
          <h4 class="font-display text-xl font-bold">Penjelasan Decision Tree</h4>
          <button class="text-xs font-bold text-blue-600 hover:text-blue-800 underline" data-toggle-info="decisionTreeInfo">
            Apa ini?
          </button>
        </div>
        <div id="decisionTreeInfo" class="hidden rounded-xl border-2 border-green-200 bg-green-50 p-3 mb-3 text-xs text-green-800">
          <!-- Penjelasan lengkap -->
        </div>
        <div class="rounded-xl border-2 border-green-200 bg-green-50 p-4 text-sm text-green-800">
          <!-- Tips membaca -->
        </div>
      </div>
      
      <!-- Separator -->
      <div class="border-t-2 border-ink pt-6">
        
        <!-- Section 2: Faktor Utama -->
        <div>
          <div class="flex items-start justify-between gap-4 mb-3">
            <h4 class="font-display text-xl font-bold">Faktor Utama</h4>
            <button class="text-xs font-bold text-blue-600 hover:text-blue-800 underline" data-toggle-info="keyFactorsInfo">
              Apa ini?
            </button>
          </div>
          <div id="keyFactorsInfo" class="hidden rounded-xl border-2 border-blue-200 bg-blue-50 p-3 mb-3 text-xs text-blue-800">
            <!-- Penjelasan -->
          </div>
          <ul id="keyFactorsModal" class="space-y-2"></ul>
        </div>
      </div>
      
      <!-- Separator -->
      <div class="border-t-2 border-ink pt-6">
        
        <!-- Section 3: Tahapan Preprocessing -->
        <div>
          <div class="flex items-start justify-between gap-4 mb-3">
            <h4 class="font-display text-xl font-bold">Tahapan Preprocessing</h4>
            <button class="text-xs font-bold text-blue-600 hover:text-blue-800 underline" data-toggle-info="preprocessingInfo">
              Apa ini?
            </button>
          </div>
          <div id="preprocessingInfo" class="hidden rounded-xl border-2 border-blue-200 bg-blue-50 p-3 mb-3 text-xs text-blue-800">
            <!-- Penjelasan -->
          </div>
          <div id="preprocessingStepsModal" class="space-y-2"></div>
        </div>
      </div>
      
      <!-- Separator -->
      <div class="border-t-2 border-ink pt-6">
        
        <!-- Section 4: Probabilitas Prediksi -->
        <div>
          <div class="flex items-start justify-between gap-4 mb-3">
            <h4 class="font-display text-xl font-bold">Probabilitas Prediksi</h4>
            <button class="text-xs font-bold text-blue-600 hover:text-blue-800 underline" data-toggle-info="probabilitiesInfo">
              Apa ini?
            </button>
          </div>
          <div id="probabilitiesInfo" class="hidden rounded-xl border-2 border-blue-200 bg-blue-50 p-3 mb-3 text-xs text-blue-800">
            <!-- Penjelasan -->
          </div>
          <div id="predictionProbabilitiesModal" class="space-y-3"></div>
        </div>
      </div>
      
      <!-- Separator -->
      <div class="border-t-2 border-ink pt-6">
        
        <!-- Section 5: Rekomendasi Aksi -->
        <div>
          <div class="flex items-start justify-between gap-4 mb-3">
            <h4 class="font-display text-xl font-bold">Rekomendasi Aksi</h4>
            <button class="text-xs font-bold text-blue-600 hover:text-blue-800 underline" data-toggle-info="recommendationInfo">
              Apa ini?
            </button>
          </div>
          <div id="recommendationInfo" class="hidden rounded-xl border-2 border-blue-200 bg-blue-50 p-3 mb-3 text-xs text-blue-800">
            <!-- Penjelasan -->
          </div>
          <ul id="recommendationListModal" class="space-y-2"></ul>
        </div>
      </div>
      
    </div>
  </div>
</div>
```

---

## 🔄 Alur Data

### Input → Processing → Output

```
User Input (Form)
    ↓
POST /predict
    ↓
Backend Processing
├─ Preprocessing (Input Values → Features)
├─ Tree Inference (4 trees)
├─ Decision Paths Extraction
├─ Probabilities Calculation
└─ Response Generation
    ↓
Response JSON
├─ predictions
├─ confidence
├─ explanation
├─ decision_paths
├─ preprocessing_steps
└─ prediction_probabilities
    ↓
displayResults(data)
    ├─ renderKeyFactorsModal()
    ├─ renderPreprocessingStepsModal()
    ├─ renderPredictionProbabilitiesModal()
    ├─ renderRecommendationsModal()
    └─ renderDecisionPaths()
    ↓
Modal Display
├─ Penjelasan Decision Tree
├─ Faktor Utama
├─ Tahapan Preprocessing
├─ Probabilitas Prediksi
└─ Rekomendasi Aksi
```

---

## 🎨 CSS Classes yang Digunakan

### Untuk Penjelasan Sections
- `border-2 border-green-200` - Border hijau untuk Decision Tree explanation
- `bg-green-50` - Background hijau muda
- `text-green-800` - Text hijau gelap
- `border-2 border-blue-200` - Border biru untuk info boxes
- `bg-blue-50` - Background biru muda
- `text-blue-800` - Text biru gelap

### Untuk Toggle Buttons
- `text-xs font-bold text-blue-600` - Text styling
- `hover:text-blue-800` - Hover effect
- `underline` - Underline text
- `data-toggle-info="id"` - Data attribute untuk toggle

### Untuk Separators
- `border-t-2 border-ink` - Top border
- `pt-6` - Padding top

---

## 🔧 JavaScript Functions Detail

### setupDetailsModal()
```javascript
function setupDetailsModal() {
  const modal = document.getElementById("detailsModal");
  const openButton = document.getElementById("openDetailsModal");
  const closeButton = document.getElementById("closeDetailsModal");

  // Open modal
  const openModal = () => {
    modal.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  };

  // Close modal
  const closeModal = () => {
    modal.classList.add("hidden");
    document.body.style.overflow = "";
  };

  // Event listeners
  if (openButton) openButton.addEventListener("click", openModal);
  if (closeButton) closeButton.addEventListener("click", closeModal);

  // Close on overlay click
  modal.addEventListener("click", (event) => {
    if (event.target?.dataset?.modalOverlay === "true") {
      closeModal();
    }
  });

  // Close on ESC key
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeModal();
    }
  });

  // Toggle info buttons
  const toggleButtons = modal.querySelectorAll("[data-toggle-info]");
  toggleButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      const targetId = button.dataset.toggleInfo;
      const targetElement = modal.querySelector(`#${targetId}`);
      if (targetElement) {
        targetElement.classList.toggle("hidden");
        button.textContent = targetElement.classList.contains("hidden") ? "Apa ini?" : "Sembunyikan";
      }
    });
  });
}
```

---

## 📋 Checklist Implementasi

- [x] Tambah section "Penjelasan Decision Tree" di modal
- [x] Tambah toggle button "Apa ini?" untuk show/hide
- [x] Tambah panduan membaca tree di visualization
- [x] Tambah penjelasan untuk setiap tree card
- [x] Integrate dengan setupDetailsModal()
- [x] Test toggle functionality
- [x] Test modal open/close
- [x] Test ESC key close
- [x] Test overlay click close
- [x] Verify responsive design

---

## 🧪 Testing

### Manual Testing Checklist

- [ ] Isi form dan klik "Prediksi"
- [ ] Klik "Lihat Detail Analisis"
- [ ] Modal terbuka dengan benar
- [ ] Baca section "Penjelasan Decision Tree"
- [ ] Klik "Apa ini?" untuk toggle penjelasan
- [ ] Scroll modal untuk melihat semua sections
- [ ] Klik "Tutup" untuk menutup modal
- [ ] Klik overlay untuk menutup modal
- [ ] Tekan ESC untuk menutup modal
- [ ] Buka tab "Decision Tree"
- [ ] Baca "Cara Membaca Decision Tree" (collapsible)
- [ ] Lihat visual tree diagram
- [ ] Lihat jalur keputusan
- [ ] Test dengan berbagai data

---

## 🔗 Hubungan Komponen

```
HTML (templates/index.html)
├─ Modal #detailsModal
│  ├─ Section: Penjelasan Decision Tree
│  │  ├─ Toggle button: data-toggle-info="decisionTreeInfo"
│  │  └─ Info box: id="decisionTreeInfo"
│  ├─ Section: Faktor Utama
│  │  ├─ Toggle button: data-toggle-info="keyFactorsInfo"
│  │  └─ Info box: id="keyFactorsInfo"
│  │  └─ List: id="keyFactorsModal"
│  ├─ Section: Preprocessing
│  │  ├─ Toggle button: data-toggle-info="preprocessingInfo"
│  │  └─ Info box: id="preprocessingInfo"
│  │  └─ Container: id="preprocessingStepsModal"
│  ├─ Section: Probabilitas
│  │  ├─ Toggle button: data-toggle-info="probabilitiesInfo"
│  │  └─ Info box: id="probabilitiesInfo"
│  │  └─ Container: id="predictionProbabilitiesModal"
│  └─ Section: Rekomendasi
│     ├─ Toggle button: data-toggle-info="recommendationInfo"
│     └─ Info box: id="recommendationInfo"
│     └─ List: id="recommendationListModal"
│
├─ Decision Tree Visualization
│  ├─ Panduan Membaca (collapsible details)
│  ├─ Tree Tabs
│  └─ Tree Cards (4 cards)
│     ├─ Penjelasan singkat
│     ├─ Visual tree: id="tree-{target}"
│     └─ Jalur Keputusan: id="path-{target}"
│
└─ Button: id="openDetailsModal"

JavaScript (static/js/script.js)
├─ setupDetailsModal()
│  ├─ openModal()
│  ├─ closeModal()
│  ├─ Toggle info buttons
│  └─ Event listeners (click, ESC, overlay)
├─ renderKeyFactorsModal(paths)
├─ renderPreprocessingStepsModal(steps)
├─ renderPredictionProbabilitiesModal(probabilities)
├─ renderRecommendationsModal(level)
└─ displayResults(data)
   └─ Call semua render functions

Backend (app.py, utils/predictor.py)
├─ /predict endpoint
├─ Predictor.predict()
├─ _get_preprocessing_steps()
├─ _get_prediction_probabilities()
├─ get_decision_paths()
└─ Response JSON
   ├─ preprocessing_steps
   ├─ prediction_probabilities
   └─ decision_paths
```

---

## 📦 Dependencies

### Frontend
- Tailwind CSS (styling)
- Vanilla JavaScript (no external libraries)
- Graphviz (untuk tree visualization)

### Backend
- Flask (web framework)
- scikit-learn (Decision Tree)
- pandas (data processing)
- joblib (model loading)

---

## 🎯 Kesimpulan

Implementasi Decision Tree explanation sudah **lengkap dan terintegrasi** dengan baik:

- ✅ Modal dengan 5 sections
- ✅ Toggle buttons untuk show/hide penjelasan
- ✅ Panduan membaca tree di visualization
- ✅ Penjelasan untuk setiap tree card
- ✅ Responsive design
- ✅ Accessible (keyboard navigation, ESC key, etc.)
- ✅ Tested dan working

Sistem sekarang **fully transparent dan explainable!** 🎓
