import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Load the merged dataset
# -------------------------------
df = pd.read_csv("data.csv")  # replace with your actual file name

st.title("🌾 Project Samarth - Intelligent Q&A System")
st.write("Ask questions about rainfall, crop production, and agriculture trends in Indian districts.")

# Display dataset preview
if st.checkbox("Show dataset"):
    st.dataframe(df.head())

# -------------------------------
# Simple question-answer logic
# -------------------------------
question = st.text_input("🔍 Enter your question:")

if st.button("Get Answer"):
    q = question.lower()

    # Highest production
    if "highest production" in q:
        top_district = df.loc[df["Sum of production"].idxmax()]
        st.subheader("🏆 District with Highest Crop Production")
        st.write(f"**District:** {top_district['District']}")
        st.write(f"**Production:** {top_district['Sum of production']}")
        st.write(f"**Rainfall:** {top_district['Sum of ka_2024_rainfall_districts.Total Actual (mm)']}")
        st.caption("Source: data.csv")

    # Lowest production
    elif "lowest production" in q:
        low_district = df.loc[df["Sum of production"].idxmin()]
        st.subheader("⬇️ District with Lowest Crop Production")
        st.write(f"**District:** {low_district['District']}")
        st.write(f"**Production:** {low_district['Sum of production']}")
        st.caption("Source: data.csv")

    # Average rainfall
    elif "rainfall" in q and "average" in q:
        avg_rain = df["Sum of ka_2024_rainfall_districts.Total Actual (mm)"].mean()
        st.subheader("🌧️ Average Rainfall Across Districts")
        st.write(f"**Average Rainfall:** {avg_rain:.2f} mm")
        st.caption("Source: data.csv")

    # Compare rainfall and production by district
    elif "compare" in q and "rainfall" in q and "production" in q:
        st.subheader("🌾 Rainfall vs Production Comparison by District")

        # Optional district selection
        districts = st.multiselect(
            "Select one or more districts to compare:",
            df["District"].unique(),
            default=df["District"].unique()[:5]
        )
        filtered_df = df[df["District"].isin(districts)]

        # Scatter plot
        fig, ax = plt.subplots()
        ax.scatter(
            filtered_df["Sum of ka_2024_rainfall_districts.Total Actual (mm)"],
            filtered_df["Sum of production"],
            color="teal"
        )
        ax.set_xlabel("Total Actual Rainfall (mm)")
        ax.set_ylabel("Crop Production")
        ax.set_title("Rainfall vs Production by District")

        # Annotate points with district names
        for i, txt in enumerate(filtered_df["District"]):
            ax.annotate(txt, (filtered_df["Sum of ka_2024_rainfall_districts.Total Actual (mm)"].iloc[i],
                              filtered_df["Sum of production"].iloc[i]),
                        fontsize=8)

        st.pyplot(fig)
        st.dataframe(filtered_df[["District",
                                  "Sum of ka_2024_rainfall_districts.Total Actual (mm)",
                                  "Sum of production"]])

    # NEM vs SWM rainfall comparison
    elif "nem" in q and "swm" in q:
        st.subheader("☔ NEM vs SWM Rainfall by District")
        chart_data = df[["District",
                         "Sum of ka_2024_rainfall_districts.NEM Actual (mm)",
                         "Sum of ka_2024_rainfall_districts.SWM Actual"]]
        st.bar_chart(chart_data.set_index("District"))

    else:
        st.warning("Sorry, I couldn’t understand that question. Try asking about rainfall or crop production.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Developed by Mokshada | Data source: data.gov.in | Project Samarth")
