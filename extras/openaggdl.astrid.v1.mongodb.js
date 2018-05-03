/*************************************************
* 
* Script para crear por primera vez la BD local
* MongoDB shell version 2.4.10
* comando para usar script:
* 
* $ mongo openaggdl openaggdl.astrid.v1.mongodb.js
* 
* mongo [DB_NAME] [SCRIPT.js]
* 
* by rasztul
* 
*************************************************/

// Se agrega usuario y password. 
/****************************************
* 
* DEBEN SER LAS CREDENCIALES QUE SE 
* USAN EN EL NODO 
* ---->>>>> sensor_persistence <<<<<------
* declarado en el archivo 
* ---->>>>> launch/lion_v.*.launch  <<<<<------
* 
****************************************/
db.addUser({user:"astrid", pwd:"2018astrid2018", roles:["readWrite", "dbAdmin"]});

/***********************
* 
* Registro inicial
* db.COLLECTION.insert(ObjectJSON)
* 
********************/
// información general del ambiente
db.info.insert(
{
	"name" :"astrid",//nombre del ambiente	
	"plant_type" : "Chlorophytum comosum", // nombre cientifico
	"location" : [20.7440693,-103.3785716], //lat,lng
	"rating" : 0.0016666667, //rate general para sensado hz
	"sensors" : [
					{ "topic" : "air_humidity", "rate" : "0.0016666667", "sensor" : "htu21df", "unit" : "" },
					{ "topic" : "air_quality", "rate" : "0.0016666667", "sensor" : "fly fishin MH MQ sensor", "unit" : "ADC" },
					{ "topic" : "air_temperature", "rate" : "0.0016666667", "sensor" : "htu21df", "unit" : "°C" },
					{ "topic" : "light_intensity", "rate" : "0.0016666667", "sensor" : "tsl2561", "unit" : "lx" },
					{ "topic" : "noise", "rate" : "0.0016666667", "sensor" : "max4466", "unit" : "ADC" },
					{ "topic" : "soil_humidity", "rate" : "0.0016666667", "sensor" : "soil moisture sensor", "unit" : "ADC" },
				]
});
// parametros a los que se desea llegar, escritos por el usuario
/*db.custom.insert(
{
	"params" : [{"topic" : "", "value" : ""},],
	"operations" : [{"topic" : "", "task": "", "args":[]},]
			
});*/
