# /env/bin/python3.5
# Natali Kuskova
import MySQLdb
import MySQLdb.cursors
from models import *


USER = 'root'
PASSWORD = '123'
DB = 'test_orm'


def get_connection():
    connection = MySQLdb.connect(user=USER,
                                 passwd=PASSWORD,
                                 db=DB,
                                 cursorclass=MySQLdb.cursors.DictCursor)
    return connection


def migrate(model_class):
    tbl_name = model_class.__class__.__name__
    attr = model_class.__class__.__dict__
    attributes = ''
    for arg in attr:
        if not arg.startswith('_'):
            if not attributes:
                attributes += arg + attr[arg].get_type()
            else:
                attributes += ', ' + arg + attr[arg].get_type()
    query = 'CREATE TABLE if not exists ' + tbl_name + '(' \
            'id int(10) AUTO_INCREMENT PRIMARY KEY, ' + \
            attributes + ')'
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.close()
    connection.close()


def insert(instance):
    tbl_name = instance.__class__.__name__
    attr = instance.__dict__
    fields = ''
    values = []
    for key in attr:
        if not fields:
            fields += key
        else:
            fields += ', ' + key
        values.append(attr[key])
    values = str(values)[1:-1]
    query = "INSERT INTO " + tbl_name + "(" + fields + ") VALUES (" + \
            values + ")"
    connection = get_connection()
    cursor = connection.cursor()
    try:
        return bool(cursor.execute(query))
    except Exception:
        return False
    finally:
        connection.commit()
        cursor.close()
        connection.close()


def select(model_class, **kwargs):
    connection = get_connection()
    cursor = connection.cursor()
    tbl_name = model_class.__name__
    filters = {
        'gt': '>',
        'gte': '>=',
        'lt': '<',
        'lte': '<=',
        'contains': ' LIKE '
    }
    query = "SELECT * FROM " + tbl_name
    sql_where = ''
    if kwargs:
        query += " Where "
        for name in kwargs.items():
            operator = '='
            name_field = name[0]
            name_value = name[1]
            if sql_where:
                sql_where += " and "
            if '__' in name[0]:
                name_field_filter = name[0].split('__')
                if name_field_filter[1] in filters:
                    operator = filters[name_field_filter[1]]
                    name_field = name_field_filter[0]
            if 'LIKE' in operator:
                name_value = "%" + name[1] + "%"
            if type(name[1]) == str:
                sql_where += name_field + operator + "'" + name_value + "'"
            else:
                sql_where += name_field + operator + str(name_value)
        query += sql_where
    cursor.execute(query)
    return cursor.fetchall()


class Person(AbstractModel):
    first_name = CharField(length=30)
    last_name = CharField(length=30)
    age = IntegerField()


class Product(AbstractModel):
    name = CharField(length=50)
    price = FloatField()
    category = CharField(length=30)
    quantity = IntegerField()


if __name__ == "__main__":

    person = Person()
    person2 = Person()
    migrate(person)

    person.first_name = 'Natali'
    person.last_name = 'Kuskova'
    person.age = 20

    person2.first_name = 'Anastasia'
    person2.last_name = 'Goloviznina'
    person2.age = 20

    result_person = insert(person)
    print(result_person)

    result_person2 = insert(person2)
    print(result_person2)

    persons = select(Person, first_name__contains='N', age__gte=20, age__lt=22)
    print(persons)

    product = Product()
    product2 = Product()
    product3 = Product()
    migrate(product)

    product.name = 'Nike Air Max'
    product.category = 'Sneakers'
    product.price = 1250.00
    product.quantity = 5

    product2.name = 'Leggings'
    product2.category = 'Sportswear'
    product2.price = 300.00
    product2.quantity = 10

    product3.name = 'Shorts'
    product3.category = 'Clothes'
    product3.price = 200
    product3.quantity = 13

    result_product = insert(product)
    print(result_product)

    result_product2 = insert(product2)
    print(result_product2)

    result_product3 = insert(product3)
    print(result_product3)

    products = select(Product, quantity__gt=4, price__gte=500)
    print(products)
