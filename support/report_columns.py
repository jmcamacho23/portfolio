# file columns

column_dict = {'.csv': ['customer_index', 'customer_id', 'first_name', 'last_name', 'company', 'city', 'country', 'phone_1', 'phone_2',
               'email', 'subscription_date', 'website']

               }

file_type_table_name = {'.csv': 'customer_source'}

type_expected_dict = {
    'customer': {'city': 'str', 'company': 'str', 'country': 'str', 'customer_id': 'str', 'customer_index': 'int64',
                 'email': 'str', 'first_name': 'str', 'last_name': 'str', 'phone_1': 'str', 'phone_2': 'str',
                 'subscription_date': 'str', 'website': 'str'}
    }
