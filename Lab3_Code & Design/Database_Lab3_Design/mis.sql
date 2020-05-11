/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2020/5/9 19:09:14                            */
/*==============================================================*/


drop  
table  if   exists   viewSellerInfo;

drop  
table  if   exists   viewOrdersInfo;

drop  
table  if   exists   viewCartInfo;

drop  
table  if   exists   viewBuyerInfo;

/*==============================================================*/
/* Table: Buyer                                                 */
/*==============================================================*/
create table Buyer
(
   buyer_no             char(10) not null,
   b_name               varchar(16) not null,
   b_sex                char(1) not null,
   b_tel                char(11) not null,
   rep                  int,
   primary key (buyer_no)
);

/*==============================================================*/
/* Table: Seller                                                */
/*==============================================================*/
create table Seller
(
   seller_no            char(10) not null,
   shop_no              char(10),
   s_name               varchar(16) not null,
   s_sex                char(1) not null,
   s_tel                char(11) not null,
   primary key (seller_no)
);

/*==============================================================*/
/* Table: admin                                                 */
/*==============================================================*/
create table admin
(
   admin_no             char(10) not null,
   a_name               varchar(16) not null,
   a_sex                char(1) not null,
   a_tel                char(11) not null,
   startdate            date not null,
   primary key (admin_no)
);

/*==============================================================*/
/* Table: cart                                                  */
/*==============================================================*/
create table cart
(
   buyer_no             char(10) not null,
   c_no                 char(10) not null,
   cartnum              int not null,
   primary key (buyer_no, c_no)
);

/*==============================================================*/
/* Table: commodity                                             */
/*==============================================================*/
create table commodity
(
   c_no                 char(10) not null,
   shop_no              char(10),
   c_name               varchar(16) not null,
   price                float(8,2) not null,
   off                  real,
   text                 text,
   primary key (c_no)
);

/*==============================================================*/
/* Table: contents                                              */
/*==============================================================*/
create table contents
(
   order_no             char(10) not null,
   c_no                 char(10) not null,
   ordernum             int not null,
   primary key (order_no, c_no)
);

/*==============================================================*/
/* Table: orders                                                */
/*==============================================================*/
create table orders
(
   order_no             char(10) not null,
   shop_no              char(10) not null,
   buyer_no             char(10) not null,
   total                float(8,2) not null,
   paytime              datetime not null,
   primary key (order_no)
);

/*==============================================================*/
/* Table: shop                                                  */
/*==============================================================*/
create table shop
(
   shop_no              char(10) not null,
   shopname             varchar(16) not null,
   title                smallint,
   managerno            char(10) not null,
   primary key (shop_no)
);

/*==============================================================*/
/* Table: userInfo                                              */
/*==============================================================*/
create table userInfo
(
   user_no              char(10) not null,
   bsa_no               char(10) not null,
   typeno               smallint,
   pwd                  varchar(20) not null,
   primary key (user_no)
);

/*==============================================================*/
/* Table: userType                                              */
/*==============================================================*/
create table userType
(
   typeno               smallint not null,
   type                 varchar(16) not null,
   primary key (typeno)
);

/*==============================================================*/
/* View: viewBuyerInfo                                          */
/*==============================================================*/
create  VIEW      viewBuyerInfo
  as
select userInfo.user_no, buyer.buyer_no, buyer.b_name, buyer.b_sex, buyer.b_tel, buyer.rep
from userInfo, buyer
where userInfo.bsa_no = buyer.buyer_no;

/*==============================================================*/
/* View: viewCartInfo                                           */
/*==============================================================*/
create  VIEW      viewCartInfo
  as
select cart.buyer_no, cart.c_no, commodity.c_name, commodity.shop_no, shop.shopname, commodity.price, commodity.off
from cart, commodity, shop
where cart.c_no = commodity.c_no
and commodity.shop_no = shop.shop_no;

/*==============================================================*/
/* View: viewOrdersInfo                                         */
/*==============================================================*/
create  VIEW      viewOrdersInfo
  as
select orders.order_no, orders.shop_no, orders.buyer_no, contents.c_no, commodity.c_name, contents.ordernum
from orders, commodity, contents
where orders.order_no = contents.order_no 
and contents.c_no = commodity.c_no;

/*==============================================================*/
/* View: viewSellerInfo                                         */
/*==============================================================*/
create  VIEW      viewSellerInfo
  as
select userInfo.user_no, seller.seller_no, seller.s_name, seller.s_sex, seller.s_tel, seller.shop_no
from userInfo, seller
where userInfo.bsa_no = seller.seller_no;

alter table Seller add constraint FK_buyer_shop foreign key (shop_no)
      references shop (shop_no) on delete restrict on update restrict;

alter table cart add constraint FK_cart foreign key (c_no)
      references commodity (c_no) on delete restrict on update restrict;

alter table cart add constraint FK_cart2 foreign key (buyer_no)
      references Buyer (buyer_no) on delete restrict on update restrict;

alter table commodity add constraint FK_shop_commodity foreign key (shop_no)
      references shop (shop_no) on delete restrict on update restrict;

alter table contents add constraint FK_contents foreign key (c_no)
      references commodity (c_no) on delete restrict on update restrict;

alter table contents add constraint FK_contents2 foreign key (order_no)
      references orders (order_no) on delete restrict on update restrict;

alter table orders add constraint FK_buyer_order foreign key (buyer_no)
      references Buyer (buyer_no) on delete restrict on update restrict;

alter table orders add constraint FK_shop_order foreign key (shop_no)
      references shop (shop_no) on delete restrict on update restrict;

alter table userInfo add constraint FK_user_admin foreign key (bsa_no)
      references admin (admin_no) on delete restrict on update restrict;

alter table userInfo add constraint FK_user_buyer foreign key (bsa_no)
      references Buyer (buyer_no) on delete restrict on update restrict;

alter table userInfo add constraint FK_user_seller foreign key (bsa_no)
      references Seller (seller_no) on delete restrict on update restrict;

alter table userInfo add constraint FK_user_type foreign key (typeno)
      references userType (typeno) on delete restrict on update restrict;

