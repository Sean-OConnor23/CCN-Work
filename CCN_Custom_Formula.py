import pandas as pd
class CCN_Formula_Parser:
    
    def __init__(self, item_type, row_data, products, csv_df, row_num):
        self.item_type = item_type
        self.row_data = row_data
        self.products = products
        self.csv_df = csv_df
        self.row_num = row_num
    
    def get_formula_breakdown(self):
        #Need product label so there must be flavor
        blend_compose = {'Flavor':self.row_data['Lineitem variant']}
        
        #Need to define what the label is going to have as its name
        #Premade blend is variable, others are hardcoded
        #If blend is custom we need to fast forward lines to get ingredients in blend and store
        if self.item_type == 'Build Your Blend Base': 

            #Customized Product Name
            product_name = self.row_data['Checkout Form: Name']
            if product_name == '': product_name = 'Build Your Blend'

            #Need to keep track of ingredients in custom blend
            blend_compose['Product Name'] = product_name
                    
            row_increment = self.row_num + 1
            #Continue to increment rows until we have all ingredients for premade blend
            while row_increment < len(self.csv_df) and not self.csv_df.iloc[row_increment]['Lineitem name'] in self.products['product_label_products']:
                temp_row = self.csv_df.iloc[row_increment]
                blend_compose[temp_row['Lineitem name']] = temp_row['Lineitem variant']
                row_increment += 1
            #Skip over these rows to optimize speed so we arent re-reading for no reason
            self.row_num = row_increment
            #print("Custom Blend --> " + str(blend_compose))

        #The customer has ordered a premade blend. Will store composition in CCN_Edit.py for easy future customization 
        else: 
            #The pipe command merges two dictionaries together
            blend_compose = blend_compose | self.products[self.item_type]
            #print("Pre-Made Blend --> " + str(blend_compose))

        #Need to run check to see all ingredients are included
        blend_compose = self.ingredient_check(blend_compose)

        #Now we have the blend composition in a "blend_compose" with everything we should need to produce a label and formula calculations.
        return blend_compose
    
    #Need to ensure all ingredients are in the dictionary even if they are zero
    def ingredient_check(self, blend_compose):
        #Go through each ingredient in list and see if the current composition includes it
        for ingredient in self.products['custom_ingredients']:
            if not ingredient in blend_compose: blend_compose[ingredient] = '0'
        return blend_compose
    
    
    #Given list of individual servings for blend and need to calculate dosages for entire blend
    def calc_formulas(self, formula):
        #Append in this order --> Product Name, Flavor, Creatine, Caffeine, L-Citrulline, L-Tyrosine, Iodized Salt, Niacin (B3), Beta-Alanine, Sweetener, Sugar Scoops
        total_formula = []
        total_formula.append(self.row_data['Billing Name'])
        #Go ahead and create variables for each ingredient
        total_formula.append(formula['Product Name'])
        total_formula.append(formula['Flavor'])
        
        #Need to convert everything to grams
        niacin = float(formula['Niacin (B3)'].replace('mg','')) / 1000
        beta_alanine = float(formula['Beta-Alanine'].replace('g',''))
        citrulline = float(formula['L-Citrulline'].replace('g',''))
        creatine = float(formula['Creatine'].replace('g',''))
        iodized_salt = float(formula['Iodized Salt'].replace('g',''))
        tyrosine = float(formula['L-Tyrosine'].replace('mg','')) / 1000
        caffeine = float(formula['Caffeine'].replace('mg','')) / 1000
        
        #Now we are ready to make out calculations
        total_formula.append(creatine * 25)
        total_formula.append(caffeine * 25)
        total_formula.append(citrulline * 25)
        total_formula.append(tyrosine * 25)
        total_formula.append(iodized_salt * 25)
        total_formula.append(niacin * 25)
        total_formula.append(beta_alanine * 25)
        
        X = (creatine * 1.409)+(citrulline * 1.48)+(tyrosine * 2.242)+(beta_alanine * 1.333)+(caffeine * 2.085)+(niacin * 1.339)+(iodized_salt * 0.755)+3.7  
        
        if X <= 14.8: total_scoops = 1
        elif X <=29.6: total_scoops = 2
        else: total_scoops = 3
        
        total_formula.append((((total_scoops * 14.8) - X) / 1.057) * 25)
        total_formula.append(total_scoops)
        #Now we have the total dosages for each blend in grams
        return total_formula
    
    #Given the final list/df of formulas and need to output to csv file
    def write_out_formulas(self, formulas):
        columns = ['Customer', 'Product Name', 'Flavor', 'Creatine', 'Caffeine', 'L-Citrulline', 'L-Tyrosine', 'Iodized Salt', 
                   'Niacin (B3)', 'Beta-Alanine', 'Sugar', 'Serving Size (Scoops)']
        formula_df = pd.DataFrame(formulas, columns=columns)
        formula_df.to_csv("FORMULA_CALCULATIONS.csv", index=False)