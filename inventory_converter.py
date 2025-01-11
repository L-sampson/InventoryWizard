import pandas as pd
import os
from typing import List

# Class to convert inventory files to new CSV format
class InventoryConverter:
    def __init__(self, files: List[str]):
        self.files = files
    
    def convert_files(self, save_directory):
        for file in self.files:
            new_path = self._file_tocsv(file, save_directory)
            print(new_path)
    
    def _file_tocsv(self,file: str, save_directory: str) -> str:
        old_file = pd.read_excel(file)
        
        new_columns=['Inventory-ID', 'Inventory-ItemName', 'Inventory-LocationName', 'Inventory-UomName', 'Inventory-Quantity', 'Inventory-Cost', 'Inventory-EventType', 'Tracking-Lot Number', 'Tracking-Expiration Date', 'TrackingSerial-SerialNumber']

        new_file = pd.DataFrame(columns=new_columns)
        new_file['Inventory-ID'] = range(1, len(old_file) +1)
        new_file['Inventory-LocationName'] = 'Warehouse'
        new_file['Inventory-UomName'] = 'Each'
        new_file['Inventory-Cost'] = 0
        new_file['Inventory-EventType'] = 'Add'

        new_file['Inventory-ItemName'] = old_file['Item']
        new_file['TrackingSerial-SerialNumber'] = old_file['Serial']
        new_file['Inventory-Quantity'] = old_file['Quantity']

        # Apply the custom function to create the 'Tracking-Lot Number' column
        new_file['Tracking-Lot Number'] = old_file.apply(self._set_lot_number, axis=1)
        new_file_path = self._create_new_file_ext(file, save_directory)
        
        new_file.to_csv(new_file_path, index=False)
        return new_file_path

    def _set_lot_number(self, row): 
        if pd.isna(row['Brand']) or row['Brand'] == '': 
            return row['Model'] 
        elif pd.isna(row['Model']) or row['Model'] == '': 
            return row['Brand'] 
        else: 
            return f"{row['Brand']} {row['Model']}"


    def _create_new_file_ext(self,file: str, save_directory: str) -> str:
        base_name= os.path.basename(os.path.splitext(file)[0]) 
        ext =".csv"
        new_file_path = os.path.join(save_directory, f"{base_name}(Cleaned){ext}")
        return new_file_path

