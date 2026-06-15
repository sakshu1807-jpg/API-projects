import json
from pathlib import Path
from typing import List, Dict
data_file = Path('..\data\products.json')

# loads data from the json file
def load_data() -> List[Dict]: #type-hint(->):it is a return value i.e what datatype to expect from the func.
        if not data_file.exists():
            return []
        
        with open(data_file,'r') as f:
              return json.load(f)

# gets all the data of the json file  
def get_all_products() -> List[Dict]:
      return load_data()

def add_product(product_data: Dict):
      products = get_all_products()
      if any(product_data['sku'] == p['sku'] for p in products):
            raise ValueError(f"The product with SKU: {product_data['sku']} is already present.")

      with open(data_file,'w') as f: #ensure_ascii means data only available when ascii value characters are here
            products.append(product_data)
            return json.dump(products, f, ensure_ascii=False, indent=2)
      
def delete_product(id: str) -> Dict:
      products = get_all_products()
      for index, product in enumerate(products):
            if product['id'] == id:
                  removed_product = products.pop(index)
                  break
      with open(data_file,'w') as f:
            json.dump(products, f, indent=2)
      return removed_product

def update_product(id: str, product_update_data: Dict) -> Dict:
      products = get_all_products()
      target_index = None
      for index, product in enumerate(products):
            if product.get('id') == id:
                  target_index=index
                  break

      if target_index is None:
            raise ValueError('No product with such Id is found')
            
      product = products[target_index]
      for key, value in product_update_data.items():
                  if isinstance(value, dict) and isinstance(product.get(key), dict):
                        product[key].update(value)
                  else:
                        product[key] = value

      products[target_index] = product

      with open(data_file,'w') as f:
            json.dump(products, f, indent=2, ensure_ascii= False)

      return product