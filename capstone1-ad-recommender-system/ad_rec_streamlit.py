'''
Quickly prototyping the interface using streamlit
'''

import streamlit as st

import dill
import csv
import json

from types import SimpleNamespace
import numpy as np
import pandas as pd

st.title("Ad Recommender System")


@st.cache_resource
def load_data():
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

    return SimpleNamespace(
        gender_label_encoder=gender_label_encoder,
        age_label_encoder=age_label_encoder,
        input_processor=input_processor,
        gender_model=gender_model,
        age_model=age_model,
        test_data=test_data,
    )


@st.cache_data
def load_campaigns():
    return [
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


# Create a text element and let the reader know the data is loading.
with st.spinner("Loading data..."):
    data = load_data()
    campaigns = load_campaigns()
    st.toast("Data loaded!")

with st.sidebar:
    option = st.selectbox("What device do you want to check?", data.test_data)
    st.write("You choose:", option)

with st.container():
    st.subheader("Processed input")
    formatted_input = data.input_processor.process_input(json.dumps(option))
    st.dataframe(formatted_input)

with st.container():
    st.subheader("Gender prediction")
    gender_pred = data.gender_model.predict_proba(formatted_input)
    gender_labels = data.gender_label_encoder.classes_
    gender_proba = pd.DataFrame(gender_pred, columns=gender_labels)
    st.dataframe(gender_proba)
    gender_final = gender_proba.idxmax(axis=1)[0]
    st.write("Predicted gender:", gender_final)

with st.container():
    st.subheader("Age prediction")
    age_pred = data.age_model.predict_proba(formatted_input)
    age_labels = data.age_label_encoder.classes_
    age_proba = pd.DataFrame(age_pred, columns=age_labels)
    st.dataframe(age_proba)
    age_final = age_proba.idxmax(axis=1)[0]
    st.write("Predicted age group:", age_final)

with st.container():
    st.subheader("Campaign prediction")
    matched_campaigns = []
    for campaign in campaigns:
        if campaign.target_gender and gender_final in campaign.target_gender:
            matched_campaigns.append(campaign)
        if campaign.target_age and age_final in campaign.target_age:
            matched_campaigns.append(campaign)
    matched_campaigns = list(map(lambda simplenamespace: simplenamespace.__dict__, matched_campaigns))
    matched_campaigns = pd.DataFrame(matched_campaigns)
    st.dataframe(matched_campaigns)
