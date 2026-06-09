"""Model training script for DSS stress prediction."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Tuple

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier, export_text

LOGGER = logging.getLogger(__name__)

FEATURES: Dict[str, List[str]] = {
    "tier_1": ["Exam_Pressure"],
    "tier_2": [
        "Sleep_Hours",
        "Social_Support",
        "Heart_Rate",
        "Physical_Activity",
    ],
    "tier_3": [
        "Assignment_Load",
        "Study_Hours",
        "Attendance",
        "Screen_Time",
        "Caffeine_Intake",
    ],
    "tier_4": [
        "Facial_Emotion",
        "Mood_State",
        "Reward_Score",
    ],
}

CATEGORICAL_ONEHOT = [
    "Facial_Emotion",
]

CATEGORICAL_ORDINAL = [
    "Mood_State",
]

MOOD_STATE_ORDER = ["Calm", "Neutral", "Tense", "Fatigued"]
ALL_CATEGORICAL = CATEGORICAL_ONEHOT + CATEGORICAL_ORDINAL

TARGETS = [
    "Stress_Level",
    "Anxiety_Level",
    "Final_State",
    "Intervention_Response",
]

DATASET_CANDIDATES = ["dataset.csv", "psychological_regulation_dataset.csv"]
MODEL_PATH = Path("model.pkl")


def _resolve_dataset_path() -> Path:
    for candidate in DATASET_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            return path
    return Path(DATASET_CANDIDATES[0])


def _get_feature_columns() -> List[str]:
    return [col for cols in FEATURES.values() for col in cols]


def _split_features(
    data: pd.DataFrame, feature_cols: List[str]
) -> Tuple[pd.DataFrame, pd.DataFrame, List[str], List[str], List[str]]:
    ordinal_cols = [col for col in CATEGORICAL_ORDINAL if col in feature_cols]
    onehot_cols = [col for col in CATEGORICAL_ONEHOT if col in feature_cols]
    all_cat = ordinal_cols + onehot_cols
    numeric_cols = [col for col in feature_cols if col not in all_cat]
    return data[feature_cols], data[TARGETS], numeric_cols, ordinal_cols, onehot_cols


def _normalize_intervention_response(data: pd.DataFrame) -> pd.DataFrame:
    if "Intervention_Response" not in data.columns:
        if "Previous_Intervention" in data.columns:
            data = data.copy()
            data["Intervention_Response"] = data["Previous_Intervention"]
        return data

    data = data.copy()
    series = data["Intervention_Response"]
    numeric_series = pd.to_numeric(series, errors="coerce")
    numeric_ratio = numeric_series.notna().sum() / len(series)

    if numeric_ratio > 0.8:
        data["Intervention_Response"] = pd.cut(
            numeric_series,
            bins=[-float("inf"), 0.33, 0.66, float("inf")],
            labels=["Negative", "Neutral", "Positive"],
        ).astype(str)
    return data


def _build_pipeline(
    numeric_cols: List[str],
    ordinal_cols: List[str],
    onehot_cols: List[str],
) -> Pipeline:
    numeric_transformer = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median"))]
    )
    transformers = []
    if numeric_cols:
        transformers.append(("num", numeric_transformer, numeric_cols))
    if ordinal_cols:
        ordinal_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                (
                    "ordinal",
                    OrdinalEncoder(
                        categories=[MOOD_STATE_ORDER],
                        handle_unknown="use_encoded_value",
                        unknown_value=-1,
                    ),
                ),
            ]
        )
        transformers.append(("cat_ordinal", ordinal_transformer, ordinal_cols))
    if onehot_cols:
        onehot_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                (
                    "onehot",
                    OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                ),
            ]
        )
        transformers.append(("cat_onehot", onehot_transformer, onehot_cols))
    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder="drop",
    )
    classifier = DecisionTreeClassifier(
        max_depth=4,
        min_samples_split=20,
        min_samples_leaf=10,
        random_state=42,
    )
    model = MultiOutputClassifier(classifier)
    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])


def _cross_validate(pipeline_template, x, y) -> None:
    from sklearn.model_selection import cross_val_score
    from sklearn.pipeline import Pipeline
    from sklearn.tree import DecisionTreeClassifier
    import numpy as np
    for idx, target in enumerate(TARGETS):
        single_pipeline = Pipeline([
            ("preprocessor", pipeline_template.named_steps["preprocessor"]),
            ("classifier", DecisionTreeClassifier(
                max_depth=4, min_samples_split=20,
                min_samples_leaf=10, random_state=42,
            )),
        ])
        scores = cross_val_score(
            single_pipeline, x, y.iloc[:, idx],
            cv=5, scoring="accuracy"
        )
        LOGGER.info(
            "CV accuracy for %s: %.4f (+/- %.4f)",
            target, scores.mean(), scores.std()
        )


def _log_metrics(y_true: pd.DataFrame, y_pred: pd.DataFrame) -> None:
    accuracies = []
    for idx, target in enumerate(TARGETS):
        target_accuracy = accuracy_score(y_true.iloc[:, idx], y_pred.iloc[:, idx])
        accuracies.append(target_accuracy)
        LOGGER.info("Accuracy for %s: %.4f", target, target_accuracy)

    if accuracies:
        LOGGER.info("Mean accuracy: %.4f", sum(accuracies) / len(accuracies))
    for idx, target in enumerate(TARGETS):
        report = classification_report(
            y_true.iloc[:, idx], y_pred.iloc[:, idx], zero_division=0
        )
        LOGGER.info("Classification report for %s:\n%s", target, report)


def _log_top_rules(pipeline: Pipeline, feature_cols: List[str]) -> None:
    preprocessor = pipeline.named_steps["preprocessor"]
    feature_names = list(preprocessor.get_feature_names_out(feature_cols))
    estimators = pipeline.named_steps["model"].estimators_
    for target, estimator in zip(TARGETS, estimators):
        rules_text = export_text(estimator, feature_names=feature_names)
        rule_lines = [line for line in rules_text.splitlines() if "class" in line]
        top_rules = rule_lines[:5]
        LOGGER.info("Top rules for %s:", target)
        for rule in top_rules:
            LOGGER.info("%s", rule)


def train() -> None:
    dataset_path = _resolve_dataset_path()
    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found. Expected one of: {DATASET_CANDIDATES}"
        )

    data = pd.read_csv(dataset_path)
    if "Intervention_Response" not in data.columns and "Previous_Intervention" in data.columns:
        LOGGER.warning(
            "Dataset is missing 'Intervention_Response'; using 'Previous_Intervention' instead."
        )
        data = data.rename(columns={"Previous_Intervention": "Intervention_Response"})
    feature_cols = _get_feature_columns()
    data = _normalize_intervention_response(data)
    missing_cols = [col for col in feature_cols + TARGETS if col not in data.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in dataset: {missing_cols}")

    x, y, numeric_cols, ordinal_cols, onehot_cols = _split_features(data, feature_cols)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=42, stratify=y[TARGETS[0]]
    )

    pipeline = _build_pipeline(numeric_cols, ordinal_cols, onehot_cols)
    pipeline.fit(x_train, y_train)
    _cross_validate(_build_pipeline(numeric_cols, ordinal_cols, onehot_cols), x, y)

    y_pred = pipeline.predict(x_test)
    y_pred_df = pd.DataFrame(y_pred, columns=TARGETS)
    _log_metrics(y_test, y_pred_df)
    _log_top_rules(pipeline, feature_cols)

    joblib.dump(pipeline, MODEL_PATH)
    LOGGER.info("Model saved to %s", MODEL_PATH)


def _configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


if __name__ == "__main__":
    _configure_logging()
    train()
