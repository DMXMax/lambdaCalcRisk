import json


def calcRisk(event, context):
    permitted_fields = ['safety', 'reliability', 'customer', 'financial']
    status = {"code":0, "msg":""}


    data_out = dict([[key,value] for [key,value] in event.items() 
        if key in permitted_fields])

    min_val = {"category":"", "value":8}
    max_val = {"category":"", "value":0}
    total = count = 0
    
    for key,value in data_out.items():
        if value < min_val["value"]:
            min_val = {"category":key, "value":value}
        if value > max_val["value"]:
            max_val = {"category":key, "value":value}
        total = total + value
        count = count + 1
    if count > 0:
        floor = max_val["value"]*10.00 if max_val["value"]>4 else 0
        raw_score = round((total/count)/7*100,2)
        adj_score = max(floor, raw_score)

        result = {
            "scores": data_out,
            "min": min_val,
            "max": max_val,
            "avg": round(total/count,2),
            "raw_score": raw_score, 
            "adj_score": adj_score
        }

    else:
        status={"code":500, "msg":"No data provided"}
        result={}

    response = {
        "status": json.dumps(status),
        "result": json.dumps(result)
    }

    return response

