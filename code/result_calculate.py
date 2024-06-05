import json
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py fileName")
        sys.exit(1)

    data = []
    result = [[0 for _ in range(3)] for _ in range(3)]
    with open("../result/%s.json"%(sys.argv[1]), "r") as f:
        data = json.load(f)
    
    if data == []:
        print("Check the file!")
        sys.exit(1)
    
    total = 0
    for item in data:
        people = item["people"]
        if item["LLM"][1] != "0" and item["LLM"][1] != "1" and item["LLM"][1] != "2":
            continue
        llm = int(item["LLM"][1])
        result[people][llm] += 1
        total += 1
    
    if result[0][0] + result[1][0] + result[2][0] != 0:
        accuracy = (result[0][0] + result[1][1] + result[2][2])*100/total
        p0 = result[0][0]/(result[0][0]+result[1][0]+result[2][0])
        p1 = result[1][1]/(result[0][1]+result[1][1]+result[2][1])
        p2 = result[2][2]/(result[0][2]+result[1][2]+result[2][2])
        p = (p0+p1+p2)/3
        r0 = result[0][0]/(sum(result[0]))
        r1 = result[1][1]/(sum(result[1]))
        r2 = result[2][2]/(sum(result[2]))
        r = (r0+r1+r2)/3
    else:
        accuracy = (result[1][1] + result[2][2])*100/total
        p1 = result[1][1]/(result[1][1]+result[2][1])
        p2 = result[2][2]/(result[1][2]+result[2][2])
        p = (p1+p2)/3
        r1 = result[1][1]/(sum(result[1]))
        r2 = result[2][2]/(sum(result[2]))
        r = (r1+r2)/3
    print(result[0][0]," ",result[0][1]," ",result[0][2])
    print(result[1][0]," ",result[1][1]," ",result[1][2])
    print(result[2][0]," ",result[2][1]," ",result[2][2])
    print("%s accuracy: %.2f, F1 score: %.2f"%(sys.argv[1], accuracy, 2*p*r*100/(p+r)))
    