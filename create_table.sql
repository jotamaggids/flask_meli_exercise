CREATE TABLE `db_dna`.`dna_data` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `dna` VARCHAR(45) NOT NULL,
  `dna_status` TINYINT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `dna_UNIQUE` (`dna` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC));