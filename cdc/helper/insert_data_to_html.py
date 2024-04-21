

def html_mail(data_array):
    if len(data_array) == 0:
        with open ('helper/noProductsFound.html', 'r') as file:
            return file.read()
    
    signs = ['i', 'n', 'p', 'k', 'y', 'b', 'l']
    pref = ""
    with open ('helper/prefix.html', 'r') as file:
        pref = file.read()
    
    whole_mail = pref
    for i in range(len(data_array)):
        data = data_array[i]
        print(data["image_link"], flush=True)
        sign_values = [data['image_link'], data['brand'] + ' ' +  data['model'], data['price'], data['kilometers'], data['first_registry'], data['gas_type'], data['ad_link']]
        temp_mail = ""
        with open ('helper/product.html', 'r') as file:
            temp_mail = file.read()
            for i in range(len(signs)):
                temp_mail = temp_mail.replace('#' + signs[i] + '#', str(sign_values[i]))
        whole_mail += temp_mail
    
    with open ('helper/suffix.html', 'r') as file:
        whole_mail += file.read()
    
    return whole_mail
