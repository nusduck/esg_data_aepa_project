# ESG Metrics BIO Tagging Scheme

## Tag Format
- B-[Category]_[Topic]_[Metric]: Beginning of an entity
- I-[Category]_[Topic]_[Metric]: Inside of an entity
- B-VALUE: Beginning of a value
- I-VALUE: Inside of a value
- B-UNIT: Beginning of a unit
- I-UNIT: Inside of a unit
- O: Outside of any entity

## Categories
1. ENV: Environmental
2. SOC: Social
3. GOV: Governance

## Environmental (ENV) Tags

### Greenhouse Gas Emissions
- B-ENV_GHG_AET: Absolute emissions (Total)
- I-ENV_GHG_AET: Absolute emissions (Total)
- B-ENV_GHG_AE1: Absolute emissions (Scope 1)
- I-ENV_GHG_AE1: Absolute emissions (Scope 1)
- B-ENV_GHG_AE2: Absolute emissions (Scope 2)
- I-ENV_GHG_AE2: Absolute emissions (Scope 2)
- B-ENV_GHG_AE3: Absolute emissions (Scope 3)
- I-ENV_GHG_AE3: Absolute emissions (Scope 3)
- B-ENV_GHG_EIT: Emission intensities (Total)
- I-ENV_GHG_EIT: Emission intensities (Total)
- B-ENV_GHG_EI1: Emission intensities (Scope 1)
- I-ENV_GHG_EI1: Emission intensities (Scope 1)
- B-ENV_GHG_EI2: Emission intensities (Scope 2)
- I-ENV_GHG_EI2: Emission intensities (Scope 2)
- B-ENV_GHG_EI3: Emission intensities (Scope 3)
- I-ENV_GHG_EI3: Emission intensities (Scope 3)

### Energy Consumption
- B-ENV_ENC_TEC: Total energy consumption
- I-ENV_ENC_TEC: Total energy consumption
- B-ENV_ENC_ECI: Energy consumption intensity
- I-ENV_ENC_ECI: Energy consumption intensity

### Water Consumption
- B-ENV_WAC_TWC: Total water consumption
- I-ENV_WAC_TWC: Total water consumption
- B-ENV_WAC_WCI: Water consumption intensity
- I-ENV_WAC_WCI: Water consumption intensity

### Waste Generation
- B-ENV_WAG_TWG: Total waste generated
- I-ENV_WAG_TWG: Total waste generated

## Social (SOC) Tags

### Gender Diversity
- B-SOC_GED_CEG_M: Current employees by gender (Male)
- I-SOC_GED_CEG_M: Current employees by gender (Male)
- B-SOC_GED_CEG_F: Current employees by gender (Female)
- I-SOC_GED_CEG_F: Current employees by gender (Female)
- B-SOC_GED_NHG_M: New hires by gender (Male)
- I-SOC_GED_NHG_M: New hires by gender (Male)
- B-SOC_GED_NHG_F: New hires by gender (Female)
- I-SOC_GED_NHG_F: New hires by gender (Female)
- B-SOC_GED_ETG_M: Employee turnover by gender (Male)
- I-SOC_GED_ETG_M: Employee turnover by gender (Male)
- B-SOC_GED_ETG_F: Employee turnover by gender (Female)
- I-SOC_GED_ETG_F: Employee turnover by gender (Female)

### Age-Based Diversity
- B-SOC_AGD_CEA_U30: Current employees by age (Under 30)
- I-SOC_AGD_CEA_U30: Current employees by age (Under 30)
- B-SOC_AGD_CEA_B35: Current employees by age (Between 30 and 50)
- I-SOC_AGD_CEA_B35: Current employees by age (Between 30 and 50)
- B-SOC_AGD_CEA_A50: Current employees by age (Above 50)
- I-SOC_AGD_CEA_A50: Current employees by age (Above 50)
- B-SOC_AGD_NHI_U30: New hires by age (Under 30)
- I-SOC_AGD_NHI_U30: New hires by age (Under 30)
- B-SOC_AGD_NHI_B35: New hires by age (Between 30 and 50)
- I-SOC_AGD_NHI_B35: New hires by age (Between 30 and 50)
- B-SOC_AGD_NHI_A50: New hires by age (Above 50)
- I-SOC_AGD_NHI_A50: New hires by age (Above 50)
- B-SOC_AGD_TOR_U30: Turnover by age (Under 30)
- I-SOC_AGD_TOR_U30: Turnover by age (Under 30)
- B-SOC_AGD_TOR_B35: Turnover by age (Between 30 and 50)
- I-SOC_AGD_TOR_B35: Turnover by age (Between 30 and 50)
- B-SOC_AGD_TOR_A50: Turnover by age (Above 50)
- I-SOC_AGD_TOR_A50: Turnover by age (Above 50)

### Development & Training
- B-SOC_DEV_ATH_M: Average training hours (Male)
- I-SOC_DEV_ATH_M: Average training hours (Male)
- B-SOC_DEV_ATH_F: Average training hours (Female)
- I-SOC_DEV_ATH_F: Average training hours (Female)

### Occupational Health & Safety
- B-SOC_OHS_FAT: Fatalities
- I-SOC_OHS_FAT: Fatalities
- B-SOC_OHS_HCI: High-consequence injuries
- I-SOC_OHS_HCI: High-consequence injuries
- B-SOC_OHS_REC: Recordable injuries
- I-SOC_OHS_REC: Recordable injuries
- B-SOC_OHS_RWI: Recordable work-related ill health cases
- I-SOC_OHS_RWI: Recordable work-related ill health cases

## Governance (GOV) Tags

### Board Composition
- B-GOV_BOC_BIN: Board independence
- I-GOV_BOC_BIN: Board independence
- B-GOV_BOC_WOB: Women on the board
- I-GOV_BOC_WOB: Women on the board

### Management Diversity
- B-GOV_MAD_WMT: Women in the management team
- I-GOV_MAD_WMT: Women in the management team

### Ethical Behaviour
- B-GOV_ETB_ACD: Anti-corruption disclosures
- I-GOV_ETB_ACD: Anti-corruption disclosures
- B-GOV_ETB_ACT_N: Anti-corruption training (Number)
- I-GOV_ETB_ACT_N: Anti-corruption training (Number)
- B-GOV_ETB_ACT_P: Anti-corruption training (Percentage)
- I-GOV_ETB_ACT_P: Anti-corruption training (Percentage)

### Certifications
- B-GOV_CER_LRC: List of relevant certifications
- I-GOV_CER_LRC: List of relevant certifications

### Alignment with Frameworks
- B-GOV_ALF_AFD: Alignment with frameworks and disclosure practices
- I-GOV_ALF_AFD: Alignment with frameworks and disclosure practices

### Assurance
- B-GOV_ASS_ASR: Assurance of sustainability report
- I-GOV_ASS_ASR: Assurance of sustainability report