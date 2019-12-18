# 聚合框架 Aggregationn Framework 可以作用在一个或多个集合上，对数据进行计算、转换。类似SQL中的group by、left outer join、as...
# pip-line、stage 整个聚合运算过程称为管道(pipeline)，由多个步骤(stage)组成 
'''
	聚合运算格式
	pipeline = [$stage1, $stage2, ...$stageN];
	db.<collection>.aggregate(pipeline, {options});
	常见步骤
	$match			=	where				$eq/$gt/$gth/$and/$or/$not/$in/$geoWWithin
	$project		=	as
	$sort			=	order by
	$group			= 	group by 			
	$skip/$limit	=	skip/limit
	$lookup			= 	left outer join
	$unwind			= 	展开数组
	$graphLookup	=	图搜索
	$facet/$bucket	=	分面搜索

	OLAP/OLTP

	select first_name as '名', last_name as '姓' 
	from Users 
	where gender = '男' 
	skip 100 limit 200

	db.users.aggregate([
		{$match:{gender:"男"}},
		{$skip:100},{$limit:200},
		{$project:{'名':'$first_name','姓':'$last_name'}}
	])

	select department, count(null) as emp_qty
	from Users
	where gender = '女'
	group by department
	having count(*) < 10

	db.users.aggregate([
		{$match:{gender:'女'}},
		{$group:{_id:'$department',emp_qty:{$sum:1}}},
		{$match:{emp_qty}:{$lt:10}}
	])

	$unwind
	db.students.findOne()
	>>>	{
			name:'张三',
			score:[
				{subject:'语文',score:84},
				{subject:'数学',score:90},
				{subject:'外语',score:69},
			]
		}

	db.students.aggregate([{$unwind:'$score'}])
	>>> {name:'张三',score:{subject:'语文',score:84}}
		{name:'张三',score:{subject:'数学',score:90}}
		{name:'张三',score:{subject:'外语',score:69}}

	$bucket
	price	->[0,10)	->120条
			->[10,20)	->20条
			->[20,30)	->30条
			->[30,40)	->500条
			->[40,...]	->10条

	db.products.aggregate([{
		$bucket:{
			groupBy:"$price",
			boundaries:[0,10,20,30,40],
			default:"Other",
			output:{"count":{$sum:1}}
		},
	}])

	$facet 多个bucket组合
	db.products.aggregate([{
		$facet:{
			price:{
				$bucket:{...}
			},
			year:{
				$bucket:{...}
			}
		}
	}])

	db.orders.aggregate([
		{$match:{
			status:"completed", 
			orderDate:{$gte:ISODate("2019-01-01"),$lt:ISODate("2019-04-01")}
			}
		},
		{$group:{
			_id:null,
			total:{$sum:"$total"},
			shippingFee:{$sum:"$shippingFee"},
			count:{$sum:1}
			}
		},
		{$project:{
			grandTotal:{$add:["$total", "$shippingFee"]},
			count:1,
			_id:0
			}
		},
		}
	])

'''