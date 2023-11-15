from flask import Flask, render_template, request

from types import SimpleNamespace

import dill
import csv
import json
import random

import numpy as np
import pandas as pd

# Load pickle files from model training phase
with open("data/gender_label_encoder.pickle", "rb") as f:
    gender_label_encoder = dill.load(f)
with open("data/age_label_encoder.pickle", "rb") as f:
    age_label_encoder = dill.load(f)
with open("data/input_processor.pickle", "rb") as f:
    input_processor = dill.load(f)
with open("data/gender_model_sc1_fit.pickle", "rb") as f:
    gender_model = dill.load(f)
with open("data/age_model_sc1_fit.pickle", "rb") as f:
    age_model = dill.load(f)

# Load test data
with open("data/deploy_data.csv", "r") as f:
    test_data = list(csv.DictReader(f))

campaigns = [
    SimpleNamespace(
        name="Campaign 1",
        detail="Specific personalized fashion-related campaigns targeting female customers",
        target_gender=[
            "F",
        ],
        target_age=None,
    ),
    SimpleNamespace(
        name="Campaign 2",
        detail="Specific cashback offers on special days (for example, International Women’s Day) targeting female customers",
        target_gender=[
            "F",
        ],
        target_age=None,
    ),
    SimpleNamespace(
        name="Campaign 3",
        detail="Personalized call and data packs targeting male customers",
        target_gender=[
            "M",
        ],
        target_age=None,
    ),
    SimpleNamespace(
        name="Campaign 4",
        detail="Bundled smartphone offers for the age group [0–24] years",
        target_gender=None,
        target_age=[
            pd.Interval(left=0, right=24),
        ],
    ),
    SimpleNamespace(
        name="Campaign 5",
        detail="Special offers for payment wallet offers - those in the age group of [24–32] years",
        target_gender=None,
        target_age=[
            pd.Interval(left=24, right=32),
        ],
    ),
    SimpleNamespace(
        name="Campaign 6",
        detail="Special cashback offers for Privilege Membership [32+] years",
        target_gender=None,
        target_age=[
            pd.Interval(left=32, right=45),
            pd.Interval(left=45, right=np.Inf),
        ],
    ),
]

def _test_subset():
    return random.choices(test_data, k=50)

def _format_input(device_id):
    option = list(filter(lambda row: row['device_id'] == device_id, test_data))[0]
    formatted_input = input_processor.process_input(json.dumps(option))
    return formatted_input

def _predict_gender(formatted_input):
    gender_pred = gender_model.predict_proba(formatted_input)
    gender_labels = gender_label_encoder.classes_
    gender_proba = pd.DataFrame(gender_pred, columns=gender_labels)
    gender_final = gender_proba.idxmax(axis=1)[0]
    return SimpleNamespace(
        gender_proba=gender_proba,
        gender_final=gender_final,
    )

def _predict_age_group(formatted_input):
    age_pred = age_model.predict_proba(formatted_input)
    age_labels = age_label_encoder.classes_
    age_proba = pd.DataFrame(age_pred, columns=age_labels)
    age_final = age_proba.idxmax(axis=1)[0]
    return SimpleNamespace(
        age_proba=age_proba,
        age_final=age_final,
    )

def _predict_campaigns(gender_final, age_final):
    matched_campaigns = []
    for campaign in campaigns:
        if campaign.target_gender and gender_final in campaign.target_gender:
            matched_campaigns.append(campaign)
        if campaign.target_age and age_final in campaign.target_age:
            matched_campaigns.append(campaign)
    return matched_campaigns

def _predict(device_id):
    formatted_input = _format_input(device_id)
    gender_preds = _predict_gender(formatted_input)
    age_preds = _predict_age_group(formatted_input)
    matched_campaigns = _predict_campaigns(gender_preds.gender_final, age_preds.age_final)
    matched_campaigns = list(map(lambda simplenamespace: simplenamespace.__dict__, matched_campaigns))
    matched_campaigns = pd.DataFrame(matched_campaigns)
    return dict(
        formatted_input=formatted_input,
        gender_proba=gender_preds.gender_proba,
        gender_final=gender_preds.gender_final,
        age_proba=age_preds.age_proba,
        age_final=age_preds.age_final,
        matched_campaigns=matched_campaigns,
    )

# Create flask app instance
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", devices=_test_subset())


@app.route("/htmx/predict", methods=['POST'])
def predict():
    device_id = request.form['device']
    prediction = _predict(device_id)
    return render_template("prediction.htmx.html", **prediction)
