# Mall keeper

## How to launch
``` git clone ```
``` docker-compose up ```

## Sample Data
### Good
```
{
	'name': "Milk",
	'good_type': "diary product"
}
```
### Worker
```
{
	'name': "Davina",
	'surname': "Keith",
	'shop': "Maxima",
	'Mall_id': 1,
	'Id_in_shop': 1
}
```

### Shop
```
{
	'shop_id': 1,
	'name': "flowers_shop",
	'floor': 1,
	'goods': good_list,
	'workers': workers_list
}
```


## Get
All shops on 1st floor
``` curl http://127.0.0.1:5000/shops/1 ```
Worker by Mall id
``` curl http://127.0.0.1:5000/workers_mall_id/2 ```
All mall workers
``` curl http://127.0.0.1:5000/all_mall_workers ```
All goods in shop by shop id 
``` curl http://127.0.0.1:5000/get_shop_goods_by_id ```

## Post
Add New shop
``` curl -X POST -H "Content-Type: application/json" -d '{"name": "new_shop", "floor": 1}' http://127.0.0.1:5000/add_shop ```
Add new good
``` curl -X POST -H "Content-Type: application/json" -d '{"good_name": "New_good", "good_type": "new_good_type", "shop_id": 1}' http://127.0.0.1:5000/add_good ```
Add new worker to the shop
``` curl -X POST -H "Content-Type: application/json" -d '{"worker_name": "Name", "worker_surname": "Surname", "shop_id": 1}' http://127.0.0.1:5000/add_worker ```

## Put
Update shop name and\or floor
``` curl -X PUT -H "Content-Type: application/json" -d '{"name": "New shop name", "floor": 2}' http://127.0.0.1:5000/update_shop/1 ```

## Delete
Delete shop by id
``` curl -X DELETE http://127.0.0.1:5000/delete_shop/1 ```
Delete good by name in shop
``` curl -X DELETE http://127.0.0.1:5000/delete_good/1/goo_name ```


