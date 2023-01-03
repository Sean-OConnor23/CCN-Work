class CCN_Products:
    #This is where we can easily edit the type of products once we add them to the website
    def get_product_info():
        product_dict ={}
        #Used in Shipping Label Generation. Create list of products we ship for ease of addition
        product_dict['shippable_products'] = ["Build Your Blend base", "Classic Max (25 Servings)", "Classic Pump (25 Servings)", "Classic Blend (25 Servings)"]
        product_dict['shipping_methods'] = ["UPS"] 

        #Array used in product label generation and formula generation. Should Occur in every instance except apparel orders
        product_dict['product_label_products'] = ["Build Your Blend base", "Classic Max (25 Servings)", "Classic Pump (25 Servings)", "Classic Blend (25 Servings)"]
        #Composition of CLASSIC MAX BLEND
        product_dict['Classic Max (25 Servings)'] = {'Product Name':'Classic Max', 'Creatine':'10g', 'Beta-Alanine':'6.5g', 'L-Citrulline':'10g',
            'L-Tyrosine':'1.6g', 'Caffeine':'400mg', 'Niacin (B3)':'30mg', 'Iodized Salt':'2g'}
        #Composition of CLASSIC PUMP BLEND
        product_dict['Classic Pump (25 Servings)'] = {'Product Name':'Classic Pump', 'Creatine':'5.0g', 'Beta-Alanine':'4.0g', 'L-Citrulline':'8.0g',
            'L-Tyrosine':'1.2g', 'Caffeine':'0mg', 'Niacin (B3)':'20mg', 'Iodized Salt':'2g'}
        #Composition of CLASSIC BLEND BLEND
        product_dict['Classic Blend (25 Servings)'] = {'Product Name':'Classic Blend', 'Creatine':'5.0g', 'Beta-Alanine':'3.5g', 'L-Citrulline':'8.0g',
            'L-Tyrosine':'1.2g', 'Caffeine':'200mg', 'Niacin (B3)':'30mg', 'Iodized Salt':'1g'}

        product_dict['custom_ingredients'] = ["Niacin (B3)", "Beta-Alanine", "L-Citrulline", "Caffeine", "Creatine", "Iodized Salt", "L-Tyrosine"]

        return product_dict