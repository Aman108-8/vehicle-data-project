import streamlit as st
from db_connection import create_connection, execute_query
import plotly.express as px
import pandas as pd

# Set page config
st.set_page_config(page_title="Vahan Dashboard", layout="wide")

# DB connection
@st.cache_resource
def init_connection():
    return create_connection()

conn = init_connection()

# Sidebar controls
with st.sidebar:
    st.header("Filters")
    
    # Common filters
    vehicle_types = st.multiselect(
        "Select Vehicle Types",
        options=["2 Wheeler", "3 Wheeler", "4 Wheeler"],
        default=["2 Wheeler", "3 Wheeler", "4 Wheeler"]
    )
    
    # View mode selection
    view_mode = st.radio("View by", ["Year-wise", "Quarter-wise"], index=0)

# Main page layout
st.title("Vahan Dashboard - Vehicle Registration Analysis")
st.subheader("Compare Year-on-Year or Quarter-on-Quarter growth by type")

# Content based on view mode
if view_mode == "Year-wise":
    # Sidebar filters
    with st.sidebar:
        start_year = st.number_input(
            "Select Start Year", 
            min_value=2002, max_value=2025, value=2002, step=1
        )
        compare_year = st.number_input(
            "Select Comparison Year", 
            min_value=2002, max_value=2025, value=2011, step=1
        )

    # Only run query if we have a connection and vehicle types
    if conn and vehicle_types:
        query = """
            WITH yearly_data AS (
                SELECT 
                    y.year_value AS year,
                    v.vehicle_name AS vehicle_type,
                    SUM(vmt.total_registration) AS total_registrations
                FROM vehicle_monthly_totals vmt
                JOIN month_year my ON vmt.month_year_id = my.id
                JOIN year_table y ON my.year_id = y.year_id
                JOIN vehicle_type_category vtc ON vmt.vehicle_type_category_id = vtc.id
                JOIN vehicle v ON vtc.vehicle_type_id = v.vehicle_id
                WHERE y.year_value BETWEEN %s AND %s
                AND v.vehicle_name IN ({})
                GROUP BY y.year_value, v.vehicle_name
            )
            SELECT 
                curr.year,
                curr.vehicle_type,
                curr.total_registrations,
                CASE 
                    WHEN prev.total_registrations IS NULL THEN 100
                    ELSE ROUND(
                        100 + ((curr.total_registrations - prev.total_registrations) * 100.0 / prev.total_registrations),
                        2
                    )
                END AS percentage_change
            FROM yearly_data curr
            LEFT JOIN yearly_data prev
                ON curr.vehicle_type = prev.vehicle_type
               AND curr.year = prev.year + 1
            ORDER BY curr.vehicle_type, curr.year;
        """.format(','.join(['%s'] * len(vehicle_types)))

        params = [start_year, compare_year] + vehicle_types
        df = execute_query(conn, query, params)

        if df is not None and not df.empty:
            st.subheader("Yearly Percentage Change in Vehicle Registrations")
            
            # Ensure correct types
            df['percentage_change'] = pd.to_numeric(df['percentage_change'], errors='coerce')
            df['year'] = df['year'].astype(int)

            # Line chart
            fig = px.line(
                df,
                x="year",
                y="percentage_change",
                color="vehicle_type",
                markers=True,
                title=f"Year-over-Year Percentage Change in Vehicle Registrations ({start_year}-{compare_year})",
                labels={
                    "year": "Year",
                    "percentage_change": "Percentage Change (%)",
                    "vehicle_type": "Vehicle Type"
                }
            )
            
            # Reference line
            fig.add_hline(y=0, line_dash="dot", line_color="gray")
            
            # Layout
            fig.update_layout(
                hovermode="x unified",
                legend_title_text="Vehicle Type",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                yaxis_title="Percentage Change (%)",
                yaxis_ticksuffix='%',
                xaxis_title="Year",
                xaxis=dict(
                    tickmode='linear',
                    dtick=1
                )
            )
            
            # Hover template
            fig.update_traces(
                hovertemplate="<b>%{fullData.name}</b><br>" +
                              "Year: %{x}<br>" +
                              "Change: %{y:.2f}%<br>" +
                              "<extra></extra>"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Data table
            st.dataframe(
                df.pivot(index='year', columns='vehicle_type', values='percentage_change')
            )
            
        else:
            st.warning("No data found for the selected vehicle types.")


else:  # Quarter-wise analysis
    # Simplified sidebar with only year selection
    with st.sidebar:
        st.markdown("**Select Year Range**")
        year_range = st.slider(
            "Select Year Range",
            min_value=2002,
            max_value=2025,
            value=(2002, 2025),
            step=1
        )
        start_year, end_year = year_range

    # Quarter-wise query and visualization
    if conn and vehicle_types:
        query = f"""
        WITH quarterly_data AS (
            SELECT 
                y.year_value AS year,
                CASE 
                    WHEN m.month_name IN ('January', 'February', 'March') THEN 'Jan-Mar'
                    WHEN m.month_name IN ('April', 'May', 'June') THEN 'Apr-Jun'
                    WHEN m.month_name IN ('July', 'August', 'September') THEN 'Jul-Sep'
                    WHEN m.month_name IN ('October', 'November', 'December') THEN 'Oct-Dec'
                END AS quarter,
                v.vehicle_name AS vehicle_type,
                SUM(vmt.total_registration) AS total_registration
            FROM vehicle_monthly_totals vmt
            JOIN month_year my ON vmt.month_year_id = my.id
            JOIN year_table y ON my.year_id = y.year_id
            JOIN month_table m ON my.month_id = m.month_id
            JOIN vehicle_type_category vtc ON vmt.vehicle_type_category_id = vtc.id
            JOIN vehicle v ON vtc.vehicle_type_id = v.vehicle_id
            WHERE v.vehicle_name IN ({','.join([f"'{vt}'" for vt in vehicle_types])})
              AND y.year_value BETWEEN {start_year} AND {end_year}
            GROUP BY 
                y.year_value,
                CASE 
                    WHEN m.month_name IN ('January', 'February', 'March') THEN 'Jan-Mar'
                    WHEN m.month_name IN ('April', 'May', 'June') THEN 'Apr-Jun'
                    WHEN m.month_name IN ('July', 'August', 'September') THEN 'Jul-Sep'
                    WHEN m.month_name IN ('October', 'November', 'December') THEN 'Oct-Dec'
                END,
                v.vehicle_name
        ),
        baseline_data AS (
            SELECT 
                vehicle_type,
                total_registration AS baseline_value
            FROM quarterly_data
            WHERE year = {start_year} AND quarter = 'Jan-Mar'
        )
        SELECT 
            qd.year,
            qd.quarter,
            qd.vehicle_type,
            qd.total_registration,
            CASE
                WHEN bd.baseline_value = 0 THEN NULL
                ELSE ROUND(100 + ((qd.total_registration - bd.baseline_value) * 100.0 / bd.baseline_value), 2)
            END AS percentage_change
        FROM quarterly_data qd
        JOIN baseline_data bd ON qd.vehicle_type = bd.vehicle_type
        ORDER BY 
            qd.vehicle_type,
            qd.year,
            CASE qd.quarter
                WHEN 'Jan-Mar' THEN 1
                WHEN 'Apr-Jun' THEN 2
                WHEN 'Jul-Sep' THEN 3
                WHEN 'Oct-Dec' THEN 4
            END;
        """

        df = execute_query(conn, query)

        if df is not None and not df.empty:
            st.subheader(f"Quarterly Vehicle Registration Trends ({start_year}-{end_year})")
            
            # Create separate tabs for each vehicle type
            tabs = st.tabs([f"**{vt}**" for vt in vehicle_types])
            
            for i, vehicle_type in enumerate(vehicle_types):
                with tabs[i]:
                    # Filter data for current vehicle type
                    type_df = df[df['vehicle_type'] == vehicle_type]
                    
                    # Create line chart for percentage change
                    fig = px.line(
                        type_df,
                        x="quarter",
                        y="percentage_change",
                        color="year",
                        markers=True,
                        title=f"{vehicle_type} - Percentage Change vs Q1 {start_year}",
                        labels={
                            "quarter": "Quarter",
                            "percentage_change": "Percentage Change (%)",
                            "year": "Year"
                        },
                        color_discrete_sequence=px.colors.qualitative.Plotly
                    )
                    
                    # Add reference line at 100% (baseline)
                    fig.add_hline(y=100, line_dash="dot", line_color="gray")
                    
                    # Customize layout
                    fig.update_layout(
                        xaxis_title="Quarter",
                        yaxis_title="Percentage Change (%)",
                        yaxis_ticksuffix='%',
                        legend_title_text="Year",
                        hovermode="x unified",
                        xaxis={
                            'categoryorder': 'array',
                            'categoryarray': ['Jan-Mar', 'Apr-Jun', 'Jul-Sep', 'Oct-Dec']
                        }
                    )
                    
                    # Add hover template
                    fig.update_traces(
                        hovertemplate="<b>Year %{color}</b><br>Quarter: %{x}<br>Change: %{y:.2f}%<extra></extra>"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show data table
                    st.write(f"Detailed Data for {vehicle_type}")
                    pivot_df = type_df.pivot(index='year', columns='quarter', values='percentage_change')
                    st.dataframe(
                        pivot_df.style.format("{:.2f}%").highlight_null(props="color: transparent;")
                    )
        else:
            st.warning("No data found for the selected years and vehicle types.")
