# 📦 Cargo Route Optimizer

An interactive route optimization app for cargo shipments across Europe and Turkey.  
Built with 🐍 Python and ⚡ [Streamlit](https://streamlit.io), it uses Dijkstra’s algorithm to find the **cheapest cargo route**, favoring **hub cities**.

## 🚀 Live Demo

🔗 [Launch the App](https://cargo-route-optimizer.streamlit.app/)

## ✨ Features

- Select source and destination cities
- Optimized routing using **cost-based Dijkstra**
- Hub cities reduce route cost via **smart discounts**
- Interactive map with:
  - 🟢 Hub cities
  - 🔵 Regular cities
  - 🔴 Optimized route
  - ⚪ Full cargo network connections

## 🧠 How It Works

- All cities and routes are defined in `final_data.json`
- Each route has a real-world distance (in km)
- Hubs apply a 20% cost discount when used in a route
- The shortest-cost path is calculated using [NetworkX](https://networkx.org)

## 📁 Project Structure

```
.
├── app.py                # Main Streamlit app
├── data.json             # Cities, hubs, and routes
├── requirements.txt      # Dependencies
└── README.md             # You're reading it
```

## ⚙️ Setup Locally (Optional)

```bash
git clone https://github.com/Emircan92/cargo-route-optimizer.git
cd cargo-route-optimizer
pip install -r requirements.txt
streamlit run app.py
```

## 📌 Author

Built with ❤️ by **Emircan Küçükmotor**  
> Just a guy optimizing cargo at a bar 🤘
