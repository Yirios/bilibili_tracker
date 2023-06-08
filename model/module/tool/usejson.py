import json

def write_json(path,info):
    with open(path,"w",encoding='utf8') as f:
        f.write(json.dumps(info, ensure_ascii=False, indent=4, separators=(',', ':')))
    return 'ok'

def read_json(path):
    with open(path,'r',encoding='utf8')as fp:
        json_data = json.load(fp)
    return json_data

if __name__ == '__main__':
    dic = {1:'31','332':{13:True,'76':[123,False]}}
    write_json('test/a.json',dic)
    print(read_json('test/a.json'))