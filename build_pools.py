import os, json, time
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
client = InferenceClient(token=os.getenv("HUGGINGFACE_TOKEN"))

def build_pool(prompt, n):
    pool=set()
    while len(pool)<n:
        try:
            r=client.chat.completions.create(
                model="mistralai/Mistral-7B-Instruct-v0.2",
                messages=[{"role":"user","content":prompt}],
                temperature=0.8
            )
            pool.add(r.choices[0].message.content.strip())
        except:
            time.sleep(1)
    return list(pool)

def build_all():
    pools={
        "sprint":build_pool("Generate realistic engineering task titles.",120),
        "campaign":build_pool("Generate realistic marketing task titles.",120),
        "sales":build_pool("Generate realistic sales task titles.",120),
        "ops":build_pool("Generate realistic operations task titles.",120),
        "support":build_pool("Generate realistic support task titles.",120),
        "hr":build_pool("Generate realistic HR task titles.",120),
        "product":build_pool("Generate realistic product task titles.",120),
        "descriptions":build_pool("Write professional Asana task descriptions.",200),
        "comments":build_pool("Write professional Asana comments.",150)
    }
    with open("pools.json","w",encoding="utf8") as f:
        json.dump(pools,f,indent=2)
    print("Pools cached.")

if __name__=="__main__":
    build_all()
