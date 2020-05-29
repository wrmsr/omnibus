import typing as ta

from ... import dataclasses as dc
from ... import lang


class Column(dc.Data, frozen=True, final=True):
    class Type(lang.AutoEnum):
        INTEGER = ...
        IDENTIFIER = ...
        DATE = ...
        DOUBLE = ...
        VARCHAR = ...

    name: str
    type: Type
    precision: ta.Optional[int] = 0
    scale: ta.Optional[int] = 0


class Entity(dc.Data, frozen=True, abstract=True):
    row_number: int


class Customer(Entity, frozen=True, final=True):
    customer_key: int = dc.field(metadata={Column: Column('c_custkey', Column.Type.IDENTIFIER)})
    name: str = dc.field(metadata={Column: Column('c_name', Column.Type.VARCHAR, 25)})
    address: str = dc.field(metadata={Column: Column('c_address', Column.Type.VARCHAR, 40)})
    nation_key: int = dc.field(metadata={Column: Column('c_nationkey', Column.Type.IDENTIFIER)})
    phone: str = dc.field(metadata={Column: Column('c_phone', Column.Type.VARCHAR, 25)})
    account_balance: int = dc.field(metadata={Column: Column('c_acctbal', Column.Type.DOUBLE)})
    market_segment: str = dc.field(metadata={Column: Column('c_mktsegment', Column.Type.VARCHAR, 10)})
    comment: str = dc.field(metadata={Column: Column('c_comment', Column.Type.VARCHAR, 117)})


class LineItem(Entity, frozen=True, final=True):
    order_key: int = dc.field(metadata={Column: Column('l_orderkey', Column.Type.IDENTIFIER)})
    part_key: int = dc.field(metadata={Column: Column('l_partkey', Column.Type.IDENTIFIER)})
    supplier_key: int = dc.field(metadata={Column: Column('l_suppkey', Column.Type.IDENTIFIER)})
    line_number: int = dc.field(metadata={Column: Column('l_linenumber', Column.Type.INTEGER)})
    quantity: int = dc.field(metadata={Column: Column('l_quantity', Column.Type.DOUBLE)})
    extended_price: int = dc.field(metadata={Column: Column('l_extendedprice', Column.Type.DOUBLE)})
    discount: int = dc.field(metadata={Column: Column('l_discount', Column.Type.DOUBLE)})
    tax: int = dc.field(metadata={Column: Column('l_tax', Column.Type.DOUBLE)})
    return_flag: str = dc.field(metadata={Column: Column('l_returnflag', Column.Type.VARCHAR, 1)})
    status: str = dc.field(metadata={Column: Column('l_linestatus', Column.Type.VARCHAR, 1)})
    ship_date: int = dc.field(metadata={Column: Column('l_shipdate', Column.Type.DATE)})
    commit_date: int = dc.field(metadata={Column: Column('l_commitdate', Column.Type.DATE)})
    receipt_date: int = dc.field(metadata={Column: Column('l_receiptdate', Column.Type.DATE)})
    ship_instructions: str = dc.field(metadata={Column: Column('l_shipinstruct', Column.Type.VARCHAR, 25)})
    ship_mode: str = dc.field(metadata={Column: Column('l_shipmode', Column.Type.VARCHAR, 10)})
    comment: str = dc.field(metadata={Column: Column('l_comment', Column.Type.VARCHAR, 44)})


class Nation(Entity, frozen=True, final=True):
    nation_key: int = dc.field(metadata={Column: Column('n_nationkey', Column.Type.IDENTIFIER)})
    name: str = dc.field(metadata={Column: Column('n_name', Column.Type.VARCHAR, 25)})
    region_key: int = dc.field(metadata={Column: Column('n_regionkey', Column.Type.IDENTIFIER)})
    comment: str = dc.field(metadata={Column: Column('n_comment', Column.Type.VARCHAR, 152)})


class Order(Entity, frozen=True, final=True):
    order_key: int = dc.field(metadata={Column: Column('o_orderkey', Column.Type.IDENTIFIER)})
    customer_key: int = dc.field(metadata={Column: Column('o_custkey', Column.Type.IDENTIFIER)})
    order_status: str = dc.field(metadata={Column: Column('o_orderstatus', Column.Type.VARCHAR, 1)})
    total_price: int = dc.field(metadata={Column: Column('o_totalprice', Column.Type.DOUBLE)})
    order_date: int = dc.field(metadata={Column: Column('o_orderdate', Column.Type.DATE)})
    order_priority: str = dc.field(metadata={Column: Column('o_orderpriority', Column.Type.VARCHAR, 15)})
    clerk: str = dc.field(metadata={Column: Column('o_clerk', Column.Type.VARCHAR, 15)})
    ship_priority: int = dc.field(metadata={Column: Column('o_shippriority', Column.Type.INTEGER)})
    comment: str = dc.field(metadata={Column: Column('o_comment', Column.Type.VARCHAR, 79)})


class Part(Entity, frozen=True, final=True):
    part_key: int = dc.field(metadata={Column: Column('p_partkey', Column.Type.IDENTIFIER)})
    name: str = dc.field(metadata={Column: Column('p_name', Column.Type.VARCHAR, 55)})
    manufacturer: str = dc.field(metadata={Column: Column('p_mfgr', Column.Type.VARCHAR, 25)})
    brand: str = dc.field(metadata={Column: Column('p_brand', Column.Type.VARCHAR, 10)})
    type: str = dc.field(metadata={Column: Column('p_type', Column.Type.VARCHAR, 25)})
    size: int = dc.field(metadata={Column: Column('p_size', Column.Type.INTEGER)})
    container: str = dc.field(metadata={Column: Column('p_container', Column.Type.VARCHAR, 10)})
    retail_price: int = dc.field(metadata={Column: Column('p_retailprice', Column.Type.DOUBLE)})
    comment: str = dc.field(metadata={Column: Column('p_comment', Column.Type.VARCHAR, 23)})


class PartSupplier(Entity, frozen=True, final=True):
    part_key: int = dc.field(metadata={Column: Column('ps_partkey', Column.Type.IDENTIFIER)})
    supplier_key: int = dc.field(metadata={Column: Column('ps_suppkey', Column.Type.IDENTIFIER)})
    available_quantity: int = dc.field(metadata={Column: Column('ps_availqty', Column.Type.INTEGER)})
    supply_cost: int = dc.field(metadata={Column: Column('ps_supplycost', Column.Type.DOUBLE)})
    comment: str = dc.field(metadata={Column: Column('ps_comment', Column.Type.VARCHAR, 199)})


class Region(Entity, frozen=True, final=True):
    region_key: int = dc.field(metadata={Column: Column('r_regionkey', Column.Type.IDENTIFIER)})
    name: str = dc.field(metadata={Column: Column('r_name', Column.Type.VARCHAR, 25)})
    comment: str = dc.field(metadata={Column: Column('r_comment', Column.Type.VARCHAR, 152)})


class Supplier(Entity, frozen=True, final=True):
    supplier_key: int = dc.field(metadata={Column: Column('s_suppkey', Column.Type.IDENTIFIER)})
    name: str = dc.field(metadata={Column: Column('s_name', Column.Type.VARCHAR, 25)})
    address: str = dc.field(metadata={Column: Column('s_address', Column.Type.VARCHAR, 40)})
    nation_key: int = dc.field(metadata={Column: Column('s_nationkey', Column.Type.IDENTIFIER)})
    phone: str = dc.field(metadata={Column: Column('s_phone', Column.Type.VARCHAR, 15)})
    account_balance: int = dc.field(metadata={Column: Column('s_acctbal', Column.Type.DOUBLE)})
    comment: str = dc.field(metadata={Column: Column('s_comment', Column.Type.VARCHAR, 101)})
