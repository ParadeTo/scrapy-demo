# model
## article
```
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `url_object_id` varchar(50) NOT NULL DEFAULT '' COMMENT 'url指纹，用作主键',
  `url` varchar(300) NOT NULL DEFAULT '' COMMENT '文章地址',
  `title` varchar(255) NOT NULL DEFAULT '' COMMENT '文章标题',
  `content` longtext,
  `website_id` int(11) NOT NULL COMMENT '所属网站的id，外键',
  `publish_time` datetime DEFAULT NULL COMMENT '文章发布时间，爬取不到时间默认为爬取时间',
  `create_time` datetime DEFAULT NULL COMMENT '爬取时间',
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

## website
```
DROP TABLE IF EXISTS `website`;
CREATE TABLE `website` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '网站名称',
  `allow_domains` varchar(500) DEFAULT NULL COMMENT '以;分隔',
  `start_urls` varchar(500) DEFAULT NULL COMMENT '开始的url，以;分隔',
  `rules_to_follow` varchar(1000) DEFAULT NULL COMMENT '继续跟踪的链接正则表达式，;分隔',
  `rules_to_parse` varchar(1000) DEFAULT NULL COMMENT '解析数据链接的正则表达式，;分隔，一般只有一个',
  `title_css` varchar(255) DEFAULT NULL COMMENT '提取标题的css选择器',
  `content_css` varchar(255) DEFAULT NULL COMMENT '提取内容的css选择器',
  `publish_time_css` varchar(255) DEFAULT NULL COMMENT '提取发布时间的css选择器',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```