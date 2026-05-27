const validationRules = {
  stress_score: { min: 0, max: 100, type: "number" },
  anxiety_score: { min: 0, max: 100, type: "number" },
  reward_score: { min: 0, max: 100, type: "number" },
  attendance: { min: 0, max: 100, type: "number" },
  exam_pressure: { min: 0, max: 10, type: "number" },
  sleep_hours: { min: 0, max: 24, type: "number", step: 0.5 },
  social_support: { min: 0, max: 10, type: "number" },
  heart_rate: { min: 40, max: 200, type: "number" },
  physical_activity: { min: 0, max: 10, type: "number" },
  assignment_load: { min: 0, max: 10, type: "number" },
  study_hours: { min: 0, max: 24, type: "number", step: 0.5 },
  screen_time: { min: 0, max: 24, type: "number", step: 0.5 },
  facial_emotion: {
    type: "select",
    options: ["Happy", "Sad", "Angry", "Neutral", "Surprised"],
  },
  mood_state: {
    type: "select",
    options: ["Happy", "Sad", "Anxious", "Neutral", "Excited"],
  },
  intervention_response: {
    type: "select",
    options: ["Positive", "Negative", "Neutral"],
  },
};

const TARGETS = [
  "stress_level",
  "anxiety_level",
  "final_state",
  "intervention_response",
];

const PATH_EMPTY_TEXT = "Klik prediksi untuk melihat jalur keputusan.";
const KEY_FACTOR_EMPTY = "Faktor utama akan muncul setelah prediksi.";
const RECOMMENDATION_EMPTY = "Rekomendasi akan muncul setelah prediksi.";

const STEP_INFO = [
  { step: 1, name: "Metrik Psikologis" },
  { step: 2, name: "Indikator Akademik" },
  { step: 3, name: "Kesehatan Fisik" },
  { step: 4, name: "Sosial & Perilaku" },
];

let currentStep = 1;
let formElement = null;

const LEVEL_CLASSES = {
  low: ["bg-emerald-200", "text-emerald-900"],
  medium: ["bg-amber-200", "text-amber-900"],
  high: ["bg-orange-200", "text-orange-900"],
  critical: ["bg-red-200", "text-red-900"],
};

const ALL_LEVEL_CLASSES = Object.values(LEVEL_CLASSES).flat();

const ACTION_RECOMMENDATIONS = {
  low: [
    "Pertahankan rutinitas tidur dan olahraga yang sudah konsisten.",
    "Jaga jadwal belajar agar tetap stabil tanpa lembur berlebihan.",
    "Terus cek mood dan lakukan refleksi singkat tiap minggu.",
  ],
  medium: [
    "Atur ulang prioritas tugas agar beban tidak menumpuk.",
    "Tambah sesi relaksasi singkat 10-15 menit setiap hari.",
    "Cari dukungan sosial ketika mulai merasa kewalahan.",
  ],
  high: [
    "Kurangi aktivitas non-prioritas dan fokus pada pemulihan.",
    "Diskusikan beban akademik dengan dosen atau mentor.",
    "Pertimbangkan konsultasi profesional jika gejala berlanjut.",
  ],
  critical: [
    "Segera cari dukungan profesional atau layanan konseling kampus.",
    "Ambil jeda dari aktivitas berat untuk stabilisasi emosi.",
    "Libatkan orang terdekat untuk pendampingan intensif.",
  ],
};

let lastPayload = null;

function updateSliderValue(slider) {
  const display = document.querySelector(`[data-for="${slider.id}"]`);
  if (display) {
    display.textContent = slider.value;
  }
}

function getFormData(form) {
  const data = new FormData(form);
  const payload = {};
  for (const [key, value] of data.entries()) {
    if (validationRules[key]?.type === "select") {
      payload[key] = value;
    } else {
      payload[key] = Number(value);
    }
  }
  return payload;
}

function validateInputs(payload) {
  for (const [field, rules] of Object.entries(validationRules)) {
    const value = payload[field];
    if (value === undefined || value === null || value === "") {
      return `Kolom ${field} wajib diisi.`;
    }

    if (rules.type === "select") {
      if (!rules.options.includes(value)) {
        return `Nilai untuk ${field} tidak valid.`;
      }
      continue;
    }

    if (Number.isNaN(value)) {
      return `Kolom ${field} harus berupa angka.`;
    }

    if (value < rules.min || value > rules.max) {
      return `Kolom ${field} harus di antara ${rules.min} dan ${rules.max}.`;
    }
  }
  return "";
}

function clearError() {
  const errorMessage = document.getElementById("errorMessage");
  if (errorMessage) {
    errorMessage.hidden = true;
  }
}

function validateStepPanel(panel) {
  if (!panel || !formElement) {
    return true;
  }

  const payload = getFormData(formElement);
  const fields = panel.querySelectorAll("input[name], select[name]");

  for (const field of fields) {
    const name = field.name;
    const rules = validationRules[name];
    if (!rules) {
      continue;
    }

    const focusTarget =
      field.type === "hidden"
        ? field.closest(".dropdown")?.querySelector(".dropdown-trigger")
        : field;

    const value = payload[name];
    if (value === undefined || value === null || value === "") {
      showError(`Kolom ${name} wajib diisi.`);
      focusTarget?.focus();
      return false;
    }

    if (rules.type === "select") {
      if (!rules.options.includes(value)) {
        showError(`Nilai untuk ${name} tidak valid.`);
        focusTarget?.focus();
        return false;
      }
      continue;
    }

    if (Number.isNaN(value)) {
      showError(`Kolom ${name} harus berupa angka.`);
      focusTarget?.focus();
      return false;
    }

    if (value < rules.min || value > rules.max) {
      showError(`Kolom ${name} harus di antara ${rules.min} dan ${rules.max}.`);
      focusTarget?.focus();
      return false;
    }
  }

  return true;
}

function setupDropdowns() {
  const dropdowns = document.querySelectorAll(".dropdown");
  if (!dropdowns.length) {
    return;
  }

  const closeAll = (except) => {
    dropdowns.forEach((dropdown) => {
      if (dropdown !== except) {
        dropdown.classList.remove("is-open");
      }
    });
  };

  dropdowns.forEach((dropdown) => {
    const trigger = dropdown.querySelector(".dropdown-trigger");
    const label = dropdown.querySelector(".dropdown-label");
    const options = dropdown.querySelectorAll(".dropdown-option");
    const hiddenInput = dropdown.querySelector("input[type='hidden']");

    if (!trigger || !label || !hiddenInput || !options.length) {
      return;
    }

    const setValue = (value, text) => {
      hiddenInput.value = value;
      dropdown.dataset.value = value;
      label.textContent = text;
      options.forEach((option) => {
        option.classList.toggle("is-selected", option.dataset.value === value);
      });
    };

    const initialValue = hiddenInput.value || dropdown.dataset.value;
    const initialOption = Array.from(options).find(
      (option) => option.dataset.value === initialValue
    );
    if (initialOption) {
      setValue(initialOption.dataset.value, initialOption.textContent);
    }

    trigger.addEventListener("click", (event) => {
      event.stopPropagation();
      const willOpen = !dropdown.classList.contains("is-open");
      closeAll(dropdown);
      dropdown.classList.toggle("is-open", willOpen);
    });

    options.forEach((option) => {
      option.addEventListener("click", (event) => {
        event.preventDefault();
        setValue(option.dataset.value, option.textContent);
        dropdown.classList.remove("is-open");
      });
    });
  });

  document.addEventListener("click", () => closeAll());
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeAll();
    }
  });
}

function validateCurrentStep() {
  const panel = document.querySelector(
    `.step-panel[data-step="${currentStep}"]`
  );
  return validateStepPanel(panel);
}

function setActiveStep(step) {
  const totalSteps = STEP_INFO.length;
  const nextStep = Math.min(Math.max(step, 1), totalSteps);
  currentStep = nextStep;

  const panels = document.querySelectorAll(".step-panel");
  panels.forEach((panel) => {
    const isActive = Number(panel.dataset.step) === currentStep;
    panel.classList.toggle("hidden", !isActive);
  });

  const dots = document.querySelectorAll(".step-dot");
  dots.forEach((dot) => {
    const dotStep = Number(dot.dataset.step);
    dot.classList.toggle("is-active", dotStep === currentStep);
    dot.classList.toggle("is-complete", dotStep < currentStep);
  });

  const stepCounter = document.getElementById("stepCounter");
  const stepTitle = document.getElementById("stepTitle");
  const stepProgress = document.getElementById("stepProgress");
  if (stepCounter) {
    stepCounter.textContent = `Step ${currentStep} dari ${totalSteps}`;
  }
  if (stepTitle) {
    stepTitle.textContent = STEP_INFO[currentStep - 1]?.name || "";
  }
  if (stepProgress) {
    stepProgress.style.width = `${(currentStep / totalSteps) * 100}%`;
  }

  const prevButton = document.getElementById("prevStep");
  const nextButton = document.getElementById("nextStep");
  const predictButton = document.getElementById("predictButton");
  if (prevButton) {
    prevButton.classList.toggle("hidden", currentStep === 1);
  }
  if (nextButton) {
    nextButton.classList.toggle("hidden", currentStep === totalSteps);
  }
  if (predictButton) {
    predictButton.classList.toggle("hidden", currentStep !== totalSteps);
  }
}

function setupStepper() {
  const prevButton = document.getElementById("prevStep");
  const nextButton = document.getElementById("nextStep");
  const dots = document.querySelectorAll(".step-dot");

  if (prevButton) {
    prevButton.addEventListener("click", () => {
      clearError();
      setActiveStep(currentStep - 1);
    });
  }

  if (nextButton) {
    nextButton.addEventListener("click", () => {
      if (!validateCurrentStep()) {
        return;
      }
      clearError();
      setActiveStep(currentStep + 1);
    });
  }

  dots.forEach((dot) => {
    dot.addEventListener("click", () => {
      const target = Number(dot.dataset.step);
      if (target > currentStep && !validateCurrentStep()) {
        return;
      }
      clearError();
      setActiveStep(target);
    });
  });

  setActiveStep(currentStep);
}

async function submitPrediction(event) {
  event.preventDefault();

  const form = event.target;
  const results = document.getElementById("results");
  const errorMessage = document.getElementById("errorMessage");

  if (errorMessage) {
    errorMessage.hidden = true;
  }
  results.hidden = true;

  if (currentStep !== STEP_INFO.length) {
    if (!validateCurrentStep()) {
      return;
    }
    clearError();
    setActiveStep(currentStep + 1);
    return;
  }

  const payload = getFormData(form);
  const validationError = validateInputs(payload);
  if (validationError) {
    showError(validationError);
    return;
  }

  lastPayload = payload;
  setLoading(true);
  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const message = errorData.error || `HTTP error ${response.status}`;
      throw new Error(message);
    }

    const result = await response.json();
    if (!result.success) {
      throw new Error(result.error || "Prediksi gagal");
    }

    displayResults(result);
  } catch (error) {
    showError(error.message || "Terjadi kesalahan");
  } finally {
    setLoading(false);
  }
}

function displayResults(data) {
  const results = document.getElementById("results");
  const quickGuide = document.getElementById("quickGuide");
  const predictions = data.predictions || {};

  const stressBadge = document.getElementById("stressBadge");
  const anxietyBadge = document.getElementById("anxietyBadge");
  const finalState = document.getElementById("finalState");
  const recommendation = document.getElementById("recommendation");
  const confidenceValue = document.getElementById("confidenceValue");
  const confidenceBar = document.getElementById("confidenceBar");
  const explanationText = document.getElementById("explanationText");

  const stressLabel = computeLevelLabel(predictions.stress_level);
  const anxietyLabel = computeLevelLabel(predictions.anxiety_level);

  stressBadge.textContent = `Stres: ${stressLabel}`;
  anxietyBadge.textContent = `Kecemasan: ${anxietyLabel}`;

  applyLevelStyles(stressBadge, stressLabel);
  applyLevelStyles(anxietyBadge, anxietyLabel);

  finalState.textContent = predictions.final_state || "-";

  let recommText = predictions.intervention_response;
  if (!recommText || String(recommText).trim() === "") {
    recommText = "-";
  }
  recommendation.textContent = recommText;

  const confidencePercent = Math.round((data.confidence || 0) * 100);
  confidenceValue.textContent = `${confidencePercent}%`;
  confidenceBar.style.width = `${confidencePercent}%`;

  explanationText.textContent = data.explanation || "-";

  renderDecisionPaths(data.decision_paths || {});
  renderKeyFactorsModal(data.decision_paths || {});
  renderPreprocessingStepsModal(data.preprocessing_steps || []);
  renderPredictionProbabilitiesModal(data.prediction_probabilities || {});
  renderRecommendationsModal(stressLabel);

  if (quickGuide) quickGuide.hidden = true;
  results.hidden = false;
  try {
    setActiveTree('intervention_response');
  } catch (e) {}
  try { loadTrees(); } catch (e) {}
  try {
    openDetailsModalWithAllInfo();
  } catch (e) {}
}

function computeLevelLabel(level) {
  const normalized = String(level || "").toLowerCase();
  if (normalized === "medium") {
    return "Medium";
  }
  if (normalized === "high") {
    return "High";
  }
  if (normalized === "low") {
    return "Low";
  }
  return level || "-";
}

function openDetailsModalWithAllInfo() {
  const modal = document.getElementById("detailsModal");
  if (!modal) {
    return;
  }

  modal.classList.remove("hidden");
  document.body.style.overflow = "hidden";

  const infoIds = [
    "decisionTreeInfo",
    "keyFactorsInfo",
    "preprocessingInfo",
    "probabilitiesInfo",
    "recommendationInfo",
  ];

  infoIds.forEach((id) => {
    const info = modal.querySelector(`#${id}`);
    if (info) {
      info.classList.remove("hidden");
    }
    const button = modal.querySelector(`[data-toggle-info="${id}"]`);
    if (button) {
      button.textContent = "Sembunyikan";
    }
  });
}

function applyLevelStyles(element, level) {
  if (!element) {
    return;
  }

  const normalized = String(level || "").toLowerCase();
  const classes = LEVEL_CLASSES[normalized] || LEVEL_CLASSES.low;
  element.classList.remove(...ALL_LEVEL_CLASSES);
  element.classList.add(...classes);
}

function renderDecisionPaths(paths) {
  TARGETS.forEach((target) => {
    const list = document.getElementById(`path-${target}`);
    if (!list) {
      return;
    }

    list.innerHTML = "";
    const steps = paths[target] || [];
    if (!steps.length) {
      const item = document.createElement("li");
      item.textContent = PATH_EMPTY_TEXT;
      item.className = "text-sm text-slate-500";
        list.appendChild(item);
        try { applyRevealToElement(item); } catch (e) {}
      return;
    }

    steps.forEach((step) => {
      const item = document.createElement("li");
      item.textContent = step;
      item.className =
        "rounded-xl border-2 border-ink bg-white px-3 py-2 text-sm text-slate-700";
        list.appendChild(item);
        try { applyRevealToElement(item); } catch (e) {}
    });
  });
}

function renderKeyFactors(paths) {
  const list = document.getElementById("keyFactors");
  if (!list) {
    return;
  }

  list.innerHTML = "";
  const steps = paths.stress_level || paths.final_state || [];
  const factors = steps.slice(0, 4);

  if (!factors.length) {
    const item = document.createElement("li");
    item.textContent = KEY_FACTOR_EMPTY;
    item.className = "text-sm text-slate-500";
      list.appendChild(item);
      try { applyRevealToElement(item); } catch (e) {}
    return;
  }

  factors.forEach((step) => {
    const item = document.createElement("li");
    item.textContent = step;
    item.className =
      "rounded-xl border-2 border-ink bg-white px-3 py-2 text-sm text-slate-700";
      list.appendChild(item);
      try { applyRevealToElement(item); } catch (e) {}
  });
}

function renderRecommendations(level) {
  const list = document.getElementById("recommendationList");
  if (!list) {
    return;
  }

  list.innerHTML = "";
  const normalized = String(level || "").toLowerCase();
  const items = ACTION_RECOMMENDATIONS[normalized];

  if (!items) {
    const item = document.createElement("li");
    item.textContent = RECOMMENDATION_EMPTY;
    item.className = "text-sm text-slate-500";
      list.appendChild(item);
      try { applyRevealToElement(item); } catch (e) {}
    return;
  }

  items.forEach((text) => {
    const item = document.createElement("li");
    item.textContent = text;
    item.className =
      "rounded-xl border-2 border-ink bg-amber-100 px-3 py-2 text-sm text-slate-900";
      list.appendChild(item);
      try { applyRevealToElement(item); } catch (e) {}
  });
}

function renderKeyFactorsModal(paths) {
  const list = document.getElementById("keyFactorsModal");
  if (!list) {
    return;
  }

  list.innerHTML = "";
  const steps = paths.stress_level || paths.final_state || [];
  const factors = steps.slice(0, 4);

  if (!factors.length) {
    const item = document.createElement("li");
    item.textContent = KEY_FACTOR_EMPTY;
    item.className = "text-sm text-slate-500";
      list.appendChild(item);
      try { applyRevealToElement(item); } catch (e) {}
    return;
  }

  factors.forEach((step) => {
    const item = document.createElement("li");
    item.textContent = step;
    item.className =
      "rounded-xl border-2 border-ink bg-white px-3 py-2 text-sm text-slate-700";
      list.appendChild(item);
      try { applyRevealToElement(item); } catch (e) {}
  });
}

function renderPreprocessingStepsModal(steps) {
  const container = document.getElementById("preprocessingStepsModal");
  if (!container) {
    return;
  }

  container.innerHTML = "";
  if (!steps || steps.length === 0) {
    container.innerHTML = '<p class="text-sm text-slate-500">Tidak ada data preprocessing.</p>';
    return;
  }

  steps.forEach((step, idx) => {
    const stepDiv = document.createElement("div");
    stepDiv.className = "rounded-xl border-2 border-ink bg-blue-50 p-4";

    let content = `<p class="font-semibold text-sm text-blue-900">Step ${step.step}: ${step.name}</p>`;
    content += `<p class="text-xs text-blue-700 mt-1">${step.description}</p>`;

    if (step.step === 1) {
      content += '<p class="text-xs text-blue-600 mt-2 italic">Ini adalah nilai mentah yang Anda input dari form. Belum ada transformasi apapun.</p>';
    } else if (step.step === 2) {
      content += '<p class="text-xs text-blue-600 mt-2 italic">Data sudah melalui normalisasi (scaling), imputation (mengisi missing values), dan encoding (mengubah kategori menjadi angka). Ini adalah format yang digunakan oleh Decision Tree model.</p>';
    }

    if (step.data) {
      const keys = Object.keys(step.data).slice(0, 5);
      content += '<div class="mt-2 text-xs text-blue-800 bg-white rounded p-2">';
      keys.forEach(key => {
        const value = step.data[key];
        content += `<div><strong>${key}:</strong> ${typeof value === 'number' ? value.toFixed(2) : value}</div>`;
      });
      if (Object.keys(step.data).length > 5) {
        content += `<div class="text-blue-600 italic">... dan ${Object.keys(step.data).length - 5} field lainnya</div>`;
      }
      content += '</div>';
    }

    if (step.features && step.sample_values) {
      content += '<div class="mt-2 text-xs text-blue-800 bg-white rounded p-2">';
      content += '<strong>Sample Features (setelah preprocessing):</strong><br>';
      for (let i = 0; i < Math.min(5, step.features.length); i++) {
        content += `<div>${step.features[i]}: ${step.sample_values[i].toFixed(4)}</div>`;
      }
      if (step.features.length > 5) {
        content += `<div class="text-blue-600 italic">... dan ${step.features.length - 5} features lainnya</div>`;
      }
      content += '</div>';
    }

    stepDiv.innerHTML = content;
    container.appendChild(stepDiv);
    try { applyRevealToElement(stepDiv, idx); } catch (e) {}
  });
}

function renderPredictionProbabilitiesModal(probabilities) {
  const container = document.getElementById("predictionProbabilitiesModal");
  if (!container) {
    return;
  }

  container.innerHTML = "";
  if (!probabilities || Object.keys(probabilities).length === 0) {
    container.innerHTML = '<p class="text-sm text-slate-500">Tidak ada data probabilitas.</p>';
    return;
  }

  const targetLabels = {
    'stress_level': 'Tingkat Stres',
    'anxiety_level': 'Tingkat Kecemasan',
    'final_state': 'Status Akhir',
    'intervention_response': 'Respons Intervensi'
  };

  const targetExplanations = {
    'stress_level': 'Probabilitas tingkat stres Anda. Semakin tinggi persentase "High", semakin besar kemungkinan Anda mengalami stres tinggi.',
    'anxiety_level': 'Probabilitas tingkat kecemasan Anda. Menunjukkan seberapa yakin model dengan prediksi level kecemasan.',
    'final_state': 'Probabilitas status akhir kesehatan mental Anda. Bisa "Relaxed", "Neutral", atau "Stress".',
    'intervention_response': 'Probabilitas respons terhadap intervensi. Menunjukkan apakah intervensi akan "Positive", "Neutral", atau "Negative".'
  };

  Object.entries(probabilities).forEach(([target, classProbs], idx) => {
    const targetDiv = document.createElement("div");
    targetDiv.className = "rounded-xl border-2 border-ink bg-purple-50 p-4";

    let content = `<p class="font-semibold text-sm text-purple-900">${targetLabels[target] || target}</p>`;
    content += `<p class="text-xs text-purple-700 mt-1">${targetExplanations[target] || 'Probabilitas prediksi untuk target ini.'}</p>`;
    content += '<div class="mt-3 space-y-2">';

    const sortedClasses = Object.entries(classProbs).sort((a, b) => b[1] - a[1]);
    sortedClasses.forEach(([className, prob]) => {
      const percentage = Math.round(prob * 100);
      const barWidth = Math.max(percentage, 5);
      content += `
        <div class="text-xs">
          <div class="flex justify-between mb-1">
            <span class="text-purple-900 font-medium">${className}</span>
            <span class="text-purple-700">${percentage}%</span>
          </div>
          <div class="w-full bg-white border border-purple-200 rounded h-2">
            <div class="bg-purple-500 h-2 rounded" style="width: ${barWidth}%"></div>
          </div>
        </div>
      `;
    });

    content += '</div>';
    content += '<p class="text-xs text-purple-600 mt-2 italic">Sumber: Dihitung dari predict_proba() method DecisionTreeClassifier.</p>';
    targetDiv.innerHTML = content;
    container.appendChild(targetDiv);
    try { applyRevealToElement(targetDiv, idx); } catch (e) {}
  });
}

function renderRecommendationsModal(level) {
  const list = document.getElementById("recommendationListModal");
  if (!list) {
    return;
  }

  list.innerHTML = "";
  const normalized = String(level || "").toLowerCase();
  const items = ACTION_RECOMMENDATIONS[normalized];

  if (!items) {
    const item = document.createElement("li");
    item.textContent = RECOMMENDATION_EMPTY;
    item.className = "text-sm text-slate-500";
      list.appendChild(item);
      try { applyRevealToElement(item); } catch (e) {}
    return;
  }

  items.forEach((text) => {
    const item = document.createElement("li");
    item.textContent = text;
    item.className =
      "rounded-xl border-2 border-ink bg-amber-100 px-3 py-2 text-sm text-slate-900";
      list.appendChild(item);
      try { applyRevealToElement(item); } catch (e) {}
  });
}

function setLoading(isLoading) {
  const loading = document.getElementById("loading");
  const submitButton = document.getElementById("predictButton");

  if (loading) {
    loading.hidden = !isLoading;
  }

  if (submitButton) {
    submitButton.disabled = isLoading;
    submitButton.classList.toggle("opacity-60", isLoading);
    submitButton.classList.toggle("cursor-not-allowed", isLoading);
  }
}

function showError(message) {
  const errorMessage = document.getElementById("errorMessage");
  if (!errorMessage) {
    return;
  }
  errorMessage.textContent = message;
  errorMessage.hidden = false;
}

function setTreeStatus(target, message) {
  const status = document.getElementById(`treeStatus-${target}`);
  if (status) {
    status.textContent = message;
  }
}

function renderTreeGraph(target, dot) {
  const container = document.getElementById(`tree-${target}`);
  if (!container) {
    return;
  }

  if (!dot || typeof dot !== 'string') {
    setTreeStatus(target, "Tidak ada data");
    container.innerHTML = `
      <div class="p-6 text-sm text-slate-600">
        <p>Pohon keputusan untuk target ini belum tersedia.</p>
        <p class="mt-3">Jika Anda baru saja memperbarui model, klik tombol di bawah untuk memuat ulang pohon.</p>
        <div class="mt-4">
          <button class="rounded-full border-2 border-ink bg-white px-4 py-2 text-xs font-bold shadow-brutal-sm" data-reload-tree>Muati Ulang Pohon</button>
        </div>
      </div>`;
    const btn = container.querySelector('[data-reload-tree]');
    if (btn) {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        setTreeStatus(target, 'Memuat...');
        loadTrees();
      });
    }
    return;
  }

  function parseDOT(dotString) {
    const nodes = {};
    const edges = [];

    // Extract nodes dengan label
    const nodeRegex = /(\w+)\s*\[\s*label="([^"]+)"[^\]]*\]/g;
    let match;

    while ((match = nodeRegex.exec(dotString)) !== null) {
      nodes[match[1]] = {
        id: match[1],
        label: match[2]
      };
    }

    // Extract edges
    const edgeRegex = /(\w+)\s*->\s*(\w+)/g;
    while ((match = edgeRegex.exec(dotString)) !== null) {
      edges.push({
        from: match[1],
        to: match[2]
      });
    }

    return { nodes, edges };
  }

  async function renderWithViz(dotString) {
    if (typeof Viz !== "function") {
      return false;
    }

    try {
      const viz = new Viz();
      const svg = await viz.renderSVGElement(dotString);
      container.innerHTML = "";
      container.appendChild(svg);
      setTreeStatus(target, "Siap");
      return true;
    } catch (error) {
      console.warn("Viz render failed, falling back to parsed tree:", error);
      return false;
    }
  }

  function organizeTreeColumns(nodes, edges) {
    if (Object.keys(nodes).length === 0) {
      return { "Tree": Object.values(nodes).map(n => n.label) };
    }

    // Find root (node with no incoming edges)
    const incomingEdges = new Set();
    edges.forEach(e => incomingEdges.add(e.to));

    const rootId = Object.keys(nodes).find(id => !incomingEdges.has(id));

    // BFS to assign levels
    const levels = {};
    const visited = new Set();
    const queue = [[rootId, 0]];

    while (queue.length > 0) {
      const [nodeId, level] = queue.shift();

      if (visited.has(nodeId)) continue;
      visited.add(nodeId);

      if (!levels[level]) levels[level] = [];
      levels[level].push(nodes[nodeId].label);

      // Add children
      edges
        .filter(e => e.from === nodeId)
        .forEach(e => {
          if (!visited.has(e.to)) {
            queue.push([e.to, level + 1]);
          }
        });
    }

    // Convert to column format
    const columns = {};
    const levelKeys = Object.keys(levels).sort((a, b) => parseInt(a) - parseInt(b));

    levelKeys.forEach((levelIdx, colIdx) => {
      const colName = `Column ${colIdx + 1}`;
      columns[colName] = levels[levelIdx];
    });

    return columns;
  }

  function renderTreeGrid(columns) {
    let html = '';

    for (const [columnTitle, items] of Object.entries(columns)) {
      html += `<div class="tree-column">`;
      html += `<div class="tree-column-title">${columnTitle}</div>`;

      items.forEach((item) => {
        // escape HTML then convert both escaped "\\n" and real newlines into <br>
        let escaped = String(item)
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;");
        const withBreaks = escaped.replace(/\\n/g, "<br>").replace(/\n/g, "<br>");
        html += `<div class="tree-item"><div class="tree-item-content">${withBreaks}</div></div>`;
      });

      html += `</div>`;
    }

    return html;
  }

  renderWithViz(dot)
    .then((vizRendered) => {
      if (vizRendered) {
        return;
      }

      const { nodes, edges } = parseDOT(dot);
      const columns = organizeTreeColumns(nodes, edges);
      const html = renderTreeGrid(columns);

      container.innerHTML = html;
      container.classList.add("tree-grid");
      setTreeStatus(target, "Siap");
    })
    .catch((error) => {
      console.error("Tree render error:", error);
      container.innerHTML = '<div class="text-slate-500">Gagal merender tree</div>';
      setTreeStatus(target, "Gagal");
    });
}

async function loadTrees() {
  try {
    const response = await fetch("/tree");
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    const data = await response.json();
    if (!data.success) {
      throw new Error(data.error || "Gagal memuat tree");
    }

    TARGETS.forEach((target) => {
      const dot = data.trees?.[target];
      if (!dot) {
        setTreeStatus(target, "Tidak ada data");
        return;
      }
      renderTreeGraph(target, dot);
    });
  } catch (error) {
    TARGETS.forEach((target) => setTreeStatus(target, "Gagal"));
  }
}

function renderDatasetTable(columns, rows) {
  const table = document.getElementById("datasetTable");
  if (!table) {
    return;
  }

  const headerRow = table.querySelector("thead tr");
  const body = table.querySelector("tbody");

  headerRow.innerHTML = "";
  body.innerHTML = "";

  columns.forEach((column) => {
    const th = document.createElement("th");
    th.textContent = column;
    th.className =
      "whitespace-nowrap border-b-2 border-ink px-3 py-2 text-left";
    headerRow.appendChild(th);
  });

  rows.forEach((row, index) => {
    const tr = document.createElement("tr");
    tr.className = index % 2 === 0 ? "bg-white" : "bg-slate-50";
    columns.forEach((column) => {
      const td = document.createElement("td");
      const value = row[column];
      td.textContent = value === null || value === undefined ? "-" : value;
      td.className =
        "whitespace-nowrap border-b border-slate-200 px-3 py-2 text-sm text-slate-700";
      tr.appendChild(td);
    });
      body.appendChild(tr);
      try { applyRevealToElement(tr, index); } catch (e) {}
  });
}

async function loadDatasetPreview() {
  const summary = document.getElementById("datasetSummary");
  const modalSummary = document.getElementById("datasetModalSummary");

  try {
    const response = await fetch("/dataset-preview");
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    const data = await response.json();
    if (!data.success) {
      throw new Error(data.error || "Gagal memuat dataset");
    }

    renderDatasetTable(data.columns || [], data.rows || []);

    const message = `Menampilkan ${data.rows?.length || 0} dari ${
      data.total_rows || 0
    } baris dataset.`;
    if (summary) {
      summary.textContent = message;
    }
    if (modalSummary) {
      modalSummary.textContent = message;
    }
  } catch (error) {
    if (summary) {
      summary.textContent = "Dataset tidak tersedia.";
    }
    if (modalSummary) {
      modalSummary.textContent = "Dataset tidak tersedia.";
    }
  }
}

function setActiveTree(target) {
  const cards = document.querySelectorAll(".tree-card");
  const tabs = document.querySelectorAll(".tree-tab");

  cards.forEach((card) => {
    const isActive = card.dataset.target === target;
    card.classList.toggle("hidden", !isActive);
    card.classList.toggle("flex", isActive);
  });

  tabs.forEach((tab) => {
    const isActive = tab.dataset.target === target;
    tab.setAttribute("aria-pressed", isActive ? "true" : "false");
    tab.classList.toggle("bg-sun", isActive);
    tab.classList.toggle("text-slate-900", isActive);
    tab.classList.toggle("shadow-brutal-sm", isActive);
    tab.classList.toggle("bg-white", !isActive);
    tab.classList.toggle("text-slate-700", !isActive);
  });
}

function setupTreeTabs() {
  const tabs = document.querySelectorAll(".tree-tab");
  if (!tabs.length) {
    return;
  }

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => setActiveTree(tab.dataset.target));
  });

  setActiveTree(tabs[0].dataset.target);
}

function setupDatasetModal() {
  const modal = document.getElementById("datasetModal");
  const openButtons = [
    document.getElementById("openDatasetModal"),
    document.getElementById("openDatasetModalSecondary"),
  ];
  const closeButton = document.getElementById("closeDatasetModal");

  if (!modal) {
    return;
  }

  const openModal = () => {
    modal.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  };

  const closeModal = () => {
    modal.classList.add("hidden");
    document.body.style.overflow = "";
  };

  openButtons.forEach((button) => {
    if (button) {
      button.addEventListener("click", openModal);
    }
  });

  if (closeButton) {
    closeButton.addEventListener("click", closeModal);
  }

  modal.addEventListener("click", (event) => {
    if (event.target?.dataset?.modalOverlay === "true") {
      closeModal();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeModal();
    }
  });
}

function setupDetailsModal() {
  const modal = document.getElementById("detailsModal");
  const openButton = document.getElementById("openDetailsModal");
  const closeButton = document.getElementById("closeDetailsModal");

  if (!modal) {
    return;
  }

  const openModal = () => {
    modal.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  };

  const closeModal = () => {
    modal.classList.add("hidden");
    document.body.style.overflow = "";
  };

  if (openButton) {
    openButton.addEventListener("click", openModal);
  }

  if (closeButton) {
    closeButton.addEventListener("click", closeModal);
  }

  modal.addEventListener("click", (event) => {
    if (event.target?.dataset?.modalOverlay === "true") {
      closeModal();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeModal();
    }
  });

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

function setupClearButton(form) {
  const clearButton = document.getElementById("clearForm");
  const results = document.getElementById("results");
  const errorMessage = document.getElementById("errorMessage");

  if (!clearButton || !form) {
    return;
  }

  clearButton.addEventListener("click", () => {
    form.reset();
    lastPayload = null;
    setActiveStep(1);
    clearError();

    document.querySelectorAll("input[type='range']").forEach((slider) => {
      updateSliderValue(slider);
    });

    renderDecisionPaths({});
    renderKeyFactors({});
    renderRecommendations(null);

    if (results) {
      results.hidden = true;
    }

    if (errorMessage) {
      errorMessage.hidden = true;
    }
    // show quick guide again when form is cleared
    try {
      const quickGuide = document.getElementById("quickGuide");
      if (quickGuide) quickGuide.hidden = false;
    } catch (e) {}
  });
}

// Global reveal observer and helpers so dynamic elements can be observed
window._revealObserver = null;
window._revealPrefersReducedMotion = false;

function applyRevealToElement(item, idx) {
  if (!item) return;
  const idxVal = typeof idx === "number" ? idx : 0;
  const delayClass = `reveal-delay-${(idxVal % 4) + 1}`;
  item.classList.add("reveal", delayClass);

  if (window._revealPrefersReducedMotion || !window._revealObserver) {
    item.classList.add("is-visible");
    return;
  }

  try {
    window._revealObserver.observe(item);
  } catch (e) {
    item.classList.add("is-visible");
      // apply reveal to tree items created via innerHTML
      const treeItems = container.querySelectorAll('.tree-item');
      treeItems.forEach((el, idx) => { try { applyRevealToElement(el, idx); } catch (e) {} });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("predictionForm");
  const sliders = document.querySelectorAll("input[type='range']");

  formElement = form;

  // ===== REVEAL ANIMATIONS (Reference style) =====
  const revealItems = document.querySelectorAll(
    ".reveal, .card-animate, .section-animate"
  );
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  window._revealPrefersReducedMotion = prefersReducedMotion;

  if (prefersReducedMotion || !("IntersectionObserver" in window)) {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  } else {
    revealItems.forEach((item, idx) => {
      const delayClass = `reveal-delay-${(idx % 4) + 1}`;
      item.classList.add(delayClass);
    });

    window._revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            try {
              window._revealObserver.unobserve(entry.target);
            } catch (e) {}
          }
        });
      },
      {
        threshold: 0.2,
        rootMargin: "0px 0px -10% 0px",
      }
    );

    revealItems.forEach((item) => window._revealObserver.observe(item));
  }

  // Auto-apply reveal classes to common site containers that may have been missed
  try {
    const autoSelectors = [
      "header",
      "main",
      "section",
      ".rounded-2xl",
      ".rounded-3xl",
      ".tree-card",
      ".tree-column",
      ".dropdown",
      ".step-panel",
      ".card-animate",
      ".section-animate",
    ];

    const nodes = document.querySelectorAll(autoSelectors.join(","));
    nodes.forEach((n, idx) => {
      if (!n.classList.contains("reveal") && !n.classList.contains("is-visible")) {
        applyRevealToElement(n, idx);
      }
    });
  } catch (e) {
    // noop
  }

  sliders.forEach((slider) => {
    updateSliderValue(slider);
    slider.addEventListener("input", () => updateSliderValue(slider));
  });

  if (form) {
    form.addEventListener("submit", submitPrediction);
  }

  renderDecisionPaths({});
  renderKeyFactorsModal({});
  renderPreprocessingStepsModal([]);
  renderPredictionProbabilitiesModal({});
  renderRecommendationsModal(null);
  loadTrees();
  loadDatasetPreview();
  setupTreeTabs();
  setupDatasetModal();
  setupDetailsModal();
  setupClearButton(form);
  setupStepper();
  setupDropdowns();
});
