/**
 * Script com funções gerais
 */

 //retira acentos da Língua Portuguesa
function retira_acentos(texto_ou_palavra) {
    com_acento = 'áàãâäéèêëíìîïóòõôöúùûüçÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÖÔÚÙÛÜÇ';
    sem_acento = 'aaaaaeeeeiiiiooooouuuucAAAAAEEEEIIIIOOOOOUUUUC';
    nova='';
    for(i=0;i<texto_ou_palavra.length;i++) {
        if (com_acento.search(texto_ou_palavra.substr(i,1))>=0) {
            nova+=sem_acento.substr(com_acento.search(texto_ou_palavra.substr(i,1)),1);
        }
        else {
            nova+=texto_ou_palavra.substr(i,1);
        }
    }
    return nova;
}

function replaceNbsps(str) {
  var re = new RegExp(String.fromCharCode(160), "g");
  return str.replace(re, " ");
}

function retira_stop_words(texto_ou_palavra){ 
	novo = texto_ou_palavra.replace( "." , ""); //tira ponto  
	novo = texto_ou_palavra.replace( "!" , ""); //tira exclamação  
	novo = texto_ou_palavra.replace( "," , ""); //tira exclamação
	
	return novo;
}