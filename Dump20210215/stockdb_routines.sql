-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: stockdb
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Temporary view structure for view `stockholdview`
--

DROP TABLE IF EXISTS `stockholdview`;
/*!50001 DROP VIEW IF EXISTS `stockholdview`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `stockholdview` AS SELECT 
 1 AS `stock_id`,
 1 AS `stock_name`,
 1 AS `20Q4`,
 1 AS `20Q3`,
 1 AS `20Q2`,
 1 AS `20Q1`,
 1 AS `19Q4`,
 1 AS `19Q3`,
 1 AS `19Q2`,
 1 AS `19Q1`,
 1 AS `18Q4`,
 1 AS `18Q3`,
 1 AS `18Q2`,
 1 AS `18Q1`,
 1 AS `17Q4`,
 1 AS `17Q3`,
 1 AS `17Q2`,
 1 AS `17Q1`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `stockidview`
--

DROP TABLE IF EXISTS `stockidview`;
/*!50001 DROP VIEW IF EXISTS `stockidview`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `stockidview` AS SELECT 
 1 AS `stock_id`,
 1 AS `stock_name`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `stockholdviewnew`
--

DROP TABLE IF EXISTS `stockholdviewnew`;
/*!50001 DROP VIEW IF EXISTS `stockholdviewnew`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `stockholdviewnew` AS SELECT 
 1 AS `stock_id`,
 1 AS `stock_name`,
 1 AS `20Q4`,
 1 AS `20Q3`,
 1 AS `20Q2`,
 1 AS `20Q1`,
 1 AS `19Q4`,
 1 AS `19Q3`,
 1 AS `19Q2`,
 1 AS `19Q1`,
 1 AS `18Q4`,
 1 AS `18Q3`,
 1 AS `18Q2`,
 1 AS `18Q1`,
 1 AS `17Q4`,
 1 AS `17Q3`,
 1 AS `17Q2`,
 1 AS `17Q1`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `stockholdview`
--

/*!50001 DROP VIEW IF EXISTS `stockholdview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `stockholdview` AS select `t0`.`stock_id` AS `stock_id`,`t0`.`stock_name` AS `stock_name`,ifnull(`t20q4`.`fundholdrate`,0) AS `20Q4`,ifnull(`t20q3`.`fundholdrate`,0) AS `20Q3`,ifnull(`t20q2`.`fundholdrate`,0) AS `20Q2`,ifnull(`t20q1`.`fundholdrate`,0) AS `20Q1`,ifnull(`t19q4`.`fundholdrate`,0) AS `19Q4`,ifnull(`t19q3`.`fundholdrate`,0) AS `19Q3`,ifnull(`t19q2`.`fundholdrate`,0) AS `19Q2`,ifnull(`t19q1`.`fundholdrate`,0) AS `19Q1`,ifnull(`t18q4`.`fundholdrate`,0) AS `18Q4`,ifnull(`t18q3`.`fundholdrate`,0) AS `18Q3`,ifnull(`t18q2`.`fundholdrate`,0) AS `18Q2`,ifnull(`t18q1`.`fundholdrate`,0) AS `18Q1`,ifnull(`t17q4`.`fundholdrate`,0) AS `17Q4`,ifnull(`t17q3`.`fundholdrate`,0) AS `17Q3`,ifnull(`t17q2`.`fundholdrate`,0) AS `17Q2`,ifnull(`t17q1`.`fundholdrate`,0) AS `17Q1` from ((((((((((((((((`stockidview` `t0` left join `fundhold20q4` `t20q4` on((`t0`.`stock_id` = `t20q4`.`stock_id`))) left join `fundhold20q3` `t20q3` on((`t0`.`stock_id` = `t20q3`.`stock_id`))) left join `fundhold20q2` `t20q2` on((`t0`.`stock_id` = `t20q2`.`stock_id`))) left join `fundhold20q1` `t20q1` on((`t0`.`stock_id` = `t20q1`.`stock_id`))) left join `fundhold19q4` `t19q4` on((`t0`.`stock_id` = `t19q4`.`stock_id`))) left join `fundhold19q3` `t19q3` on((`t0`.`stock_id` = `t19q3`.`stock_id`))) left join `fundhold19q2` `t19q2` on((`t0`.`stock_id` = `t19q2`.`stock_id`))) left join `fundhold19q1` `t19q1` on((`t0`.`stock_id` = `t19q1`.`stock_id`))) left join `fundhold18q4` `t18q4` on((`t0`.`stock_id` = `t18q4`.`stock_id`))) left join `fundhold18q3` `t18q3` on((`t0`.`stock_id` = `t18q3`.`stock_id`))) left join `fundhold18q2` `t18q2` on((`t0`.`stock_id` = `t18q2`.`stock_id`))) left join `fundhold18q1` `t18q1` on((`t0`.`stock_id` = `t18q1`.`stock_id`))) left join `fundhold17q4` `t17q4` on((`t0`.`stock_id` = `t17q4`.`stock_id`))) left join `fundhold17q3` `t17q3` on((`t0`.`stock_id` = `t17q3`.`stock_id`))) left join `fundhold17q2` `t17q2` on((`t0`.`stock_id` = `t17q2`.`stock_id`))) left join `fundhold17q1` `t17q1` on((`t0`.`stock_id` = `t17q1`.`stock_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `stockidview`
--

/*!50001 DROP VIEW IF EXISTS `stockidview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `stockidview` AS select `fundhold18q1`.`stock_id` AS `stock_id`,`fundhold18q1`.`stock_name` AS `stock_name` from `fundhold18q1` union select `fundhold18q2`.`stock_id` AS `stock_id`,`fundhold18q2`.`stock_name` AS `stock_name` from `fundhold18q2` union select `fundhold18q3`.`stock_id` AS `stock_id`,`fundhold18q3`.`stock_name` AS `stock_name` from `fundhold18q3` union select `fundhold18q4`.`stock_id` AS `stock_id`,`fundhold18q4`.`stock_name` AS `stock_name` from `fundhold18q4` union select `fundhold19q1`.`stock_id` AS `stock_id`,`fundhold19q1`.`stock_name` AS `stock_name` from `fundhold19q1` union select `fundhold19q2`.`stock_id` AS `stock_id`,`fundhold19q2`.`stock_name` AS `stock_name` from `fundhold19q2` union select `fundhold19q3`.`stock_id` AS `stock_id`,`fundhold19q3`.`stock_name` AS `stock_name` from `fundhold19q3` union select `fundhold19q4`.`stock_id` AS `stock_id`,`fundhold19q4`.`stock_name` AS `stock_name` from `fundhold19q4` union select `fundhold20q1`.`stock_id` AS `stock_id`,`fundhold20q1`.`stock_name` AS `stock_name` from `fundhold20q1` union select `fundhold20q2`.`stock_id` AS `stock_id`,`fundhold20q2`.`stock_name` AS `stock_name` from `fundhold20q2` union select `fundhold20q3`.`stock_id` AS `stock_id`,`fundhold20q3`.`stock_name` AS `stock_name` from `fundhold20q3` union select `fundhold20q4`.`stock_id` AS `stock_id`,`fundhold20q4`.`stock_name` AS `stock_name` from `fundhold20q4` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `stockholdviewnew`
--

/*!50001 DROP VIEW IF EXISTS `stockholdviewnew`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `stockholdviewnew` AS select `t0`.`stock_id` AS `stock_id`,`t0`.`stock_name` AS `stock_name`,ifnull(`t0`.`fundholdrate`,0) AS `20Q4`,ifnull(`t20q3`.`fundholdrate`,0) AS `20Q3`,ifnull(`t20q2`.`fundholdrate`,0) AS `20Q2`,ifnull(`t20q1`.`fundholdrate`,0) AS `20Q1`,ifnull(`t19q4`.`fundholdrate`,0) AS `19Q4`,ifnull(`t19q3`.`fundholdrate`,0) AS `19Q3`,ifnull(`t19q2`.`fundholdrate`,0) AS `19Q2`,ifnull(`t19q1`.`fundholdrate`,0) AS `19Q1`,ifnull(`t18q4`.`fundholdrate`,0) AS `18Q4`,ifnull(`t18q3`.`fundholdrate`,0) AS `18Q3`,ifnull(`t18q2`.`fundholdrate`,0) AS `18Q2`,ifnull(`t18q1`.`fundholdrate`,0) AS `18Q1`,ifnull(`t17q4`.`fundholdrate`,0) AS `17Q4`,ifnull(`t17q3`.`fundholdrate`,0) AS `17Q3`,ifnull(`t17q2`.`fundholdrate`,0) AS `17Q2`,ifnull(`t17q1`.`fundholdrate`,0) AS `17Q1` from (((((((((((((((`fundhold20q4new` `t0` left join `fundhold20q3new` `t20q3` on((`t0`.`stock_id` = `t20q3`.`stock_id`))) left join `fundhold20q2new` `t20q2` on((`t0`.`stock_id` = `t20q2`.`stock_id`))) left join `fundhold20q1new` `t20q1` on((`t0`.`stock_id` = `t20q1`.`stock_id`))) left join `fundhold19q4new` `t19q4` on((`t0`.`stock_id` = `t19q4`.`stock_id`))) left join `fundhold19q3new` `t19q3` on((`t0`.`stock_id` = `t19q3`.`stock_id`))) left join `fundhold19q2new` `t19q2` on((`t0`.`stock_id` = `t19q2`.`stock_id`))) left join `fundhold19q1new` `t19q1` on((`t0`.`stock_id` = `t19q1`.`stock_id`))) left join `fundhold18q4new` `t18q4` on((`t0`.`stock_id` = `t18q4`.`stock_id`))) left join `fundhold18q3new` `t18q3` on((`t0`.`stock_id` = `t18q3`.`stock_id`))) left join `fundhold18q2new` `t18q2` on((`t0`.`stock_id` = `t18q2`.`stock_id`))) left join `fundhold18q1new` `t18q1` on((`t0`.`stock_id` = `t18q1`.`stock_id`))) left join `fundhold17q4new` `t17q4` on((`t0`.`stock_id` = `t17q4`.`stock_id`))) left join `fundhold17q3new` `t17q3` on((`t0`.`stock_id` = `t17q3`.`stock_id`))) left join `fundhold17q2new` `t17q2` on((`t0`.`stock_id` = `t17q2`.`stock_id`))) left join `fundhold17q1new` `t17q1` on((`t0`.`stock_id` = `t17q1`.`stock_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-02-15 23:00:24
