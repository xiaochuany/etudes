import polars as pl
import pandas as pd

def to_polars(df):
    return pl.from_pandas(df)

#------------------------------------------------------------
#1821* Write a solution to report the customers with postive revenue in the year 2021 
data = [['1', '2018', '50'], ['1', '2021', '30'], ['1', '2020', '70'], ['2', '2021', '-50'], ['3', '2018', '10'], ['3', '2016', '50'], ['4', '2021', '20']]
customers = pd.DataFrame(data, columns=['customer_id', 'year', 'revenue']).astype({'customer_id':'Int64', 'year':'Int64', 'revenue':'Int64'}).pipe(to_polars)

def revenue_positive_2021(customers):
    return customers.filter(pl.col("year")==2021).filter(pl.col("revenue")>0).select("customer_id").unique()

# print(revenue_positive_2021(customers))

#------------------------------------------------------------
#183* find all customers who never order anything.
data = [[1, 'Joe'], [2, 'Henry'], [3, 'Sam'], [4, 'Max']]
customers = pd.DataFrame(data, columns=['id', 'name']).astype({'id':'Int64', 'name':'object'}).pipe(to_polars)
data = [[1, 3], [2, 1]]
orders = pd.DataFrame(data, columns=['id', 'customerId']).astype({'id':'Int64', 'customerId':'Int64'}).pipe(to_polars)

def customers_never_order(customers, orders):
    return customers.filter(pl.col("id").is_in(orders["customerId"]).not_()).select("name")

# print(customers_never_order(customers, orders))

#------------------------------------------------------------
#1873* The bonus of an employee is 100% of their salary if the ID of the employee is an odd number
# and the employee's name does not start with the character 'M'. The bonus of an employee is 0 otherwise.
data = [[2, 'Meir', 3000], [3, 'Michael', 3800], [7, 'Addilyn', 7400], [8, 'Juan', 6100], [9, 'Kannon', 7700]]
employees = pd.DataFrame(data, columns=['employee_id', 'name', 'salary']).astype({'employee_id':'int64', 'name':'object', 'salary':'int64'}).pipe(to_polars)

def bonus(employees):
    return employees.select(
        pl.col("employee_id"),
        pl.when(pl.col("name").str.starts_with("M").not_() & pl.col("employee_id")%2==1).then(pl.col("salary")).otherwise(0)
    ).sort(by="salary", descending=True)

# print(bonus(employees))

#------------------------------------------------------------
#1398** customers who bought products "A", "B" but did not buy the product "C"

data = [[1, 'Daniel'], [2, 'Diana'], [3, 'Elizabeth'], [4, 'Jhon']]
customers = pd.DataFrame(data, columns=['customer_id', 'customer_name']).astype({'customer_id':'Int64', 'customer_name':'object'}).pipe(to_polars)
data = [[10, 1, 'A'], [20, 1, 'B'], [30, 1, 'D'], [40, 1, 'C'], [50, 2, 'A'], [60, 3, 'A'], [70, 3, 'B'], [80, 3, 'D'], [90, 4, 'C']]
orders = pd.DataFrame(data, columns=['order_id', 'customer_id', 'product_name']).astype({'order_id':'Int64', 'customer_id':'Int64', 'product_name':'object'}).pipe(to_polars)

def customers_bought_products(customers, orders):
    return orders.group_by("customer_id").agg(pl.col("product_name").str.concat("")).filter(
        pl.col("product_name").str.contains("A") & 
        pl.col("product_name").str.contains("B") & 
        pl.col("product_name").str.contains("C").not_()).join(customers, on="customer_id").select(["customer_id","customer_name"])

# print(customers_bought_products(customers, orders))

#------------------------------------------------------------
#1440** evalaute boolean expression

data = [['x', 66], ['y', 77]]
variables = pd.DataFrame(data, columns=['name', 'value']).astype({'name':'object', 'value':'Int64'}).pipe(to_polars)
data = [['x', '>', 'y'], ['x', '<', 'y'], ['x', '=', 'y'], ['y', '>', 'x'], ['y', '<', 'x'], ['x', '=', 'x']]
expressions = pd.DataFrame(data, columns=['left_operand', 'operator', 'right_operand']).astype({'left_operand':'object', 'operator':'object', 'right_operand':'object'}).pipe(to_polars)

def evaluate_expression(expressions, variables):
    return expressions.join(variables, left_on="left_operand", right_on="name").join(variables, left_on="right_operand", right_on="name").select(
        pl.when(pl.col("operator")=="=")
        .then(pl.col("value")==pl.col("value_right"))
        .when(pl.col("operator")==">")
        .then(pl.col("value")>pl.col("value_right"))
        .otherwise(pl.col("value")<pl.col("value_right"))
    )

# print(evaluate_expression(expressions, variables))

#------------------------------------------------------------
#1212** team scores in football tournament

data = [[10, 'Leetcode FC'], [20, 'NewYork FC'], [30, 'Atlanta FC'], [40, 'Chicago FC'], [50, 'Toronto FC']]
teams = pd.DataFrame(data, columns=['team_id', 'team_name']).astype({'team_id':'Int64', 'team_name':'object'}).pipe(to_polars)
data = [[1, 10, 20, 3, 0], [2, 30, 10, 2, 2], [3, 10, 50, 5, 1], [4, 20, 30, 1, 0], [5, 50, 30, 1, 0]]
matches = pd.DataFrame(data, columns=['match_id', 'host_team', 'guest_team', 'host_goals', 'guest_goals']).astype({'match_id':'Int64', 'host_team':'Int64', 'guest_team':'Int64', 'host_goals':'Int64', 'guest_goals':'Int64'}).pipe(to_polars)

def team_scores(teams, matches):
    def compute_points(col1, col2):
        """win 3 draw 1 lose 0"""
        return pl.when(col1 > col2).then(3).when(col1 == col2).then(1).otherwise(0)
    
    col1, col2 = pl.col("host_goals"), pl.col("guest_goals")
    x = (matches.lazy().with_columns(
            compute_points(col1, col2).alias("home_points"), 
            compute_points(col2, col1).alias("guest_points")))
    cat = pl.concat([x.select("host_team", "home_points").rename({"host_team":"team_id", "home_points":"points"}), 
               x.select("guest_team", "guest_points").rename({"guest_team":"team_id", "guest_points":"points"})])
    q = cat.group_by("team_id").agg(pl.sum("points")).join(teams.lazy(), on = "team_id").select("team_name", "points").sort(by="points", descending=True)
    return q.collect()

# print(team_scores(teams, matches))

#------------------------------------------------------------
#1517* warehouse manager

data = [['LCHouse1', 1, 1], ['LCHouse1', 2, 10], ['LCHouse1', 3, 5], ['LCHouse2', 1, 2], ['LCHouse2', 2, 2], ['LCHouse3', 4, 1]]
warehouse = pd.DataFrame(data, columns=['name', 'product_id', 'units']).astype({'name':'object', 'product_id':'Int64', 'units':'Int64'}).pipe(to_polars)
data = [[1, 'LC-TV', 5, 50, 40], [2, 'LC-KeyChain', 5, 5, 5], [3, 'LC-Phone', 2, 10, 10], [4, 'LC-T-Shirt', 4, 10, 20]]
products = pd.DataFrame(data, columns=['product_id', 'product_name', 'Width', 'Length', 'Height']).astype({'product_id':'Int64', 'product_name':'object', 'Width':'Int64', 'Length':'Int64', 'Height':'Int64'}).pipe(to_polars)

def warehouse_manager(warehouse, products):
    q = (
        warehouse.lazy()
        .join(products.lazy(), on="product_id")
        .with_columns(pl.fold(acc=pl.lit(1), function=lambda acc, x: acc*x, exprs=[pl.col("Width", "Length", "Height", "units")]).alias("vol"))
        .group_by("name").agg(pl.sum("vol"))
        .sort(by="name")
    )
    return q.collect()

# print(warehouse_manager(warehouse, products))

#------------------------------------------------------------
#1445** Apples and Oranges

data = [['2020-05-01', 'apples', 10], ['2020-05-01', 'oranges', 8], ['2020-05-02', 'apples', 15], ['2020-05-02', 'oranges', 15], ['2020-05-03', 'apples', 20], ['2020-05-03', 'oranges', 0], ['2020-05-04', 'apples', 15], ['2020-05-04', 'oranges', 16]]
sales = pd.DataFrame(data, columns=['sale_date', 'fruit', 'sold_num']).astype({'sale_date':'datetime64[ns]', 'fruit':'object', 'sold_num':'Int64'}).pipe(to_polars)

def apples_oranges(sales):
    q = (
        sales.with_columns(pl.col("sale_date").cast(pl.Date))
        .pivot(index="sale_date", columns="fruit", values="sold_num")
        .select(pl.first(), pl.reduce(lambda x,y:x-y, exprs=pl.col("*").exclude("sale_date")).alias("diff"))
    )
    return q

# print(apples_oranges(sales))

#------------------------------------------------------------
#1699** number of calls between two persons
 
data = [[1, 2, 59], [2, 1, 11], [1, 3, 20], [3, 4, 100], [3, 4, 200], [3, 4, 200], [4, 3, 499]]
calls = pd.DataFrame(data, columns=['from_id', 'to_id', 'duration']).astype({'from_id':'Int64', 'to_id':'Int64', 'duration':'Int64'}).pipe(to_polars)

def number_of_calls(calls):
    q = (
        calls
        .with_columns(callers = pl.concat_list(pl.all().exclude("duration")).list.sort())
        .group_by("callers").agg(pl.sum("duration"))
        .select("callers", "duration")
    )
    return q

# print(number_of_calls(calls))