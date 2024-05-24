import json
import sys

def pandallm_reverse():
    with open("../dataset/PandaLM_test.json", "r") as f:
        data = json.load(f)
    
    for dic in data:
        dic["response2"], dic["response1"] = dic["response1"], dic["response2"]
        
        if dic["annotator1"] == 1:
            dic["annotator1"] = 2
        elif dic["annotator1"] == 2:
            dic["annotator1"] = 1

        if dic["annotator2"] == 1:
            dic["annotator2"] = 2
        elif dic["annotator2"] == 2:
            dic["annotator2"] = 1

        if dic["annotator3"] == 1:
            dic["annotator3"] = 2
        elif dic["annotator3"] == 2:
            dic["annotator3"] = 1
    
    with open("../dataset/PandaLM_test_reverse.json", "w") as f:
        data = json.dump(data, f, indent=4)

def autoj_reverse():
    with open("../dataset/AutoJ_test.jsonl", "r") as fr:
        with open("../dataset/AutoJ_test_reverse.jsonl", "w") as fw:
            for line in fr:
                dic = json.loads(line.strip())
                dic["response 1"], dic["response 2"] = dic["response 2"], dic["response 1"]
                if dic["label"] == 1:
                    dic["label"] = 2
                elif dic["label"] == 2:
                    dic["label"] = 1
                s = json.dumps(dic)
                fw.write(s+"\n")

def llmbar_reverse():
    with open("../dataset/LLMBar.json", "r") as f:
        data = json.load(f)
    
    for dic in data:
        dic["output_1"], dic["output_2"] = dic["output_2"], dic["output_1"]
        if dic["label"] == 1:
            dic["label"] = 2
        elif dic["label"] == 2:
            dic["label"] = 1
        
    with open("../dataset/LLMBar_test_reverse.json", "w") as f:
        data = json.dump(data, f, indent=4)

if __name__ == "__main__":
    pandallm_reverse()
    autoj_reverse()
    llmbar_reverse()
