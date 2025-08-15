import streamlit as st
import numpy as np
import numpy_financial as npf
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Compare Mortgage Fixes",
    page_icon="🔎",
)

st.markdown("#### Compare Mortgage Fixes")

st.markdown("Use this tool to compare two different mortgage fixes based on their interest rate and fees." \
" This is best used if all parameters of the mortgage are the same other than interest rates and upfront fees.")

st.divider()

with st.sidebar:
    with st.expander("Settings"):
        same_principal = st.checkbox(
            "Use same principal for both mortgages?",
            True,
            )
        assume_interest_forever = st.checkbox(
            "Assume the interest rate stays after the fixed period?",
            True,
        )
        assume_no_overpayments = st.checkbox(
            "Assume there are no overpayments?",
            True
        )

if same_principal:
    p1 = st.number_input(
        "Mortgage principal (£)",
        min_value=1000,
        max_value=None,
        value=255000,
        step=1000,
    )
    p2 = p1

fix = st.number_input(
    "Enter the fix period (years)",
    min_value=1,
    max_value=40,
    value=5,
    step=1,
    key="fix",
)                  

col1, col2 = st.columns(2,
                        border=True)

with col1:
    st.write("Mortgage 1")

    if not same_principal:
        p1 = st.number_input(
            "Enter mortgage 1's principal (£)",
            min_value=None,
            max_value=None,
            key="p1",
        )

    i1 = st.number_input(
        "Interest rate (%)",
        min_value=0.01,
        max_value=100.00,
        step=0.01,
        value=4.01,
        key="i1"
    ) / 100 / 12

    f1 = st.number_input(
        "Upfront fees (£)",
        min_value=0.00,
        step=1.00,
        value=1099.00,
        key="f1"
    )

    l1 = st.number_input(
        "Length (years)",
        min_value=1,
        max_value=40,
        step=1,
        value=25,
        key="l1",
    ) * 12

    payment1 = npf.pmt(
        rate=i1,
        nper=l1,
        pv=-p1,
        fv=0,
        when=1
    )
    st.write(f"Monthly payment: £{round(payment1,2)}")

    per1 = np.arange(fix*12) + 1
    ipmt1 = npf.ipmt(
        rate=i1,
        per=per1,
        nper=l1,
        pv=-p1,
        fv=0,
        when=1,
    )
    interest1 = np.sum(ipmt1)

    val1 = npf.fv(
        rate=i1,
        nper=fix*12,
        pmt=payment1,
        pv=-p1,
        when=1,
    )

    list = []

    for period in per1:
        print(period)
        val = npf.fv(
            rate=i1,
            nper=period,
            pmt=payment1,
            pv=-p2,
            when=1,
        )
        
        list.append({"Months out": period, "Principal_m1": val})

    df1 = pd.DataFrame(list)

    st.write(f"Interest paid in {fix} year fix period: £{round(interest1,2)}")

    c1 = interest1 + f1

    st.write(f"Total 'cost' over the {fix} year period: £{round(c1,2)}")

    st.write(f"Principal remaining at end of fix: £{round(val1,2)}")

with col2:
    st.write("Mortgage 2")

    if not same_principal:
        p2 = st.number_input(
            "Enter mortgage 2's principal (£)",
            min_value=None,
            max_value=None,
            key="p2"
        )

    i2 = st.number_input(
        "Interest rate (%)",
        min_value=0.01,
        max_value=100.00,
        step=0.01,
        value=4.02,
        key="i2"
    ) / 100 / 12

    f2 = st.number_input(
        "Upfront fees (£)",
        min_value=0.00,
        step=1.00,
        value=934.00,
        key="f2"
    )

    l2 = st.number_input(
        "Length (years)",
        min_value=1,
        max_value=40,
        step=1,
        value=25,
        key="l2",
    ) * 12

    payment2 = npf.pmt(
        rate=i2,
        nper=l2,
        pv=-p2,
        fv=0,
        when=1
    )
    st.write(f"Monthly payment: £{round(payment2,2)}")

    per2 = np.arange(fix*12) + 1
    ipmt2 = npf.ipmt(
        rate=i2,
        per=per2,
        nper=l2,
        pv=-p2,
        fv=0,
        when=1,
    )
    interest2 = np.sum(ipmt2)

    val2 = npf.fv(
        rate=i2,
        nper=fix*12,
        pmt=payment2,
        pv=-p2,
        when=1,
    )

    list = []

    for period in per2:
        print(period)
        val = npf.fv(
            rate=i2,
            nper=period,
            pmt=payment2,
            pv=-p2,
            when=1,
        )
        
        list.append({"Months out": period, "Principal_m2": val})

    df2 = pd.DataFrame(list)

    st.write(f"Interest paid in {fix} year fix period: £{round(interest2,2)}")

    c2 = interest2 + f2

    st.write(f"Total 'cost' over the {fix} year period: £{round(c2,2)}")

    st.write(f"Principal remaining at end of fix: £{round(val2,2)}")

diff = round(abs(c1 - c2),2)
if c1 > c2:
    st.write(f"Mortgage 2 is cheaper than Mortgage 1 by £{diff}")
elif c1 < c2:
    st.write(f"Mortgage 1 is cheaper than Mortgage 2 by £{diff}")

# df = df1.merge(
#     df2,
#     how="left",
#     on="Months out"
# )

# st.dataframe(df)

# fig = px.line(
#     df,
#     x="Months out",
#     y=["Principal_m1", "Principal_m2"],
#     range_y=[0, p1]
# )

# st.plotly_chart(fig)