import streamlit as st
from db_connection import create_connection, execute_query
import plotly.express as px

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
    # Year-wise filters in sidebar
    with st.sidebar:
        start_year = st.number_input("Select Start Year", min_value=2002, max_value=2025, value=2002, step=1)
        compare_year = st.number_input("Select Comparison Year", min_value=2002, max_value=2025, value=2011, step=1)

    # Year-wise query and visualization
    if conn and vehicle_types:
        query = f"""
            SELECT 
                y.year_value AS year,
                v.vehicle_name AS vehicle_type,
                SUM(vmt.total_registration) AS total_registrations
            FROM vehicle_monthly_totals vmt
            JOIN month_year my ON vmt.month_year_id = my.id
            JOIN year_table y ON my.year_id = y.year_id
            JOIN month_table m ON my.month_id = m.month_id
            JOIN vehicle_type_category vtc ON vmt.vehicle_type_category_id = vtc.id
            JOIN vehicle v ON vtc.vehicle_type_id = v.vehicle_id
            JOIN vehicle_category vc ON vtc.category_id = vc.category_id
            WHERE y.year_value IN (%s, %s)
            AND v.vehicle_name IN ({','.join(['%s']*len(vehicle_types))})
            GROUP BY y.year_value, v.vehicle_name
            ORDER BY v.vehicle_name, y.year_value;
        """

        params = [start_year, compare_year] + vehicle_types
        df = execute_query(conn, query, params)

        if df is not None and not df.empty:
            st.subheader("Registration Data")
            st.dataframe(df)

            st.subheader(f"Yearly Comparison: {start_year} vs {compare_year}")
            # Convert year to string to make it discrete/categorical
            df['year'] = df['year'].astype(str)

            # Grouped bar chart with discrete colors
            fig = px.bar(
                df,
                x="vehicle_type",
                y="total_registrations",
                color="year",
                barmode="group",
                text="total_registrations",
                title=f"Vehicle Registrations Comparison",
                color_discrete_sequence=px.colors.qualitative.Set2,
                category_orders={"year": [str(start_year), str(compare_year)]}
            )

            # Styling
            fig.update_traces(
                texttemplate='%{text:.0f}',
                textposition='outside',
                marker_line_color='rgb(0,0,0)',
                marker_line_width=1
            )
            
            fig.update_layout(
                legend_title_text="Year",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                xaxis_title="Vehicle Type",
                yaxis_title="Total Registrations",
                xaxis={'type': 'category'}
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data found for the selected years and filters.")

else:  # Quarter-wise
    # Quarter-wise filters in sidebar
    with st.sidebar:
        start_year = st.number_input("Select Start Year", min_value=2002, max_value=2025, value=2002, step=1)
        compare_year = st.number_input("Select Comparison Year", min_value=2002, max_value=2025, value=2011, step=1)
        all_months = ['January', 'February', 'March', 'April', 'May', 'June', 
                    'July', 'August', 'September', 'October', 'November', 'December']
        
        st.markdown("**Select exactly 3 months for comparison**")
        selected_months = st.multiselect(
            "Select 3 Months",
            options=all_months,
            default=['January', 'February', 'March'],
            key="month_selector"
        )
    
    # Validate selection
    if len(selected_months) != 3:
        st.warning("Please select exactly 3 months")
        st.stop()

    # Quarter-wise query and visualization
    if conn and vehicle_types and len(selected_months) == 3:
        # Convert selected months to SQL format
        months_sql = ",".join([f"'{m}'" for m in selected_months])
        
        query = f"""
        SELECT 
            y.year_value AS year,
            m.month_name AS month,
            v.vehicle_name AS vehicle_type,
            SUM(vmt.total_registration) AS total_registration
        FROM vehicle_monthly_totals vmt
        JOIN month_year my ON vmt.month_year_id = my.id
        JOIN year_table y ON my.year_id = y.year_id AND y.year_value IN ({start_year}, {compare_year})
        JOIN month_table m ON my.month_id = m.month_id AND m.month_name IN ({months_sql})
        JOIN vehicle_type_category vtc ON vmt.vehicle_type_category_id = vtc.id
        JOIN vehicle v ON vtc.vehicle_type_id = v.vehicle_id
        WHERE v.vehicle_name IN ({','.join([f"'{vt}'" for vt in vehicle_types])})
        GROUP BY y.year_value, m.month_name, v.vehicle_name
        ORDER BY 
            v.vehicle_name,
            CASE m.month_name 
                WHEN 'January' THEN 1 
                WHEN 'February' THEN 2 
                WHEN 'March' THEN 3
                WHEN 'April' THEN 4
                WHEN 'May' THEN 5
                WHEN 'June' THEN 6
                WHEN 'July' THEN 7
                WHEN 'August' THEN 8
                WHEN 'September' THEN 9
                WHEN 'October' THEN 10
                WHEN 'November' THEN 11
                WHEN 'December' THEN 12
            END,
            y.year_value;
        """

        df = execute_query(conn, query)

        if df is not None and not df.empty:
            st.subheader("Quarterly Registration Data")
            st.dataframe(df)
            
            st.subheader(f"Quarterly Comparison: {start_year} vs {compare_year}")
            # Create columns for side-by-side charts
            cols = st.columns(2)
            
            # Get unique vehicle types
            unique_vehicle_types = df['vehicle_type'].unique()
            
            # Display charts in pairs
            for i in range(0, len(unique_vehicle_types), 2):
                # First chart in pair
                if i < len(unique_vehicle_types):
                    with cols[0]:
                        vehicle_type = unique_vehicle_types[i]
                        type_df = df[df['vehicle_type'] == vehicle_type]
                        
                        fig = px.line(
                            type_df,
                            x="month",
                            y="total_registration",
                            color="year",
                            markers=True,
                            title=f"{vehicle_type}",
                            labels={
                                "month": "Month",
                                "total_registration": "Total Registrations",
                                "year": "Year"
                            }
                        )
                        fig.update_layout(
                            xaxis=dict(categoryorder='array', categoryarray=selected_months),
                            legend_title_text="Year"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                # Second chart in pair
                if i+1 < len(unique_vehicle_types):
                    with cols[1]:
                        vehicle_type = unique_vehicle_types[i+1]
                        type_df = df[df['vehicle_type'] == vehicle_type]
                        
                        fig = px.line(
                            type_df,
                            x="month",
                            y="total_registration",
                            color="year",
                            markers=True,
                            title=f"{vehicle_type}",
                            labels={
                                "month": "Month",
                                "total_registration": "Total Registrations",
                                "year": "Year"
                            }
                        )
                        fig.update_layout(
                            xaxis=dict(categoryorder='array', categoryarray=selected_months),
                            legend_title_text="Year"
                        )
                        st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data found for the selected years and filters.")