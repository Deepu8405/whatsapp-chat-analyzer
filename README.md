# WhatsApp Chat Analyzer 📱📈

An end-to-end data science application that transforms raw WhatsApp chat exports into actionable insights through an interactive web dashboard.

## 🚀 [Live Demo](Your-Streamlit-Share-Link-Here)

---

## 🎯 Project Objective
The goal was to build a tool that can parse unstructured text data from chat exports and visualize patterns in communication, peak engagement times, and vocabulary usage.

## 🛠️ Tech Stack
* **Framework:** Streamlit (UI/UX).
* **Data Processing:** Pandas, Regex[cite: 24].
* **NLP:** NLTK (Stopword removal and text cleaning)[cite: 25].
* **Visualization:** Matplotlib, Seaborn, WordCloud[cite: 21, 24].

## 🔍 Key Features
* **Activity Timelines:** Track message frequency across months and days.
* **Engagement Maps:** Identify peak hours and the most active days of the week.
* **Top Statistics:** Instant counts of total messages, words, media shared, and links.
* **Word Cloud:** Visual representation of the most frequently used terms.

## 📂 How to Use
1. Export your WhatsApp chat (without media) as a `.txt` file.
2. Upload the file to the sidebar of the application.
3. Select a specific user or "Overall" to view the generated insights.
