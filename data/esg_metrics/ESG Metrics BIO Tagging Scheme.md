# ESG Metrics BIO Tagging Scheme

## Tag Format
- B-[Category]_[Topic]_[Metric]: Beginning of an entity
- I-[Category]_[Topic]_[Metric]: Inside of an entity
- O: Outside of any entity

## Categories
1. ENV: Environmental
2. SOC: Social
3. GOV: Governance

## Environmental (ENV) Tags

### Greenhouse Gas Emissions
- B/I-ENV_GHG_AET: Absolute emissions (Total)
- B/I-ENV_GHG_AE1: Absolute emissions (Scope 1)
- B/I-ENV_GHG_AE2: Absolute emissions (Scope 2)
- B/I-ENV_GHG_AE3: Absolute emissions (Scope 3)
- B/I-ENV_GHG_EIT: Emission intensities (Total)
- B/I-ENV_GHG_EI1: Emission intensities (Scope 1)
- B/I-ENV_GHG_EI2: Emission intensities (Scope 2)
- B/I-ENV_GHG_EI3: Emission intensities (Scope 3)

### Energy Consumption
- B/I-ENV_ENC_TEC: Total energy consumption
- B/I-ENV_ENC_ECI: Energy consumption intensity

### Water Consumption
- B/I-ENV_WAC_TWC: Total water consumption
- B/I-ENV_WAC_WCI: Water consumption intensity

### Waste Generation
- B/I-ENV_WAG_TWG: Total waste generated

## Social (SOC) Tags

### Gender Diversity
- B/I-SOC_GED_CEG_M: Current employees by gender (Male)
- B/I-SOC_GED_CEG_F: Current employees by gender (Female)
- B/I-SOC_GED_NHG_M: New hires by gender (Male)
- B/I-SOC_GED_NHG_F: New hires by gender (Female)
- B/I-SOC_GED_ETG_M: Employee turnover by gender (Male)
- B/I-SOC_GED_ETG_F: Employee turnover by gender (Female)

### Age-Based Diversity
- B/I-SOC_AGD_CEA_U30: Current employees by age (Under 30)
- B/I-SOC_AGD_CEA_B35: Current employees by age (Between 30 and 50)
- B/I-SOC_AGD_CEA_A50: Current employees by age (Above 50)
- B/I-SOC_AGD_NHI_U30: New hires by age (Under 30)
- B/I-SOC_AGD_NHI_B35: New hires by age (Between 30 and 50)
- B/I-SOC_AGD_NHI_A50: New hires by age (Above 50)
- B/I-SOC_AGD_TOR_U30: Turnover by age (Under 30)
- B/I-SOC_AGD_TOR_B35: Turnover by age (Between 30 and 50)
- B/I-SOC_AGD_TOR_A50: Turnover by age (Above 50)

### Development & Training
- B/I-SOC_DEV_ATH_M: Average training hours (Male)
- B/I-SOC_DEV_ATH_F: Average training hours (Female)

### Occupational Health & Safety
- B/I-SOC_OHS_FAT: Fatalities
- B/I-SOC_OHS_HCI: High-consequence injuries
- B/I-SOC_OHS_REC: Recordable injuries
- B/I-SOC_OHS_RWI: Recordable work-related ill health cases

## Governance (GOV) Tags

### Board Composition
- B/I-GOV_BOC_BIN: Board independence
- B/I-GOV_BOC_WOB: Women on the board

### Management Diversity
- B/I-GOV_MAD_WMT: Women in the management team

### Ethical Behaviour
- B/I-GOV_ETB_ACD: Anti-corruption disclosures
- B/I-GOV_ETB_ACT_N: Anti-corruption training (Number)
- B/I-GOV_ETB_ACT_P: Anti-corruption training (Percentage)

### Certifications
- B/I-GOV_CER_LRC: List of relevant certifications

### Alignment with Frameworks
- B/I-GOV_ALF_AFD: Alignment with frameworks and disclosure practices

### Assurance
- B/I-GOV_ASS_ASR: Assurance of sustainability report