import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import os
import CCN_Shipping
import CCN_Edit
import CCN_Custom_Formula

class CCN_Automation:

    def __init__(self, window): 
        #Initializing window
        self.window = window
        self.window.title("Classic Custom Nutrition")

        #Upload CSV
        self.csv_name = tk.Label(self.window, text="CSV File Path Here", borderwidth=2, relief="solid")
        self.csv_upload_but = tk.Button(self.window, text="Upload (.csv)", command=self.choose_file)
        
        #Checkbox variables
        self.shipping_val = tk.IntVar()
        self.product_val = tk.IntVar()
        self.invoice_val = tk.IntVar()
        self.formula_val = tk.IntVar()

        #Checkboxes for shipping labels, generate invoice, product label (with nutrition label), ingredient formula
        self.ship_label = tk.Checkbutton(self.window, text="Generate Shipping Labels", variable=self.shipping_val)
        self.prod_label = tk.Checkbutton(self.window, text="Generate Product Labels", variable=self.product_val)
        self.invoice_label = tk.Checkbutton(self.window, text="Generate Invoice", variable=self.invoice_val)
        self.formula_label = tk.Checkbutton(self.window, text="Generate Formula Dosages", variable=self.formula_val)

        #Submit button
        self.submit_but = tk.Button(self.window, text="Submit", command=self.read_and_parse_csv)

        #Setting grids
        self.csv_upload_but.grid(row=0,column=3, padx=5, pady=5)
        self.csv_name.grid(row=0,column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.ship_label.grid(row=1, column=0)
        self.prod_label.grid(row=1, column=1)
        self.invoice_label.grid(row=1, column=2)
        self.formula_label.grid(row=1, column=3)
        self.submit_but.grid(row=2, column=1, columnspan=2, sticky="nsew", pady=5)
        
    #Allows user to choose file and should be reflected in the file label box
    def choose_file(self):
        self.csv_file_name = filedialog.askopenfile(filetypes=[("CSV", "*.csv")], initialdir=os.getcwd())
        self.csv_name['text'] = self.csv_file_name.name.split('/')[-1]

    #Allows user to choose folder to save contents into
    def choose_folder(self):
        messagebox.showinfo("Folder Selection", "Please Choose A Folder Location To Save Contents")
        folder_path = filedialog.askdirectory(title='Please Select Folder To Store Contents', initialdir=os.getcwd())
        return folder_path

    #Read in given .csv file, ensure it is proper one, and return as dataframe
    def read_and_parse_csv(self):
        #Add error handling to ensure a .csv file was inputted
        if self.csv_name['text'] == 'CSV File Path Here': messagebox.showerror(
            'File Error', 'Must Choose File Prior To Submission.\nPlease Try Again.')
    
        #Read in csv file and fill nan values then choose folder for data to be saved
        self.csv_df = pd.read_csv(self.csv_file_name)
        self.csv_df = self.csv_df.fillna('')
        self.folder_save = self.choose_folder()
        #For Formula Calculations:
            #Create list of ingredients for each product and do dictionary of lists
            #Key will be name of blend "Checkout Form: Name" --> Dictionary will be used for formula calculations, invoice, etc.
    
        #Returns a dictionary of lists with all of the current products offered
        products = CCN_Edit.CCN_Products.get_product_info()
        write_out_form = []

        for row_num, row_data in self.csv_df.iterrows():
            item_type = row_data['Lineitem name']
            
            #Create instance of class for calculating formula and writing out. Used in product label generation and formula output
            formula_calculator = CCN_Custom_Formula.CCN_Formula_Parser(item_type, row_data, products, self.csv_df, row_num)
            
            #Checking to see if row has all requirements for shipping label population
            if self.shipping_val.get() == 1 and item_type in products['shippable_products'] and row_data['Shipping Method'] in products['shipping_methods']:
                CCN_Shipping.CCN_Shipping(self.folder_save, row_data).generate_shipping_label()
                
            #NEXT --> Create IF Statement for producing a product label
            if self.product_val.get() == 1 and item_type in products['product_label_products']:
                
                #Returns the formula composition of ONE blend at a time based on current row
                blend_composition = formula_calculator.get_formula_breakdown()
                
                #If we want to calculate formulas go ahead and append so we dont have to recalculate again later
                if self.formula_val.get() == 1 and item_type in products['formula_products']:
                    total_composition = formula_calculator.calc_formulas(blend_composition)
                    write_out_form.append(total_composition)
                    
                #If it is an else we assume our product is a supplement and not a pre such as creatine, beta-alanine, etc.
                else:
                    print('This part needs supplements to begin being purchased to create')
                #Now we have all of the ingredients we need to generate product label --> START HERE
                
                
            #NEXT --> Create IF Statement for creating formula calculations and outputting in a file
            #We need to check if product val hasnt already calculated what we need
            if self.formula_val.get() == 1 and item_type in products['formula_products'] and not self.product_val.get() == 1:
                blend_composition = formula_calculator.get_formula_breakdown()
                total_composition = formula_calculator.calc_formulas(blend_composition)
                write_out_form.append(total_composition)
            
        #If the length of our list of formulas is greater than zero we need to write it out to csv file
        if len(write_out_form) > 0:
            formula_calculator.write_out_formulas(write_out_form)
                

                
    


def main():
    #Setting Window Elements
    window = tk.Tk()
    main_win = CCN_Automation(window)
    window.mainloop()
if __name__ == "__main__":
    main()
