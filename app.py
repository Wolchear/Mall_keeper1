from flask import Flask, request, jsonify
from mall import Mall
app = Flask(__name__)

mall = Mall()

@app.route('/shops/<int:floor>', methods=['GET'])
def get_shops_by_floor(floor):
    shops = mall.getShopListByFloor(floor)
    return jsonify(shops)

@app.route('/workers_mall_id/<int:mall_id>', methods=['GET'])
def get_workers_by_mall_id(mall_id):
    workers = mall.get_workers_by_mall_id(mall_id)
    return jsonify(workers)
    
@app.route('/all_mall_workers', methods=['GET'])
def get_all_mall_workers():
    all_workers = mall.workers
    return jsonify([worker.as_dict() for worker in all_workers])
    
@app.route('/get_shop_goods_by_id/<int:shop_id>', methods=['GET'])
def get_shop_goods(shop_id):
    goods = mall.get_shop_goods(shop_id)
    return jsonify([good.as_dict() for good in goods])

@app.route('/add_shop', methods=['POST'])
def add_shop():
	new_shop = request.json
	shop_name = new_shop.get('name')
	shop_floor = new_shop.get('floor')
	
	if shop_floor is None or shop_name is None:
		return jsonify({'error':' No floor or name'}), 400
		
	mall.add_shop(shop_name, shop_floor)
	
	return jsonify({'message':'New shop sucesffuly added'}), 201

@app.route('/add_good', methods=['POST'])
def add_good():
	new_good = request.json
	good_name = new_good.get('good_name')
	good_floor = new_good.get('good_type')
	shop_id = new_good.get('shop_id')
	
	if good_name is None or good_name is None or shop_id is None:
		return jsonify({'error':' No good name, good type or shop id'}), 400
	
	if(mall.if_good_exists(shop_id, good_name)):
		return jsonify({'error':' Good already exist'}), 400
	mall.add_good(shop_id, good_name,good_floor)
	
	return jsonify({'message':'New good sucesffuly added'}), 201

@app.route('/add_worker', methods=['POST'])
def add_worker():
	new_worker = request.json
	worker_name = new_worker.get('worker_name')
	worker_surname = new_worker.get('worker_surname')
	shop_id = new_worker.get('shop_id')
	
	if worker_name is None or worker_surname is None or shop_id is None:
		return jsonify({'error':' No worker name, worker surname or shop id'}), 400
		
	mall.add_worker(shop_id, worker_name, worker_surname)
	
	return jsonify({'message':'New worker sucesffuly added'}), 201

@app.route('/update_shop/<int:shop_id>', methods=['PUT'])
def update_shop(shop_id):
	updated_data = request.json
	shop_to_update = None
	for shop in mall.shops:
		if shop.shop_id == shop_id:
			shop_to_update = shop
			break

	if shop_to_update is None:
		return jsonify({'error': 'Shop not found'}), 404

	if(mall.if_wrong_shop_update):
		return jsonify({'error': 'Shop on this floor already exists'}), 404
	
	if 'name' in updated_data:
		shop_to_update.name = updated_data['name']
	if 'floor' in updated_data:
		shop_to_update.floor = updated_data['floor']

	return jsonify({'message': 'Shop updated successfully'}), 200

@app.route('/delete_shop/<int:shop_id>', methods=['DELETE'])
def delete_shop(shop_id):
	shop_to_delete = None
	for shop in mall.shops:
		if shop.shop_id == shop_id:
			shop_to_delete = shop
			break

	if shop_to_delete is None:
		return jsonify({'error': 'Shop not found'}), 404

	mall.shops.remove(shop_to_delete)
	mall.update_ids_after_shop_delete(shop_id)
	return jsonify({'message': 'Shop deleted successfully'}), 200

@app.route('/delete_good/<int:shop_id>/<string:good_name>', methods=['DELETE'])
def delete_good(shop_id, good_name):
	shop_to_update = None
	for shop in mall.shops:
		if shop.shop_id == shop_id:
			shop_to_update = shop
			break

	if shop_to_update is None:
		return jsonify({'error': 'Shop not found'}), 404
		
	good_to_delete = None
	for good in shop_to_update.goods:
		if good.name == good_name:
			good_to_delete = good
			break
	
	if good_to_delete is None:
		return jsonify({'error': 'Coul dont find good in shop'}), 404

	shop_to_update.goods.remove(good_to_delete)
	return jsonify({'message': 'Good deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
