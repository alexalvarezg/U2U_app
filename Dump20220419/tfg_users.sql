DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;

CREATE TABLE `users` (
 `id` int NOT NULL AUTO_INCREMENT,
 `nombre` varchar(30) NOT NULL,
 `email` varchar(50) NOT NULL,
 `password` VARCHAR(50) NOT NULL,
 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;