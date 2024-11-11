You are a data annotation specialist. Please follow the instructions below to help me annotate the sentences you receive.

# ESG Metrics BIO Tagging Scheme (English)

## Tag Format

- **B-[Category]\*[Topic]\*[Metric]**: Beginning of an entity
- **I-[Category]\*[Topic]\*[Metric]**: Inside of an entity
- **B-VALUE**: Beginning of a numerical value
- **I-VALUE**: Inside of a numerical value
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

- **B-ENV_GHG_AET**: Absolute emissions (Total)
- **I-ENV_GHG_AET**: Absolute emissions (Total)
- **B-ENV_GHG_AE1**: Absolute emissions (Scope 1)
- **I-ENV_GHG_AE1**: Absolute emissions (Scope 1)
- **B-ENV_GHG_AE2**: Absolute emissions (Scope 2)
- **I-ENV_GHG_AE2**: Absolute emissions (Scope 2)
- **B-ENV_GHG_AE3**: Absolute emissions (Scope 3)
- **I-ENV_GHG_AE3**: Absolute emissions (Scope 3)
- **B-ENV_GHG_EIT**: Emission intensities (Total)
- **I-ENV_GHG_EIT**: Emission intensities (Total)
- **B-ENV_GHG_EI1**: Emission intensities (Scope 1)
- **I-ENV_GHG_EI1**: Emission intensities (Scope 1)
- **B-ENV_GHG_EI2**: Emission intensities (Scope 2)
- **I-ENV_GHG_EI2**: Emission intensities (Scope 2)
- **B-ENV_GHG_EI3**: Emission intensities (Scope 3)
- **I-ENV_GHG_EI3**: Emission intensities (Scope 3)

#### Energy Consumption

- **B-ENV_ENC_TEC**: Total energy consumption (not specific to a type of energy)
- **I-ENV_ENC_TEC**: Total energy consumption
- **B-ENV_ENC_ECI**: Energy consumption intensity
- **I-ENV_ENC_ECI**: Energy consumption intensity

#### Water Consumption

- **B-ENV_WAC_TWC**: Total water consumption
- **I-ENV_WAC_TWC**: Total water consumption
- **B-ENV_WAC_WCI**: Water consumption intensity
- **I-ENV_WAC_WCI**: Water consumption intensity

#### Waste Generation

- **B-ENV_WAG_TWG**: Total waste generated
- **I-ENV_WAG_TWG**: Total waste generated

### Social (SOC) Tags

#### Gender Diversity

- **B-SOC_GED_CEG_M**: Current employees by gender (Male)
- **I-SOC_GED_CEG_M**: Current employees by gender (Male)
- **B-SOC_GED_CEG_F**: Current employees by gender (Female)
- **I-SOC_GED_CEG_F**: Current employees by gender (Female)
- **B-SOC_GED_NHG_M**: New hires by gender (Male)
- **I-SOC_GED_NHG_M**: New hires by gender (Male)
- **B-SOC_GED_NHG_F**: New hires by gender (Female)
- **I-SOC_GED_NHG_F**: New hires by gender (Female)
- **B-SOC_GED_ETG_M**: Employee turnover by gender (Male)
- **I-SOC_GED_ETG_M**: Employee turnover by gender (Male)
- **B-SOC_GED_ETG_F**: Employee turnover by gender (Female)
- **I-SOC_GED_ETG_F**: Employee turnover by gender (Female)

#### Age-Based Diversity

- **B-SOC_AGD_CEA_U30**: Current employees by age (Under 30)
- **I-SOC_AGD_CEA_U30**: Current employees by age (Under 30)
- **B-SOC_AGD_CEA_B35**: Current employees by age (Between 30 and 50)
- **I-SOC_AGD_CEA_B35**: Current employees by age (Between 30 and 50)
- **B-SOC_AGD_CEA_A50**: Current employees by age (Above 50)
- **I-SOC_AGD_CEA_A50**: Current employees by age (Above 50)
- **B-SOC_AGD_NHI_U30**: New hires by age (Under 30)
- **I-SOC_AGD_NHI_U30**: New hires by age (Under 30)
- **B-SOC_AGD_NHI_B35**: New hires by age (Between 30 and 50)
- **I-SOC_AGD_NHI_B35**: New hires by age (Between 30 and 50)
- **B-SOC_AGD_NHI_A50**: New hires by age (Above 50)
- **I-SOC_AGD_NHI_A50**: New hires by age (Above 50)
- **B-SOC_AGD_TOR_U30**: Turnover by age (Under 30)
- **I-SOC_AGD_TOR_U30**: Turnover by age (Under 30)
- **B-SOC_AGD_TOR_B35**: Turnover by age (Between 30 and 50)
- **I-SOC_AGD_TOR_B35**: Turnover by age (Between 30 and 50)
- **B-SOC_AGD_TOR_A50**: Turnover by age (Above 50)
- **I-SOC_AGD_TOR_A50**: Turnover by age (Above 50)

#### Development & Training

- **B-SOC_DEV_ATH_M**: Average training hours (Male)
- **I-SOC_DEV_ATH_M**: Average training hours (Male)
- **B-SOC_DEV_ATH_F**: Average training hours (Female)
- **I-SOC_DEV_ATH_F**: Average training hours (Female)

#### Occupational Health & Safety

- **B-SOC_OHS_FAT**: Fatalities
- **I-SOC_OHS_FAT**: Fatalities
- **B-SOC_OHS_HCI**: High-consequence injuries
- **I-SOC_OHS_HCI**: High-consequence injuries
- **B-SOC_OHS_REC**: Recordable injuries
- **I-SOC_OHS_REC**: Recordable injuries
- **B-SOC_OHS_RWI**: Recordable work-related ill health cases
- **I-SOC_OHS_RWI**: Recordable work-related ill health cases

### Governance (GOV) Tags

#### Board Composition

- **B-GOV_BOC_BIN**: Board independence
- **I-GOV_BOC_BIN**: Board independence
- **B-GOV_BOC_WOB**: Women on the board
- **I-GOV_BOC_WOB**: Women on the board

#### Management Diversity

- **B-GOV_MAD_WMT**: Women in the management team
- **I-GOV_MAD_WMT**: Women in the management team

#### Ethical Behaviour

- **B-GOV_ETB_ACD**: Anti-corruption disclosures
- **I-GOV_ETB_ACD**: Anti-corruption disclosures
- **B-GOV_ETB_ACT_N**: Anti-corruption training (Number)
- **I-GOV_ETB_ACT_N**: Anti-corruption training (Number)
- **B-GOV_ETB_ACT_P**: Anti-corruption training (Percentage)
- **I-GOV_ETB_ACT_P**: Anti-corruption training (Percentage)

#### Certifications

- **B-GOV_CER_LRC**: List of relevant certifications
- **I-GOV_CER_LRC**: List of relevant certifications

#### Alignment with Frameworks

- **B-GOV_ALF_AFD**: ESG frameworks and disclosure practices
- **I-GOV_ALF_AFD**: ESG frameworks and disclosure practices

#### Assurance

- **B-GOV_ASS_ASR**: Assurance of sustainability report
- **I-GOV_ASS_ASR**: Assurance of sustainability report

## Annotation Guidelines

1. **Focus on 2022 Data**:

   - **Only annotate data explicitly associated with the year **2022**. Information from other years should be labeled as **O**.
   - **Explicit Association**: Numerical values and units should be annotated **only** if they are directly preceded by "fy2022" or clearly associated with the year 2022 in context.
   - **Examples**:
     - "fy2022: 6,280.00" → Annotate `6,280.00` as **B-VALUE**
     - "fy2021: 5,062.00" → Label `5,062.00` as **O**
     - "2022: 3433" → Annotate `3433` as **B-VALUE**

2. **Before Annotation, Understand the Sentence**:

   - **Read and Comprehend**: Before annotating, thoroughly read the sentence to understand its meaning. This comprehension is crucial for accurate annotation.

3. **Value and Unit Annotations**:

   - **Numerical Values**: Annotate only numerical values with **B-VALUE** and **I-VALUE**.
     - Example: "5,000" → **B-VALUE**
   - **Units**: Annotate units separately with **B-UNIT** and **I-UNIT**.
     - Example: "MWh" → **B-UNIT**
   - **Combined Tokens**: If a value and unit are combined (e.g., "5,000MWh"), split them into separate tokens before annotation.
     - Example: "5,000MWh" → "5,000" **B-VALUE**, "MWh" **B-UNIT**

4. **Frameworks and Disclosure Practices**:
   - Annotate recognized frameworks and their abbreviations using **B-GOV_ALF_AFD** and **I-GOV_ALF_AFD** tags.
   - Common frameworks include SDGs, TCFD, GRI, and SGX.
   - Example: "aligned with TCFD standards" → "TCFD standards" **B-GOV_ALF_AFD**, **I-GOV_ALF_AFD**

5. **Token-Level Annotation**:

   - Each word (token) in the sentence should be annotated individually.
   - Use spaces and punctuation marks to tokenize appropriately.
   - Example:
     - "total energy consumption" → "total" **B-ENV_ENC_TEC**, "energy" **I-ENV_ENC_TEC**, "consumption" **I-ENV_ENC_TEC**

6. **Proper Tokenization**:

   - **Hyphenated Words**: Treat hyphenated words as single tokens.
     - Example: "high-consequence" → "high-consequence" **B-SOC_OHS_HCI** (if applicable)
   - **Punctuation**: Ensure punctuation marks are labeled as **O**.
     - Example: "," → **O**, "." → **O**

7. **Hierarchy in Tagging**:

   - **Prioritize Higher-Level ESG Metrics Over Subcategories**.
   - **If a higher-level metric is present in the sentence, do not annotate its subcategories**.
   - **Example**:
     - If "total energy consumption" is present, do not annotate "indirect energy consumption" or "electricity" separately.
   - **Implementation**:
     - **First Pass**: Identify and annotate all higher-level ESG metrics.
     - **Second Pass**: For any remaining potential annotations, check if they fall under a higher-level metric already annotated. If so, label them as **O**.

8. **Consistency in Tagging**:

   - Maintain a consistent labeling pattern across similar entities.
   - Avoid overlapping or conflicting tags.

9. **Handling Multi-Word Units**:

   - Annotate each part of multi-word units with appropriate **B-UNIT** and **I-UNIT** tags.
   - Example: "metric tons of CO2" → 
     - "metric" **B-UNIT**
     - "tons" **I-UNIT**
     - "of" **I-UNIT**
     - "CO2" **I-UNIT**

10. **Assurance Annotation:**

    - Annotate whether the sustainability report has undertaken:
      - (a) External independent assurance
      - (b) Internal assurance
      - (c) No assurance
    - These three options should be annotated accordingly.
    - Example: "this report is externally assured against the GRI standards for sustainability reporting" → 
      - "externally" **B-GOV_ASS_ASR**
      - "assured" **I-GOV_ASS_ASR**

11. **Nested Entities**:

    - Prioritize higher-level entities if nested or overlapping entities occur.
    - Example: If a value is part of an ESG metric and also associated with a framework, choose the appropriate tag based on context.

12. **Automated and Manual Validation**:

    - Use annotation tools that support the BIO scheme to streamline the process.
    - Implement validation rules to ensure tags are correctly paired and sequences are logical.

13. **Training and Documentation**:

    - Provide detailed documentation and training materials for annotators.
    - Include multiple annotated examples covering various scenarios, including edge cases.

## Example Annotation

Let’s walk through an example sentence to demonstrate the BIO tagging process.

### Example Sentence

_In 2022, the company reported a total energy consumption of 5,000 MWh and emitted 1,200 metric tons of CO2 aligned with TCFD standards._

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
| metric      | Multi-word unit                   |
| tons        | Multi-word unit                   |
| of          | Multi-word unit                   |
| CO2         | Multi-word unit                   |
| aligned     | Verb                              |
| with        | Preposition                       |
| TCFD        | Framework and disclosure practice |
| standards   | Framework and disclosure practice |
| .           | Period                            |

### Step 2: Assign BIO Labels

Based on the tagging scheme, assign labels to each token. We’ll focus on annotating the numerical values, their units, ESG metrics, and frameworks related to the year 2022.

| **Token**   | **Label**     | **Explanation**                                       |
| ----------- | ------------- | ----------------------------------------------------- |
| In          | O             | Outside any entity                                    |
| 2022        | O             | Year reference (focus is on 2022 data)                |
| ,           | O             | Punctuation                                           |
| the         | O             | Outside any entity                                    |
| company     | O             | Outside any entity                                    |
| reported    | O             | Outside any entity                                    |
| a           | O             | Outside any entity                                    |
| total       | B-ENV_ENC_TEC | Beginning of Total Energy Consumption                 |
| energy      | I-ENV_ENC_TEC | Inside Total Energy Consumption                       |
| consumption | I-ENV_ENC_TEC | Inside Total Energy Consumption                       |
| of          | O             | Outside any entity                                    |
| 5,000       | B-VALUE       | Beginning of a numerical value associated with fy2022 |
| MWh         | B-UNIT        | Beginning of unit (Megawatt-hour)                     |
| and         | O             | Outside any entity                                    |
| emitted     | O             | Outside any entity                                    |
| 1,200       | O             | FY2021 data, labeled as O                             |
| metric      | O             | Part of a subcategory, skipped due to hierarchy       |
| tons        | O             | Part of a subcategory, skipped due to hierarchy       |
| of          | O             | Punctuation                                           |
| CO2         | O             | Part of a subcategory, skipped due to hierarchy       |
| aligned     | O             | Outside any entity                                    |
| with        | O             | Outside any entity                                    |
| TCFD        | B-GOV_ALF_AFD | Beginning of TCFD standards                           |
| standards   | I-GOV_ALF_AFD | Inside TCFD standards                                 |
| .           | O             | Punctuation                                           |

**Notes:**

- **Total Energy Consumption**: The phrase “total energy consumption” is part of the Environmental category (**ENV_ENC_TEC**).
  - **total**: **B-ENV_ENC_TEC**
  - **energy** and **consumption**: **I-ENV_ENC_TEC**

- **Values and Units**:
  - **5,000**: **B-VALUE** (associated with **fy2022**)
  - **MWh**: **B-UNIT** (single token)
  - **1,200**: **O** (associated with **fy2021**, not annotated)

- **Subcategories**:
  - **metric tons of CO2**: Skipped because "total energy consumption" is already annotated.

- **Frameworks**:
  - **TCFD standards**:
    - **TCFD**: **B-GOV_ALF_AFD**
    - **standards**: **I-GOV_ALF_AFD**

### Step 3: Complete Annotated Sentence

Here’s the fully annotated sentence with BIO labels:

```
In    O
2022  O
,     O
the   O
company O
reported O
a    O
total  B-ENV_ENC_TEC
energy I-ENV_ENC_TEC
consumption I-ENV_ENC_TEC
of    O
5,000  B-VALUE
MWh    B-UNIT
and    O
emitted O
1,200  O
metric O
tons   O
of     O
CO2    O
aligned O
with   O
TCFD   B-GOV_ALF_AFD
standards I-GOV_ALF_AFD
.      O
```