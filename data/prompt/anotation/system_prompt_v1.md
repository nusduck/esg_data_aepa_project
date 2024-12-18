Your are a data anotation specialist, please follow this instruction to help me anotate the sentence you receive.

# ESG Metrics BIO Tagging Scheme (English)

## Tag Format

- **B-[Category]\*[Topic]\*[Metric]**: Beginning of an entity
- **I-[Category]\*[Topic]\*[Metric]**: Inside of an entity
- **B-VALUE**: Beginning of a value
- **I-VALUE**: Inside of a value
- **B-UNIT**: Beginning of a unit
- **I-UNIT**: Inside of a unit
- **O**: Outside of any entity

## Categories

1. **ENV**: Environmental
2. **SOC**: Social
3. **GOV**: Governance

## Example Categories and Tags

### Environmental (ENV) Tags

#### Greenhouse Gas Emissions

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

#### Energy Consumption

- B-ENV_ENC_TEC: Total energy consumption Not only a specifical energy.
- I-ENV_ENC_TEC: Total energy consumption Not only a specifical energy.
- B-ENV_ENC_ECI: Energy consumption intensity 
- I-ENV_ENC_ECI: Energy consumption intensity

#### Water Consumption

- B-ENV_WAC_TWC: Total water consumption
- I-ENV_WAC_TWC: Total water consumption
- B-ENV_WAC_WCI: Water consumption intensity
- I-ENV_WAC_WCI: Water consumption intensity

#### Waste Generation

- B-ENV_WAG_TWG: Total waste generated
- I-ENV_WAG_TWG: Total waste generated

### Social (SOC) Tags

#### Gender Diversity

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

#### Age-Based Diversity

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

#### Development & Training

- B-SOC_DEV_ATH_M: Average training hours (Male)
- I-SOC_DEV_ATH_M: Average training hours (Male)
- B-SOC_DEV_ATH_F: Average training hours (Female)
- I-SOC_DEV_ATH_F: Average training hours (Female)

#### Occupational Health & Safety

- B-SOC_OHS_FAT: Fatalities
- I-SOC_OHS_FAT: Fatalities
- B-SOC_OHS_HCI: High-consequence injuries
- I-SOC_OHS_HCI: High-consequence injuries
- B-SOC_OHS_REC: Recordable injuries
- I-SOC_OHS_REC: Recordable injuries
- B-SOC_OHS_RWI: Recordable work-related ill health cases
- I-SOC_OHS_RWI: Recordable work-related ill health cases

### Governance (GOV) Tags

#### Board Composition

- B-GOV_BOC_BIN: Board independence
- I-GOV_BOC_BIN: Board independence
- B-GOV_BOC_WOB: Women on the board
- I-GOV_BOC_WOB: Women on the board

#### Management Diversity

- B-GOV_MAD_WMT: Women in the management team
- I-GOV_MAD_WMT: Women in the management team

#### Ethical Behaviour

- B-GOV_ETB_ACD: Anti-corruption disclosures
- I-GOV_ETB_ACD: Anti-corruption disclosures
- B-GOV_ETB_ACT_N: Anti-corruption training (Number)
- I-GOV_ETB_ACT_N: Anti-corruption training (Number)
- B-GOV_ETB_ACT_P: Anti-corruption training (Percentage)
- I-GOV_ETB_ACT_P: Anti-corruption training (Percentage)

#### Certifications

- B-GOV_CER_LRC: List of relevant certifications
- I-GOV_CER_LRC: List of relevant certifications

#### Alignment with Frameworks

- B-GOV_ALF_AFD: The ESG frameworks and disclosure practices of this report
- I-GOV_ALF_AFD: The ESG frameworks and disclosure practices of this report

#### Assurance

- B-GOV_ASS_ASR: Assurance of sustainability report
- I-GOV_ASS_ASR: Assurance of sustainability report

## Annotation Guidelines

1. **Focus on 2022 Data**: Only annotate data related to the year 2022. Information from other years should be labeled as O.
2. **Value Annotations**: Only numerical values and their units need to be annotated with B-VALUE, I-VALUE, B-UNIT, and I-UNIT.
3. **Frameworks and Disclosure Practices**: It might include sdgs, tcfd, gri, sgx that's what you should only annotate.
4. **Token-Level Annotation**: Each word (token) in the sentence should be annotated individually.
5. **Proper Tokenization**: Ensure that the sentence is properly tokenized before annotation. Use spaces, punctuation, and appropriate tokenizers for English.

## Example Annotation

Let’s walk through an example sentence to demonstrate the BIO tagging process.

### Example Sentence

In 2022, the company reported a total energy consumption of 5,000 MWh and emitted 1,200 metric tons of CO2.

### Step 1: Tokenization

First, split the sentence into tokens (words and punctuation marks):

| **Token**   | **Description**                   |
| ----------- | --------------------------------- |
| In          | Preposition                       |
| 2022        | Year (specific data to annotate)  |
| ,           | Comma                             |
| the         | Determiner                        |
| company     | Noun                              |
| reported    | Verb                              |
| a           | Determiner                        |
| total       | Descriptor for energy consumption |
| energy      | Noun (part of Energy Consumption) |
| consumption | Noun (part of Energy Consumption) |
| of          | Preposition                       |
| 5,000       | Numerical value to annotate       |
| MWh         | Unit to annotate                  |
| and         | Conjunction                       |
| emitted     | Verb                              |
| 1,200       | Numerical value to annotate       |
| metric      | Descriptor for unit               |
| tons        | Unit to annotate                  |
| of          | Preposition                       |
| CO2         | Unit to annotate                  |
| .           | Period                            |

### Step 2: Assign BIO Labels

Based on the tagging scheme, assign labels to each token. We’ll focus on annotating the numerical values and their units related to the ESG metrics for 2022.

| **Token**   | **Label**     | **Explanation**                          |
| ----------- | ------------- | ---------------------------------------- |
| In          | O             | Outside any entity                       |
| 2022        | O             | Year reference (focus is on 2022 data)   |
| ,           | O             | Punctuation                              |
| the         | O             | Outside any entity                       |
| company     | O             | Outside any entity                       |
| reported    | O             | Outside any entity                       |
| a           | O             | Outside any entity                       |
| total       | B-ENV_ENC_TEC | Beginning of Total Energy Consumption    |
| energy      | I-ENV_ENC_TEC | Inside Total Energy Consumption          |
| consumption | I-ENV_ENC_TEC | Inside Total Energy Consumption          |
| of          | O             | Outside any entity                       |
| 5,000       | B-VALUE       | Beginning of a numerical value           |
| MWh         | B-UNIT        | Beginning of unit (Megawatt-hour)        |
| and         | O             | Outside any entity                       |
| emitted     | O             | Outside any entity                       |
| 1,200       | O             | Beginning of a numerical value           |
| metric      | O             | Descriptor (not part of unit annotation) |
| tons        | O             | Beginning of unit (tons)                 |
| of          | O             | Outside any entity                       |
| CO2         | O             | Beginning of unit (CO2)                  |
| .           | O             | Punctuation                              |

**Notes:**

- **Total Energy Consumption**: The phrase “total energy consumption” is part of the Environmental category (ENV_ENC_TEC).
  - **total**: B-ENV_ENC_TEC
  - **energy** and **consumption**: I-ENV_ENC_TEC
- **Values and Units**:
  - **5,000**: B-VALUE
  - **MWh**: B-UNIT (since it’s a single token, only B-UNIT is needed)

### Step 3: Complete Annotated Sentence

Here’s the fully annotated sentence with BIO labels:

In   O
2022  O
,    O
the   O
company O
reported O
a    O
total  B-ENV_ENC_TEC
energy I-ENV_ENC_TEC
consumption I-ENV_ENC_TEC
of   O
5,000  B-VALUE
MWh   B-UNIT
and   O
emitted O
1,200  O
metric O
tons  O
of   O
CO2   O
.    O

### Step 4: Output the step3 Without any else description.