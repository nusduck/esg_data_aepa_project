import os
import json
import pprint

if __name__ == '__main__':
    folder_path = "data/esg_label_result/" 
    label_dict ={
        "B-ENV_GHG_AET": 0,
        "I-ENV_GHG_AET": 0,
        "B-ENV_GHG_AE1": 0,
        "I-ENV_GHG_AE1": 0,
        "B-ENV_GHG_AE2": 0,
        "I-ENV_GHG_AE2": 0,
        "B-ENV_GHG_AE3": 0,
        "I-ENV_GHG_AE3": 0,
        "B-ENV_GHG_EIT": 0,
        "I-ENV_GHG_EIT": 0,
        "B-ENV_GHG_EI1": 0,
        "I-ENV_GHG_EI1": 0,
        "B-ENV_GHG_EI2": 0,
        "I-ENV_GHG_EI2": 0,
        "B-ENV_GHG_EI3": 0,
        "I-ENV_GHG_EI3": 0,
        "B-ENV_ENC_TEC": 0,
        "I-ENV_ENC_TEC": 0,
        "B-ENV_ENC_ECI": 0,
        "I-ENV_ENC_ECI": 0,
        "B-ENV_WAC_TWC": 0,
        "I-ENV_WAC_TWC": 0,
        "B-ENV_WAC_WCI": 0,
        "I-ENV_WAC_WCI": 0,
        "B-ENV_WAG_TWG": 0,
        "I-ENV_WAG_TWG": 0,
        "B-SOC_GED_CEG_M": 0,
        "I-SOC_GED_CEG_M": 0,
        "B-SOC_GED_CEG_F": 0,
        "I-SOC_GED_CEG_F": 0,
        "B-SOC_GED_NHG_M": 0,
        "I-SOC_GED_NHG_M": 0,
        "B-SOC_GED_NHG_F": 0,
        "I-SOC_GED_NHG_F": 0,
        "B-SOC_GED_ETG_M": 0,
        "I-SOC_GED_ETG_M": 0,
        "B-SOC_GED_ETG_F": 0,
        "I-SOC_GED_ETG_F": 0,
        "B-SOC_AGD_CEA_U30": 0,
        "I-SOC_AGD_CEA_U30": 0,
        "B-SOC_AGD_CEA_B35": 0,
        "I-SOC_AGD_CEA_B35": 0,
        "B-SOC_AGD_CEA_A50": 0,
        "I-SOC_AGD_CEA_A50": 0,
        "B-SOC_AGD_NHI_U30": 0,
        "I-SOC_AGD_NHI_U30": 0,
        "B-SOC_AGD_NHI_B35": 0,
        "I-SOC_AGD_NHI_B35": 0,
        "B-SOC_AGD_NHI_A50": 0,
        "I-SOC_AGD_NHI_A50": 0,
        "B-SOC_AGD_TOR_U30": 0,
        "I-SOC_AGD_TOR_U30": 0,
        "B-SOC_AGD_TOR_B35": 0,
        "I-SOC_AGD_TOR_B35": 0,
        "B-SOC_AGD_TOR_A50": 0,
        "I-SOC_AGD_TOR_A50": 0,
        "B-SOC_DEV_ATH_M": 0,
        "I-SOC_DEV_ATH_M": 0,
        "B-SOC_DEV_ATH_F": 0,
        "I-SOC_DEV_ATH_F": 0,
        "B-SOC_OHS_FAT": 0,
        "I-SOC_OHS_FAT": 0,
        "B-SOC_OHS_HCI": 0,
        "I-SOC_OHS_HCI": 0,
        "B-SOC_OHS_REC": 0,
        "I-SOC_OHS_REC": 0,
        "B-SOC_OHS_RWI": 0,
        "I-SOC_OHS_RWI": 0,
        "B-GOV_BOC_BIN": 0,
        "I-GOV_BOC_BIN": 0,
        "B-GOV_BOC_WOB": 0,
        "I-GOV_BOC_WOB": 0,
        "B-GOV_MAD_WMT": 0,
        "I-GOV_MAD_WMT": 0,
        "B-GOV_ETB_ACD": 0,
        "I-GOV_ETB_ACD": 0,
        "B-GOV_ETB_ACT_N": 0,
        "I-GOV_ETB_ACT_N": 0,
        "B-GOV_ETB_ACT_P": 0,
        "I-GOV_ETB_ACT_P": 0,
        "B-GOV_CER_LRC": 0,
        "I-GOV_CER_LRC": 0,
        "B-GOV_ALF_AFD": 0,
        "I-GOV_ALF_AFD": 0,
        "B-GOV_ASS_ASR": 0,
        "I-GOV_ASS_ASR": 0,
        "B-VALUE": 0,
        "I-VALUE": 0,
        "B-UNIT": 0,
        "I-UNIT": 0
    }
    for filename in os.listdir(folder_path):
        print(filename)
        json_filepath = os.path.join(folder_path, filename)
        with open(json_filepath, "r", encoding="utf-8") as file:
            json_content = file.read()
            json_content = json.loads(json_content)
        for item in json_content:
            entity = item['entity']
            for en in entity:
                label = en['labels'][0]
                if label in label_dict.keys():
                    label_dict[label] += 1
    pprint.pprint(label_dict)
            
            