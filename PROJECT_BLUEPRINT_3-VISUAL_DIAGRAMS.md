# 📊 PROJECT_BLUEPRINT_3: Visual Diagrams & Architecture

This document contains the visual representations of the **Smart Traffic Violation Pattern Detector Dashboard**, including high-level architecture, data flow sequences, and component interactions.

## 1. High-Level Architecture

The application follows a modular architecture where `app.py` serves as the entry point, orchestrating navigation between different pages. Core business logic, data processing, and plotting functions are decoupled into the `core/` directory.

```mermaid
graph TD
    User[User] -->|Interacts| App["Streamlit App (app.py)"]
    
    subgraph "Frontend Layer (Pages)"
        App --> Sidebar[Sidebar Navigation]
        App --> HomePage["00_Home_Page.py"]
        App --> Dashboard["app.py (Dashboard View)"]
        App --> Numerical["01_Numerical_Analysis.py"]
        App --> Viz["02_Visualize_Data.py"]
        App --> Trends["03_Trend_Analysis.py"]
        App --> Map["04_Map_Visualization.py"]
        App --> AutoAnalyzer["05_Know_Your_Data.py"]
        App --> Upload["09_Upload_Dataset.py"]
        App --> View["10_View_Dataset.py"]
        App --> About["11_About_Page.py"]
    end
    
    subgraph "Core Logic Layer (core/)"
        Sidebar --> Utils["utils.py"]
        Dashboard --> Summary["dashboard_summary.py"]
        Dashboard --> DashPlots["dashboard_plot.py"]
        Viz --> VizPlots["visualize_plot.py"]
        Trends --> TrendPlots["trend_plot.py"]
        Map --> MapPlots["map_plot.py"]
        Upload --> Generator["data_generator.py"]
        
        Summary & VizPlots & TrendPlots & MapPlots --> Utils
    end
    
    subgraph "Data Layer"
        Utils --> Load[Load CSV]
        AutoAnalyzer --> ManualLoad[Direct Upload CSV]
        Load --> RawData[(CSV Datasets)]
        Generator --> GenData[Generated Datasets]
    end
```

## 2. Data Flow Sequence

This sequence describes how data flows from the user's interaction (selecting a dataset) through the processing layer to the final visualization.

### 2.1 Standard Analysis Flow

```mermaid
sequenceDiagram
    participant User
    participant App
    participant Sidebar
    participant Logic
    participant Data

    rect rgb(240, 248, 255)
    note right of User: Standard Analysis Flow
    User->>Sidebar: Select Traffic Dataset
    Sidebar->>Data: Load CSV
    Data-->>Sidebar: Return DataFrame
    Sidebar->>Logic: Pass Filtered Data
    Logic->>App: Render Dashboard/Pages
    App->>User: Display Insights
    end
```

### 2.2 Auto-Analyzer Flow (Independent Upload)

```mermaid
sequenceDiagram
    participant User
    participant App
    
    rect rgb(255, 250, 250)
    note right of User: Auto-Analyzer Flow (Page 05)
    User->>App: Upload Raw CSV (Any Format)
    App->>App: Auto-clean Strings/Numbers
    App->>User: Show Preview & Stats
    User->>App: Select Column to Analyze
    App->>App: Generate Histograms/Boxplots
    App->>User: Display Single/Multi-col Plots
    end
```

## 3. Component Interaction Map

A refined view of how specific pages interact with core modules.

```mermaid
graph LR
    subgraph "Analysis Pages"
        P1[Numerical Analysis]
        P2[Visualize Data]
        P3[Trend Analysis]
    end

    subgraph "Shared Core Modules"
        U[utils.py]
        S[sidebar.py]
        D[data_variables.py]
    end

    P1 & P2 & P3 --> S
    P1 & P2 & P3 --> U
    P1 & P2 --> D
```
