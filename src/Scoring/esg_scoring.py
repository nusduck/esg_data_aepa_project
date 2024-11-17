import json
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import zscore
import numpy as np  

# Set the working directory to the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Define ESG indicators and weights
indicator_weights = {
    'ENV': {'GHG': 0.4, 'Energy': 0.3, 'Water': 0.2, 'Waste': 0.1},
    'SOC': {'Diversity': 0.4, 'Employment': 0.3, 'HealthSafety': 0.2, 'Training': 0.1},
    'GOV': {'BoardComposition': 0.3, 'ManagementDiversity': 0.3, 'Ethics': 0.1, 'Transparency': 0.1, 'Certifications': 0.1, 'Assurance':0.1}
}

# Weights for ESG dimensions
weights = {'E': 0.25, 'S': 0.3, 'G': 0.35, 'Coverage': 0.1}

positive_metrics = ['Diversity', 'Employment', 'Training', 'HealthSafety', 'BoardComposition', 'ManagementDiversity',
                    'Ethics', 'Certifications', 'Transparency']
negative_metrics = ['GHG', 'Waste', 'Water', 'Energy']

# Label Mapping
replacement_dict = {
    "B-ENV_GHG_AET": "GHG", "I-ENV_GHG_AET": "GHG",
    "B-ENV_GHG_AE1": "GHG", "I-ENV_GHG_AE1": "GHG",
    "B-ENV_GHG_AE2": "GHG", "I-ENV_GHG_AE2": "GHG",
    "B-ENV_GHG_AE3": "GHG", "I-ENV_GHG_AE3": "GHG",
    "B-ENV_GHG_EIT": "GHG", "I-ENV_GHG_EIT": "GHG",
    "B-ENV_GHG_EI1": "GHG", "I-ENV_GHG_EI1": "GHG",
    "B-ENV_GHG_EI2": "GHG", "I-ENV_GHG_EI2": "GHG",
    "B-ENV_GHG_EI3": "GHG", "I-ENV_GHG_EI3": "GHG",
    "B-ENV_ENC_TEC": "Energy", "I-ENV_ENC_TEC": "Energy",
    "B-ENV_ENC_ECI": "Energy", "I-ENV_ENC_ECI": "Energy",
    "B-ENV_WAC_TWC": "Water", "I-ENV_WAC_TWC": "Water",
    "B-ENV_WAC_WCI": "Water", "I-ENV_WAC_WCI": "Water",
    "B-ENV_WAG_TWG": "Waste", "I-ENV_WAG_TWG": "Waste",
    "B-SOC_GED_CEG_M": "Diversity", "I-SOC_GED_CEG_M": "Diversity",
    "B-SOC_GED_CEG_F": "Diversity", "I-SOC_GED_CEG_F": "Diversity",
    "B-SOC_GED_NHG_M": "Diversity", "I-SOC_GED_NHG_M": "Diversity",
    "B-SOC_GED_NHG_F": "Diversity", "I-SOC_GED_NHG_F": "Diversity",
    "B-SOC_GED_ETG_M": "Diversity", "I-SOC_GED_ETG_M": "Diversity",
    "B-SOC_GED_ETG_F": "Diversity", "I-SOC_GED_ETG_F": "Diversity",
    "B-SOC_AGD_CEA_U30": "Employment", "I-SOC_AGD_CEA_U30": "Employment",
    "B-SOC_AGD_CEA_B35": "Employment", "I-SOC_AGD_CEA_B35": "Employment",
    "B-SOC_AGD_CEA_A50": "Employment", "I-SOC_AGD_CEA_A50": "Employment",
    "B-SOC_AGD_NHI_U30": "Employment", "I-SOC_AGD_NHI_U30": "Employment",
    "B-SOC_AGD_NHI_B35": "Employment", "I-SOC_AGD_NHI_B35": "Employment",
    "B-SOC_AGD_NHI_A50": "Employment", "I-SOC_AGD_NHI_A50": "Employment",
    "B-SOC_AGD_TOR_U30": "Employment", "I-SOC_AGD_TOR_U30": "Employment",
    "B-SOC_AGD_TOR_B35": "Employment", "I-SOC_AGD_TOR_B35": "Employment",
    "B-SOC_AGD_TOR_A50": "Employment", "I-SOC_AGD_TOR_A50": "Employment",
    "B-SOC_EMP_TNM": "Employment", "B-SOC_EMP_TTN": "Employment",
    "B-SOC_DEV_ATH_M" :"Training", "B-SOC_DEV_ATH_F": "Training",
    "B-SOC_DEV_ATH_M": "HealthSafety", "I-SOC_DEV_ATH_M": "HealthSafety",
    "B-SOC_DEV_ATH_F": "HealthSafety", "I-SOC_DEV_ATH_F": "HealthSafety",
    "B-SOC_OHS_FAT": "HealthSafety", "I-SOC_OHS_FAT": "HealthSafety",
    "B-SOC_OHS_HCI": "HealthSafety", "I-SOC_OHS_HCI": "HealthSafety",
    "B-SOC_OHS_REC": "HealthSafety", "I-SOC_OHS_REC": "HealthSafety",
    "B-SOC_OHS_RWI": "HealthSafety", "I-SOC_OHS_RWI": "HealthSafety",
    "B-GOV_BOC_BIN": "BoardComposition", "I-GOV_BOC_BIN": "BoardComposition",
    "B-GOV_BOC_WOB": "BoardComposition", "I-GOV_BOC_WOB": "BoardComposition",
    "B-GOV_MAD_WMT": "ManagementDiversity", "I-GOV_MAD_WMT": "ManagementDiversity",
    "B-GOV_ETB_ACD": "Ethics", "I-GOV_ETB_ACD": "Ethics",
    "B-GOV_ETB_ACT_N": "Ethics", "I-GOV_ETB_ACT_N": "Ethics",
    "B-GOV_ETB_ACT_P": "Ethics", "I-GOV_ETB_ACT_P": "Ethics",
    "B-GOV_CER_LRC": "Certifications", "I-GOV_CER_LRC": "Certifications",
    "B-GOV_ALF_AFD": "Transparency", "I-GOV_ALF_AFD": "Transparency",
    "B-GOV_ASS_ASR": "Assurance", "I-GOV_ASS_ASR": "Assurance",
}

# Define Letter Rating
def assign_rating(score):
    if score >= 8.571:
        return "AAA"
    elif score >= 7.143:
        return "AA"
    elif score >= 5.714:
        return "A"
    elif score >= 4.286:
        return "BBB"
    elif score >= 2.857:
        return "BB"
    elif score >= 1.429:
        return "B"
    else:
        return "CCC"

# Define a function to handle z-score scoring
def z_score_interval_score(value, mean, std_dev, is_positive=True):
    if value is None:
        return 5  # Neutral score for missing data
    if std_dev == 0:
        return 5  # Neutral score if no variance
    z = (value - mean) / std_dev
    if is_positive:
        if z >= 1.5:
            return 10
        elif 1.0 <= z < 1.5:
            return 9
        elif 0.5 <= z < 1.0:
            return 7
        elif -0.5 <= z < 0.5:
            return 5
        elif -1.0 <= z < -0.5:
            return 3
        else:
            return 1
    else:
        if z <= -1.5:
            return 10
        elif -1.5 < z <= -1.0:
            return 9
        elif -1.0 < z <= -0.5:
            return 7
        elif -0.5 < z <= 0.5:
            return 5
        elif 0.5 < z <= 1.0:
            return 3
        else:
            return 1

# Extract numeric values, skip non-numeric entries
def extract_numeric_value(value_str):
    try:
        return float(value_str.replace(",", ""))
    except (ValueError, TypeError):
        return 0.0

# extract_company_data 
def extract_company_data(company_data):
    esg_data = {'ENV': {}, 'SOC': {}, 'GOV': {}}
    for entry in company_data:
        question_id = entry['question_id']
        response = entry['response']
        value = response.get('value', "0")
        
        mapped_label = replacement_dict.get(question_id)
        if not mapped_label:
            continue

        # Handle scoring for special text indicators
        if mapped_label == "Certifications":
            esg_data['GOV'][mapped_label] = 10 if value != "None" else 0
        elif mapped_label == "Transparency":
            esg_data['GOV'][mapped_label] = 10 if "GRI" in value or "TCFD" in value or "SASB" in value else 0
        elif mapped_label == "Assurance":
            if value.lower() == "internal, external":
                esg_data['GOV'][mapped_label] = 10
            elif value.lower() == "external":
                esg_data['GOV'][mapped_label] = 8
            elif value.lower() == "internal":
                esg_data['GOV'][mapped_label] = 5
            elif value.lower() == "none":
                esg_data['GOV'][mapped_label] = 0
        else:
            # Store numeric indicators
            if "ENV" in question_id:
                esg_data['ENV'][mapped_label] = esg_data['ENV'].get(mapped_label, 0) + extract_numeric_value(value)
            elif "SOC" in question_id:
                esg_data['SOC'][mapped_label] = esg_data['SOC'].get(mapped_label, 0) + extract_numeric_value(value)
            elif "GOV" in question_id:
                esg_data['GOV'][mapped_label] = esg_data['GOV'].get(mapped_label, 0) + extract_numeric_value(value)

    return esg_data

# Calculate report coverage
def calculate_coverage(esg_data):
    total_metrics = sum(len(metrics) for metrics in indicator_weights.values())
    reported_metrics = sum(1 for metrics in esg_data.values() for metric, value in metrics.items() if value > 0)
    coverage = reported_metrics / total_metrics
    return coverage

# Calculate coverage score
def calculate_coverage_score(coverage):
    return coverage * 10





# Define fixed-baseline-averages and standard deviations
fixed_industry_averages = {
    'ENV': {'GHG': 75, 'Energy': 50, 'Water': 30, 'Waste': 20},
    'SOC': {'Diversity': 0.6, 'Employment': 0.7, 'HealthSafety': 0.8, 'Training': 0.5},
    'GOV': {'BoardComposition': 0.4, 'ManagementDiversity': 0.3, 'Ethics': 0.5, 'Transparency': 0.6, 'Certifications': 0.4, 'Assurance': 0.3}
}

fixed_industry_std_devs = {
    'ENV': {'GHG': 10, 'Energy': 15, 'Water': 5, 'Waste': 8},
    'SOC': {'Diversity': 0.1, 'Employment': 0.05, 'HealthSafety': 0.15, 'Training': 0.2},
    'GOV': {'BoardComposition': 0.2, 'ManagementDiversity': 0.15, 'Ethics': 0.1, 'Transparency': 0.15, 'Certifications': 0.05, 'Assurance': 0.1}
}


def calculate_all_esg_scores(json_folder):
    
    # Use fixed averages and std devs instead of dynamically calculated values
    results = []
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(json_folder, filename)
            with open(file_path, 'r') as f:
                json_data = json.load(f)
                for company_name, company_data in json_data.items():
                    
                    # Use fixed baseline averages and std deviations
                    total_score, env_score, soc_score, gov_score, env_details, soc_details, gov_details, coverage, coverage_score = calculate_esg_score(
                        company_data, fixed_industry_averages, fixed_industry_std_devs)

                    result = {
                        'Company': company_name,
                        'Total ESG Score': total_score,
                        'ENV Score': env_score,
                        'SOC Score': soc_score,
                        'GOV Score': gov_score,
                        'Coverage': coverage,
                        'Coverage Score': coverage_score,
                        **{f'ENV_{k}': v for k, v in env_details.items()},
                        **{f'SOC_{k}': v for k, v in soc_details.items()},
                        **{f'GOV_{k}': v for k, v in gov_details.items()}
                    }
                    results.append(result)

    df = pd.DataFrame(results)
    scaler = MinMaxScaler(feature_range=(0, 10))
    df['Normalized Score'] = scaler.fit_transform(df[['Total ESG Score']])
    df['Letter Rating'] = df['Normalized Score'].apply(assign_rating)

    return df
    
# calculate detailed scores
def calculate_detailed_scores(values, sub_weights, dimension):
    dimension_score = 0
    detailed_scores = {}
    total_weight = 0  # Track the total weight for metrics reported
    
    # Use fixed-baseline-averages and std devs based on dimension
    averages = fixed_industry_averages[dimension]
    std_devs = fixed_industry_std_devs[dimension]
    
    for metric, weight in sub_weights.items():
        value = values.get(metric, averages.get(metric, None))  
        mean = averages.get(metric, 0)
        std_dev = std_devs.get(metric, 1)
        is_positive = metric in positive_metrics
        adjusted_score = z_score_interval_score(value, mean, std_dev, is_positive)
        
        metric_score = adjusted_score * weight
        dimension_score += metric_score
        detailed_scores[metric] = metric_score
        if value is not None:
            total_weight += weight  # Only count weights for non-missing metrics

    # Normalize the dimension score by the total weight of reported metrics
    dimension_score = (dimension_score / total_weight) if total_weight > 0 else 0
    return dimension_score, detailed_scores


def calculate_esg_score(company_data):
    esg_values = extract_company_data(company_data)
    
    env_score, env_details = calculate_detailed_scores(esg_values.get('ENV', {}), indicator_weights['ENV'], 'ENV')
    soc_score, soc_details = calculate_detailed_scores(esg_values.get('SOC', {}), indicator_weights['SOC'], 'SOC')
    gov_score, gov_details = calculate_detailed_scores(esg_values.get('GOV', {}), indicator_weights['GOV'], 'GOV')
    
    coverage = calculate_coverage(esg_values)
    coverage_score = calculate_coverage_score(coverage)
    
    # Calculate the total ESG score using weights for each ESG dimension
    total_score = (env_score * weights['E'] +
                   soc_score * weights['S'] + 
                   gov_score * weights['G'] +
                   coverage_score * weights['Coverage'])
    
    return total_score, env_score, soc_score, gov_score, env_details, soc_details, gov_details, coverage, coverage_score

# Main function for calculating all ESG scores
def calculate_all_esg_scores(json_folder):
    results = []
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(json_folder, filename)
            with open(file_path, 'r') as f:
                json_data = json.load(f)
                for company_name, company_data in json_data.items():
                    
                    # Use fixed-baseline-averages and std deviations
                    total_score, env_score, soc_score, gov_score, env_details, soc_details, gov_details, coverage, coverage_score = calculate_esg_score(
                        company_data)

                    result = {
                        'Company': company_name,
                        'Total ESG Score': total_score,
                        'ENV Score': env_score,
                        'SOC Score': soc_score,
                        'GOV Score': gov_score,
                        'Coverage': coverage,
                        'Coverage Score': coverage_score,
                        **{f'ENV_{k}': v for k, v in env_details.items()},
                        **{f'SOC_{k}': v for k, v in soc_details.items()},
                        **{f'GOV_{k}': v for k, v in gov_details.items()}
                    }
                    results.append(result)

    df = pd.DataFrame(results)
    scaler = MinMaxScaler(feature_range=(0, 10))
    df['Normalized Score'] = scaler.fit_transform(df[['Total ESG Score']])
    df['Letter Rating'] = df['Normalized Score'].apply(assign_rating)

    # Excel 
    output_path = os.path.join(script_dir, "../../data/esg_scores/esg_scores_detailed_with_ratings.xlsx")
    df.to_excel(output_path, index=False)

    return df

# Run the main function
json_folder_path = '../../data/esg_validation'
esg_scores_df = calculate_all_esg_scores(json_folder_path)
print(esg_scores_df)
