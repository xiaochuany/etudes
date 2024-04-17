import polars as pl
import pandas as pd

#1821 Write a solution to report the customers with postive revenue in the year 2021.
data = [['1', '2018', '50'], ['1', '2021', '30'], ['1', '2020', '70'], ['2', '2021', '-50'], ['3', '2018', '10'], ['3', '2016', '50'], ['4', '2021', '20']]
customers = pd.DataFrame(data, columns=['customer_id', 'year', 'revenue']).astype({'customer_id':'Int64', 'year':'Int64', 'revenue':'Int64'})
df = pl.from_pandas(customers)

q = (df.filter(pl.col("year")==2021)
     .group_by("customer_id")
     .agg(pl.sum("revenue"))
     .filter(pl.col("revenue")>0)
     .select("customer_id")
)
print(q)

#183 find all customers who never order anything.

data = [[1, 'Joe'], [2, 'Henry'], [3, 'Sam'], [4, 'Max']]
customers = pl.from_pandas(pd.DataFrame(data, columns=['id', 'name']).astype({'id':'Int64', 'name':'object'}))
data = [[1, 3], [2, 1]]
orders = pl.from_pandas(pd.DataFrame(data, columns=['id', 'customerId']).astype({'id':'Int64', 'customerId':'Int64'}))

q = (
    customers.filter(
        ~pl.col("id").is_in(orders["customerId"])
    ).select("name")
)
print(q)

#1873 The bonus of an employee is 100% of their salary if the ID of the employee is an odd number
# and the employee's name does not start with the character 'M'. The bonus of an employee is 0 otherwise.


data = [[2, 'Meir', 3000], [3, 'Michael', 3800], [7, 'Addilyn', 7400], [8, 'Juan', 6100], [9, 'Kannon', 7700]]
employees = pd.DataFrame(data, columns=['employee_id', 'name', 'salary']).astype({'employee_id':'int64', 'name':'object', 'salary':'int64'})

df = pl.from_pandas(employees)

# mask = ~df["name"].str.starts_with("M") & (df["employee_id"]%2==1)

# q = (
#     df
#     .select(
#         pl.col('employee_id'),
#         pl.col('salary')*mask,
#     )
#     .sort(by=["salary","employee_id"], descending=[True,False])
# )

## using when then otherwise clause 
q = (
    df.select(
        pl.col("employee_id"),
        pl.when(~pl.col("name").str.starts_with("M") & pl.col("employee_id")%2==1).then(pl.col("salary")).otherwise(0)
    )
    .sort(by="salary", descending=True)
)

print(q)

#1398 customers who bought products "A", "B" but did not buy the product "C"

data = [[1, 'Daniel'], [2, 'Diana'], [3, 'Elizabeth'], [4, 'Jhon']]
customers = pl.from_pandas(pd.DataFrame(data, columns=['customer_id', 'customer_name']).astype({'customer_id':'Int64', 'customer_name':'object'}))
data = [[10, 1, 'A'], [20, 1, 'B'], [30, 1, 'D'], [40, 1, 'C'], [50, 2, 'A'], [60, 3, 'A'], [70, 3, 'B'], [80, 3, 'D'], [90, 4, 'C']]
orders = pl.from_pandas(pd.DataFrame(data, columns=['order_id', 'customer_id', 'product_name']).astype({'order_id':'Int64', 'customer_id':'Int64', 'product_name':'object'}))

q = (
    orders.group_by("customer_id").agg(pl.col("product_name").str.concat(""))
    .filter(pl.col("product_name").str.contains("A") &
            pl.col("product_name").str.contains("B") &
            ~pl.col("product_name").str.contains("C"))
    .join(customers, on="customer_id")
    .select(["customer_id","customer_name"])
)

print(q)