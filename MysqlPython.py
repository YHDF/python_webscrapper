import MySQLdb
import initialize
import Amazon_Scrapping
import Ebay_Scrapping
import Jumia_Scrapping
import WallMart_Scrapping
import re
import hashlib

page_number = 10
group_name = ["APhones", "Ephones", "Jphones", "WMphones", "ELaptops", "EMacbooks", "WMLaptops", "JLaptops"]
attributes = [""'.sg-col-20-of-24' + '.s-result-item'"", ".s-item", ".sku", ""'.Grid-col' + '.u-size-6-12' + '.u-size-1-4-m'"", ".s-item", ".s-item", ""'.Grid-col' + '.u-size-6-12' + '.u-size-1-4-m'"", ".sku"]

url = ["" for x in range(len(group_name))]
db = MySQLdb.connect(host="localhost",   
                     user="root",        
                     passwd="dell", 
                     db="Testing")       
cur = db.cursor()
def get_url(s):
    cur.execute("SELECT link FROM Testing.groups WHERE name = '" + group_name[s] + "';")
    url[s] = cur.fetchone()
    return url[s][0]

def get_grp(s):
    cur.execute("SELECT id_group FROM Testing.groups WHERE name = '" + group_name[s] + "';")
    id = cur.fetchone()
    return id[0]

def temp_product_storage():
    id_product = 0
    cur.execute("DELETE FROM Testing.temps")
    for s in range(len(group_name)):
        for i in range (page_number):
            initdata = initialize.init(i+1,get_url(s),attributes[s])
            if(group_name[s] == "JLaptops" and initdata.count < 47):
                break;
            data = [[0 for j in range(initdata.count)] for i in range(page_number)]
            for j in range(initdata.count):
                if(group_name[s] == "Ephones" or group_name[s] == "ELaptops" or group_name[s] == "EMacbooks"):
                    data[i][j] = Ebay_Scrapping.phone_scrap(initdata.section, j)
                if(group_name[s] == "APhones" or group_name[s] == "AComputers"):
                    data[i][j] = Amazon_Scrapping.phone_scrap(initdata.section, j)
                if(group_name[s] == "Jphones" or group_name[s] == "JLaptops"):
                    data[i][j] = Jumia_Scrapping.phone_scrap(initdata, j)
                if(group_name[s] == "WMphones" or group_name[s] == "WMLaptops"):
                    data[i][j] = WallMart_Scrapping.phone_scrap(initdata.section, j)
                if data[i][j] is None:
                    continue;
                name = data[i][j].name
                prices = data[i][j].price
                img_link = data[i][j].img
                link = data[i][j].link
                prices = prices.replace('$', '')
                prices = prices.replace(',', '')
                prices = re.sub(' .*', '' , prices)
                prices = re.sub("\..*", '' , prices)
                name = list(name)
                prices = list(prices)
                img_link = list(img_link)
                for k in range(len(name)):
                    if name[k] == "'" or name[k] == '"' or name[k] == '-' :
                        name[k] = ""
                name = "".join(name)
                for k in range(len(prices)):
                    if prices[k] == "'" or prices[k] == '"' or prices[k] == '-' or ord(prices[k]) == 160:
                        prices[k] = ""
                prices = "".join(prices)
                for k in range(len(img_link)):
                    if img_link[k] == "'" or img_link[k] == '"':
                        img_link[k] = " "
                img_link = "".join(img_link)
                data[i][j].name = name
                if(prices == 'N/a' or prices == 'Amazon' or prices == 'alexa' or prices == 'Works' or prices == '5%' or prices == 'From' or prices == '10%' or prices == ''):
                    prices = 0
                prices = int(prices)
                data[i][j].price = prices
                data[i][j].img = img_link
                id_product = hashlib.sha256(data[i][j].link.encode('utf-8')).hexdigest()
                sql_statement = "INSERT INTO Testing.temps VALUES (%s, %s, %s, %s, %s, %s)"
                values = (id_product, get_grp(s),data[i][j].name, data[i][j].img, data[i][j].price, data[i][j].link)
                cur.execute(sql_statement, values)
                db.commit()
            
def random_choice() :
    id_grp = 7 
    best_data = [[0 for j in range(8)] for i in range(20)]
    while id_grp <= 15:
        if(id_grp == 11):
            id_grp += 1
        sql_statement = "SELECT * FROM Testing.products WHERE name <> 'N/a' AND price <> 0 AND group_id = %s limit 0,2" %(str(id_grp))
        cur.execute(sql_statement)
        temp_data = cur.fetchall()
        list_temp_data = list(temp_data)
        for i in range(len(temp_data)):
            row = list(list_temp_data[i])
            row[7] = 1
            sql_statement = "UPDATE Testing.products SET best = %s  WHERE id_product = %s"
            values = (row[7],row[0])
            cur.execute(sql_statement, values)
        id_grp += 1
    db.commit()
        


def filter_identical(list_temp_data):
    filtered_list = []
    filtered_list.append(list_temp_data[0])
    for i in range(len(list_temp_data)):
        for j in range(len(filtered_list)):
            if(list_temp_data[i][0] == filtered_list[j][0]):
                break
            else:
                if(list_temp_data[i][0] != filtered_list[j][0] and j == len(filtered_list) - 1):
                    filtered_list.append(list_temp_data[i])
                    break
    return filtered_list




def product_storage():
    id_product = 0
    cur.execute("DELETE FROM Testing.products")
    sql_statement = "SELECT * FROM Testing.temps"
    cur.execute(sql_statement)
    temp_data = cur.fetchall()
    list_temp_data = list(temp_data)
    list_temp_data = filter_identical(list_temp_data)
    temp_data = tuple(list_temp_data)
    for row in temp_data:
        sql_statement = "INSERT INTO Testing.products VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (row[0], row[1], row[2] , row[3], row[4], row[5], 0, 0)
        cur.execute(sql_statement, values)
    db.commit()
        



temp_product_storage()
product_storage()
random_choice()
print("done")
db.close()