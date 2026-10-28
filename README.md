# Scheduling Solar

A desktop application that predicts the total duration of a residential solar panel installation using a multiple linear regression model trained on real job data.

Built by Harper Talbott, modeled on real solar panel installation data.

## What it does

Given a few job parameters, the app predicts how many labor hours the installation will take. Drive time is entered separately and added to the prediction at runtime.

**Model performance:** Cross-validated R² ≈ 0.54 (5-fold, averaged over 10 random seeds) — the model explains roughly 54% of variance in install duration. The remaining variance reflects factors not captured in the data, such as crew experience and site complexity.

**Features used:**
- Panel quantity
- Number of arrays
- Crew size (people on site)
- Install season
- Panel quantity × crew size interaction (captures multiplicative labor scaling)

## Project Structure

```
Scheduling Solar/
├── main.py                   # Entry point — run this to launch the app
├── model.py                  # Linear regression model (train + predict)
├── data/
│   ├── solar_data.csv        # Training data (264 roof mount jobs, 6 columns)
│   └── solar_data_full.csv   # Full dataset with all fields (used by analysis notebook)
├── analysis_colab.ipynb      # Data analysis notebook (run in Google Colab)
├── requirements.txt
└── .gitignore
```

## Setup

1. Clone the repo and navigate into the folder:
   ```bash
   git clone <your-repo-url>
   cd Scheduling-Solar
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

```bash
python main.py
```

> **Note:** Login credentials are placeholders (`user` / `pass`) for demonstration purposes. Replace `CORRECT_USERNAME` and `CORRECT_PASSWORD` in `main.py` with a proper auth system before any real deployment.

Enter the job details and click **Calculate** to get a predicted labor duration. Add drive time in the corresponding field — it is applied on top of the model's prediction.

## Data

Training data is proprietary and not included in this repository. To run the app with your own data, create a `data/` folder and add a `solar_data.csv` file with the following columns:

| Column | Type | Description |
|---|---|---|
| `Panel QTY` | integer | Number of panels installed |
| `# of Arrays` | integer | Number of roof arrays |
| `Estimated Total # of People on Site` | integer | Crew size |
| `Install Season` | string | Spring / Summer / Fall / Winter |
| `Estimated Total Direct Time` | float | Labor hours (target variable) |

## Data Analysis

Open `analysis_colab.ipynb` in [Google Colab](https://colab.research.google.com) to explore the dataset, test different models, and visualize feature relationships. The notebook expects a `solar_data_full.csv` with the full set of job fields — upload your own data when prompted.

## Limitations & Future Work

- R² ceiling is primarily a data problem, not a modeling problem. The variables most likely to improve accuracy — crew experience, site complexity, roof pitch — are not currently tracked.
- Model was trained on 264 roof mount jobs. Accuracy will improve as more records are logged.
- A future `evaluate.py` script could expose cross-validation results for reproducibility.
