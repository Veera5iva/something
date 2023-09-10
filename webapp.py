import streamlit as st
import sqlite3

# Create a SQLite database connection
conn = sqlite3.connect('blog.db')
cursor = conn.cursor()

# Create a table to store blog posts if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS blog_posts (
        id INTEGER PRIMARY KEY,
        title TEXT,
        content TEXT
    )
''')

# Create a table to store links
cursor.execute('''
    CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY,
        title TEXT,
        url TEXT
    )
''')

conn.commit()

def create_post(title, content):
    cursor.execute('INSERT INTO blog_posts (title, content) VALUES (?, ?)', (title, content))
    conn.commit()

def create_link(title, url):
    cursor.execute('INSERT INTO links (title, url) VALUES (?, ?)', (title, url))
    conn.commit()

def reset_database():
    cursor.execute('DELETE FROM blog_posts')
    cursor.execute('DELETE FROM links')
    conn.commit()

def get_posts():
    cursor.execute('SELECT id, title, content FROM blog_posts')
    return cursor.fetchall()

def get_links():
    cursor.execute('SELECT id, title, url FROM links')
    return cursor.fetchall()

def main():
    st.title("Ajay's chapters")

    # Create a sidebar to add new blog posts
    st.sidebar.header("Create a Nee Incident")
    post_title = st.sidebar.text_input("Title")
    post_content = st.sidebar.text_area("Content")
    if st.sidebar.button("Create Post"):
        if post_title and post_content:
            create_post(post_title, post_content)
            st.sidebar.success("Blog post created successfully!")
        else:
            st.sidebar.error("Please enter both a title and content for the post.")

    # Create a sidebar to add new links
    st.sidebar.header("Add a New Link")
    link_title = st.sidebar.text_input("Link Title")
    link_url = st.sidebar.text_input("Link URL")
    if st.sidebar.button("Add Link"):
        if link_title and link_url:
            create_link(link_title, link_url)
            st.sidebar.success("Link added successfully!")
        else:
            st.sidebar.error("Please enter both a title and URL for the link.")

    # Display existing blog posts
    st.header("Incidents :")
    posts = get_posts()
    if posts:
        for post_id, title, content in posts:
            st.subheader(title)
            st.write(content)
            if st.button(f"Edit '{title}'"):
                new_title = st.text_input(f"New title for '{title}':", value=title)
                new_content = st.text_area(f"New content for '{title}':", value=content)
                if st.button("Save Changes"):
                    edit_post(post_id, new_title, new_content)
                    st.success("Post updated successfully!")

    # Display existing links
    st.header("Links")
    links = get_links()
    if links:
        for link_id, title, url in links:
            st.subheader(title)
            st.write(url)
            if st.button(f"Edit '{title}'"):
                new_title = st.text_input(f"New title for '{title}':", value=title)
                new_url = st.text_input(f"New URL for '{title}':", value=url)
                if st.button("Save Changes"):
                    edit_link(link_id, new_title, new_url)
                    st.success("Link updated successfully!")

    # Add a "Reset Database" button
    if st.button("Reset Database"):
        reset_database()
        st.success("Database reset successfully!")

if __name__ == "__main__":
    main()
