SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `drvicecloud_schema` ;
USE `drvicecloud_schema` ;

-- -----------------------------------------------------
-- Table `drvicecloud_schema`.`device_type`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `drvicecloud_schema`.`device_type` (
  `iddevice_type` INT NOT NULL ,
  `device_type_name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`iddevice_type`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `drvicecloud_schema`.`devices`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `drvicecloud_schema`.`devices` (
  `iddevices` INT NOT NULL ,
  `device_type_iddevice_type` INT NOT NULL ,
  `device_id` VARCHAR(45) NOT NULL ,
  `device_mac` VARCHAR(45) NOT NULL ,
  `IP Address` VARCHAR(16) NOT NULL ,
  `Global_Address` VARCHAR(16) NOT NULL ,
  `Description` VARCHAR(45) NULL ,
  `Contact` VARCHAR(45) NULL ,
  `Location` VARCHAR(45) NULL ,
  PRIMARY KEY (`iddevices`) ,
  UNIQUE INDEX `device_mac_UNIQUE` (`device_mac` ASC) ,
  UNIQUE INDEX `device_id_UNIQUE` (`device_id` ASC) ,
  INDEX `fk_devices_device_type_idx` (`device_type_iddevice_type` ASC) ,
  CONSTRAINT `fk_devices_device_type`
    FOREIGN KEY (`device_type_iddevice_type` )
    REFERENCES `drvicecloud_schema`.`device_type` (`iddevice_type` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `drvicecloud_schema` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
