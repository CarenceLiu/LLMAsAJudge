import json
import sys
from openai import OpenAI

prompt = "I will give you an instruction. You need to help me choose the most suited classification of the instruction. The classifications are: post_summarization,writing_advertisement,language_polishing,writing_product_description,writing_news_article,writing_marketing_materials,note_summarization,text_simplification,writing_biography,keywords_extraction,writing_scientific_paper,code_simplification,explaining_general,others,creative_writing,asking_how_to_question,chitchat,brainstorming,math_reasoning,solving_exam_question_with_math,open_question,instructional_rewriting,roleplay,code_generation,seeking_advice,ranking,writing_email,counterfactual,value_judgement,verifying_fact,writing_song_lyrics,writing_personal_essay,text_to_text_translation,question_generation,functional_writing,planning,text_summarization,analyzing_general,code_correction_rewriting,recommendation,writing_blog_post,explaining_code,writing_presentation_script,information_extraction,paraphrasing,solving_exam_question_without_math,code_to_code_translation,classification_identification,data_analysis,writing_cooking_recipe,title_generation,text_correction,writing_social_media_post,reading_comprehension,writing_legal_document,writing_technical_document,topic_modeling,writing_job_application."
prompt_2 = " You need to directly give the classification without any explanation.(the classification must be in the above list). The instruction is: "
client = OpenAI(api_key="sk-71287091fdfe4b2888b64653fbbf5fac", base_url="https://api.deepseek.com")

def query_LLM(question):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": question}
        ],
        stream=False
    )
    return response.choices[0].message.content


def query_classification_pandalm():
    with open("../dataset/PandaLM_test.json", "r") as f:
        data = json.load(f)
    i = 0
    try:
        for dic in data:
            insturction = dic["instruction"]
            query = prompt+prompt_2+insturction
            response = query_LLM(query)
            dic["scenario"] = response
            i += 1
            print(i, " instuction: ", insturction, "scenario: ", response)
    except Exception as e:
        print(e)
        with open("../result/pandalm_classification.json", "w") as f:
            data = json.dump(data, f, indent=4)

    with open("../result/pandalm_classification.json", "w") as f:
        data = json.dump(data, f, indent=4)
    return data

if __name__ == "__main__":
    print("AutoJ")
    total = {}
    correct = {}
    with open("../dataset/AutoJ_test_reverse.jsonl", "r") as fr:
        with open("../result/autoj_normal_reverse.json", "r") as fr2:
            data = json.load(fr2)
            idx = 0
            for line in fr:
                dic = json.loads(line.strip())
                if dic["scenario"] in total:
                    total[dic["scenario"]] += 1
                else:
                    total[dic["scenario"]] = 1
                if dic["scenario"] not in correct:
                    correct[dic["scenario"]] = 0
                if str(data[idx]["people"]) == data[idx]["LLM"][1]:
                    correct[dic["scenario"]] += 1
                idx += 1
    for key in total:
        print(key, " ", correct[key], " ", total[key], " ", correct[key]/total[key])

    print("****************************")
    print("****************************")
    print("****************************")
    print("PandaLM")
    total = {}
    correct = {}
    with open("../result/pandalm_classification.json", "r") as fr:
        with open("../result/pandalm_normal.json", "r") as fr2:
            text = json.load(fr)
            data = json.load(fr2)
            idx = 0
            for dic in text:
                if dic["scenario"] in total:
                    total[dic["scenario"]] += 1
                else:
                    total[dic["scenario"]] = 1
                if dic["scenario"] not in correct:
                    correct[dic["scenario"]] = 0
                if str(data[idx]["people"]) == data[idx]["LLM"][1]:
                    correct[dic["scenario"]] += 1
                idx += 1
    for key in total:
        print(key, " ", correct[key], " ", total[key], " ", correct[key]/total[key])