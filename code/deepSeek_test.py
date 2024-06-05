from openai import OpenAI
import json
import sys
import time
import random

client = OpenAI(api_key="sk-71287091fdfe4b2888b64653fbbf5fac", base_url="https://api.deepseek.com")

# prompt = "You are a professional teacher, who are judging items. For the problem, there are two answers, [1] and [2]. You need to choose the better one based on the instruction and the input. Please show your anwser with a pair of brackets directly in the response, like [0], [1] or [2]. If you think [1] is better than [2], return [1]. If you think [2] is better than [1], return [2]. If you think they are similar, return [0].  You don't need to give other addtional response. "
pandalm_prompt = "For the problem, there are two answers, [1] and [2]. You need to choose the better one based on the instruction and the input. Please show your anwser with a pair of brackets directly in the response, like [0], [1] or [2]. If you think [1] is better than [2], return [1]. If you think [2] is better than [1], return [2]. If you think they are similar, return [0].  You don't need to give other addtional response. "
# autoj_prompt = "For the problem in a specific scenario, there are two answers, [1] and [2]. You need to choose the better one based on the instruction and the input. Please show your anwser with a pair of brackets directly in the response, like [0], [1] or [2]. If you think [1] is better than [2], return [1]. If you think [2] is better than [1], return [2]. If you think they are similar, return [0].  You don't need to give other addtional response. "
# autoj_prompt = "There are one instruction and two responses ([1] and [2]). You need to choose the better one based on the instruction and the input. Please show your anwser with a pair of brackets directly in the response, like [0], [1] or [2]. If you think [1] is better than [2], return [1]. If you think [2] is better than [1], return [2]. If you think they are similar, return [0].  You don't need to give other addtional response. "
# autoj_prompt = "For the problem in a specific scenario, there are one instruction and two responses ([1] and [2]). You need to choose the better one based on the instruction and the input. Please show your anwser with a pair of brackets directly in the response, like [0], [1] or [2]. If you think [1] is better than [2], return [1]. If you think [2] is better than [1], return [2]. If there is no significant difference between the two , return [0]. For example: scenario: reading_comprehensio, task:Read the table below regarding \"Shagun Sharma\" to answer the given question.\n\nYear | 2016 | 2016 | 2019 | 2017 | 2019 | 2017\u201318 | 2019 | 2015\nChannel | Sony TV | &TV | &TV | Star Plus | &TV | Colors TV | &TV | Star Plus\nTitle | Kuch Rang Pyar Ke Aise Bhi | Gangaa | Shaadi Ke Siyape | Iss Pyaar Ko Kya Naam Doon 3 | Vikram Betaal Ki Rahasya Gatha | Tu Aashiqui | Laal Ishq | Kuch Toh Hai Tere Mere Darmiyaan\nRole | Khushi | Aashi Jhaa | Dua | Meghna Narayan Vashishth | Rukmani/Kashi | Richa Dhanrajgir | Pernia | Sanjana Kapoor\n\nQuestion: What TV shows was Shagun Sharma seen in 2019?, response 1: In 2019, Shagun Sharma was seen in the TV shows \"Shaadi Ke Siyape\" and \"Vikram Betaal Ki Rahasya Gatha\" on &TV, as well as \"Laal Ishq\" also on &TV. response 2: Shagun Sharma was seen in the TV shows Kuch Rang Pyar Ke Aise Bhi, Gangaa, Iss Pyaar Ko Kya Naam Doon 3, Vikram Betaal Ki Rahasya Gatha, and Tu Aashiqui. Your anwser should be [0]"
# autoj_prompt = "There are one instruction and two responses ([1] and [2]). You need to choose the better one based on the instruction and the input. Please show your anwser with a pair of brackets directly in the response, like [1] or [2]. If you think [1] is better than [2], return [1]. If you think [2] is better than [1], return [2]. You don't need to give other addtional response. "
autoj_prompt = "For the problem in a specific scenario, there are one instruction and two responses ([1] and [2]). You need to choose the better one based on the instruction and the input. Please show your anwser with a pair of brackets directly in the response, like [0], [1] or [2]. If you think [1] is better than [2], return [1]. If you think [2] is better than [1], return [2]. If there is no significant difference between the two , return [0]. For example: Read the table below regarding \"Shagun Sharma\" to answer the given question.\n\nYear | 2016 | 2016 | 2019 | 2017 | 2019 | 2017\u201318 | 2019 | 2015\nChannel | Sony TV | &TV | &TV | Star Plus | &TV | Colors TV | &TV | Star Plus\nTitle | Kuch Rang Pyar Ke Aise Bhi | Gangaa | Shaadi Ke Siyape | Iss Pyaar Ko Kya Naam Doon 3 | Vikram Betaal Ki Rahasya Gatha | Tu Aashiqui | Laal Ishq | Kuch Toh Hai Tere Mere Darmiyaan\nRole | Khushi | Aashi Jhaa | Dua | Meghna Narayan Vashishth | Rukmani/Kashi | Richa Dhanrajgir | Pernia | Sanjana Kapoor\n\nQuestion: What TV shows was Shagun Sharma seen in 2019?, response 1 Shagun Sharma was seen in \"Shaadi Ke Siyape\" and \"Vikram Betaal Ki Rahasya Gatha\" in 2019., response 2: In 2019, Shagun Sharma was seen in the TV shows \"Shaadi Ke Siyape\" and \"Vikram Betaal Ki Rahasya Gatha\" on &TV, and \"Laal Ishq\" on &TV. Your anwser should be [1]"


llmbar_prompt = "For the problem, there are two answers, [1] and [2]. You need to choose the better one based on the instruction and the input. Please show your anwser with a pair of brackets directly in the response, like [1] or [2]. If you think [1] is better than [2], return [1]. If you think [2] is better than [1], return [2].  You don't need to give other addtional response. "

def query_LLM(question):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": question}
        ],
        # temperature=0.0,
        stream=False
    )
    return response.choices[0].message.content



def test_pandalm(output_filename, reverse=False):
    result = []
    data = []
    if reverse:
        with open("../dataset/PandaLM_test_reverse.json", "r") as f:
            data = json.load(f)
    else:
        with open("../dataset/PandaLM_test.json", "r") as f:
            data = json.load(f)

    #send prompt
    try:
        for dic in data:
            sleep_time = random.uniform(0, 0.05)
            time.sleep(sleep_time)

            answerList = [0,0,0]
            instruction = dic["instruction"]
            input_ = dic["input"]
            answer1 = dic["response1"]
            answer2 = dic["response2"]
            query = pandalm_prompt+ "\nInstruction: "+ instruction+ "\nInput: "+ input_ + "\nAnswer 1: "+ str(answer1) + "\nAnswer 2: "+ str(answer2)

            answerList[dic["annotator1"]] += 1
            answerList[dic["annotator2"]] += 1
            answerList[dic["annotator3"]] += 1
            if answerList[0] >= 2:
                peopleAnswer = 0
            elif answerList[1] >= 2:
                peopleAnswer = 1
            else:
                peopleAnswer = 2
            response = query_LLM(query)
            print(dic["idx"], ", LLM: ", response, " people: ", peopleAnswer)
            result.append({"idx": dic["idx"], "people":peopleAnswer, "LLM": response})
    except Exception as e:
        print(e)
        if reverse:
            with open("../result/%s_reverse.json"%(output_filename), "w") as f:
                json.dump(result, f, indent=4)
        else:
            with open("../result/%s.json"%(output_filename), "w") as f:
                json.dump(result, f, indent=4)
    if reverse:
        with open("../result/%s_reverse.json"%(output_filename), "w") as f:
            json.dump(result, f, indent=4)
    else:
        with open("../result/%s.json"%(output_filename), "w") as f:
            json.dump(result, f, indent=4)
    
    return

def test_autoj(output_filename, reverse=False):
    result = []
    data = []
    if reverse:
        with open("../dataset/AutoJ_test_reverse.jsonl", "r") as f:
            for line in f:
                data.append(json.loads(line.strip()))
    else:
        with open("../dataset/AutoJ_test.jsonl", "r") as f:
            for line in f:
                data.append(json.loads(line.strip()))
    
    #send prompt
    try:
        idx = 0
        for dic in data:
            # if idx <= current_idx+1:
            #     idx += 1 
            #     continue
            sleep_time = random.uniform(0, 0.05)
            time.sleep(sleep_time)

            instruction = dic["prompt"]
            answer1 = dic["response 1"]
            answer2 = dic["response 2"]
            scenario = dic["scenario"]
            # query = autoj_prompt + "\nScenario: " + scenario + "\nInstruction: "+ instruction + "\nAnswer 1: "+ str(answer1) + "\nAnswer 2: "+ str(answer2)
            query = autoj_prompt + "\nInstruction: "+ instruction + "\nAnswer 1: "+ str(answer1) + "\nAnswer 2: "+ str(answer2)
            peopleAnswer = dic["label"]
            response = query_LLM(query)
            print(idx, ", LLM: ", response, " people: ", peopleAnswer)
            result.append({"idx": idx, "people":peopleAnswer, "LLM": response})
            idx += 1
    except Exception as e:
        print(e)
        if reverse:
            with open("../result/%s_reverse.json"%(output_filename), "w") as f:
                json.dump(result, f, indent=4)
        else:
            with open("../result/%s.json"%(output_filename), "w") as f:
                json.dump(result, f, indent=4)
    if reverse:
        with open("../result/%s_reverse.json"%(output_filename), "w") as f:
            json.dump(result, f, indent=4)
    else:
        with open("../result/%s.json"%(output_filename), "w") as f:
            json.dump(result, f, indent=4)
    
    return


def test_llmbar(output_filename, reverse=False):
    result = []
    data = []

    if reverse:
        with open("../dataset/LLMBar_test_reverse.json", "r") as f:
            data = json.load(f)
    else:
        with open("../dataset/LLMBar.json", "r") as f:
            data = json.load(f)
    
    #send prompt
    try:
        idx = 0
        for dic in data:
            # if idx <= current_idx+1:
            #     idx += 1 
            #     continue
            sleep_time = random.uniform(0, 0.05)
            time.sleep(sleep_time)

            instruction = dic["input"]
            answer1 = dic["output_1"]
            answer2 = dic["output_2"]
            query = llmbar_prompt+ "\nInstruction: "+ instruction + "\nAnswer 1: "+ str(answer1) + "\nAnswer 2: "+ str(answer2)

            peopleAnswer = dic["label"]
            response = query_LLM(query)
            print(idx, ", LLM: ", response, " people: ", peopleAnswer)
            result.append({"idx": idx, "people":peopleAnswer, "LLM": response})
            idx += 1
    except Exception as e:
        print(e)
        if reverse:
            with open("../result/%s_reverse.json"%(output_filename), "w") as f:
                json.dump(result, f, indent=4)
        else:
            with open("../result/%s.json"%(output_filename), "w") as f:
                json.dump(result, f, indent=4)
    if reverse:
        with open("../result/%s_reverse.json"%(output_filename), "w") as f:
            json.dump(result, f, indent=4)
    else:
        with open("../result/%s.json"%(output_filename), "w") as f:
            json.dump(result, f, indent=4)
    
    return

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python script.py benchmark(PandaLM/Auto-J/LLMBar/MTBench + _reverse) output_filename")
        sys.exit(1)
    
    benchmark_name = sys.argv[1]
    if benchmark_name == "PandaLM":
        test_pandalm(sys.argv[2])
    elif benchmark_name == "AutoJ":
        test_autoj(sys.argv[2])
    elif benchmark_name == "LLMBar":
        test_llmbar(sys.argv[2])
    elif benchmark_name == "PandaLM_reverse":
        test_pandalm(sys.argv[2],True)
    elif benchmark_name == "AutoJ_reverse":
        test_autoj(sys.argv[2],True)
    elif benchmark_name == "LLMBar_reverse":
        test_llmbar(sys.argv[2],True)