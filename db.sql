/*
SQLyog Ultimate v12.09 (64 bit)
MySQL - 8.0.26 : Database - rice_recognition
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`rice_recognition` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `rice_recognition`;

/*Table structure for table `admin` */

DROP TABLE IF EXISTS `admin`;

CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号id',
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '密码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3 COMMENT='管理员';

/*Data for the table `admin` */

insert  into `admin`(`id`,`username`,`password`) values (1,'admin','admin');

/*Table structure for table `category` */

DROP TABLE IF EXISTS `category`;

CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '类型名',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COMMENT='类型';

/*Data for the table `category` */

insert  into `category`(`id`,`name`) values (1,'叶片病虫害'),(2,'谷子病虫害');

/*Table structure for table `category_list` */

DROP TABLE IF EXISTS `category_list`;

CREATE TABLE `category_list` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号id',
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '名称',
  `img_url` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '图片地址',
  `detail` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '详情',
  `category_id` int DEFAULT NULL COMMENT '分类id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COMMENT='中草药';

/*Data for the table `category_list` */

insert  into `category_list`(`id`,`title`,`img_url`,`detail`,`category_id`) values (1,'水稻细菌性谷枯病','http://5b0988e595225.cdn.sohucs.com/images/20180817/e9d05fef652142a784abf6986f612eab.jpeg','水稻细菌性谷枯病是一种危害严重的细菌性病害。它不但侵害谷粒 ，而且还引起水稻秧苗腐烂。\r\n水稻细菌性谷枯病特征\r\n苗期症状：谷粒在萌发时受侵染，引起谷粒腐烂而无法出苗，在谷粒腐烂处可形成发病中心。芽谷受侵染，幼芽弯曲，病斑由水渍状转褐色，严重的腐烂枯死，幸存病苗叶鞘内有深褐色病斑。\r\n\r\n穗期症状：水稻齐穗后乳熟期的绿色穗直立，染病谷粒初现苍白色似缺水状萎凋，渐变为灰白色至浅黄褐色，内外颖的先端或基部变成紫褐色，护颖也呈紫褐色。\r\n\r\n细菌性谷枯病的防治方法\r\n（1）农业防治一是种子消毒处理。\r\n\r\n二是水稻抽穗扬花期避开高温天气，所以适当延迟播种可以避免水稻抽穗开花期与高温天气相遇，从而减轻病害的发生和危害。\r\n\r\n三是合理进行水肥管理。施用氮肥太多是大多数病虫害严重发生的重要原因，后期严格控氮肥。\r\n\r\n四是减少初侵染源，及时清除病田间的残留物。\r\n\r\n（２）化学防治水稻谷枯病不同于水稻粒瘟，但谷枯病与水稻粒瘟引起的水稻减产具有同一性，所以及时防治还是非常重要的，一般采用稻瘟灵或75%肟菌酯·戊唑醇（耘彩®）即刻治疗。（当病症出现时才喷药防治，已错过了最佳防治时期，防治效果很差或几乎无防治效果）防治时间：打第一次药为破口前５－７天、齐穗后施第二次药。湖北省农业科学院植保土肥研究所的用药建议是：75%肟菌酯·戊唑醇（耘彩®）+46%CU（OH）2、12.5%烯唑醇+25%咪鲜胺、10%苯醚甲环唑+33.5%喹啉铜复配剂可兼防稻曲病、穗腐病。\r\n\r\n其他药剂：2%嘉赐霉素溶液（kasugamycin）250倍液或60%百菌通可湿性粉剂500倍液、12%绿乳铜乳油500倍液、47%加瑞农可湿性粉剂600-700倍液、53.8%可杀得2000干悬浮剂1200倍液。',2),(2,'稻瘟病','https://bkimg.cdn.bcebos.com/pic/d1a20cf431adcbef7609cccd7fe639dda3cc7dd931ec','稻瘟病是水稻重要病害之一，可引起大幅度减产，严重时减产40%～50%，甚至颗粒无收。世界各稻区均匀发生。本病在各地均有发生，其中以叶部、节部发生为多，发生后可造成不同程度减产，尤其穗颈瘟或节瘟发生早而重，可造成白穗以致绝产。近年来，广东稻瘟病年发生面积不少于50万亩，而且出现逐年增加趋势，局部大爆发并不少见，稻瘟病可能发生在省域内的任何年头、任何季节。\r\n防治方法\r\n播报\r\n编辑\r\n（1）因地制宜选用2-3个适合当地抗病品种。\r\n（2）无病田留种，处理病稻草，消灭菌源。使用土壤消毒剂处理。\r\n（3）加强肥、水管理 科学管理肥、水，既可改善环境条件，控制病菌的繁殖和侵染，又可促使水稻健壮生长，提高抗病性，从而获得高产稳产。注意氮、磷、钾配合施用，基肥、有机肥和化肥配合使用，适当施用含硅酸的肥料（如草木灰、矿渣、窑灰钾肥等），做到施足钾肥，早施追肥，中期看苗、看田、看天巧用施肥技术。硅、镁肥混施，可促进硅酸的吸收，能较大幅度地降低发病率。绿肥埋青量要适当，适量施用石灰可促进其腐烂，中和酸性。冷浸田应注意增施磷肥。\r\n（4）生物防治：\r\n（5）咪鲜胺防治叶温时期在7月上、中旬，叶瘟发生初期用药。要预防穗颈瘟在水稻始穗期、齐穗期各喷一次预防效果明显。',1),(3,'水稻细菌性褐斑病','https://att.191.cn/attachment/Mon_1405/343_188394_33ad856e73041b7.jpg?72','水稻细菌性褐斑病又称细菌性鞘腐病，由假丁香单胞杆菌引起的一种细菌性病害，主要发生于黑龙江、吉林等水稻主产区，在长江流域也可见，近些年由偶发性局部危害变成了常发性病害。',1),(4,'水稻东格鲁病毒病','https://gss0.baidu.com/-4o3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/908fa0ec08fa513de22d3831316d55fbb3fbd95e.jpg','水稻东格鲁病毒病，简称RTSV，又称东格鲁球状病毒，属玉米褪绿矮缩病毒组。\r\n防治方法\r\n播报\r\n编辑\r\n(1)选用抗(耐)病品种 如国际26等。\r\n(2)要成片种植，防止叶蝉在早、晚稻和不同熟性品种上传毒。早稻早收，避免虫源迁入晚稻。收割时要背向晚稻。\r\n(3)加强管理，促进稻苗早发，提高抗病能力。\r\n(4)推广化学除草，消灭看麦娘等杂草，压低越冬虫源。(5)治虫防病。及时防治在稻田繁殖的第一代若虫，并要抓住黑尾叶蝉迁飞双季晚稻秧田和本田的高峰期，把虫源消灭在传毒之前。可选用25%噻嗪酮可湿性粉剂，每667m225g或35%速虱净乳油100ml、25%速灭威可湿性粉剂100g，对水50L喷洒，隔3-5天1次，连防1-3次。',1);

/*Table structure for table `knowledge` */

DROP TABLE IF EXISTS `knowledge`;

CREATE TABLE `knowledge` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号id',
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '标题',
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '内容',
  `datetime` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '创建时间',
  `detail` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '详情',
  `img_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '图片地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3 COMMENT='健康知识';

/*Data for the table `knowledge` */

insert  into `knowledge`(`id`,`title`,`content`,`datetime`,`detail`,`img_url`) values (1,'水稻常见病虫害及防治方法','水稻是人们耐以生活的粮食来源，人要吃饭就离不开水稻的生产，所以为了保障人们的粮食供给，种植水稻的面积还在进一步扩大，基本满足了人们对于粮食的需求，那么种植水稻常见病虫害及防治方法有哪些呢？接下来一起了解下吧！','2025-4-7','1、稻瘟病该病发生的部位不同，病症也不一样，秧苗发病后，会直接导致枯黄而死，稻叶感病后，会出现黄色和褐色病斑，节瘟多发生在穗颈第一二节，甚至会扩散至整个节部。穗颈瘟和枝梗瘟主要发生在穗颈、穗轴、枝梗上，病斑先为水浸状淡褐色小点，后期变为褐色或墨绿色，发病后会出现白穗。防治方法：播种前，需对种子进行晾晒，用70%甲基托布津可湿性粉剂500倍液或者50%多菌灵可湿性粉剂250倍液拌种消毒，种植后，合理浇水施肥，能够很好的预防该病害发生。2、纹枯病该病发生后，会产生暗绿色的水渍状不规则小斑点，扩大后斑点呈椭圆形，由于遭受病原菌破坏，叶片会快速枯黄，干燥环境下，病斑变为暗褐色，潮湿环境，病部长出许多白色蛛丝状菌丝体，后期导致植株倒伏或腐烂而死。菌丝能在水稻体内生长，也可以表面结成菌核。防治方法：培育壮秧、合理密植、施足基肥、并增施磷钾肥，提高水稻抗病能力，当发生病害时，可以使用井岗霉素粉剂、苯甲丙环唑乳油、已唑醇悬浮剂等药剂进行防治，防治效果非常不错。3、二化螟该虫害在水稻生长周期内会对水稻进行啃食，严重影响水稻的产量和品质。防治方法：发生虫害时，一般可以使用杀虫灯吸引二化螟，然后集中进行灭杀，还可以使用化学药剂氯虫苯甲酰胺、溴氰虫酰胺等药剂进行防治，效果很不错。4、稻纵卷叶虫稻纵卷叶虫喜在生长茂密而嫩绿的稻田产卵，对于水稻生产很不利。防治方法：发生虫害时，一般都使用低毒、低残留类药剂进行防治，50%杀虫螟乳油、90%晶体敌百虫、15%巴丹可湿性粉剂都是不错的选择，喷雾的时候要注意天气因素。','https://img.mp.sohu.com/q_70,c_zoom,w_640/upload/20170810/bf8b41df9bde4ffab4b0ccaf183bab8d_th.jpg');

/*Table structure for table `prevention_suggestion` */

DROP TABLE IF EXISTS `prevention_suggestion`;

CREATE TABLE `prevention_suggestion` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `title` varchar(55) DEFAULT NULL COMMENT '病害信息',
  `content` text COMMENT '防治建议',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `prevention_suggestion` */

insert  into `prevention_suggestion`(`id`,`title`,`content`) values (1,'水稻细菌性谷枯病','<ol style=\"margin: 5px 0; padding-left: 20px;\">\r\n            <li>使用20%噻菌铜悬浮剂500倍液喷雾</li>\r\n            <li>播种前用50%氯溴异氰尿酸浸种6小时</li>\r\n            <li>发病初期及时拔除病株</li>\r\n            <li>保持田间排水通畅</li>\r\n        </ol>'),(2,'稻瘟病','<ol style=\"margin: 5px 0; padding-left: 20px;\">\r\n            <li>使用40%稻瘟灵乳油1000倍液喷雾</li>\r\n            <li>合理施用硅肥增强抗病性</li>\r\n            <li>保持合理种植密度（丛距20×20cm）</li>\r\n            <li>及时处理病稻草，减少菌源</li>\r\n </ol>'),(3,'水稻细菌性褐斑病','        <ol style=\"margin: 5px 0; padding-left: 20px;\">\r\n            <li>使用20%叶枯唑可湿性粉剂500倍液</li>\r\n            <li>增施钾肥（每亩氯化钾5-7公斤）</li>\r\n            <li>避免深水灌溉，采用浅湿灌溉</li>\r\n            <li>收获后深耕灭茬（深度15-20cm）</li>\r\n        </ol>'),(4,'水稻东格鲁病毒病','        <ol style=\"margin: 5px 0; padding-left: 20px;\">\r\n            <li>使用10%吡虫啉防治叶蝉等传毒媒介</li>\r\n            <li>发现病株立即拔除并销毁</li>\r\n            <li>选用抗病品种（如IR36、IR50）</li>\r\n            <li>避免晚稻早栽（避开6月虫媒高峰期）</li>\r\n        </ol>');

/*Table structure for table `recognition_records` */

DROP TABLE IF EXISTS `recognition_records`;

CREATE TABLE `recognition_records` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
  `user_id` int NOT NULL COMMENT '用户id',
  `recognition_time` datetime NOT NULL COMMENT '识别时间',
  `image_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '图片地址',
  `recognition_result` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '识别结果',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='识别记录';

/*Data for the table `recognition_records` */

insert  into `recognition_records`(`id`,`user_id`,`recognition_time`,`image_url`,`recognition_result`) values (1,1,'2025-04-07 22:44:16','static/all_records/image_20250407224416.jpg','稻瘟病'),(2,1,'2025-04-07 22:44:24','static/all_records/image_20250407224424.jpg','水稻东格鲁病毒病'),(3,1,'2025-04-07 22:44:31','static/all_records/image_20250407224431.jpg','水稻细菌性褐斑病'),(4,1,'2025-04-07 22:46:43','static/all_records/image_20250407224642.jpg','水稻细菌性褐斑病'),(5,1,'2025-04-07 22:46:48','static/all_records/image_20250407224648.jpg','水稻细菌性褐斑病'),(6,1,'2025-04-07 22:46:53','static/all_records/image_20250407224653.jpg','水稻细菌性褐斑病'),(7,1,'2025-04-07 22:47:00','static/all_records/image_20250407224700.jpg','稻瘟病'),(8,1,'2025-04-07 22:47:07','static/all_records/image_20250407224707.jpg','稻瘟病'),(9,1,'2025-04-07 22:47:14','static/all_records/image_20250407224714.jpg','水稻东格鲁病毒病'),(10,1,'2025-05-08 14:55:54','static/all_records/image_20250508145552.jpg','稻瘟病'),(11,1,'2025-05-08 14:58:22','static/all_records/image_20250508145821.jpg','稻瘟病'),(12,1,'2025-05-08 14:58:54','static/all_records/image_20250508145854.jpg','稻瘟病'),(13,1,'2025-05-08 14:58:57','static/all_records/image_20250508145857.jpg','稻瘟病'),(14,1,'2025-05-08 14:58:59','static/all_records/image_20250508145859.jpg','稻瘟病'),(15,1,'2025-05-08 14:59:02','static/all_records/image_20250508145902.jpg','稻瘟病'),(16,1,'2025-05-08 14:59:05','static/all_records/image_20250508145905.jpg','稻瘟病'),(17,1,'2025-05-08 14:59:09','static/all_records/image_20250508145909.jpg','稻瘟病'),(18,1,'2025-05-08 14:59:13','static/all_records/image_20250508145913.jpg','稻瘟病');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '密码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3 COMMENT='用户';

/*Data for the table `user` */

insert  into `user`(`id`,`username`,`password`) values (1,'admin','admin'),(3,'xiaoming','xiaoming'),(5,'xiaohong','xiaohong'),(6,'xiaoliu','xiaoliu'),(7,NULL,NULL);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
