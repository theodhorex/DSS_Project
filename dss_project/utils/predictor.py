"""Prediction wrapper and explanation logic.

ANXIETY LEVEL — Variable Importance & Rationale
=================================================
Target output classes: Low / Medium / High

All 13 input features are available to this tree.
Feature importances from actual retrained model (sorted descending):

1. Exam_Pressure     0.6590 — tekanan ujian adalah prediktor kecemasan terkuat
2. Social_Support    0.3076 — dukungan sosial rendah meningkatkan kecemasan
3. Screen_Time       0.0278 — paparan layar berlebih berkontribusi pada kecemasan
4. Mood_State        0.0055 — mood tense/fatigued sebagai indikator kecemasan
   (Calm=0, Neutral=1, Tense=2, Fatigued=3)
   (Fitur lain: 0.0000 — tidak digunakan oleh tree untuk anxiety_level)

Theoretical justification for key anxiety indicators:

1. Exam_Pressure — academic stressor triggering anticipatory anxiety
   (terbukti sebagai fitur paling dominan: 65.9% importance)
2. Social_Support — low support increases perceived threat / anxiety
   (31.8% importance — validasi teori)
3. Screen_Time — excessive screen exposure linked to anxiety
   (2.8% — kontribusi kecil tapi terdeteksi)
4. Mood_State — Tense / Fatigued moods correlate with anxiety states
   (0.6% — kontribusi minimal pada model ini)
5. Heart_Rate, Sleep_Hours, Caffeine_Intake — tidak digunakan oleh tree
   (model memilih split pada Exam_Pressure dan Social_Support saja)

Model: DecisionTreeClassifier (max_depth=4, min_samples_leaf=10)
       via MultiOutputClassifier.
All 13 features feed into a shared pipeline; the tree learns which
splits are most predictive for anxiety_level specifically.

Mood_State is now ordinal-encoded (Calm=0 < Neutral=1 < Tense=2 < Fatigued=3)
so tree splits on Mood_State are semantically meaningful thresholds.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.tree import export_graphviz

LOGGER = logging.getLogger(__name__)

FEATURE_MAPPING = {
    "exam_pressure": "Exam_Pressure",
    "sleep_hours": "Sleep_Hours",
    "social_support": "Social_Support",
    "heart_rate": "Heart_Rate",
    "physical_activity": "Physical_Activity",
    "assignment_load": "Assignment_Load",
    "study_hours": "Study_Hours",
    "attendance": "Attendance",
    "screen_time": "Screen_Time",
    "caffeine_intake": "Caffeine_Intake",
    "facial_emotion": "Facial_Emotion",
    "mood_state": "Mood_State",
    "reward_score": "Reward_Score",
}

TARGETS = [
    "stress_level",
    "anxiety_level",
    "final_state",
    "intervention_response",
]

CATEGORICAL_COLUMNS = [
    "Facial_Emotion",
]

ORDINAL_COLUMNS = [
    "Mood_State",
]

MOOD_STATE_MAP = {0: "Calm", 1: "Neutral", 2: "Tense", 3: "Fatigued"}
MOOD_STATE_REVERSE_MAP = {v: k for k, v in MOOD_STATE_MAP.items()}


@dataclass
class PredictionOutput:
    success: bool
    predictions: Dict[str, str]
    confidence: float
    explanation: str


class Predictor:
    """Wrapper for DSS model predictions."""

    def __init__(self, model_path: str) -> None:
        self.model_path = model_path
        self.pipeline = self._load_model()
        self.is_ready = self.pipeline is not None
        self._tree_cache: Dict[str, str] | None = None
        self._feature_names_cache: List[str] | None = None

    def _load_model(self) -> Any:
        try:
            return joblib.load(self.model_path)
        except Exception as exc:  # noqa: BLE001
            LOGGER.error("Failed to load model: %s", exc)
            return None

    def _prepare_frame(self, payload: Dict[str, Any]) -> pd.DataFrame:
        mapped = {FEATURE_MAPPING[key]: payload[key] for key in FEATURE_MAPPING}
        return pd.DataFrame([mapped])

    def _get_preprocessor(self) -> Any:
        return self.pipeline.named_steps["preprocessor"]

    def _get_feature_names(self) -> List[str]:
        if self._feature_names_cache is not None:
            return self._feature_names_cache

        preprocessor = self._get_preprocessor()
        input_features = list(preprocessor.feature_names_in_)
        raw_names = preprocessor.get_feature_names_out(input_features)
        formatted = [self._format_feature_label(name) for name in raw_names]
        self._feature_names_cache = list(formatted)
        return self._feature_names_cache

    def _format_feature_label(self, raw_name: str) -> str:
        name = raw_name.split("__", 1)[-1]
        for column in CATEGORICAL_COLUMNS:
            if name.startswith(f"{column}_"):
                category = name[len(column) + 1 :]
                return f"{column}={category}"
        if name in ORDINAL_COLUMNS:
            mapping_str = ",".join(f"{k}={v}" for k, v in MOOD_STATE_MAP.items())
            return f"{name} ({mapping_str})"
        return name

    def _split_onehot(self, feature_name: str) -> Tuple[str, str] | None:
        for column in CATEGORICAL_COLUMNS:
            prefix = f"{column}="
            if feature_name.startswith(prefix):
                return column, feature_name[len(prefix) :]
        return None

    def _lookup_ordinal(self, feature_name: str, value: float) -> str | None:
        base = feature_name.split(" ")[0]
        if base in ORDINAL_COLUMNS:
            nearest = int(round(value))
            return MOOD_STATE_MAP.get(nearest, str(value))
        return None

    def _format_decision_step(
        self,
        feature_name: str,
        value: float,
        threshold: float,
        is_left: bool,
    ) -> str:
        direction = "left" if is_left else "right"
        onehot = self._split_onehot(feature_name)
        if onehot:
            column, category = onehot
            is_match = value > 0.5
            result = "true" if is_match else "false"
            return f"{column} IS {category}: {result} -> {direction}"

        ordinal_mood = self._lookup_ordinal(feature_name, value)
        if ordinal_mood:
            base = feature_name.split(" ")[0]
            return (
                f"{base} <= {threshold:.2f} "
                f"(value={value:.2f} -> {ordinal_mood}) -> {direction}"
            )

        return (
            f"{feature_name} <= {threshold:.2f} "
            f"(value={value:.2f}) -> {direction}"
        )

    def _confidence(self, probas: List[np.ndarray]) -> float:
        max_probs = [float(np.max(prob)) for prob in probas if prob.size]
        if not max_probs:
            return 0.0
        return float(np.mean(max_probs))

    def _get_prediction_probabilities(self, frame: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Extract probabilities for each target and class."""
        try:
            probas = self.pipeline.predict_proba(frame)
        except (AttributeError, TypeError):
            return {}

        estimators = self.pipeline.named_steps["model"].estimators_
        result = {}

        for target, estimator, proba in zip(TARGETS, estimators, probas):
            class_probs = {}
            for class_label, prob_value in zip(estimator.classes_, proba[0]):
                class_probs[str(class_label)] = round(float(prob_value), 4)
            result[target] = class_probs

        return result

    def _explanation(self, predictions: Dict[str, Any]) -> str:
        stress = predictions.get("stress_level", "Low")
        anxiety = predictions.get("anxiety_level", "Low")
        final = predictions.get("final_state", "Relaxed")
        intervention = predictions.get("intervention_response", "Neutral")

        if stress == "High" or anxiety == "High":
            tier = "high"
        elif stress == "Medium" or anxiety == "Medium":
            tier = "medium"
        else:
            tier = "low"

        if tier == "high":
            stress_part = (
                f"Tingkat stres terdeteksi {'tinggi' if stress == 'High' else 'sedang'} "
                f"dan tingkat kecemasan {'tinggi' if anxiety == 'High' else 'sedang'}."
            )
            state_part = "Status akhir menunjukkan kondisi yang memerlukan perhatian segera."
            if intervention == "Positive":
                action_part = (
                    "Sangat disarankan untuk segera mencari dukungan dari konselor, "
                    "dosen pembimbing, atau orang-orang terdekat."
                )
            elif intervention == "Neutral":
                action_part = (
                    "Disarankan untuk mulai mengurangi beban akademik dan "
                    "meningkatkan waktu istirahat."
                )
            else:
                action_part = (
                    "Kondisi memerlukan evaluasi menyeluruh. "
                    "Pertimbangkan untuk berkonsultasi dengan profesional kesehatan mental."
                )
        elif tier == "medium":
            stress_part = (
                f"Tingkat stres berada di level {'sedang' if stress == 'Medium' else 'rendah'} "
                f"dengan kecemasan {'sedang' if anxiety == 'Medium' else 'rendah'}."
            )
            if final == "Neutral":
                state_part = "Status akhir menunjukkan kondisi yang perlu diperhatikan."
            else:
                state_part = "Status akhir menunjukkan kondisi yang cukup stabil namun perlu dipantau."
            action_part = (
                "Disarankan untuk mengatur ulang prioritas, "
                "menambah waktu relaksasi, dan menjaga keseimbangan aktivitas harian."
            )
        else:  # low
            stress_part = "Tingkat stres dan kecemasan berada di level rendah."
            state_part = "Status akhir menunjukkan kondisi yang rileks dan sehat."
            action_part = (
                "Pertahankan rutinitas positif yang sudah berjalan dengan baik."
            )

        return f"{stress_part} {state_part} {action_part}"

    def _override_final_state(self, predictions: Dict[str, str]) -> Dict[str, str]:
        stress = predictions.get("stress_level", "Low")
        anxiety = predictions.get("anxiety_level", "Low")
        final = predictions.get("final_state", "Relaxed")

        if stress == "High" or anxiety == "High":
            if final == "Relaxed":
                predictions["final_state"] = "Stress"

        elif stress == "Medium" and anxiety == "Medium":
            if final == "Relaxed":
                predictions["final_state"] = "Neutral"

        elif stress == "Medium" and anxiety == "Low":
            if final == "Relaxed":
                predictions["final_state"] = "Neutral"

        if stress == "Low" and anxiety == "Low":
            if final == "Stress":
                predictions["final_state"] = "Relaxed"

        return predictions

    def _get_preprocessing_steps(self, payload: Dict[str, Any], frame: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate detailed preprocessing steps for transparency."""
        steps = []

        steps.append({
            "step": 1,
            "name": "Input Values",
            "description": "Raw input dari form",
            "data": payload
        })

        preprocessor = self._get_preprocessor()
        try:
            transformed = preprocessor.transform(frame)
            feature_names = self._get_feature_names()

            steps.append({
                "step": 2,
                "name": "Feature Preprocessing",
                "description": "Setelah normalisasi, imputation, dan encoding",
                "features": feature_names,
                "sample_values": [float(v) for v in transformed[0]]
            })
        except Exception as e:
            LOGGER.warning("Could not extract preprocessing details: %s", e)

        return steps

    def _build_decision_path(
        self, estimator: Any, feature_names: List[str], sample: np.ndarray
    ) -> List[str]:
        tree = estimator.tree_
        node = 0
        steps: List[str] = []
        while tree.feature[node] != -2:
            feature_index = tree.feature[node]
            threshold = tree.threshold[node]
            value = float(sample[feature_index])
            is_left = value <= threshold
            feature_name = feature_names[feature_index]
            steps.append(
                self._format_decision_step(feature_name, value, threshold, is_left)
            )
            node = tree.children_left[node] if is_left else tree.children_right[node]
        return steps

    def get_tree_dots(self) -> Dict[str, str]:
        if self._tree_cache is not None:
            return self._tree_cache

        if not self.pipeline:
            return {}

        feature_names = self._get_feature_names()
        estimators = self.pipeline.named_steps["model"].estimators_
        trees: Dict[str, str] = {}
        for target, estimator in zip(TARGETS, estimators):
            class_names = [str(label) for label in estimator.classes_]
            dot = export_graphviz(
                estimator,
                feature_names=feature_names,
                class_names=class_names,
                filled=True,
                rounded=True,
                proportion=False,
                impurity=False,
            )
            trees[target] = dot

        self._tree_cache = trees
        return trees

    def get_decision_paths(self, payload: Dict[str, Any]) -> Dict[str, List[str]]:
        if not self.pipeline:
            return {}

        frame = self._prepare_frame(payload)
        preprocessor = self._get_preprocessor()
        transformed = preprocessor.transform(frame)
        sample = np.asarray(transformed)[0]
        feature_names = self._get_feature_names()

        estimators = self.pipeline.named_steps["model"].estimators_
        paths: Dict[str, List[str]] = {}
        for target, estimator in zip(TARGETS, estimators):
            paths[target] = self._build_decision_path(
                estimator, feature_names, sample
            )
        return paths

    def get_feature_importances(self) -> Dict[str, Dict[str, float]]:
        if not self.pipeline:
            return {}

        raw_names = list(self.pipeline.named_steps["preprocessor"].feature_names_in_)
        feature_names_out = self._get_feature_names()

        estimators = self.pipeline.named_steps["model"].estimators_
        result: Dict[str, Dict[str, float]] = {}
        for target, estimator in zip(TARGETS, estimators):
            importances = {}
            for i, imp in enumerate(estimator.feature_importances_):
                if imp > 0:
                    fname = feature_names_out[i] if i < len(feature_names_out) else f"feature_{i}"
                    importances[fname] = round(float(imp), 4)
            sorted_imp = dict(
                sorted(importances.items(), key=lambda x: x[1], reverse=True)
            )
            result[target] = sorted_imp

        return result

    def predict(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.pipeline:
            raise RuntimeError("Model is not loaded")

        frame = self._prepare_frame(payload)
        prediction = self.pipeline.predict(frame)[0]

        probas = self.pipeline.predict_proba(frame)
        confidence = self._confidence(probas)

        predictions = dict(zip(TARGETS, prediction))
        predictions = self._override_final_state(predictions)
        recommendation = predictions.get("intervention_response", "No recommendation")
        explanation = self._explanation(predictions)
        decision_paths = self.get_decision_paths(payload)
        preprocessing_steps = self._get_preprocessing_steps(payload, frame)
        prediction_probabilities = self._get_prediction_probabilities(frame)

        output = PredictionOutput(
            success=True,
            predictions=predictions,
            confidence=round(confidence, 2),
            explanation=explanation,
        )
        response = output.__dict__
        response["decision_paths"] = decision_paths
        response["preprocessing_steps"] = preprocessing_steps
        response["prediction_probabilities"] = prediction_probabilities
        return response
