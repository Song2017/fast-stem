
 create table "ranger_order" (
    "envoy_order_id" serial primary key,
    "carrier" varchar(100),
    "store_id" varchar(100),
    "order_id" varchar(100),
    "sub_order_id" varchar(100),
    "outer_order_id" varchar(100),
    "customs_order_id" varchar(100),
    "waybill_id" varchar(100),
    "customer_id" varchar(50),
    "platform_name" varchar(50),
    -- WAIT_BUYER_PAY, WAIT_SELLER_SEND_GOODS, WAIT_BUYER_CONFIRM_GOODS, TRADE_SUCCESS, TRADE_CLOSED, TRADE_REFUND, TRADE_FAILED
    "status" varchar(50),
    -- platform status: UNPROCESSED, ORDER_PROCESSED, PAYMENT_PROCESSED, TRADE_REFUND, EXCEPTION
    -- WAYBILL_CREATION, WAYBILL_FAILED, SHIPPED, PLATFORM_PROCESSED
    "platform_status" varchar(50),

    "platform_order" jsonb,
    "customer" jsonb,
    "payer" jsonb,
    "product" jsonb,
    "waybill" jsonb,
    "customs" jsonb,
    "request" jsonb,
    "response" jsonb,
    "kafka_msg" jsonb,

    "total_price" numeric(9,3),
    "tax" numeric(9,3),
    "shipping_cost" numeric(9,3),
    "discount" numeric(9,3),
    "pay_amount" numeric(9,3),
    "insurance_fee" numeric(9,3),

    "currency" varchar(50),
    "created_at" varchar(100),
    "updated_at" varchar(100),
    "paid_at" varchar(100),
    "pay_method" varchar(30),
    "pay_merchant_name" varchar(100),
    "pay_id" varchar(100),
    "payment_pay_id" varchar(100),
    "customer_note" varchar,
    "cancel_reason" varchar,
    "reason" varchar,
    "waybill_reason" varchar,
    "warehouse_code" varchar(50),
    "express_type" varchar(50),
    "alerted" boolean default false,
    "create_time" timestamp(3) with time zone default current_timestamp,
    "modify_time" timestamp(3) with time zone default current_timestamp,
    "create_by" varchar(100),
    "modify_by" varchar(100)
);


COMMENT ON COLUMN ranger_order.status
    IS 'WAIT_BUYER_PAY, WAIT_SELLER_SEND_GOODS, WAIT_BUYER_CONFIRM_GOODS, TRADE_SUCCESS, TRADE_CLOSED, TRADE_REFUND, TRADE_FAILED';
COMMENT ON COLUMN ranger_order.platform_status
    IS 'UNPROCESSED, ORDER_PROCESSED, PAYMENT_PROCESSED, TRADE_REFUND, EXCEPTION, WAYBILL_CREATION, WAYBILL_FAILED, SHIPPED, PLATFORM_PROCESSED';
