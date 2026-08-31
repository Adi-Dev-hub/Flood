# Flood
Flood Risk Assessment Using GIS and AHP

A Python-based prototype for spatial flood-risk assessment using Geographic Information System (GIS) data and the Analytic Hierarchy Process (AHP).

Overview

This project explores a GIS-based approach to combining multiple geographical and environmental factors into a single flood-risk score.

The current implementation uses an AHP weighting method to combine six factors:

- Elevation
- Slope
- Proximity to rivers
- Land cover
- Rainfall
- Historical flood occurrence

The resulting score is attached to the input geographic features and visualized as a flood-risk map.

The current project is a prototype for experimentation with GIS-based multi-criteria risk assessment, rather than a validated operational flood-prediction system.

Method

The current risk-assessment pipeline is approximately:

Geospatial Input
      │
      ├── Elevation
      ├── Slope
      ├── River Proximity
      ├── Land Cover
      ├── Rainfall
      └── Historical Floods
              │
              ▼
       AHP Weight Calculation
              │
              ▼
       Weighted Risk Score
              │
              ▼
        GIS Visualization

AHP weighting

The project defines a pairwise comparison matrix for the six factors and calculates:

1. Normalized factor weights
2. A priority vector
3. Maximum eigenvalue approximation
4. Consistency Index (CI)
5. Consistency Ratio (CR)

The implementation rejects the weighting matrix when the calculated consistency ratio is greater than "0.1".

The current pairwise matrix and AHP implementation are defined in "GIS.py".

Current Implementation

The main application is implemented in "GIS.py".

It provides a basic PyQt5 interface that allows the user to:

- Select a study-area shapefile
- Optionally select a DEM GeoTIFF
- Run the flood-risk calculation
- Display the resulting risk map

The project uses:

- Python
- GeoPandas for vector geospatial data
- Rasterio for raster/GeoTIFF processing
- NumPy for numerical calculations
- Matplotlib for visualization
- PyQt5 for the desktop interface
- Pillow for image handling

The repository also contains supporting scripts for rainfall, slope, land-cover processing, raster handling, visualization, and testing.

Data

The repository currently contains or references several GIS-related resources, including:

- A Pune district boundary shapefile
- Raster/GeoTIFF files
- Rainfall data in CSV format
- Land-use/land-cover processing scripts
- Slope and rainfall processing scripts
- Generated risk-map output

The project should not be interpreted as having a complete, authoritative flood-risk dataset.

Important data limitation

The current "GIS.py" implementation contains placeholder/synthetic values for several factors.

When a DEM is not provided, elevation values are randomly generated. In addition, the current implementation generates random values for:

- Slope
- River proximity
- Land cover
- Rainfall
- Historical flood occurrence

Therefore, the resulting risk score should currently be treated as a prototype output, not as a validated representation of real-world flood risk.

Replacing these placeholders with properly aligned, sourced and validated datasets is necessary for meaningful geographic risk assessment.

Repository Structure

Flood/
│
├── Features/
├── GUI/
├── Testing/
├── data/
│
├── GIS.py
├── colorFind.py
├── createFiles.py
├── debug_shape.py
├── displayFiles.py
│
├── lulcEx.py
├── lulcMB.py
├── lulc_integer_check.py
│
├── rainele.py
├── rainpre.py
├── rainfall_data.csv
│
├── slopeelerain.py
├── sloperain.py
├── testTiff.py
├── tifpredict.py
│
├── Punelc.tif
├── dubdistrict_boundry_pune.shp
│
├── combined_risk_output.png
├── requirements.txt
└── README.md

The exact role and maturity of individual supporting scripts varies; some are exploratory or utility scripts rather than components of a single production pipeline.

Installation

Clone the repository:

git clone https://github.com/Adi-Dev-hub/Flood.git
cd Flood

Install the Python dependencies:

pip install -r requirements.txt

The project uses geospatial Python libraries, so installation may require platform-specific support depending on the operating system and Python environment.

Running the Current Prototype

The main application can be started with:

python GIS.py

The interface asks for:

1. A study-area shapefile
2. Optionally, a DEM TIFF file

After selecting the inputs, use Predict Flood Risk to execute the current risk-scoring pipeline.

Limitations

The current implementation has several limitations that should be considered before using it for real-world decision-making.

1. Synthetic factor values

Several risk factors are currently generated randomly rather than derived from corresponding spatial datasets.

This means the resulting map is not suitable for real-world flood-risk decisions.

2. Spatial alignment

The current implementation does not yet provide a complete, robust pipeline for aligning all raster and vector factors to a common spatial reference, resolution and extent.

This is necessary before combining heterogeneous GIS datasets reliably.

3. Risk-score normalization

The current implementation directly combines factor values using AHP weights. The individual factors are not yet consistently normalized into a common risk scale before aggregation.

This can make factors with larger numerical ranges disproportionately influential.

4. AHP methodology

The pairwise comparison matrix is manually defined in the current implementation.

The quality of the final risk score therefore depends on the validity of these expert-assigned comparisons and on the quality of the underlying factor data.

5. Validation

The repository does not currently establish that the calculated risk scores have been validated against an authoritative flood-risk map or sufficiently documented historical flood events.

Validation should be added before treating the system as predictive.

6. Desktop prototype

The current main interface is implemented using PyQt5. It is not currently a web-based GIS application.

Planned Improvements

Potential development directions include:

- Replace synthetic values with real geospatial datasets
- Normalize individual risk factors before AHP aggregation
- Improve raster/vector spatial alignment
- Add reproducible data preprocessing pipelines
- Incorporate additional hazard layers
- Improve historical-event validation
- Provide configurable AHP weights
- Add uncertainty information to risk outputs
- Improve map visualization
- Separate data-processing, risk-model and UI components
- Develop a web-based GIS interface
- Add automated testing for geospatial processing

Relation to Multi-Hazard Risk Assessment

The current architecture can potentially be extended beyond flood-only assessment.

A generalized version could combine multiple hazard layers:

Flood
  +
Landslide
  +
Other Available Hazards
  +
Exposure
  +
Vulnerability
       │
       ▼
Multi-Criteria Spatial Analysis
       │
       ▼
Risk Classification
       │
       ▼
GIS Decision-Support Interface

Such an extension would require additional hazard-specific datasets and a revised methodology. It should not be considered part of the current implementation.

Project Status

Status: Prototype / Experimental

The project currently demonstrates the basic implementation of a GIS-based AHP risk-scoring workflow. It is not yet a validated operational flood prediction or disaster-management system.


Until a license is added, the repository should not be assumed to grant general permission to reuse, modify or redistribute the code.


