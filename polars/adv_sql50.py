"""pipe pandas dataframe to polars dataframe
then write idiomatic polars queries for selected problems in leetcode advanced SQL 50 series. 
"""
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

#------------------------------------------------------------
#1501** countries you safely invest in

data = [[3, 'Jonathan', '051-1234567'], [12, 'Elvis', '051-7654321'], [1, 'Moncef', '212-1234567'], [2, 'Maroua', '212-6523651'], [7, 'Meir', '972-1234567'], [9, 'Rachel', '972-0011100']]
person = pd.DataFrame(data, columns=['id', 'name', 'phone_number']).astype({'id':'Int64', 'name':'object', 'phone_number':'object'}).pipe(to_polars)
data = [['Peru', '051'], ['Israel', '972'], ['Morocco', '212'], ['Germany', '049'], ['Ethiopia', '251']]
country = pd.DataFrame(data, columns=['name', 'country_code']).astype({'name':'object', 'country_code':'object'}).pipe(to_polars)
data = [[1, 9, 33], [2, 9, 4], [1, 2, 59], [3, 12, 102], [3, 12, 330], [12, 3, 5], [7, 9, 13], [7, 1, 3], [9, 7, 1], [1, 7, 7]]
calls = pd.DataFrame(data, columns=['caller_id', 'callee_id', 'duration']).astype({'caller_id':'Int64', 'callee_id':'Int64', 'duration':'Int64'}).pipe(to_polars)

def countries_to_invest(person, country, calls):
    q = (
        pl.concat(
            [calls.lazy().select(pl.first(),"duration").rename({"caller_id":"id"}),
            calls.lazy().select("callee_id", "duration").rename({"callee_id":"id"})]
    ).join(
        person.lazy().select(
            "id",
            pl.col("phone_number").str.slice(0,3).alias("country_code")
        ),
        on="id"
    ).with_columns(globl=pl.col("duration").mean())
    .group_by("country_code").agg(pl.mean("duration"), pl.mean("globl"))
    .filter(pl.col("duration")>pl.col("globl"))
    .join(country.lazy(), on="country_code")
    .select("name")
    )
    return q.collect()

# print(countries_to_invest(person, country, calls))

#------------------------------------------------------------
#1264** page recommendations

data = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [2, 5], [6, 1]]
friendship = pd.DataFrame(data, columns=['user1_id', 'user2_id']).astype({'user1_id':'Int64', 'user2_id':'Int64'}).pipe(to_polars)
data = [[1, 88], [2, 23], [3, 24], [4, 56], [5, 11], [6, 33], [2, 77], [3, 77], [6, 88]]
likes = pd.DataFrame(data, columns=['user_id', 'page_id']).astype({'user_id':'Int64', 'page_id':'Int64'}).pipe(to_polars)

def page_recommendations(friendship, likes):
    q = (
        friendship
        .with_columns(
            friend = pl.when(pl.col("user1_id")==1).then(pl.col("user2_id"))
            .when(pl.col("user2_id")==1).then(pl.col("user1_id"))
            .otherwise(None)
            )
        .drop_nulls()
        )
    q2 = likes.filter(
        pl.col("user_id").is_in(q.select("friend")) &
        pl.col("page_id").is_in(likes.filter(pl.col("user_id")==1).select("page_id")).not_()
    ).select(pl.col("page_id").alias("recommended_page_id")).unique()
    return q2 

# print(page_recommendations(friendship, likes))

#------------------------------------------------------------
#608** tree node

data = [[1, None], [2, 1], [3, 1], [4, 2], [5, 2]]
tree = pd.DataFrame(data, columns=['id', 'p_id']).astype({'id':'Int64', 'p_id':'Int64'}).pipe(to_polars)

def tree_node(tree):
    q = (
        tree
        .with_columns(
            root=pl.col("p_id").is_null(),
            is_parent=pl.col("id").is_in("p_id")
        )
        .with_columns(type=pl.col("root")+pl.col("is_parent"))
        .select(
            "id",
            pl.when(pl.col("type")==2).then(pl.lit("Root")).when(pl.col("type")==1).then(pl.lit("Inner")).otherwise(pl.lit("Leaf"))
        )
    )
    return q

# print(tree_node(tree))

#------------------------------------------------------------
#534** game play analysis III

data = [[1, 2, '2016-03-01', 5], [1, 2, '2016-05-02', 6], [1, 3, '2017-06-25', 1], [3, 1, '2016-03-02', 0], [3, 4, '2018-07-03', 5]]
activity = pd.DataFrame(data, columns=['player_id', 'device_id', 'event_date', 'games_played']).astype({'player_id':'Int64', 'device_id':'Int64', 'event_date':'datetime64[ns]', 'games_played':'Int64'}).pipe(to_polars)

def game_play_analysis(activity):
    q = (
        activity
        .group_by("player_id","event_date").agg(pl.sum("games_played"))
        .sort(by=["player_id", "event_date"])
        .with_columns(
            pl.col("games_played").cum_sum().over("player_id").alias("games_played_so_far"),
            pl.col("event_date").dt.date()
        )
    )
    return q

# print(game_play_analysis(activity))

#------------------------------------------------------------
#1783** grand slam titles

data = [[1, 'Nadal'], [2, 'Federer'], [3, 'Novak']]
players = pd.DataFrame(data, columns=['player_id', 'player_name']).astype({'player_id':'Int64', 'player_name':'object'}).pipe(to_polars)
data = [[2018, 1, 1, 1, 1], [2019, 1, 1, 2, 2], [2020, 2, 1, 2, 2]]
championships = pd.DataFrame(data, columns=['year', 'Wimbledon', 'Fr_open', 'US_open', 'Au_open']).astype({'year':'Int64', 'Wimbledon':'Int64', 'Fr_open':'Int64', 'US_open':'Int64', 'Au_open':'Int64'}).pipe(to_polars)

def grand_slam_titles(players, championships):
    q=(
        championships
        .melt(id_vars="year",value_vars=["Wimbledon", "Fr_open", "US_open", "Au_open"], variable_name="tournament", value_name="player_id")
        .group_by("player_id").agg(pl.col("tournament").count())
        .join(players, on="player_id")
    )
    return q

# print(grand_slam_titles(players, championships))

#------------------------------------------------------------
#1747** leetflex banned account

data = [[1, 1, '2021-02-01 09:00:00', '2021-02-01 09:30:00'], [1, 2, '2021-02-01 08:00:00', '2021-02-01 11:30:00'], [2, 6, '2021-02-01 20:30:00', '2021-02-01 22:00:00'], [2, 7, '2021-02-02 20:30:00', '2021-02-02 22:00:00'], [3, 9, '2021-02-01 16:00:00', '2021-02-01 16:59:59'], [3, 13, '2021-02-01 17:00:00', '2021-02-01 17:59:59'], [4, 10, '2021-02-01 16:00:00', '2021-02-01 17:00:00'], [4, 11, '2021-02-01 17:00:00', '2021-02-01 17:59:59']]
log_info = pd.DataFrame(data, columns=['account_id', 'ip_address', 'login', 'logout']).astype({'account_id':'Int64', 'ip_address':'Int64', 'login':'datetime64[ns]', 'logout':'datetime64[ns]'}).pipe(to_polars)

def banned_account(log_info):
    q =(
        log_info.lazy().join(log_info.lazy(),how="cross")
        .filter(
            (pl.col("account_id")==pl.col("account_id_right")) &
            (pl.col("ip_address")!=pl.col("ip_address_right")) &
            (pl.col("login_right")<=pl.col("logout")) &
            (pl.col("logout_right")>=pl.col("login"))
        )
        .select("account_id").unique()
    )
    return q.collect()

# print(banned_account(log_info))

#------------------------------------------------------------
#184** department highest salary

data = [[1, 'Joe', 70000, 1], [2, 'Jim', 90000, 1], [3, 'Henry', 80000, 2], [4, 'Sam', 60000, 2], [5, 'Max', 90000, 1]]
employee = pd.DataFrame(data, columns=['id', 'name', 'salary', 'departmentId']).astype({'id':'Int64', 'name':'object', 'salary':'Int64', 'departmentId':'Int64'}).pipe(to_polars)
data = [[1, 'IT'], [2, 'Sales']]
department = pd.DataFrame(data, columns=['id', 'name']).astype({'id':'Int64', 'name':'object'}).pipe(to_polars)

def department_highest_salary(employee, department):
    q = (
        employee
        .with_columns(
            pl.col("salary").max().over("departmentId").alias("max_salary")
        )
        .filter(pl.col("max_salary")==pl.col("salary"))
        .join(department, left_on="departmentId", right_on="id")
        .rename({"name_right":"department"})
        .select("name","department","salary")
    )
    return q

# print(department_highest_salary(employee, department))

#------------------------------------------------------------
#1532** the most recent three orders

data = [[1, 'Winston'], [2, 'Jonathan'], [3, 'Annabelle'], [4, 'Marwan'], [5, 'Khaled']]
customers = pd.DataFrame(data, columns=['customer_id', 'name']).astype({'customer_id':'Int64', 'name':'object'}).pipe(to_polars)
data = [[1, '2020-07-31', 1, 1], [2, '2020-7-30', 2, 2], [3, '2020-08-29', 3, 3], [4, '2020-07-29', 4, 1], [5, '2020-06-10', 1, 2], [6, '2020-08-01', 2, 1], [7, '2020-08-01', 3, 1], [8, '2020-08-03', 1, 2], [9, '2020-08-07', 2, 3], [10, '2020-07-15', 1, 2]]
orders = pd.DataFrame(data, columns=['order_id', 'order_date', 'customer_id', 'product_id']).astype({'order_id':'Int64', 'order_date':'datetime64[ns]', 'customer_id':'Int64', 'product_id':'Int64'}).pipe(to_polars)   

def most_recent_order(customers, orders):
    q=(
        orders.lazy()
        .with_columns(
            pl.col("order_date").rank(descending=True).over("customer_id").alias("rank")
        )
        .filter(pl.col("rank")<=3)
        .join(customers.lazy(),on="customer_id")
        .sort(by=["name","customer_id","order_date"], descending=[False,False,True])
        .select("name","customer_id","order_id","order_date")
    )
    return q.collect()

# print(most_recent_order(customers, orders))

#------------------------------------------------------------
#1841** maximum transaction each day

data = [[8, '2021-4-3 15:57:28', 57], [9, '2021-4-28 08:47:25', 21], [1, '2021-4-29 13:28:30', 58], [5, '2021-4-28 16:39:59', 40], [6, '2021-4-29 23:39:28', 58]]
transactions = pd.DataFrame(data, columns=['transaction_id', 'day', 'amount']).astype({'transaction_id':'Int64', 'day':'datetime64[ns]', 'amount':'Int64'}).pipe(to_polars)

def max_transaction(transactions):
    q = (
        transactions
        .with_columns(
            pl.col("amount").max().over(pl.col("day").dt.date()).alias("max_amount")
        )
        .filter(pl.col("max_amount")==pl.col("amount"))
        .select("transaction_id")

    )
    return q

# print(max_transaction(transactions))

#------------------------------------------------------------
#1077** project employees III

data = [[1, 1], [1, 2], [1, 3], [2, 1], [2, 4]]
project = pd.DataFrame(data, columns=['project_id', 'employee_id']).astype({'project_id':'Int64', 'employee_id':'Int64'}).pipe(to_polars)
data = [[1, 'Khaled', 3], [2, 'Ali', 2], [3, 'John', 3], [4, 'Doe', 2]]
employee = pd.DataFrame(data, columns=['employee_id', 'name', 'experience_years']).astype({'employee_id':'Int64', 'name':'object', 'experience_years':'Int64'}).pipe(to_polars)

def project_employees(project, employee):
    q=(
        project.join(employee, on="employee_id")
        .with_columns(
            pl.col("experience_years").max().over("project_id").alias("max_experience")
        )
        .filter(pl.col("experience_years")==pl.col("max_experience"))
    )
    return q

# print(project_employees(project, employee))

#------------------------------------------------------------
#1286** find the start and end number of continuous ranges

data = [[1], [2], [3], [7], [8], [10]]
logs = pd.DataFrame(data, columns=['log_id']).astype({'log_id':'Int64'}).pipe(to_polars)

def continuous_ranges(logs):
    q=(
        logs.lazy()
        .with_columns(
            diff=pl.col("log_id").diff(), 
            id_shift=pl.col("log_id").shift(1)
            )
        .filter(
            (pl.col("diff")!=1) | (pl.col("diff").is_null())
            )
        .with_columns(pl.col("id_shift").shift(-1))
        .select(
            start=pl.col("log_id"),
            end=pl.when(pl.col("id_shift").is_null()).then("log_id").otherwise("id_shift"),
            )
    )
    return q.collect()

# print(continuous_ranges(logs))

#------------------------------------------------------------
#1596** the most frequently ordered products for each customer

data = [[1, 'Alice'], [2, 'Bob'], [3, 'Tom'], [4, 'Jerry'], [5, 'John']]
customers = pd.DataFrame(data, columns=['customer_id', 'name']).astype({'customer_id':'Int64', 'name':'object'}).pipe(to_polars)
data = [[1, '2020-07-31', 1, 1], [2, '2020-7-30', 2, 2], [3, '2020-08-29', 3, 3], [4, '2020-07-29', 4, 1], [5, '2020-06-10', 1, 2], [6, '2020-08-01', 2, 1], [7, '2020-08-01', 3, 3], [8, '2020-08-03', 1, 2], [9, '2020-08-07', 2, 3], [10, '2020-07-15', 1, 2]]
orders = pd.DataFrame(data, columns=['order_id', 'order_date', 'customer_id', 'product_id']).astype({'order_id':'Int64', 'order_date':'datetime64[ns]', 'customer_id':'Int64', 'product_id':'Int64'}).pipe(to_polars)
data = [[1, 'keyboard', 120], [2, 'mouse', 80], [3, 'screen', 600], [4, 'hard disk', 450]]
products = pd.DataFrame(data, columns=['product_id', 'product_name', 'price']).astype({'product_id':'Int64', 'product_name':'object', 'price':'Int64'}).pipe(to_polars)

def most_frequent_products(customers, orders, products):
    q=(
        orders
        .group_by("customer_id","product_id").agg(pl.count())
        .with_columns(
            pl.col("count").max().over("customer_id").alias("max_count")
        )
        .filter(pl.col("count")==pl.col("max_count"))
        .sort("customer_id")
        .join(products, on="product_id")
        .select("customer_id","product_id", "product_name")
    )
    return q

# print(most_frequent_products(customers, orders, products))

#------------------------------------------------------------
#1709** biggest window between visits

data = [['1', '2020-11-28'], ['1', '2020-10-20'], ['1', '2020-12-3'], ['2', '2020-10-5'], ['2', '2020-12-9'], ['3', '2020-11-11']]
user_visits = pd.DataFrame(data, columns=['user_id', 'visit_date']).astype({'user_id':'Int64', 'visit_date':'datetime64[ns]'}).pipe(to_polars)

def biggest_window(user_visits):
    arti_visit = user_visits.lazy().select(pl.col("user_id").unique(), pl.date(2021,1,1).alias("visit_date"))
    q = (
        pl.concat([user_visits.lazy().with_columns(pl.col("visit_date").cast(pl.Date)), arti_visit])
        .sort("visit_date")
        .with_columns(
            pl.col("visit_date").diff().over("user_id").alias("diff")
        )
        .drop_nulls()
        .group_by("user_id").agg(pl.max("diff"))
    )
    return q.collect()

# print(biggest_window(user_visits))

#------------------------------------------------------------
#1270** all people report to the given manager

data = [[1, 'Boss', 1], [3, 'Alice', 3], [2, 'Bob', 1], [4, 'Daniel', 2], [7, 'Luis', 4], [8, 'John', 3], [9, 'Angela', 8], [77, 'Robert', 1]]
employees = pd.DataFrame(data, columns=['employee_id', 'employee_name', 'manager_id']).astype({'employee_id':'Int64', 'employee_name':'object', 'manager_id':'Int64'}).pipe(to_polars)

def report_to_manager(employees):
    q = (
        employees
        .join(employees, left_on="manager_id", right_on="employee_id", suffix="_d1")
        .join(employees, left_on="manager_id_d1", right_on="employee_id",suffix="_d2")
        .filter((pl.col("manager_id_d2")==1) & (pl.col("employee_id")!=1))
        .select("employee_name")
    )
    return q

# print(report_to_manager(employees))