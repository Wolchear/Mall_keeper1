from flask import Flask, request, jsonify
from mall import Mall

app = Flask(__name__)

mall = Mall()

@app.route('/shops', methods=['GET'])
def get_shops():
	shops = mall.getShopListByFloor()
	return jsonify(shops)

@app.route('/workers/<int:mall_id>', methods=['GET'])
def get_workers_by_mall_id(mall_id):
	workers = mall.get_workers_by_mall_id(mall_id)
	if workers is None:
		return jsonify({'error': 'Woker not found'}), 404
	return jsonify(workers.as_dict())
    
@app.route('/workers', methods=['GET'])
def get_all_mall_workers():
	mall.update_workers_set()
	all_workers = mall.workers
	return jsonify([worker.as_dict() for worker in all_workers])
    
@app.route('/shops/<int:shop_id>/goods', methods=['GET'])
def get_shop_goods(shop_id):
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404
		
	if not shop.goods:
		return jsonify({'error': 'Where is no goods in shop'}), 404
	
	return jsonify([good.as_dict() for good in shop.goods])
	
@app.route('/shops', methods=['POST'])
def add_shop():
	new_shop = request.json
	shop_name = new_shop.get('name')
	shop_floor = new_shop.get('floor')
	
	if shop_floor is None or shop_floor == "":
		return jsonify({'error':'shop_floor is Null'}), 400
		
	if shop_name is None or shop_name == "":
		return jsonify({'error':'shop_name is Null'}), 400
	
	if mall.if_shop_exists_by_name_floor(shop_name, shop_floor):
		return jsonify({'error':'Shop on this floor already exists'}), 400
				
	mall.add_shop(shop_name, shop_floor)
	shop = mall.getShopByName(shop_name, shop_floor)

	return jsonify(shop.as_dict()), 201


@app.route('/shops/<int:shop_id>/goods', methods=['POST'])
def add_good(shop_id):
	new_good = request.json
	good_name = new_good.get('good_name')
	good_type = new_good.get('good_type')
	
	if good_name is None or good_name == "":
		return jsonify({'error':'good_name is Null'}), 400
		
	if good_type is None or good_type == "":
		return jsonify({'error':'good_type is Null'}), 400
	
	if shop_id is None or shop_id == "":
		return jsonify({'error':'shop_id is Null'}), 400
	
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404
		
	good = shop.getGood(good_name)
	if good:
		return jsonify({'error':' Good already exist'}), 400
		
	shop.addGood(good_name,good_type)
	good = shop.getGood(good_name)
	return jsonify(good.as_dict()), 201

@app.route('/shops/<int:shop_id>/workers', methods=['POST'])
def add_worker(shop_id):
	new_worker = request.json
	worker_name = new_worker.get('worker_name')
	worker_surname = new_worker.get('worker_surname')
	worker_sex = new_worker.get('sex')
	worker_position = new_worker.get('position')
	worker_salary = new_worker.get('salary')
	
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404
	
	if worker_name is None or worker_name == '':
		return jsonify({'error':'worker_name is Null'}), 400
	
	if worker_surname is None or worker_surname == '':
		return jsonify({'error':'worker_surname is Null'}), 400
		
	shop.addWorker(worker_name, worker_surname, worker_sex, worker_position, worker_salary)
	new_worker = shop.getWorker(worker_name, worker_surname)
	return jsonify(new_worker.as_dict()), 201

@app.route('/shops/<int:shop_id>', methods=['PUT'])
def update_shop(shop_id):
	updated_data = request.json
	new_name = updated_data.get('new_name')
	new_floor = updated_data.get('new_floor')
	
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404
	
	if(mall.if_wrong_shop_update(new_name, new_floor)):
		return jsonify({'error': 'Shop on this floor already exists'}), 400
	
	shop.name = new_name
	shop.floor = int(new_floor)
	for worker in shop.workers:
		worker.shop = new_name
	
	return jsonify(shop.as_dict()), 200

@app.route('/shops/<int:shop_id>', methods=['DELETE'])
def delete_shop(shop_id):
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404

	mall.shops.remove(shop)
	return jsonify({'message': 'Shop deleted successfully'}), 200

@app.route('/shops/<int:shop_id>/goods/<int:good_id>', methods=['DELETE'])
def delete_good(shop_id, good_id):
	shop = mall.getShopById(shop_id)
	if shop is None:
		return jsonify({'error': 'Shop not found'}), 404
	
	if good_id is None:
		return jsonify({'error': 'Good_id is none'}), 404
	
	good_to_delete = None	
	for good in shop.goods:
		if good.good_id == good_id:
			good_to_delete = good
			break
	
	if good_to_delete is None:
		return jsonify({'error': 'Could not find good in shop'}), 404

	shop.goods.remove(good_to_delete)
	return jsonify({'message': 'Good deleted successfully'}), 200

@app.route('/')
def index():
	return "Move to /shops endpoint to see full informations"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug = True)
