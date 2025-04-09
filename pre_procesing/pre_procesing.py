
# Importacion de librerias -------------------------
import pandas as pd 

# Lecturas de datasets --------------------------------------
df_contract = pd.read_csv('datasets/contract.csv')
df_internet = pd.read_csv('datasets/internet.csv')
df_personal = pd.read_csv('datasets/personal.csv')
df_phone  = pd.read_csv('datasets/phone.csv')

# Observando duplicados 
print("Duplicados en contrato:" ,df_contract['customerID'].duplicated().sum())
print("Duplicados en clientes:",df_personal['customerID'].duplicated().sum())

#Juntamos las tablas con inner join
df_customer_and_contract = df_personal.merge(df_contract, on='customerID')
df_customer_and_contract.info()


# duplicados en internet
print("Duplicados en internet: ", df_internet['customerID'].duplicated().sum())

df_customer_and_internet = df_personal.merge(df_internet, how='outer', on='customerID')
df_customer_and_internet.info()


print('Cantidad de usuarios que no tienen el servicio de Internet: ',df_customer_and_internet[df_customer_and_internet['InternetService'].isna()].shape[0])

# data de clientes sin el servicio de internet 
customer_without_internet = df_customer_and_internet[df_customer_and_internet['InternetService'].isna()].copy()

# duplicados en internet
print("Duplicados en telefonia: ", df_phone['customerID'].duplicated().sum())

# clientes sin internet con el servicio de telefonia
df_only_phone= customer_without_internet.merge(df_phone,how='inner', on= 'customerID')

df_only_phone.info()

# Juntando todas las tablas -----------------------------------------
df_customer_and_internet.dropna(inplace= True) # quitamos los clientes que tienen solo telefonia 
df_all_internet = df_customer_and_internet.merge(df_phone,how= 'left', on='customerID')  # Agregamos los datos de telefonia para los que tienen telefonia e internet 
df_end = pd.concat([df_all_internet,df_only_phone], axis=0, ignore_index= True)  # Juntamos a los que solo tiene telefonia 
df_end = df_end.merge(df_contract, on= 'customerID')
df_end.info()


# Tratamiento de datos ausentes ------------------------------

# Cliente que solo tiene telefonia 
df_end[df_end['InternetService'].isna()].sample(1,random_state= 321)
# Cliente que solo tiene internet 
df_end[df_end['MultipleLines'].isna()].sample(1, random_state= 321)
columns = ['Partner','Dependents','OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport','StreamingTV','StreamingMovies','MultipleLines']
df_end = df_end.replace({'Yes':1 ,'No':0}) 
df_end.fillna(0, inplace=True) # Valores ausente como 'No' -> 0 
# Cliente que solo tiene internet 
df_end[df_end['MultipleLines'] == 0].sample(1, random_state= 321)
# Cliente que solo tiene telefonia 
df_end[df_end['InternetService'] == 0].sample(1,random_state= 321)
# Veamos el objetivo 
df_end['EndDate'].value_counts()
df_end.info.head(3)