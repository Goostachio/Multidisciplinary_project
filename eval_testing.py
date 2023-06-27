print("Test eval")
equation = 'x1+2*x2+x3'
def modify_value(x1,x2,x3):
    result = eval(equation)
    print(result)
    return result
a=5
modify_value(a,2,3)



def init_glogal_equation():
    headers={}
    aio_url="https://io.adafruit.com/api/v2/Multidisciplinary_Project/feeds/equation"
    x = requests.get(url=aio_url, headers=headers, verify=False)
    data=x.json()
    global_equation = data["last_value"]
    print("Get lastest value:", global_equation)



    init_glogal_equation()