# ============================================================
# app.py - Streamlit Application
# Stage 4: Table Viewer — connects to MySQL and displays tables
# Stage 5: File Importer — will be added below in Stage 5
# ============================================================

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os

# ============================================================
# PAGE CONFIGURATION
# Sets the browser tab title and uses wide layout
# ============================================================
st.set_page_config(
    page_title="My App",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Database Viewer & File Importer")
st.markdown("---")

# ============================================================
# DATABASE CONNECTION
# Reads connection details from environment variables
# (set in docker-compose.yml so the app knows where MySQL is)
# @st.cache_resource = creates the connection once and reuses it
# ============================================================
DB_HOST = os.getenv("DB_HOST", "db")          # container name of MySQL service
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASS = os.getenv("DB_PASS", "apppassword")
DB_NAME = os.getenv("DB_NAME", "appdb")

@st.cache_resource
def get_engine():
    """Create and return a SQLAlchemy database engine (connection pool)."""
    connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    return create_engine(connection_string)

# ============================================================
# SECTION 1: DATABASE TABLE VIEWER
# ============================================================
st.header("🗄️ Database Tables")
st.write("Select a table from the dropdown to view its records.")

try:
    # Get the database engine (connection)
    engine = get_engine()

    # Query MySQL to get list of all tables in the database
    with engine.connect() as conn:
        result = conn.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        table_names = [row[0] for row in tables]

    if not table_names:
        st.warning("No tables found in the database.")
    else:
        # Show a dropdown with all table names
        selected_table = st.selectbox(
            "📋 Choose a table:",
            options=table_names,
            help="Select a table to see all its records"
        )

        if selected_table:
            # Fetch all records from the selected table
            with engine.connect() as conn:
                df = pd.read_sql(
                    f"SELECT * FROM `{selected_table}`",
                    conn
                )

            # Display record count
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(f"📄 Table: `{selected_table}`")
            with col2:
                st.metric("Total Records", len(df))

            # Display the data as an interactive table
            # use_container_width=True makes it fill the full page width
            st.dataframe(df, use_container_width=True, height=400)

            # Show column info
            with st.expander("🔍 Column Details"):
                col_info = pd.DataFrame({
                    "Column Name": df.columns,
                    "Data Type": [str(df[col].dtype) for col in df.columns],
                    "Non-Null Count": [df[col].count() for col in df.columns]
                })
                st.dataframe(col_info, use_container_width=True)

except Exception as e:
    st.error(f"❌ Database connection error: {e}")
    st.info("💡 Make sure the MySQL container is running and healthy.")

st.markdown("---")

# ============================================================
# SECTION 2: FILE IMPORTER
# Stage 5: Upload a file from your Mac into the container
# ============================================================
st.header("📁 File Importer")
st.write("Upload a file from your local machine into the container's target directory.")

# Define source and target directories inside the container
SOURCE_DIR = "/app/uploads"           # mounted from your Mac's uploads/ folder
TARGET_DIR = "/app/imported_files"    # destination inside the container

# Ensure the target directory exists
os.makedirs(TARGET_DIR, exist_ok=True)

# ---- Upload via Streamlit file uploader ----
st.subheader("⬆️ Upload a File")
uploaded_file = st.file_uploader(
    "Choose a file from your local machine:",
    type=None,   # accepts any file type
    help="Select any file — it will be saved to /app/imported_files inside the container"
)

if uploaded_file is not None:
    target_path = os.path.join(TARGET_DIR, uploaded_file.name)
    with open(target_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ File **'{uploaded_file.name}'** successfully imported to `{TARGET_DIR}`")

st.markdown("---")

# ---- Show files available in the source (uploads/) directory ----
st.subheader("📂 Source Directory (uploads/ on your Mac → /app/uploads in container)")
if os.path.exists(SOURCE_DIR):
    source_files = os.listdir(SOURCE_DIR)
    if source_files:
        st.write(f"Files available to import from `{SOURCE_DIR}`:")
        for fname in source_files:
            fpath = os.path.join(SOURCE_DIR, fname)
            fsize = os.path.getsize(fpath)
            col1, col2, col3 = st.columns([4, 2, 2])
            with col1:
                st.write(f"📄 {fname}")
            with col2:
                st.write(f"{fsize:,} bytes")
            with col3:
                # Button to copy file from source to target
                if st.button(f"Import →", key=f"import_{fname}"):
                    import shutil
                    dest = os.path.join(TARGET_DIR, fname)
                    shutil.copy2(fpath, dest)
                    st.success(f"✅ '{fname}' copied to {TARGET_DIR}")
                    st.rerun()
    else:
        st.info(f"No files in `{SOURCE_DIR}` yet. Drop files into the `uploads/` folder on your Mac.")
else:
    st.warning(f"Source directory `{SOURCE_DIR}` not found.")

st.markdown("---")

# ---- Show files already imported in the target directory ----
st.subheader("📥 Target Directory (/app/imported_files inside container)")
if os.path.exists(TARGET_DIR):
    imported_files = os.listdir(TARGET_DIR)
    if imported_files:
        st.write(f"Files currently in `{TARGET_DIR}`:")
        for fname in imported_files:
            fpath = os.path.join(TARGET_DIR, fname)
            fsize = os.path.getsize(fpath)
            col1, col2, col3 = st.columns([4, 2, 2])
            with col1:
                st.write(f"✅ {fname}")
            with col2:
                st.write(f"{fsize:,} bytes")
            with col3:
                # Button to delete a file from the target directory
                if st.button(f"🗑️ Delete", key=f"delete_{fname}"):
                    os.remove(fpath)
                    st.warning(f"🗑️ '{fname}' deleted from {TARGET_DIR}")
                    st.rerun()
    else:
        st.info("No files imported yet. Use the uploader above or the Import button.")
else:
    st.warning(f"Target directory `{TARGET_DIR}` not found.")
