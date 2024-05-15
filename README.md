# Mall keeper

## How to launch
```git clone https://github.com/Wolchear/Mall_keeper1.git```

```docker-compose up```



## Endpoints
```
/shops
/shops/<shop_id>
/shops/<shop_id>/goods
/shops/<shop_id>/goods/<good_id>
/workers
/workers/<mall_id>
```

## Sample Data
### Good
```
{
	'name': "Milk",
	'good_type': "diary product",
	'good_id': 1
}
```
### Worker
```
{
	'name': "Davina",
	'surname': "Keith",
	'shop': "Maxima",
	'Mall_id': 1,
	'Id_in_shop': 1,
	'Sex': "Female",
	'Salary': 1000,
	'Position': "Manager"
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


### Get
All shops:
```curl -X GET http://127.0.0.1:5000/shops```

All mall workers:
```curl http://127.0.0.1:5000/workers```

Worker by Mall id:
```curl http://172.19.0.2:5000/workers/<mall_id>```

All goods in shop by shop id:
```curl http://172.19.0.2:5000/shops/<shop_id>/goods```

### Post
Add New shop:
```curl -X POST -H "Content-Type: application/json" -d '{"name": "shop_name", "floor": "1"}' http://172.19.0.2:5000/shops```

Add new good:
```curl -X POST -H "Content-Type: application/json" -d '{"good_name": "good_name", "good_type": "good_type"}' http://172.19.0.2:5000/shops/<shop_id>/goods```

Add new worker to the shop:
```curl -X POST -H "Content-Type: application/json" -d '{"worker_name": "name", "worker_surname": "surname", "sex": "male", "position": "manager", "salary": "1200"}' http://172.19.0.2:5000/shops/<shop_id>/workers```

### Put
Update shop name and\or floor:
```curl -X PUT -H "Content-Type: application/json" -d '{"new_name": "new_name", "new_floor": "new_floor"}' http://172.19.0.2:5000/shops/<shop_id>```

### Delete
Delete shop by id:
```curl -X DELETE http://172.19.0.2:5000/shops/<shop_id>```

Delete good by name in shop:
```curl -X DELETE http://172.19.0.2:5000/shops/<shop_id>/goods/<good_id>```
