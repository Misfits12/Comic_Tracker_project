"""
STREAMLIT COMIC TRACKER APP
"""

import streamlit as st
import pandas as pd
import datetime
from comic_book import ComicBook
import os

DATA_FILE = "collection.txt"
PUBLISHERS = ("DC", "Marvel", "Image", "Dark Horse")
CONDITIONS = ("Mint", "Good", "Fair", "Poor")


# ==================== DATA FUNCTIONS ====================

def parse_collection_file():
    """Parse the collection.txt file and return a list of comic dictionaries."""
    comics = []
    
    if not os.path.exists(DATA_FILE):
        return comics
    
    with open(DATA_FILE, "r") as file:
        content = file.read().split("----------------------\n")
    
    for entry in content:
        lines = entry.strip().split("\n")
        if len(lines) < 5:
            continue
        
        # Parse timestamp and user
        header = lines[0].strip()
        if "[" in header and "]" in header:
            timestamp_str = header.split("[")[1].split("]")[0]
            user = header.split("] ")[1] if "] " in header else "Unknown"
        else:
            continue
        
        comic_data = {
            "timestamp": timestamp_str,
            "user": user,
            "title": lines[1].strip() if len(lines) > 1 else "",
            "issue": "",
            "publisher": "",
            "condition": "",
            "value": 0.0
        }
        
        # Parse other fields
        for line in lines[2:]:
            if line.startswith("Issue:"):
                comic_data["issue"] = line.replace("Issue:", "").strip()
            elif line.startswith("Publisher:"):
                comic_data["publisher"] = line.replace("Publisher:", "").strip()
            elif line.startswith("Condition:"):
                comic_data["condition"] = line.replace("Condition:", "").strip()
            elif "Value:" in line or "Estimated Value:" in line:
                value_str = line.split("$")[1].strip() if "$" in line else "0"
                try:
                    comic_data["value"] = float(value_str)
                except ValueError:
                    comic_data["value"] = 0.0
        
        if comic_data["title"]:
            comics.append(comic_data)
    
    return comics


def save_comic_to_file(user, comic):
    """Save a comic to the collection file."""
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(DATA_FILE, "a") as file:
        file.write(f"\n[{time}] {user}\n")
        file.write(f"{comic.title}\n")
        file.write(f"Issue: {comic.issue}\n")
        file.write(f"Publisher: {comic.publisher}\n")
        file.write(f"Condition: {comic.condition}\n")
        file.write(f"Estimated Value: ${comic.get_value():.2f}\n")
        file.write("----------------------\n")


def update_comic_in_file(index, comic_data):
    """Update a comic entry in the collection file."""
    comics = parse_collection_file()
    
    if 0 <= index < len(comics):
        # Rebuild the entire file
        with open(DATA_FILE, "w") as file:
            for i, comic in enumerate(comics):
                if i == index:
                    # Use the updated comic data
                    file.write(f"\n[{comic['timestamp']}] {comic['user']}\n")
                    file.write(f"{comic_data['title']}\n")
                    file.write(f"Issue: {comic_data['issue']}\n")
                    file.write(f"Publisher: {comic_data['publisher']}\n")
                    file.write(f"Condition: {comic_data['condition']}\n")
                    file.write(f"Estimated Value: ${comic_data['value']:.2f}\n")
                    file.write("----------------------\n")
                else:
                    file.write(f"\n[{comic['timestamp']}] {comic['user']}\n")
                    file.write(f"{comic['title']}\n")
                    file.write(f"Issue: {comic['issue']}\n")
                    file.write(f"Publisher: {comic['publisher']}\n")
                    file.write(f"Condition: {comic['condition']}\n")
                    file.write(f"Estimated Value: ${comic['value']:.2f}\n")
                    file.write("----------------------\n")


def delete_comic_from_file(index):
    """Delete a comic from the collection file."""
    comics = parse_collection_file()
    
    if 0 <= index < len(comics):
        comics.pop(index)
        
        # Rebuild the file
        with open(DATA_FILE, "w") as file:
            for comic in comics:
                file.write(f"\n[{comic['timestamp']}] {comic['user']}\n")
                file.write(f"{comic['title']}\n")
                file.write(f"Issue: {comic['issue']}\n")
                file.write(f"Publisher: {comic['publisher']}\n")
                file.write(f"Condition: {comic['condition']}\n")
                file.write(f"Estimated Value: ${comic['value']:.2f}\n")
                file.write("----------------------\n")


def get_comic_value(condition):
    """Calculate comic value based on condition."""
    base = 10.0
    if condition.lower() == "mint":
        return base * 2
    elif condition.lower() == "good":
        return base * 1.5
    elif condition.lower() == "fair":
        return base
    else:
        return base * 0.5


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Comic Tracker",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Comic Tracker")
st.markdown("---")

# ==================== MAIN APP ====================

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["🔍 View All", "➕ Add Comic", "✏️ Edit Comic", "🗑️ Delete Comic", "📊 Analytics", "📥 Export"]
)

# ==================== TAB 1: VIEW ALL ====================
with tab1:
    st.header("View Your Comic Collection")
    
    comics = parse_collection_file()
    
    if not comics:
        st.info("No comics in collection yet!")
    else:
        # Search bar
        search_query = st.text_input("🔍 Search across all fields:", placeholder="Search by title, publisher, user, issue...")
        
        # Filter by user
        users = list(set([comic["user"] for comic in comics]))
        selected_user = st.selectbox("Filter by User:", ["All Users"] + users)
        
        # Filter by publisher
        publishers = list(set([comic["publisher"] for comic in comics]))
        selected_publisher = st.selectbox("Filter by Publisher:", ["All Publishers"] + publishers)
        
        # Filter by condition
        conditions = list(set([comic["condition"] for comic in comics]))
        selected_condition = st.selectbox("Filter by Condition:", ["All Conditions"] + conditions)
        
        # Apply filters
        filtered_comics = comics.copy()
        
        # Apply search
        if search_query:
            search_lower = search_query.lower()
            filtered_comics = [
                comic for comic in filtered_comics
                if search_lower in comic["title"].lower()
                or search_lower in comic["publisher"].lower()
                or search_lower in comic["user"].lower()
                or search_lower in comic["issue"].lower()
            ]
        
        # Apply user filter
        if selected_user != "All Users":
            filtered_comics = [comic for comic in filtered_comics if comic["user"] == selected_user]
        
        # Apply publisher filter
        if selected_publisher != "All Publishers":
            filtered_comics = [comic for comic in filtered_comics if comic["publisher"] == selected_publisher]
        
        # Apply condition filter
        if selected_condition != "All Conditions":
            filtered_comics = [comic for comic in filtered_comics if comic["condition"] == selected_condition]
        
        st.write(f"**Found: {len(filtered_comics)} comic(s)**")
        
        if filtered_comics:
            # Display as table
            df = pd.DataFrame(filtered_comics)
            df = df[["title", "issue", "publisher", "condition", "value", "user", "timestamp"]]
            df.columns = ["Title", "Issue", "Publisher", "Condition", "Value ($)", "User", "Added"]
            st.dataframe(df, use_container_width=True)
            
            # Show individual details
            st.subheader("📋 Detailed View")
            selected_idx = st.selectbox("Select a comic to view details:", range(len(filtered_comics)))
            selected_comic = filtered_comics[selected_idx]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Title:** {selected_comic['title']}")
                st.write(f"**Issue:** {selected_comic['issue']}")
                st.write(f"**Publisher:** {selected_comic['publisher']}")
            with col2:
                st.write(f"**Condition:** {selected_comic['condition']}")
                st.write(f"**Estimated Value:** ${selected_comic['value']:.2f}")
                st.write(f"**Owner:** {selected_comic['user']}")
                st.write(f"**Added:** {selected_comic['timestamp']}")
        else:
            st.warning("No comics match your filters!")

# ==================== TAB 2: ADD COMIC ====================
with tab2:
    st.header("Add a New Comic")
    
    with st.form("add_comic_form"):
        user = st.text_input("Your Name:", placeholder="e.g., Robert")
        title = st.text_input("Comic Title:", placeholder="e.g., Flash")
        issue = st.text_input("Issue Number:", placeholder="e.g., 22")
        publisher = st.selectbox("Publisher:", PUBLISHERS)
        condition = st.selectbox("Condition:", CONDITIONS)
        
        submitted = st.form_submit_button("➕ Add Comic", use_container_width=True)
        
        if submitted:
            if user and title and issue:
                comic = ComicBook(title, issue, publisher, condition)
                save_comic_to_file(user, comic)
                st.success(f"✅ Added '{title}' (Issue #{issue}) - Estimated Value: ${comic.get_value():.2f}")
            else:
                st.error("❌ Please fill in all required fields!")

# ==================== TAB 3: EDIT COMIC ====================
with tab3:
    st.header("Edit a Comic")
    
    comics = parse_collection_file()
    
    if not comics:
        st.info("No comics to edit!")
    else:
        # Select comic to edit
        comic_options = [f"{comic['title']} (Issue #{comic['issue']}) - {comic['user']}" for comic in comics]
        selected_idx = st.selectbox("Select a comic to edit:", range(len(comics)), format_func=lambda i: comic_options[i])
        
        selected_comic = comics[selected_idx]
        
        with st.form("edit_comic_form"):
            new_title = st.text_input("Title:", value=selected_comic["title"])
            new_issue = st.text_input("Issue Number:", value=selected_comic["issue"])
            new_publisher = st.selectbox("Publisher:", PUBLISHERS, index=PUBLISHERS.index(selected_comic["publisher"]) if selected_comic["publisher"] in PUBLISHERS else 0)
            new_condition = st.selectbox("Condition:", CONDITIONS, index=CONDITIONS.index(selected_comic["condition"]) if selected_comic["condition"] in CONDITIONS else 0)
            
            submitted = st.form_submit_button("✏️ Update Comic", use_container_width=True)
            
            if submitted:
                new_value = get_comic_value(new_condition)
                updated_data = {
                    "title": new_title,
                    "issue": new_issue,
                    "publisher": new_publisher,
                    "condition": new_condition,
                    "value": new_value
                }
                update_comic_in_file(selected_idx, updated_data)
                st.success(f"✅ Updated '{new_title}'!")
                st.rerun()

# ==================== TAB 4: DELETE COMIC ====================
with tab4:
    st.header("Delete a Comic")
    
    comics = parse_collection_file()
    
    if not comics:
        st.info("No comics to delete!")
    else:
        comic_options = [f"{comic['title']} (Issue #{comic['issue']}) - {comic['user']}" for comic in comics]
        selected_idx = st.selectbox("Select a comic to delete:", range(len(comics)), format_func=lambda i: comic_options[i])
        
        selected_comic = comics[selected_idx]
        
        st.warning(f"⚠️ Are you sure you want to delete '{selected_comic['title']}' (Issue #{selected_comic['issue']})?")
        
        if st.button("🗑️ Delete Comic", use_container_width=True, type="secondary"):
            delete_comic_from_file(selected_idx)
            st.success("✅ Comic deleted!")
            st.rerun()

# ==================== TAB 5: ANALYTICS ====================
with tab5:
    st.header("📊 Collection Analytics")
    
    comics = parse_collection_file()
    
    if not comics:
        st.info("No data to display yet!")
    else:
        df = pd.DataFrame(comics)
        
        # Total collection value
        total_value = df["value"].sum()
        st.metric("💰 Total Collection Value", f"${total_value:.2f}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📚 Total Comics", len(comics))
        
        with col2:
            unique_users = df["user"].nunique()
            st.metric("👥 Unique Collectors", unique_users)
        
        with col3:
            unique_publishers = df["publisher"].nunique()
            st.metric("🏢 Unique Publishers", unique_publishers)
        
        st.markdown("---")
        
        # Comics per publisher
        st.subheader("📊 Comics per Publisher")
        publisher_counts = df["publisher"].value_counts()
        st.bar_chart(publisher_counts)
        
        # Comics per user
        st.subheader("👥 Comics per Collector")
        user_counts = df["user"].value_counts()
        st.bar_chart(user_counts)
        
        # Condition distribution
        st.subheader("📈 Condition Distribution")
        condition_counts = df["condition"].value_counts()
        st.bar_chart(condition_counts)
        
        # Value by publisher
        st.subheader("💵 Total Value by Publisher")
        value_by_publisher = df.groupby("publisher")["value"].sum()
        st.bar_chart(value_by_publisher)

# ==================== TAB 6: EXPORT ====================
with tab6:
    st.header("📥 Export Analytics")
    
    comics = parse_collection_file()
    
    if not comics:
        st.info("No data to export!")
    else:
        df = pd.DataFrame(comics)
        
        # Create analytics summary
        analytics = {
            "Metric": [
                "Total Comics",
                "Total Collection Value",
                "Unique Collectors",
                "Unique Publishers",
                "Average Value per Comic"
            ],
            "Value": [
                len(comics),
                f"${df['value'].sum():.2f}",
                df["user"].nunique(),
                df["publisher"].nunique(),
                f"${df['value'].mean():.2f}"
            ]
        }
        
        analytics_df = pd.DataFrame(analytics)
        
        # Publisher breakdown
        st.subheader("📊 Publisher Breakdown")
        publisher_breakdown = df.groupby("publisher").agg({
            "title": "count",
            "value": "sum"
        }).rename(columns={"title": "Count", "value": "Total Value"})
        publisher_breakdown["Total Value"] = publisher_breakdown["Total Value"].apply(lambda x: f"${x:.2f}")
        st.write(publisher_breakdown)
        
        # Condition breakdown
        st.subheader("📈 Condition Breakdown")
        condition_breakdown = df.groupby("condition").agg({
            "title": "count",
            "value": "sum"
        }).rename(columns={"title": "Count", "value": "Total Value"})
        condition_breakdown["Total Value"] = condition_breakdown["Total Value"].apply(lambda x: f"${x:.2f}")
        st.write(condition_breakdown)
        
        # Export buttons
        st.subheader("📥 Download Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export analytics summary
            analytics_csv = analytics_df.to_csv(index=False)
            st.download_button(
                label="📊 Download Analytics Summary (CSV)",
                data=analytics_csv,
                file_name=f"comic_analytics_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Export full collection
            collection_csv = df.to_csv(index=False)
            st.download_button(
                label="📚 Download Full Collection (CSV)",
                data=collection_csv,
                file_name=f"comic_collection_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
