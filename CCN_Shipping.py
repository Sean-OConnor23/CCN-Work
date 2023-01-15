import easypost
import os
import wget
import shutil
import datetime


class CCN_Shipping():

    def __init__(self, folder_save_path_in, ship_info_in):

        self.folder_save= folder_save_path_in
        self.ship_info= ship_info_in

    #Will use EasyPost API and given address info to generate shipping labels
    def generate_shipping_label(self):
        easypost.api_key = "EZTKd1d7eb2403954c0e84b730efd8d4a020CgJy1M6VEzzLTRlcPvhYpg" #TEST API KEY
        #easypost.api_key = "EZAKd1d7eb2403954c0e84b730efd8d4a020eBydUBdeNki0arw70VqYSg" #PRODUCTION API KEY
        
        #The address the shipping label will make for from
        fromAddress = easypost.Address.create(
            verify = True,
            company = "Classic Custom Nutrition",
            street1 = "325 Wrightsburg Ct",
            city = "Fayetteville",
            state = "GA",
            zip = "30215",
            #phone = "2567770239", #Taking out for the time being
            country = 'US'
        )

        #Created based on user given information
        toAddress = easypost.Address.create(
            verify = True,
            name = self.ship_info['Shipping Name'],
            street1 = self.ship_info['Shipping Address1'],
            street2 = self.ship_info['Shipping Address2'],
            city = self.ship_info['Shipping City'],
            state = self.ship_info['Shipping Province'],
            zip = int(self.ship_info['Shipping Zip']),
            country = self.ship_info['Shipping Country']
        )

        #Measurements are in inches and Weight is in ounces
        #This is our default size atm, could pass in new size in the future
        parcel = easypost.Parcel.create(
            length = 8,
            width = 8,
            height = 7,
            weight = 64
        )

        #return and buyer address defaulted from the fromAddress
        shipment = easypost.Shipment.create(
            to_address = toAddress,
            from_address = fromAddress,
            parcel = parcel
        )

        shipping_label_info = shipment.buy(rate=shipment.lowest_rate(carriers=['UPSDAP'], services=['Ground']))
        
        #Pull proper data from Easypost reply
        shipping_label_url = shipping_label_info['postage_label']['label_url']
        tracking_number = shipping_label_info['tracking_code']

        #Temporary management of tracking number
        print("\nName: " + str(self.ship_info['Shipping Name']) + " --> Tracking Number: " + str(tracking_number))

        #Check to see if directory exists. If not, make it
        folder_path = os.path.join(self.folder_save,'Shipping_Labels')
        if not os.path.exists(folder_path): os.makedirs(folder_path)
        
        #Get timestamp and append to file name to ensure shipping labels are unique
        current_time = str(datetime.datetime.now())
        current_time = current_time.replace('.', '_')
        file_path = os.path.join(folder_path,self.ship_info['Shipping Name'] + " " + str(current_time) + ".png")
        response = wget.download(shipping_label_url, file_path)
